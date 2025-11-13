import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3.1:free")
        
        self.base = os.getenv("OPENROUTER_BASE", "https://openrouter.ai")

    def chat(self, code, lang):
        

        payload = {
            
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}
        
       
        resp = httpx.post(
            f"{self.base}/api/v1/chat/completions", 
            json=payload, 
            headers=headers, 
            timeout=120
        )
        resp.raise_for_status()

    def chat(self, code, lang):
        prompt = f"""
You are a senior {lang} developer.
Analyze the following code and return JSON with:
1. "summary": short description of what it does.
2. "errors": list of bugs, logical issues, or bad practices.
3. "suggestions": list of improvements or optimizations.
Respond ONLY in JSON.
"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a coding assistant."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": code},
            ],
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = httpx.post(f"{self.base}/v1/chat/completions", json=payload, headers=headers, timeout=120)
        resp.raise_for_status()

        try:
            return json.loads(resp.json()["choices"][0]["message"]["content"])
        except Exception:
            return {"summary": "Error parsing model output", "errors": [], "suggestions": []}
