"""
Main Flask Application
API endpoint that receives requests, generates code, and deploys to GitHub
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from llm_generator import LLMGenerator
from github_manager import GitHubManager
import requests
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
llm_generator = LLMGenerator()
github_manager = GitHubManager()

# Store processed tasks to handle Round 2
processed_tasks = {}

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'LLM Code Deployment API',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api-endpoint', methods=['POST'])
def api_endpoint():
    """
    Main endpoint that receives build/update requests
    
    Expected JSON payload:
    {
        "email": "student@example.com",
        "secret": "...",
        "task": "task-id",
        "round": 1,
        "nonce": "unique-id",
        "brief": "Build this app...",
        "checks": ["Check 1", "Check 2"],
        "evaluation_url": "https://...",
        "attachments": [{"name": "file.csv", "url": "data:..."}]
    }
    """
    try:
        # Get JSON payload
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        print(f"\n{'='*60}")
        print(f"📨 Received request at {datetime.now().isoformat()}")
        print(f"{'='*60}")
        
        # Step 1: Verify secret
        if not verify_secret(data.get('secret')):
            print("✗ Secret verification failed")
            return jsonify({'error': 'Invalid secret'}), 403
        
        print("✓ Secret verified")
        
        # Step 2: Extract request data
        email = data.get('email')
        task_id = data.get('task')
        round_num = data.get('round', 1)
        nonce = data.get('nonce')
        brief = data.get('brief')
        checks = data.get('checks', [])
        evaluation_url = data.get('evaluation_url')
        attachments = data.get('attachments', [])
        
        # Validate required fields
        required_fields = ['email', 'task', 'nonce', 'brief', 'evaluation_url']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return jsonify({'error': f'Missing required fields: {", ".join(missing)}'}), 400
        
        print(f"📧 Email: {email}")
        print(f"🎯 Task: {task_id}")
        print(f"🔄 Round: {round_num}")
        print(f"🎲 Nonce: {nonce}")
        
        # Step 3: Process based on round
        if round_num == 1:
            result = process_round_1(
                email, task_id, round_num, nonce, brief, 
                checks, evaluation_url, attachments
            )
        else:
            result = process_round_2(
                email, task_id, round_num, nonce, brief,
                checks, evaluation_url, attachments
            )
        
        if result.get('success'):
            print(f"\n✅ Request processed successfully!")
            print(f"{'='*60}\n")
            return jsonify({
                'status': 'success',
                'message': f'Round {round_num} completed',
                'repo_url': result.get('repo_url'),
                'pages_url': result.get('pages_url')
            }), 200
        else:
            print(f"\n❌ Request failed: {result.get('error')}")
            print(f"{'='*60}\n")
            return jsonify({
                'status': 'error',
                'message': result.get('error')
            }), 500
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Internal error: {str(e)}'
        }), 500

def verify_secret(provided_secret):
    """Verify the provided secret matches the configured secret"""
    return provided_secret == Config.STUDENT_SECRET

def process_round_1(email, task_id, round_num, nonce, brief, checks, evaluation_url, attachments):
    """Process Round 1: Build and deploy new app"""
    print(f"\n🚀 Starting Round 1 processing...")
    
    try:
        # Step 1: Generate code using LLM
        print(f"\n[1/4] Generating code with Gemini Pro...")
        generated_files = llm_generator.generate_app(
            brief=brief,
            checks=checks,
            attachments=attachments,
            task_id=task_id
        )
        
        # Step 2: Create GitHub repo and deploy
        print(f"\n[2/4] Creating GitHub repository...")
        repo_info = github_manager.create_and_deploy_repo(
            task_id=task_id,
            files=generated_files
        )
        
        # Step 3: Store for Round 2
        repo_name = github_manager._generate_repo_name(task_id)
        processed_tasks[task_id] = {
            'repo_name': repo_name,
            'round_1_completed': True
        }
        
        # Step 4: Notify evaluation API
        print(f"\n[3/4] Notifying evaluation API...")
        notification_success = notify_evaluation_api(
            evaluation_url=evaluation_url,
            email=email,
            task=task_id,
            round_num=round_num,
            nonce=nonce,
            repo_url=repo_info['repo_url'],
            commit_sha=repo_info['commit_sha'],
            pages_url=repo_info['pages_url']
        )
        
        if not notification_success:
            print("⚠ Warning: Evaluation API notification failed (but repo was created)")
        
        print(f"\n[4/4] Round 1 complete! ✓")
        
        return {
            'success': True,
            'repo_url': repo_info['repo_url'],
            'commit_sha': repo_info['commit_sha'],
            'pages_url': repo_info['pages_url']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def process_round_2(email, task_id, round_num, nonce, brief, checks, evaluation_url, attachments):
    """Process Round 2: Update existing app"""
    print(f"\n🔄 Starting Round 2 processing...")
    
    try:
        # Generate repo name from task_id (same logic as in github_manager)
        repo_name = github_manager._generate_repo_name(task_id)
        
        # Check if the repo exists on GitHub
        if not github_manager.repo_exists(repo_name):
            return {
                'success': False,
                'error': f'Repository {repo_name} does not exist. Round 1 must be completed first or task name is incorrect.'
            }
        
        # Step 1: Get existing code
        print(f"\n[1/4] Retrieving existing code...")
        existing_code = github_manager.get_repo_file_content(repo_name, 'index.html')
        
        if not existing_code:
            return {
                'success': False,
                'error': 'Could not retrieve existing code'
            }
        
        # Step 2: Update code using LLM
        print(f"\n[2/4] Updating code with Gemini Pro...")
        updated_files = llm_generator.update_app(
            existing_code=existing_code,
            brief=brief,
            checks=checks,
            attachments=attachments
        )
        
        # Also update README
        updated_files['README.md'] = llm_generator._generate_readme(
            brief=f"[Updated] {brief}",
            checks=checks,
            task_id=task_id,
            attachment_info=llm_generator._process_attachments(attachments)
        )
        
        # Step 3: Update GitHub repo
        print(f"\n[3/4] Updating GitHub repository...")
        repo_info = github_manager.update_repo(
            repo_name=repo_name,
            files=updated_files
        )
        
        # Step 4: Notify evaluation API
        print(f"\n[4/4] Notifying evaluation API...")
        notification_success = notify_evaluation_api(
            evaluation_url=evaluation_url,
            email=email,
            task=task_id,
            round_num=round_num,
            nonce=nonce,
            repo_url=repo_info['repo_url'],
            commit_sha=repo_info['commit_sha'],
            pages_url=repo_info['pages_url']
        )
        
        if not notification_success:
            print("⚠ Warning: Evaluation API notification failed (but repo was updated)")
        
        print(f"\n✓ Round 2 complete!")
        
        return {
            'success': True,
            'repo_url': repo_info['repo_url'],
            'commit_sha': repo_info['commit_sha'],
            'pages_url': repo_info['pages_url']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def notify_evaluation_api(evaluation_url, email, task, round_num, nonce, repo_url, commit_sha, pages_url):
    """
    Notify the evaluation API with repo details
    Implements retry logic with exponential backoff
    """
    payload = {
        'email': email,
        'task': task,
        'round': round_num,
        'nonce': nonce,
        'repo_url': repo_url,
        'commit_sha': commit_sha,
        'pages_url': pages_url
    }
    
    print(f"📤 Posting to: {evaluation_url}")
    
    # Try with exponential backoff
    for attempt, delay in enumerate([0] + Config.RETRY_DELAYS, 1):
        if delay > 0:
            print(f"⏳ Waiting {delay}s before retry #{attempt}...")
            time.sleep(delay)
        
        try:
            response = requests.post(
                evaluation_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✓ Evaluation API responded: 200 OK")
                return True
            else:
                print(f"⚠ Evaluation API responded: {response.status_code}")
                print(f"  Response: {response.text[:200]}")
                
        except requests.RequestException as e:
            print(f"⚠ Request failed: {str(e)}")
    
    print(f"✗ All {len(Config.RETRY_DELAYS) + 1} attempts failed")
    return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 LLM Code Deployment API")
    print("="*60)
    print(f"📍 Running on http://localhost:{Config.PORT}")
    print(f"📡 Endpoint: http://localhost:{Config.PORT}/api-endpoint")
    print(f"👤 GitHub User: {Config.GITHUB_USERNAME}")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
