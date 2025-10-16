# LLM Code Deployment System

An AI-powered application that automatically builds, deploys, and updates web applications based on natural language briefs.

## Overview

This system:
1. Receives POST requests with app requirements
2. Uses Google Gemini Pro to generate code
3. Creates GitHub repositories automatically
4. Deploys to GitHub Pages
5. Handles revision requests

## Setup

### Prerequisites

- Python 3.9+
- GitHub account with Personal Access Token
- Google Gemini API key

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd Project1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```
STUDENT_SECRET=your-secret-from-google-form
GITHUB_TOKEN=ghp_your_github_token
GEMINI_API_KEY=your-gemini-api-key
GITHUB_USERNAME=your-github-username
```

## Usage

### Running the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000/api-endpoint`

### Testing

Send a POST request:
```bash
curl http://localhost:5000/api-endpoint \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

## Project Structure

```
Project1/
├── app.py                 # Main Flask application
├── llm_generator.py       # Gemini code generation
├── github_manager.py      # GitHub API interactions
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
└── README.md            # This file
```

## License

MIT License - see LICENSE file for details
