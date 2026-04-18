import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def call_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()

        if "choices" not in res_json:
            print("LLM Raw Error:", res_json)
            return "❌ LLM failed."

        return res_json["choices"][0]["message"]["content"]

    except Exception as e:
        print("Exception in LLM:", str(e))
        return "❌ LLM crashed."    