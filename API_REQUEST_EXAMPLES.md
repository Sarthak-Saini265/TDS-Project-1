# Example POST Request to Deployed Hugging Face API

## URL
POST https://YOUR-USERNAME-SPACE-NAME.hf.space/api-endpoint

## Headers
Content-Type: application/json

## Body (JSON)
{
  "email": "student@example.com",
  "secret": "geralt_of_rivia",
  "task": "my-app-task-12345",
  "round": 1,
  "nonce": "unique-nonce-xyz",
  "brief": "Create a todo list app with Bootstrap 5. Users can add tasks via an input field with id='task-input', display them in a list with id='task-list', and mark tasks as complete by clicking them.",
  "checks": [
    "Page uses Bootstrap 5",
    "Has input field with id='task-input'",
    "Has task list with id='task-list'",
    "Can add new tasks",
    "Can mark tasks as complete"
  ],
  "evaluation_url": "https://example.com/notify",
  "attachments": []
}

## Curl Example
curl https://YOUR-USERNAME-SPACE-NAME.hf.space/api-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "geralt_of_rivia",
    "task": "my-app-task-12345",
    "round": 1,
    "nonce": "unique-nonce-xyz",
    "brief": "Create a simple hello world page with Bootstrap 5",
    "checks": ["Page displays Hello World"],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
  }'

## PowerShell Example
$body = @{
    email = "student@example.com"
    secret = "geralt_of_rivia"
    task = "my-app-task-12345"
    round = 1
    nonce = "unique-nonce-xyz"
    brief = "Create a simple hello world page with Bootstrap 5"
    checks = @("Page displays Hello World")
    evaluation_url = "https://httpbin.org/post"
    attachments = @()
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://YOUR-USERNAME-SPACE-NAME.hf.space/api-endpoint" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"

## Python Example
import requests

url = "https://YOUR-USERNAME-SPACE-NAME.hf.space/api-endpoint"

payload = {
    "email": "student@example.com",
    "secret": "geralt_of_rivia",
    "task": "my-app-task-12345",
    "round": 1,
    "nonce": "unique-nonce-xyz",
    "brief": "Create a simple hello world page with Bootstrap 5",
    "checks": ["Page displays Hello World"],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
}

response = requests.post(url, json=payload)
print(response.json())

## JavaScript/Fetch Example
fetch('https://YOUR-USERNAME-SPACE-NAME.hf.space/api-endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: "student@example.com",
    secret: "geralt_of_rivia",
    task: "my-app-task-12345",
    round: 1,
    nonce: "unique-nonce-xyz",
    brief: "Create a simple hello world page with Bootstrap 5",
    checks: ["Page displays Hello World"],
    evaluation_url: "https://httpbin.org/post",
    attachments: []
  })
})
.then(response => response.json())
.then(data => console.log(data));

## Expected Response (Success - 200 OK)
{
  "status": "success",
  "message": "Round 1 completed",
  "repo_url": "https://github.com/Sarthak-Saini265/my-app-task-12345",
  "pages_url": "https://Sarthak-Saini265.github.io/my-app-task-12345/"
}

## Round 2 Example (Update Existing App)
{
  "email": "student@example.com",
  "secret": "geralt_of_rivia",
  "task": "my-app-task-12345",  // SAME task name as Round 1
  "round": 2,  // This is Round 2!
  "nonce": "unique-nonce-round2",
  "brief": "Add a delete button to each task that removes it from the list",
  "checks": [
    "Each task has a delete button",
    "Clicking delete removes the task"
  ],
  "evaluation_url": "https://httpbin.org/post",
  "attachments": []
}

## Field Descriptions

- **email**: Your email address (for tracking)
- **secret**: Your authentication secret (must match STUDENT_SECRET in HF secrets)
- **task**: Unique identifier for this app (used as repo name)
- **round**: 1 for new app, 2 for update
- **nonce**: Unique identifier for this specific request
- **brief**: Natural language description of what to build
- **checks**: List of criteria for evaluation
- **evaluation_url**: Where to POST the results (repo URL, commit SHA, pages URL)
- **attachments**: Array of files with data URLs (e.g., CSV, images as base64)

## With Attachments Example
{
  "email": "student@example.com",
  "secret": "geralt_of_rivia",
  "task": "data-visualizer-123",
  "round": 1,
  "nonce": "nonce-123",
  "brief": "Create a page that reads data.csv from attachments and displays it in a Bootstrap table",
  "checks": ["Displays CSV data", "Uses Bootstrap table"],
  "evaluation_url": "https://httpbin.org/post",
  "attachments": [
    {
      "name": "data.csv",
      "url": "data:text/csv;base64,bmFtZSxhZ2UKSm9obiwzMApKYW5lLDI1"
    }
  ]
}

## Testing Locally Before HF Deploy
# Use localhost while developing
curl http://localhost:5000/api-endpoint -H "Content-Type: application/json" -d '...'

## After Deploying to HF
# Replace localhost with your HF Space URL
curl https://YOUR-USERNAME-SPACE-NAME.hf.space/api-endpoint -H "Content-Type: application/json" -d '...'
