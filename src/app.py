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
    
    # 尝试从 Secrets 读取 Key
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("已自动加载 API Key ✅")
    except Exception:
        pass

    if not api_key:
        api_key = st.text_input("输入 Google Gemini API Key", type="password")
    
    category = st.selectbox(
        "选择领域",
        (
            "astro-ph (天体物理)",
            "cond-mat (凝聚态物理)",
            "gr-qc (广义相对论)",
            "hep-ex (高能物理实验)",
            "hep-lat (高能物理-格子)",
            "hep-ph (高能物理-粒子)",
            "hep-th (高能理论)",
            "math-ph (数学物理)",
            "nlin (非线性物理)",
            "nucl-ex (核物理实验)",
            "nucl-th (核物理理论)",
            "physics (物理学)",
            "quant-ph (量子物理)",
            "math (数学)",
            "cs (计算机科学)",
            "q-bio (生物物理)",
            "q-fin (金融数学)",
            "stat (统计学)",
            "eess (电子工程与系统科学)",
            "econ (经济学)"
        )
    )
    
    custom_query = st.text_input(
        "自定义细分方向 / 关键词搜索",
        placeholder="例如: physics.optics 或 quantum computing",
        help="留空则使用上方选中的预设领域。输入类别号(如 physics.optics)即按分类搜索；输入其他词语则按关键词全局搜索。"
    )
    
    if custom_query.strip():
        query_text = custom_query.strip()
        if ":" in query_text:
            search_query = query_text
        elif " " not in query_text and "." in query_text:
            search_query = f"cat:{query_text}"
        else:
            search_query = f"all:{query_text}"
        display_category = query_text
    else:
        search_query = f"cat:{category.split()[0]}"
        display_category = category
    
    max_results = st.slider("获取论文数量", 5, 20, 10)
    
    st.info("提示：点击具体的论文卡片可展开查看详情。")
    
    st.divider()
    st.markdown("### 👨‍💻 关于作者")
    st.link_button("💻 访问 GitHub 仓库", "https://github.com/langxubai/arxiv_summarizer")
    # st.markdown("📧 **联系邮箱**: [您的邮箱地址](mailto:your.email@example.com)")

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
        st.error(f"无法连接到 ArXiv: {e}")
        return []

def ai_summarize(text, api_key):
    if not api_key: return "⚠️ 请先在侧边栏输入 API Key"
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        你是一位资深的理论物理学教授。请阅读以下 arXiv 论文的摘要，并用中文为你的博士生做一个简洁的学术总结。
        
        摘要内容：
        {text}
        
        要求：
        1. **核心问题**：这篇文章解决了什么物理问题？
        2. **方法**：作者使用了什么理论或数值方法？
        3. **结论**：主要结果是什么？有什么新颖性？
        4. 格式使用 Markdown，重点词汇加粗。数学公式使用 LaTeX。
        """
        response = client.models.generate_content(
            model='gemini-flash-latest', contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ AI 总结失败: {str(e)}"

def ai_qa(paper_abstract, summary, question, chat_history, api_key):
    """
    处理针对特定论文的问答
    """
    if not api_key: return "⚠️ 请输入 API Key"
    try:
        client = genai.Client(api_key=api_key)
        
        # 构建上下文 Prompt
        context_prompt = f"""
        你是一位物理学导师。
        
        【当前论文摘要】:
        {paper_abstract}
        
        【之前的总结】:
        {summary}
        
        【学生的历史提问】:
        {chat_history}
        
        【学生当前问题】:
        {question}
        
        请针对学生的当前问题进行解答。如果是解释概念，请尽量通俗易懂但保持学术严谨性。
        """
        
        response = client.models.generate_content(
            model='gemini-flash-latest', contents=context_prompt
        )
        return response.text
    except Exception as e:
        return f"回答失败: {str(e)}"

# --- 4. 主界面逻辑 ---

if not api_key:
    st.warning("👈 请先在左侧侧边栏输入你的 Google Gemini API Key")

with st.spinner(f"正在从 ArXiv 抓取 {display_category} 的最新论文..."):
    papers = fetch_arxiv_papers(search_query, max_results)

st.success(f"成功获取 {len(papers)} 篇最新论文")

# 初始化 session state
if "summaries" not in st.session_state:
    st.session_state.summaries = {}
if "chats" not in st.session_state: # 用于存储每篇论文的聊天记录
    st.session_state.chats = {}

for i, paper in enumerate(papers):
    paper_id = paper['url']
    
    with st.expander(f"📄 {i+1}. {paper['title']} ({paper['published']})"):
        st.markdown(f"**作者**: {paper['authors']}")
        st.markdown(f"**原文链接**: [ArXiv Page]({paper['url']}) | [PDF Download]({paper['pdf_url']})")
        
        col1, col2 = st.columns([1, 1])
        
        # --- 左侧：原始摘要 ---
        with col1:
            st.subheader("原始摘要")
            st.caption(paper['abstract'])
            
        # --- 右侧：AI 互动区 ---
        with col2:
            st.subheader("🤖 AI 导读 & 互动")
            
            # 1. 生成/显示总结
            has_summary = paper_id in st.session_state.summaries
            
            if has_summary:
                # 【修改点 1】使用 container 固定高度，实现内部滚动
                with st.container(height=400, border=True):
                    st.markdown(st.session_state.summaries[paper_id])
            else:
                if st.button(f"生成中文总结", key=f"btn_{i}"):
                    with st.spinner("AI 正在阅读..."):
                        summary = ai_summarize(paper['abstract'], api_key)
                        st.session_state.summaries[paper_id] = summary
                        st.rerun()
                else:
                    st.info("点击上方按钮生成总结")

            # 2. Q&A 问答区 (只有生成了总结才显示)
            if has_summary:
                st.divider()
                st.markdown("#### 💬 对这篇论文有疑问？")
                
                # 初始化这篇论文的聊天记录
                if paper_id not in st.session_state.chats:
                    st.session_state.chats[paper_id] = []
                
                # 显示历史对话
                # 为了不占用太多空间，也可以给聊天记录加个滚动条，或者直接显示
                for chat in st.session_state.chats[paper_id]:
                    with st.chat_message(chat["role"]):
                        st.markdown(chat["content"])
                
                # 【修改点 2】输入框和处理逻辑
                # 使用回调函数处理输入，避免页面刷新导致逻辑混乱
                def submit_question(pid=paper_id):
                    user_input = st.session_state[f"input_{pid}"]
                    if user_input:
                        # 1. 记录用户问题
                        st.session_state.chats[pid].append({"role": "user", "content": user_input})
                        
                        # 2. 获取 AI 回答
                        answer = ai_qa(
                            paper_abstract=paper['abstract'],
                            summary=st.session_state.summaries[pid],
                            question=user_input,
                            chat_history=st.session_state.chats[pid][:-1], # 传入之前的历史
                            api_key=api_key
                        )
                        
                        # 3. 记录 AI 回答
                        st.session_state.chats[pid].append({"role": "assistant", "content": answer})
                        
                        # 4. 清空输入框 (通过设置 key 对应的 session_state 为空)
                        st.session_state[f"input_{pid}"] = ""

                st.text_input(
                    "输入你的问题 (例如：'这里的 DMRG 是什么意思？')",
                    key=f"input_{paper_id}",
                    on_change=submit_question,
                    args=(paper_id,) # 传递参数给回调函数
                )
