from google import genai
import os

# 建议：不要硬编码 Key，从环境变量读取，或者运行时手动输入测试
# api_key = os.environ.get("GEMINI_API_KEY") 
# client = genai.Client(api_key=api_key)

# 仅仅为了列出模型，通常需要先实例化 Client。
# 如果你只是想测试环境，可以使用以下代码：

def list_models():
    api_key = input("请输入你的 API Key: ")
    try:
        client = genai.Client(api_key=api_key)
        print("正在获取可用模型列表...")
        # 新版 SDK 获取模型列表的方式略有不同，通常通过 models.list()
        for model in client.models.list():
            # 过滤出支持 generateContent 的模型
            if "generateContent" in model.supported_generation_methods:
                print(f"模型 ID: {model.name}")
                print(f"显示名称: {model.display_name}")
                print("-" * 20)
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    list_models()