import os
import requests

class AIService:

    def summarize_repo(self, data):
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Summarize this GitHub repository in a clean format:

        Name: {data['repo']['name']}
        Stars: {data['repo']['stars']}
        Language: {data['repo']['language']}
        Open Issues: {data['issues']['open']}
        Contributors: {len(data['contributors'])}

        Give output in this format:

        1. What it is:
        2. Activity level:
        3. Code quality:
        4. Short conclusion:

        Keep it very short and clean.
        """

        body = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=body)

        # 🔥 ADD THIS CHECK
        if response.status_code != 200:
            return f"AI Error: {response.text}"

        result = response.json()

        # 🔥 SAFE ACCESS
        try:
            return result["choices"][0]["message"]["content"]
        except:
            return "AI response format error"
        

    def rate_repo(self, data):
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Analyze this GitHub repository and give a rating.

        Name: {data['repo']['name']}
        Stars: {data['repo']['stars']}
        Open Issues: {data['issues']['open']}
        Contributors: {len(data['contributors'])}

        Give ONLY one word rating from:
        Excellent / Good / Average / Needs Improvement

        No explanation. Just the rating word.
        """

        body = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code != 200:
            return "Unknown"

        try:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except:
            return "Unknown"
        
    
    def get_suggestions(self, data):
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Analyze this GitHub repository and give improvement suggestions.

        Name: {data['repo']['name']}
        Stars: {data['repo']['stars']}
        Open Issues: {data['issues']['open']}
        Contributors: {len(data['contributors'])}

        Give 3 to 5 short actionable suggestions to improve the repository.

        Keep each suggestion in one line.
        Do not use numbering or extra symbols.
        """

        body = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=body)

            if response.status_code != 200:
                return ["No suggestions available"]

            result = response.json()
            text = result["choices"][0]["message"]["content"]

            suggestions = [line.strip() for line in text.split("\n") if line.strip()]
            return suggestions

        except:
            return ["No suggestions available"]
            
    