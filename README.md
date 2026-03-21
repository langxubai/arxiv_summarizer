<!-- ---
title: ArXiv AI Daily Summarizer
emoji: ⚛️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.31.0
app_file: src/app.py
pinned: false
license: MIT
--- -->

# ⚛️ ArXiv AI Daily Summarizer

[English](#ArXiv-AI-Daily-Summarizer) | [中文版](#Arxiv-AI-每日总结)

********************
Update: 2026-01-28 This project is now available on Streamlit Community Cloud: [https://arxiv-summarizer-2026.streamlit.app/](https://arxiv-summarizer-2026.streamlit.app/)
********************

**ArXiv AI Daily Summarizer** is a quick paper-reading tool designed specifically for researchers in the fields of physics and artificial intelligence (AI).

It leverages the powerful capabilities of the **Google Gemini** large model to automatically fetch the latest uploaded papers on ArXiv. It then generates targeted academic summaries in Chinese, helping you quickly filter daily literature and keep up with research frontiers.

## ✨ Key Features

* **Daily Latest Paper Fetching**: Automatically gets the latest uploaded papers from specific domains on ArXiv.
* **Multi-Domain Support**:
    * Strongly Correlated Electrons (cond-mat.str-el)
    * Mesoscale and Nanoscale Physics (cond-mat.mes-hall)
    * Quantum Physics (quant-ph)
    * Artificial Intelligence (cs.AI)
    * Computational Physics (physics.comp-ph)
* **AI In-depth Guide**: Calls the Google Gemini model (Gemini Flash) to generate professional summaries from three dimensions: "Core Problem", "Research Method", and "Main Conclusion".
* **One-Click Access**: Provides ArXiv links and PDF download links to the original papers.
* **Convenient Interaction**: A modern interface built with Streamlit, supporting sidebar configuration and card-based reading.

## 🚀 Quick Start (Local Run)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/arxiv_summarizer.git
cd arxiv_summarizer
```

### 2. Environment Configuration

It is recommended to use an environment with Python 3.10+.

```bash
pip install -r requirements.txt
```

### 3. Set API Key

You can configure the Google Gemini API Key in two ways:

* **Method A (Recommended)**: Create a `.streamlit/secrets.toml` file in the project's root directory:
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "Your_GOOGLE_GEMINI_API_KEY"
```

* **Method B**: Manually enter the Key in the sidebar of the web page after running it.

### 4. Run the Application

Note: The source code of this project is located in the `src` directory.

```bash
streamlit run src/app.py
```

## 🐳 Docker Deployment

This project includes a `Dockerfile` and supports containerized deployment.

1. **Build Image**
```bash
docker build -t arxiv-summarizer .
```

2. **Run Container**
```bash
docker run -p 8501:8501 arxiv-summarizer
```

## 🤗 Deploy to Hugging Face Spaces

This project is already configured with metadata tailored for Hugging Face Spaces and can be deployed directly.

1. Create a new Space on Hugging Face.
2. Select **Streamlit** as the SDK.
3. Upload the code of this project to your Space repository. **Note: The YAML Front Matter in the README is commented out. You need to uncomment it when deploying to Hugging Face.**
4. In the **Settings** -> **Variables and secrets** page of the Space:
* Add a new Secret with the name `GEMINI_API_KEY` and the value being your Google Gemini API Key.

5. Wait for the build to complete, and it will be ready to use!

> **Note**: Since the main program of this project is located at `src/app.py`, the YAML configuration at the top of the README has already specified `app_file: src/app.py`. There is no need to manually modify the Space config.

## 🛠️ Project Structure

```text
.
├── src/
│   └── app.py          # Main Streamlit application
├── requirements.txt    # Project dependencies
├── Dockerfile          # Docker build file
├── .gitattributes      # Git attributes configuration
├── .gitignore          # Git ignore configuration
└── README.md           # Project description
```

## 📝 Dependencies

* [Streamlit](https://streamlit.io/)
* [ArXiv API Wrapper](https://github.com/lukasschwab/arxiv.py)
* [Google GenAI SDK](https://ai.google.dev/)

---

*Powered by Google Gemini & ArXiv*

---

# ⚛️ ArXiv AI 每日总结

**ArXiv AI 每日总结** 是一个专为物理学和人工智能领域科研人员设计的论文速读工具。

它利用 **Google Gemini** 大模型的强大能力，自动抓取 ArXiv 上最新的论文，并生成针对性的中文学术总结，帮助你快速筛选每日文献，紧跟学术前沿。

## ✨ 主要功能

* **每日最新论文抓取**：自动从 ArXiv 获取指定领域的最新上传论文。
* **多领域支持**：
    * 强关联电子 (cond-mat.str-el)
    * 介观物理 (cond-mat.mes-hall)
    * 量子物理 (quant-ph)
    * 人工智能 (cs.AI)
    * 计算物理 (physics.comp-ph)
* **AI 深度导读**：调用 Google Gemini 模型 (Gemini Flash)，从“核心问题”、“研究方法”、“主要结论”三个维度生成专业的中文摘要。
* **一键直达**：提供原始论文的 ArXiv 链接和 PDF 下载链接。
* **便捷交互**：基于 Streamlit 构建的现代化界面，支持侧边栏配置和卡片式阅读。

## 🚀 快速开始 (本地运行)

### 1. 克隆项目
```bash
git clone https://github.com/your-username/arxiv_summarizer.git
cd arxiv_summarizer
```

### 2. 环境配置

建议使用 Python 3.10+ 环境。

```bash
pip install -r requirements.txt
```

### 3. 设置 API Key

你有两种方式配置 Google Gemini API Key：

* **方式 A (推荐)**：在项目根目录创建 `.streamlit/secrets.toml` 文件：
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "你的_GOOGLE_GEMINI_API_KEY"
```

* **方式 B**：直接在运行后的网页侧边栏中手动输入 Key。

### 4. 运行应用

注意：本项目的源码位于 `src` 目录下。

```bash
streamlit run src/app.py
```

## 🐳 Docker 部署

本项目包含 `Dockerfile`，支持容器化部署。

1. **构建镜像**
```bash
docker build -t arxiv-summarizer .
```

2. **运行容器**
```bash
docker run -p 8501:8501 arxiv-summarizer
```

## 🤗 部署到 Hugging Face Spaces

本项目已配置好适配 Hugging Face Spaces 的元数据，可直接部署。

1. 在 Hugging Face 上创建一个新的 Space。
2. 选择 **Streamlit** 作为 SDK。
3. 将本项目代码上传至 Space 仓库。**注意该项目README中YAML Front Matter被注释，部署到Hugging Face时需要取消注释。**
4. 在 Space 的 **Settings** -> **Variables and secrets** 页面中：
* 添加一个新的 Secret，名称为 `GEMINI_API_KEY`，值为你的 Google Gemini API Key。

5. 等待构建完成即可使用！

> **注意**：由于本项目的主程序位于 `src/app.py`，README 顶部的 YAML 配置中已指定 `app_file: src/app.py`，无需手动修改 Space 配置。

## 🛠️ 项目结构

```text
.
├── src/
│   └── app.py          # Streamlit 主程序
├── requirements.txt    # 项目依赖
├── Dockerfile          # Docker 构建文件
├── .gitattributes      # Git 属性配置
├── .gitignore          # Git 忽略配置
└── README.md           # 项目说明
```

## 📝 依赖库

* [Streamlit](https://streamlit.io/)
* [ArXiv API Wrapper](https://github.com/lukasschwab/arxiv.py)
* [Google GenAI SDK](https://ai.google.dev/)

---

*Powered by Google Gemini & ArXiv*
