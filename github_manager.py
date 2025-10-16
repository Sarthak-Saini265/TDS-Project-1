"""
GitHub Repository Manager
Handles repo creation, pushing code, and enabling GitHub Pages
"""
from github import Github, GithubException
from config import Config
import time

class GitHubManager:
    """Manages GitHub repository operations"""
    
    def __init__(self):
        self.github = Github(Config.GITHUB_TOKEN)
        self.user = self.github.get_user()
        print(f"✓ Connected to GitHub as: {self.user.login}")
    
    def create_and_deploy_repo(self, task_id, files):
        """
        Create a repository, push files, and enable GitHub Pages
        
        Args:
            task_id: Unique identifier for the repo name
            files: Dict of filename -> content
        
        Returns:
            dict with repo_url, commit_sha, pages_url
        """
        # Generate unique repo name
        repo_name = self._generate_repo_name(task_id)
        print(f"\n📦 Creating repository: {repo_name}")
        
        try:
            # Create the repository
            repo = self.user.create_repo(
                repo_name,
                description=f"Auto-generated app for task {task_id}",
                private=False,  # Must be public
                auto_init=False  # We'll push our own files
            )
            print(f"✓ Repository created: {repo.html_url}")
            
            # Push files
            self._push_files(repo, files)
            
            # Get the commit SHA
            commit_sha = repo.get_commits()[0].sha
            print(f"✓ Latest commit: {commit_sha[:7]}")
            
            # Enable GitHub Pages
            pages_url = self._enable_github_pages(repo)
            
            return {
                'repo_url': repo.html_url,
                'commit_sha': commit_sha,
                'pages_url': pages_url
            }
            
        except GithubException as e:
            print(f"✗ GitHub error: {e.status} - {e.data.get('message', 'Unknown error')}")
            raise
    
    def update_repo(self, repo_name, files):
        """
        Update an existing repository with new files
        
        Args:
            repo_name: Name of the repository to update
            files: Dict of filename -> content
        
        Returns:
            dict with repo_url, commit_sha, pages_url
        """
        print(f"\n🔄 Updating repository: {repo_name}")
        
        try:
            # Get the existing repository
            repo = self.user.get_repo(repo_name)
            
            # Update files
            self._update_files(repo, files)
            
            # Get the new commit SHA
            commit_sha = repo.get_commits()[0].sha
            print(f"✓ Updated commit: {commit_sha[:7]}")
            
            # Pages URL remains the same
            pages_url = f"https://{self.user.login}.github.io/{repo_name}/"
            
            return {
                'repo_url': repo.html_url,
                'commit_sha': commit_sha,
                'pages_url': pages_url
            }
            
        except GithubException as e:
            print(f"✗ GitHub error: {e.status} - {e.data.get('message', 'Unknown error')}")
            raise
    
    def _generate_repo_name(self, task_id):
        """Generate a unique repository name from task ID"""
        # Clean the task ID to be a valid repo name
        repo_name = task_id.replace('_', '-').replace(' ', '-').lower()
        # Ensure it starts with a letter
        if not repo_name[0].isalpha():
            repo_name = 'task-' + repo_name
        return repo_name
    
    def _push_files(self, repo, files):
        """Push multiple files to the repository"""
        print(f"📤 Pushing {len(files)} files...")
        
        for filename, content in files.items():
            try:
                repo.create_file(
                    path=filename,
                    message=f"Add {filename}",
                    content=content
                )
                print(f"  ✓ {filename}")
            except GithubException as e:
                print(f"  ✗ Failed to create {filename}: {e.data.get('message', 'Unknown error')}")
                raise
    
    def _update_files(self, repo, files):
        """Update existing files in the repository"""
        print(f"📤 Updating {len(files)} files...")
        
        for filename, content in files.items():
            try:
                # Try to get existing file
                try:
                    existing_file = repo.get_contents(filename)
                    # Update existing file
                    repo.update_file(
                        path=filename,
                        message=f"Update {filename}",
                        content=content,
                        sha=existing_file.sha
                    )
                    print(f"  ✓ Updated {filename}")
                except GithubException as e:
                    if e.status == 404:
                        # File doesn't exist, create it
                        repo.create_file(
                            path=filename,
                            message=f"Add {filename}",
                            content=content
                        )
                        print(f"  ✓ Created {filename}")
                    else:
                        raise
            except GithubException as e:
                print(f"  ✗ Failed to update {filename}: {e.data.get('message', 'Unknown error')}")
                raise
    
    def _enable_github_pages(self, repo):
        """Enable GitHub Pages for the repository"""
        print("🌐 Enabling GitHub Pages...")
        
        try:
            # Enable Pages using the main branch via API
            # PyGithub doesn't have direct Pages support, so we'll use the REST API
            import requests
            
            url = f"https://api.github.com/repos/{repo.full_name}/pages"
            headers = {
                "Authorization": f"token {Config.GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            data = {
                "source": {
                    "branch": "main",
                    "path": "/"
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 201:
                print("✓ GitHub Pages enabled")
            elif response.status_code == 409:
                print("✓ GitHub Pages already enabled")
            else:
                print(f"⚠ Warning: Pages API returned {response.status_code}: {response.text}")
        except Exception as e:
            print(f"⚠ Warning: Could not enable Pages via API: {e}")
        
        # Construct the Pages URL
        pages_url = f"https://{self.user.login}.github.io/{repo.name}/"
        print(f"✓ Pages URL: {pages_url}")
        
        # Wait a moment for Pages to be ready
        print("⏳ Waiting for GitHub Pages to deploy...")
        time.sleep(5)
        
        return pages_url
    
    def get_repo_file_content(self, repo_name, filename):
        """
        Get the content of a specific file from a repository
        
        Args:
            repo_name: Name of the repository
            filename: Name of the file to retrieve
        
        Returns:
            str: Content of the file
        """
        try:
            repo = self.user.get_repo(repo_name)
            file_content = repo.get_contents(filename)
            return file_content.decoded_content.decode('utf-8')
        except GithubException as e:
            print(f"✗ Could not retrieve {filename}: {e.data.get('message', 'Unknown error')}")
            return None
    
    def repo_exists(self, repo_name):
        """Check if a repository exists"""
        try:
            self.user.get_repo(repo_name)
            return True
        except GithubException:
            return False
