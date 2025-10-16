"""
Configuration Management
Loads environment variables and provides configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Student credentials
    STUDENT_SECRET = os.getenv('STUDENT_SECRET')
    
    # GitHub settings
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
    
    # Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Server settings
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Timeouts and retries
    EVALUATION_TIMEOUT = 600  # 10 minutes in seconds
    RETRY_DELAYS = [1, 2, 4, 8]  # Exponential backoff in seconds
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        required = [
            'STUDENT_SECRET',
            'GITHUB_TOKEN',
            'GITHUB_USERNAME',
            'GEMINI_API_KEY'
        ]
        
        missing = []
        for var in required:
            if not getattr(cls, var):
                missing.append(var)
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please create a .env file with these variables."
            )
        
        return True

# Validate configuration on import
try:
    Config.validate()
    print("✓ Configuration loaded successfully")
except ValueError as e:
    print(f"✗ Configuration error: {e}")
