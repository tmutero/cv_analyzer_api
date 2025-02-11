import openai
from openai import AsyncOpenAI
import os
from app.settings import settings
import json
import re
class OpenAIService:


    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.api_key = api_key or settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("An API key must be provided or set in the OPENAI_API_KEY environment variable.")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = model


    async def query(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """
        Sends a prompt to the OpenAI API and returns the generated text.
        :param prompt: The prompt text to send to the model.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: Sampling temperature to control randomness.
        :return: The text generated by the model.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API request failed: {e}")


    async def assess_application(self, app_description: str):
        prompt = f"""
        You are a CV writing expert. You will receive a plain-text string containing a CV. Analyze this CV by performing the following checks:
    
        1. **Grammar and Spelling**  
           - Identify any grammatical errors, spelling mistakes, or typos.
    
        2. **Clarity and Readability**  
           - Check sentence structure, use of action verbs, and overall flow.
    
        3. **Required Sections**  
           - Look for missing or incomplete sections typically found in a CV (e.g., Contact Information, Summary/Objective, Work Experience, Education, Skills).
    
        4. **Relevant Terminology**  
           - Ensure use of correct and relevant industry or role-specific terminology.
    
        5. **Detail and Completeness**  
           - Check if key accomplishments, responsibilities, and achievements are adequately described.
    
        6. **Formatting & Consistency**  
           - Assess whether headings, bullet points, and dates are presented consistently.
    
        After analyzing, provide your response strictly in the following JSON format:
    
         ```json
            {{
              "score": 0,
              "suggested_improvements": [
                {{
                  "section": "Section",
                  "issues": [
                    {{
                      "issue": "Text",
                      "suggestion": "Text"
                    }}
                  ]
                }}
              ]
            }}
            ```
    
        CV Content:
        {app_description}
        """
        response = await self.query(prompt, max_tokens=500, temperature=0.5)

        cleaned_text = re.sub(r"```json\n|\n```", "", response)

        return json.loads(cleaned_text)




