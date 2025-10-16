# Setup Instructions for LLM Code Deployment System

## Step 1: Create .env file

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and fill in your actual values:

```
STUDENT_SECRET=your-secret-from-google-form
GITHUB_TOKEN=ghp_your_github_personal_access_token
GITHUB_USERNAME=your-github-username
GEMINI_API_KEY=your-gemini-api-key
PORT=5000
```

## Step 2: Get GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name like "LLM Code Deployment"
4. Select these permissions:
   - `repo` (all)
   - `admin:repo_hook` (optional, for webhooks)
5. Click "Generate token"
6. Copy the token (starts with `ghp_`)
7. Paste it in your `.env` file

## Step 3: Get Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key
4. Paste it in your `.env` file

## Step 4: Install Python Dependencies

Create a virtual environment and install packages:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Test the Configuration

```powershell
python -c "from config import Config; print('Config OK!')"
```

If you see "✓ Configuration loaded successfully", you're ready!

## Step 6: Run the Server

```powershell
python app.py
```

You should see:
```
🚀 LLM Code Deployment API
📍 Running on http://localhost:5000
```

## Step 7: Test with Sample Request

In a new terminal:

```powershell
# Edit test_request.json to use your actual secret first!

# Then send the request
curl http://localhost:5000/api-endpoint `
  -H "Content-Type: application/json" `
  -d "@test_request.json"
```

Or use PowerShell:

```powershell
$json = Get-Content test_request.json -Raw
Invoke-RestMethod -Uri http://localhost:5000/api-endpoint -Method Post -Body $json -ContentType "application/json"
```

## Troubleshooting

### "Missing required environment variables"
- Make sure your `.env` file exists and has all required variables
- Check that there are no spaces around the `=` signs

### "GitHub error: 401"
- Your GitHub token is invalid or expired
- Make sure the token has the correct permissions

### "Module not found"
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

### "Gemini API error"
- Check that your API key is correct
- Ensure you have API quota available
