"""
AIpipe Integration
Uses AIpipe API as an alternative to Google Gemini for code generation
"""
import requests
from config import Config

class AIpipeGenerator:
    """Generates code using AIpipe API (via OpenRouter)"""
    
    def __init__(self):
        # Use OpenRouter endpoint which is more reliable
        self.api_url = "https://aipipe.org/openrouter/v1"
        self.token = Config.AIPIPE_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        print(f"✓ Connected to AIpipe API via OpenRouter")
    
    def generate_content(self, prompt):
        """
        Generate content using AIpipe's OpenRouter proxy
        
        Args:
            prompt: The prompt to send to AIpipe
        
        Returns:
            Response object with Gemini-compatible structure
        """
        # Use OpenRouter's chat completions format with Gemini model
        payload = {
            "model": "google/gemini-2.0-flash-lite-001",  # Free Gemini model via OpenRouter
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
            
            # OpenRouter returns OpenAI-style format, convert to Gemini-style
            # Create a response object that mimics Gemini's structure
            class AIpipeResponse:
                def __init__(self, openrouter_response):
                    # Extract text from OpenRouter response format
                    if 'choices' in openrouter_response and len(openrouter_response['choices']) > 0:
                        choice = openrouter_response['choices'][0]
                        if 'message' in choice and 'content' in choice['message']:
                            self.text = choice['message']['content']
                        else:
                            self.text = ""
                    else:
                        self.text = ""
                    
                    # Store the full response structure
                    self._raw_response = openrouter_response
                    
                    # Create Gemini-compatible structure
                    self.candidates = [
                        type('Candidate', (), {
                            'content': type('Content', (), {
                                'parts': [type('Part', (), {'text': self.text})()]
                            })()
                        })()
                    ]
                    
                    # Create parts list for compatibility
                    self.parts = []
                    if self.text:
                        part_obj = type('Part', (), {'text': self.text})()
                        self.parts.append(part_obj)
            
            return AIpipeResponse(result)
                
        except requests.exceptions.RequestException as e:
            print(f"✗ AIpipe API error: {e}")
            raise
        except Exception as e:
            print(f"✗ Error processing AIpipe response: {e}")
            raise
