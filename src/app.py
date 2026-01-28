import streamlit as st
import arxiv
from google import genai
from google.genai import types
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="ArXiv 物理论文速递", page_icon="⚛️", layout="wide")

st.title("⚛️ ArXiv AI Daily Summarizer")


st.markdown("专为物理科研人员设计的论文速读工具 (Powered by Gemini)")

# --- 2. 侧边栏设置 ---
with st.sidebar:
    st.header("⚙️ 设置")
    
    api_key = None
    
    # 尝试从 Secrets 读取 Key，如果本地没有配置文件则捕获异常，改为手动输入
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("已自动加载 API Key ✅")
    except FileNotFoundError:
        # 本地没文件，跳过，等待手动输入
        pass
    except Exception:
        # 其他错误（如 Key 不存在），也跳过
        pass

    # 如果没找到 Key，显示输入框
    if not api_key:
        api_key = st.text_input("输入 Google Gemini API Key", type="password")
    
    # 选择 ArXiv 分类
    category = st.selectbox(
        "选择物理领域",
        (
            "cond-mat.str-el (强关联电子)",
            "cond-mat.mes-hall (介观物理)",
            "quant-ph (量子物理)",
            "cs.AI (人工智能)",
            "physics.comp-ph (计算物理)"
        )
    )
    search_query = f"cat:{category.split()[0]}"
    
    max_results = st.slider("获取论文数量", 5, 20, 10)
    
    st.info("提示：点击具体的论文卡片可展开查看详情。")

# --- 3. 核心功能函数 ---

@st.cache_data(ttl=3600)
def fetch_arxiv_papers(query, max_results):
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
    
        results = []
        for result in client.results(search):
            results.append({
                "title": result.title,
                "authors": ", ".join([author.name for author in result.authors]),
                "abstract": result.summary,
                "published": result.published.strftime("%Y-%m-%d"),
                "url": result.entry_id,
                "pdf_url": result.pdf_url
            })
        return results

    except Exception as e:
        st.error(f"无法连接到 ArXiv，请稍后重试。错误信息: {e}")
        return []

def ai_summarize(text, api_key):
    if not api_key:
        return "⚠️ 请先在侧边栏输入 API Key"
    
    try:
        # --- 新版 SDK (google-genai) 的写法 ---
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        你是一位资深的理论物理学教授。请阅读以下 arXiv 论文的摘要，并用中文为你的博士生做一个简洁的学术总结。
        
        摘要内容：
        {text}
        
        要求：
        1. **核心问题**：这篇文章解决了什么物理问题？
        2. **方法**：作者使用了什么理论或数值方法（如 DMRG, DFT, QMC 等）？
        3. **结论**：主要结果是什么？有什么新颖性？
        4. 格式使用 Markdown，重点词汇加粗。如果出现数学公式，请使用 LaTeX 格式（例如 $H$）。
        5. **关联性**：如果文中涉及“张量网络(Tensor Networks)”、“量子纠缠”、“拓扑序”或“机器学习应用”，请特别高亮指出。
        """
        
        # 调用 generate_content
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ AI 总结失败: {str(e)}"

# --- 4. 主界面逻辑 ---

if not api_key:
    st.warning("👈 请先在左侧侧边栏输入你的 Google Gemini API Key 以启用 AI 功能。")

with st.spinner(f"正在从 ArXiv 抓取 {category} 的最新论文..."):
    papers = fetch_arxiv_papers(search_query, max_results)

st.success(f"成功获取 {len(papers)} 篇最新论文")

if "summaries" not in st.session_state:
    st.session_state.summaries = {}

for i, paper in enumerate(papers):
    with st.expander(f"📄 {i+1}. {paper['title']} ({paper['published']})"):
        st.markdown(f"**作者**: {paper['authors']}")
        st.markdown(f"**原文链接**: [ArXiv Page]({paper['url']}) | [PDF Download]({paper['pdf_url']})")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("原始摘要")
            st.caption(paper['abstract'])
            
        with col2:
            st.subheader("🤖 AI 导读")
            
            # 检查是否已经有缓存的总结
            paper_id = paper['url'] # 使用 URL 作为唯一 ID
            
            if paper_id in st.session_state.summaries:
                # 如果有，直接显示，不需要再显示按钮
                st.markdown(st.session_state.summaries[paper_id])
                # 也可以加个“重新生成”的按钮（可选）
            else:
                # 如果没有，显示生成按钮
                if st.button(f"生成中文总结", key=f"btn_{i}"):
                    with st.spinner("AI 正在阅读摘要..."):
                        summary = ai_summarize(paper['abstract'], api_key)
                        # 保存到 session_state
                        st.session_state.summaries[paper_id] = summary
                        # 强制刷新页面以显示结果（或者直接在这里 st.markdown 也可以，但刷新更稳妥）
                        st.rerun()
                else:
                    st.write("点击按钮开始分析...")