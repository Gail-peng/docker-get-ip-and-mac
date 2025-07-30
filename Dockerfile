# 使用Python基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app


# 复制应用代码
COPY . .

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY /requirements.txt .
RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 5000

# 运行Flask应用
CMD ["python", "web_app.py"]  