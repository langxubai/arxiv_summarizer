import streamlit as st
import arxiv
from google import genai
from google.genai import types
import os

# --- 0. 页面配置与多语言字典 ---
st.set_page_config(page_title="ArXiv AI Daily Summarizer", page_icon="⚛️", layout="wide")

TRANSLATIONS = {
    "zh": {
        "app_title": "⚛️ ArXiv AI Daily Summarizer",
        "app_desc": "专为物理科研人员设计的论文速读工具 (Powered by Gemini)",
        "language_select": "🌐 Language / 语言",
        "sidebar_settings": "⚙️ 设置",
        "api_loaded": "已自动加载 API Key ✅",
        "api_input": "输入 Google Gemini API Key",
        "select_domain": "选择领域",
        "domains": [
            "astro-ph (天体物理)", "cond-mat (凝聚态物理)", "gr-qc (广义相对论)",
            "hep-ex (高能物理实验)", "hep-lat (高能物理-格子)", "hep-ph (高能物理-粒子)",
            "hep-th (高能理论)", "math-ph (数学物理)", "nlin (非线性物理)",
            "nucl-ex (核物理实验)", "nucl-th (核物理理论)", "physics (物理学)",
            "quant-ph (量子物理)", "math (数学)", "cs (计算机科学)",
            "q-bio (生物物理)", "q-fin (金融数学)", "stat (统计学)",
            "eess (电子工程与系统科学)", "econ (经济学)"
        ],
        "custom_query": "自定义细分方向 / 关键词搜索",
        "custom_query_ph": "例如: physics.optics 或 quantum computing",
        "custom_query_help": "留空则使用上方选中的预设领域。输入类别号(如 physics.optics)即按分类搜索；输入其他词语则按关键词全局搜索。",
        "num_papers": "获取论文数量",
        "tip_expand": "提示：点击具体的论文卡片可展开查看详情。",
        "about_author": "### 👨‍💻 关于作者",
        "github_link": "💻 访问 GitHub 仓库",
        "arxiv_error": "无法连接到 ArXiv: {e}",
        "ai_summary_fail": "❌ AI 总结失败: {str_e}",
        "ai_qa_fail": "回答失败: {str_e}",
        "warn_api_key": "👈 请先在左侧侧边栏输入你的 Google Gemini API Key",
        "fetching": "正在从 ArXiv 抓取 {category} 的最新论文...",
        "fetch_success": "成功获取 {count} 篇最新论文",
        "authors": "**作者**: ",
        "orig_link": "**原文链接**: ",
        "orig_abstract": "原始摘要",
        "ai_interaction": "🤖 AI 导读 & 互动",
        "btn_generate": "生成总结",
        "ai_reading": "AI 正在阅读...",
        "click_to_generate": "点击上方按钮生成总结",
        "any_questions": "#### 💬 对这篇论文有疑问？",
        "input_question": "输入你的问题 (例如：'这里的 DMRG 是什么意思？')",
        "prompt_summary_lang": "中文",
        "prompt_qa_lang": "中文",
        "api_key_required": "⚠️ 请先在侧边栏输入 API Key"
    },
    "en": {
        "app_title": "⚛️ ArXiv AI Daily Summarizer",
        "app_desc": "A paper reading tool designed for physics researchers (Powered by Gemini)",
        "language_select": "🌐 Language / 语言",
        "sidebar_settings": "⚙️ Settings",
        "api_loaded": "API Key loaded automatically ✅",
        "api_input": "Enter Google Gemini API Key",
        "select_domain": "Select Domain",
        "domains": [
            "astro-ph (Astrophysics)", "cond-mat (Condensed Matter)", "gr-qc (General Relativity)",
            "hep-ex (High Energy Physics - Experiment)", "hep-lat (High Energy Physics - Lattice)", "hep-ph (High Energy Physics - Phenomenology)",
            "hep-th (High Energy Physics - Theory)", "math-ph (Mathematical Physics)", "nlin (Nonlinear Sciences)",
            "nucl-ex (Nuclear Experiment)", "nucl-th (Nuclear Theory)", "physics (Physics)",
            "quant-ph (Quantum Physics)", "math (Mathematics)", "cs (Computer Science)",
            "q-bio (Quantitative Biology)", "q-fin (Quantitative Finance)", "stat (Statistics)",
            "eess (Electrical Engineering and Systems Science)", "econ (Economics)"
        ],
        "custom_query": "Custom Sub-domain / Keyword Search",
        "custom_query_ph": "e.g., physics.optics or quantum computing",
        "custom_query_help": "Leave blank to use the preset domain selected above. Enter a category code (e.g., physics.optics) to search by category; enter other words for global keyword search.",
        "num_papers": "Number of papers to fetch",
        "tip_expand": "Tip: Click on specific paper cards to expand and view details.",
        "about_author": "### 👨‍💻 About the Author",
        "github_link": "💻 Visit GitHub Repository",
        "arxiv_error": "Failed to connect to ArXiv: {e}",
        "ai_summary_fail": "❌ AI Summary failed: {str_e}",
        "ai_qa_fail": "Answer failed: {str_e}",
        "warn_api_key": "👈 Please enter your Google Gemini API Key in the left sidebar first",
        "fetching": "Fetching the latest papers for {category} from ArXiv...",
        "fetch_success": "Successfully fetched {count} latest papers",
        "authors": "**Authors**: ",
        "orig_link": "**Link**: ",
        "orig_abstract": "Original Abstract",
        "ai_interaction": "🤖 AI Summary & Interaction",
        "btn_generate": "Generate Summary",
        "ai_reading": "AI is reading...",
        "click_to_generate": "Click the button above to generate summary",
        "any_questions": "#### 💬 Any questions about this paper?",
        "input_question": "Enter your question (e.g., 'What does DMRG mean here?')",
        "prompt_summary_lang": "English",
        "prompt_qa_lang": "English",
        "api_key_required": "⚠️ Please enter your API Key first"
    }
}

# 初始化语言设置
if "lang" not in st.session_state:
    st.session_state.lang = "en"

with st.sidebar:
    selected_lang_name = st.radio(
        "🌐 Language / 语言",
        ("English", "中文"),
        index=0 if st.session_state.lang == "en" else 1,
        horizontal=True
    )
    st.session_state.lang = "en" if selected_lang_name == "English" else "zh"

t = TRANSLATIONS[st.session_state.lang]

st.title(t["app_title"])
st.markdown(t["app_desc"])

# --- 2. 侧边栏设置 ---
with st.sidebar:
    st.header(t["sidebar_settings"])
    
    api_key = None
    
    # 尝试从 Secrets 读取 Key
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success(t["api_loaded"])
    except Exception:
        pass

    if not api_key:
        api_key = st.text_input(t["api_input"], type="password")
    
    category = st.selectbox(
        t["select_domain"],
        tuple(t["domains"])
    )
    
    custom_query = st.text_input(
        t["custom_query"],
        placeholder=t["custom_query_ph"],
        help=t["custom_query_help"]
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
    
    max_results = st.slider(t["num_papers"], 5, 20, 10)
    
    st.info(t["tip_expand"])
    
    st.divider()
    st.markdown(t["about_author"])
    st.link_button(t["github_link"], "https://github.com/langxubai/arxiv_summarizer")

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
        error_msg = str(t["arxiv_error"]).replace("{e}", str(e))
        st.error(error_msg)
        return []

def ai_summarize(text, api_key, lang):
    t_func = TRANSLATIONS[lang]
    if not api_key: return t_func["api_key_required"]
    try:
        client = genai.Client(api_key=api_key)
        prompt_lang = t_func["prompt_summary_lang"]
        prompt = f"""
        你是一位资深的理论物理学教授。请阅读以下 arXiv 论文的摘要，并用{prompt_lang}为你的博士生做一个简洁的学术总结。若选择的语言为English，请用英文回答。
        
        摘要内容：
        {text}
        
        要求：
        1. **核心问题**（Core Problem）：这篇文章解决了什么物理问题？
        2. **方法**（Method）：作者使用了什么理论或数值方法？
        3. **结论**（Conclusion）：主要结果是什么？有什么新颖性？
        4. 格式使用 Markdown，重点词汇加粗。数学公式使用 LaTeX。
        """
        response = client.models.generate_content(
            model='gemini-flash-latest', contents=prompt
        )
        return response.text
    except Exception as e:
        return str(t_func["ai_summary_fail"]).replace("{str_e}", str(e))

def ai_qa(paper_abstract, summary, question, chat_history, api_key, lang):
    """
    处理针对特定论文的问答
    """
    t_func = TRANSLATIONS[lang]
    if not api_key: return t_func["api_key_required"]
    try:
        client = genai.Client(api_key=api_key)
        
        prompt_lang = t_func["prompt_qa_lang"]
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
        请使用 {prompt_lang} 进行回答。若为English，请全部使用英文回答。
        """
        
        response = client.models.generate_content(
            model='gemini-flash-latest', contents=context_prompt
        )
        return response.text
    except Exception as e:
        return str(t_func["ai_qa_fail"]).replace("{str_e}", str(e))

# --- 4. 主界面逻辑 ---

if not api_key:
    st.warning(t["warn_api_key"])

fetching_msg = str(t["fetching"]).replace("{category}", display_category)
with st.spinner(fetching_msg):
    papers = fetch_arxiv_papers(search_query, max_results)

success_msg = str(t["fetch_success"]).replace("{count}", str(len(papers)))
st.success(success_msg)

# 初始化 session state
if "summaries" not in st.session_state:
    st.session_state.summaries = {}
if "chats" not in st.session_state: # 用于存储每篇论文的聊天记录
    st.session_state.chats = {}
# 用于存储该摘要是在哪种语言下生成的
if "summary_langs" not in st.session_state:
    st.session_state.summary_langs = {}

for i, paper in enumerate(papers):
    paper_id = paper['url']
    
    with st.expander(f"📄 {i+1}. {paper['title']} ({paper['published']})"):
        st.markdown(f"{t['authors']} {paper['authors']}")
        st.markdown(f"{t['orig_link']} [ArXiv Page]({paper['url']}) | [PDF Download]({paper['pdf_url']})")
        
        col1, col2 = st.columns([1, 1])
        
        # --- 左侧：原始摘要 ---
        with col1:
            st.subheader(t["orig_abstract"])
            st.caption(paper['abstract'])
            
        # --- 右侧：AI 互动区 ---
        with col2:
            st.subheader(t["ai_interaction"])
            
            # 1. 生成/显示总结
            has_summary = paper_id in st.session_state.summaries
            
            # 如果语言切换了，可能需要提示用户重新生成，目前简单处理：保持原有内容的语言，或直接显示
            if has_summary:
                with st.container(height=400, border=True):
                    st.markdown(st.session_state.summaries[paper_id])
                    # 添加一个重新生成按钮来适应当前语言
                    if st.session_state.summary_langs.get(paper_id) != st.session_state.lang:
                        if st.button(t["btn_generate"], key=f"btn_regen_{i}"):
                            with st.spinner(t["ai_reading"]):
                                summary = ai_summarize(paper['abstract'], api_key, st.session_state.lang)
                                st.session_state.summaries[paper_id] = summary
                                st.session_state.summary_langs[paper_id] = st.session_state.lang
                                st.rerun()
            else:
                if st.button(t["btn_generate"], key=f"btn_{i}"):
                    with st.spinner(t["ai_reading"]):
                        summary = ai_summarize(paper['abstract'], api_key, st.session_state.lang)
                        st.session_state.summaries[paper_id] = summary
                        st.session_state.summary_langs[paper_id] = st.session_state.lang
                        st.rerun()
                else:
                    st.info(t["click_to_generate"])

            # 2. Q&A 问答区 (只有生成了总结才显示)
            if has_summary:
                st.divider()
                st.markdown(t["any_questions"])
                
                # 初始化这篇论文的聊天记录
                if paper_id not in st.session_state.chats:
                    st.session_state.chats[paper_id] = []
                
                for chat in st.session_state.chats[paper_id]:
                    with st.chat_message(chat["role"]):
                        st.markdown(chat["content"])
                
                def submit_question(pid=paper_id):
                    user_input = st.session_state[f"input_{pid}"]
                    if user_input:
                        st.session_state.chats[pid].append({"role": "user", "content": user_input})
                        
                        answer = ai_qa(
                            paper_abstract=paper['abstract'],
                            summary=st.session_state.summaries[pid],
                            question=user_input,
                            chat_history=st.session_state.chats[pid][:-1],
                            api_key=api_key,
                            lang=st.session_state.lang
                        )
                        
                        st.session_state.chats[pid].append({"role": "assistant", "content": answer})
                        
                        st.session_state[f"input_{pid}"] = ""

                st.text_input(
                    t["input_question"],
                    key=f"input_{paper_id}",
                    on_change=submit_question,
                    args=(paper_id,) # 传递参数给回调函数
                )
