FROM python:3.13.5-slim

WORKDIR /app

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# # 【新增】更换为阿里云镜像源，解决 apt-get 无法连接或速度慢的问题
# # 注意：Python 3.12+ slim 版本通常基于 Debian Bookworm，源文件位置已变更为 /etc/apt/sources.list.d/debian.sources
# RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# RUN printf "%s\n" \
# 	"deb https://mirrors.tuna.tsinghua.edu.cn/debian stable main contrib non-free non-free-firmware" \
# 	"deb https://mirrors.tuna.tsinghua.edu.cn/debian stable-updates main contrib non-free non-free-firmware" \
# 	"deb https://mirrors.tuna.tsinghua.edu.cn/debian-security stable-security main contrib non-free non-free-firmware" \
# 	> /etc/apt/sources.list

=======
>>>>>>> c8b9531 (Add Dockerfile)
=======
# 【新增】更换为阿里云镜像源，解决 apt-get 无法连接或速度慢的问题
# 注意：Python 3.12+ slim 版本通常基于 Debian Bookworm，源文件位置已变更为 /etc/apt/sources.list.d/debian.sources
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources
=======
# # 【新增】更换为阿里云镜像源，解决 apt-get 无法连接或速度慢的问题
# # 注意：Python 3.12+ slim 版本通常基于 Debian Bookworm，源文件位置已变更为 /etc/apt/sources.list.d/debian.sources
# RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources
>>>>>>> d094f40 (Refresh .gitignore rules)

# RUN printf "%s\n" \
# 	"deb https://mirrors.tuna.tsinghua.edu.cn/debian stable main contrib non-free non-free-firmware" \
# 	"deb https://mirrors.tuna.tsinghua.edu.cn/debian stable-updates main contrib non-free non-free-firmware" \
# 	"deb https://mirrors.tuna.tsinghua.edu.cn/debian-security stable-security main contrib non-free non-free-firmware" \
# 	> /etc/apt/sources.list

>>>>>>> d6a6970 (Merge Hugging Face config)
=======
>>>>>>> 8c090af (Duplicate from streamlit/streamlit-template-space)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY src/ ./src/

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# RUN pip3 install -r requirements.txt

# # 【新增】使用清华源安装 Python 依赖 (解决 pip install 慢/失败)
# RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
=======
RUN pip3 install -r requirements.txt
>>>>>>> c8b9531 (Add Dockerfile)
=======
# RUN pip3 install -r requirements.txt

<<<<<<< HEAD
# 【新增】使用清华源安装 Python 依赖 (解决 pip install 慢/失败)
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
>>>>>>> d6a6970 (Merge Hugging Face config)
=======
# # 【新增】使用清华源安装 Python 依赖 (解决 pip install 慢/失败)
# RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
>>>>>>> d094f40 (Refresh .gitignore rules)
=======
RUN pip3 install -r requirements.txt
>>>>>>> 8c090af (Duplicate from streamlit/streamlit-template-space)

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

<<<<<<< HEAD
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

=======
ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
>>>>>>> 8c090af (Duplicate from streamlit/streamlit-template-space)
