"""
AIpipe Integration
Uses AIpipe API as an alternative to Google Gemini for code generation
"""
import requests
from config import Config

class AIpipeGenerator:
    """Generates code using AIpipe API"""
    
    def __init__(self):
        self.api_url = "https://aipipe.ds.study.iitm.ac.in"
        self.token = Config.AIPIPE_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        print(f"✓ Connected to AIpipe API")
    
    def generate_content(self, prompt):
        """
        Generate content using AIpipe API
        
        Args:
            prompt: The prompt to send to AIpipe
        
        Returns:
            Response object with text attribute
        """
        payload = {
            "model": "gemini-2.0-flash-exp",  # or whatever model AIpipe supports
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 8192
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                json=payload,
                headers=self.headers,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Create a response object that mimics Gemini's structure
            class AIpipeResponse:
                def __init__(self, content):
                    self.text = content
                    self.parts = [type('Part', (), {'text': content})()]
                    self.candidates = [
                        type('Candidate', (), {
                            'content': type('Content', (), {
                                'parts': [type('Part', (), {'text': content})()]
                            })()
                        })()
                    ]
            
            # Extract the generated text from AIpipe response
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return AIpipeResponse(content)
            else:
                raise ValueError("No content in AIpipe response")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ AIpipe API error: {e}")
            raise
        except Exception as e:
            print(f"✗ Error processing AIpipe response: {e}")
            raise
