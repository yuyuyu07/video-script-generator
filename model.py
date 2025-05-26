from langchain_openai import ChatOpenAI
import os

class Model:
    def __init__(self, temperature,api_key):
        self.gemini_2_flash = ChatOpenAI(
            temperature=temperature,
            model="gemini-2.0-flash",
            api_key= api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        self.deepseek_v3 = ChatOpenAI(
            temperature=temperature,
            model = "deepseek-chat",
            api_key = api_key,
            base_url="https://api.deepseek.com/v1")
        self.kimi_moonshot_v1_8k = ChatOpenAI(
            temperature=temperature,
            model = "moonshot-v1-8k",
            api_key = api_key,
            base_url = "https://api.moonshot.cn/v1")
