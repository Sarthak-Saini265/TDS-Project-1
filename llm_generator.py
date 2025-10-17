"""
LLM Code Generator using Google Gemini Pro or AIpipe
Generates web application code based on briefs and requirements
Automatically falls back to AIpipe if Gemini fails
"""
import google.generativeai as genai
from config import Config
import json
import base64

# Always configure both if available
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    print("✓ Gemini configured (primary)")

if Config.AIPIPE_TOKEN:
    from aipipe_generator import AIpipeGenerator
    print("✓ AIpipe configured (fallback)")

if Config.USE_AIPIPE:
    print("⚠ AIpipe set as primary in config")

class LLMGenerator:
    """Generates code using Google Gemini Pro with AIpipe fallback"""
    
    def __init__(self):
        # Initialize both models if available
        self.gemini_model = None
        self.aipipe_model = None
        self.last_provider_used = None  # Track which provider was actually used
        
        if Config.GEMINI_API_KEY:
            self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        
        if Config.AIPIPE_TOKEN:
            self.aipipe_model = AIpipeGenerator()
        
        # Determine primary model
        if Config.USE_AIPIPE and self.aipipe_model:
            self.primary = "aipipe"
            print("🔄 Using AIpipe as primary LLM")
        elif self.gemini_model:
            self.primary = "gemini"
            print("🔄 Using Gemini as primary LLM")
        elif self.aipipe_model:
            self.primary = "aipipe"
            print("🔄 Using AIpipe (Gemini not available)")
        else:
            raise ValueError("No LLM provider configured! Need either GEMINI_API_KEY or AIPIPE_TOKEN")
    
    def _generate_with_fallback(self, prompt, generation_config=None):
        """
        Try to generate content with automatic fallback
        Tries primary model first, falls back to secondary on failure
        """
        errors = []
        
        # Try primary model first
        if self.primary == "gemini" and self.gemini_model:
            try:
                print("🤖 Trying Gemini...")
                if generation_config:
                    response = self.gemini_model.generate_content(prompt, generation_config=generation_config)
                else:
                    response = self.gemini_model.generate_content(prompt)
                print("✓ Gemini successful")
                self.last_provider_used = "Gemini"  # Track successful provider
                return response
            except Exception as e:
                error_msg = str(e)
                errors.append(f"Gemini failed: {error_msg}")
                print(f"⚠ Gemini failed: {error_msg}")
                
                # Check if it's a quota or timeout error
                if any(keyword in error_msg.lower() for keyword in ['quota', 'timeout', '429', '504', 'exceeded']):
                    print("💡 Quota/timeout error detected, trying AIpipe fallback...")
                    if self.aipipe_model:
                        try:
                            print("🤖 Falling back to AIpipe...")
                            response = self.aipipe_model.generate_content(prompt)
                            print("✓ AIpipe fallback successful")
                            self.last_provider_used = "AIpipe (fallback)"  # Track fallback
                            return response
                        except Exception as e2:
                            errors.append(f"AIpipe fallback failed: {str(e2)}")
                            print(f"✗ AIpipe fallback failed: {str(e2)}")
                raise Exception(f"Both providers failed: {'; '.join(errors)}")
        
        elif self.primary == "aipipe" and self.aipipe_model:
            try:
                print("🤖 Trying AIpipe...")
                response = self.aipipe_model.generate_content(prompt)
                print("✓ AIpipe successful")
                self.last_provider_used = "AIpipe"  # Track successful provider
                return response
            except Exception as e:
                error_msg = str(e)
                errors.append(f"AIpipe failed: {error_msg}")
                print(f"⚠ AIpipe failed: {error_msg}")
                
                # Try Gemini fallback
                if self.gemini_model:
                    try:
                        print("🤖 Falling back to Gemini...")
                        if generation_config:
                            response = self.gemini_model.generate_content(prompt, generation_config=generation_config)
                        else:
                            response = self.gemini_model.generate_content(prompt)
                        print("✓ Gemini fallback successful")
                        self.last_provider_used = "Gemini (fallback)"  # Track fallback
                        return response
                    except Exception as e2:
                        errors.append(f"Gemini fallback failed: {str(e2)}")
                        print(f"✗ Gemini fallback failed: {str(e2)}")
                raise Exception(f"Both providers failed: {'; '.join(errors)}")
        
        raise Exception("No LLM provider available")
    
    def generate_app(self, brief, checks, attachments=None, task_id=None):
        """
        Generate a complete web application based on the brief
        
        Args:
            brief: Description of what the app should do
            checks: List of evaluation criteria
            attachments: List of attachment objects with name and data URL
            task_id: Unique task identifier
        
        Returns:
            dict with 'index.html' and 'README.md' content
        """
        print(f"\n🤖 Generating code for task: {task_id}")
        print(f"📝 Brief: {brief[:100]}...")
        
        # Decode attachments if present
        attachment_info = self._process_attachments(attachments)
        
        # Build the prompt
        prompt = self._build_prompt(brief, checks, attachment_info)
        
        # Generate code with configuration
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192,
        }
        
        response = self._generate_with_fallback(
            prompt,
            generation_config=generation_config
        )
        
        # Extract text from response properly
        response_text = self._extract_response_text(response)
        
        # Parse the response
        generated_files = self._parse_response(response_text)
        
        # Add README
        generated_files['README.md'] = self._generate_readme(
            brief, checks, task_id, attachment_info
        )
        
        # Add LICENSE
        generated_files['LICENSE'] = self._generate_mit_license()
        
        print(f"✓ Generated {len(generated_files)} files")
        return generated_files
    
    def _process_attachments(self, attachments):
        """Process and decode attachments"""
        if not attachments:
            return []
        
        attachment_info = []
        for att in attachments:
            name = att.get('name', 'attachment')
            data_url = att.get('url', '')
            
            # Parse data URI
            if data_url.startswith('data:'):
                try:
                    # Format: data:mime/type;base64,<data>
                    header, encoded = data_url.split(',', 1)
                    mime_type = header.split(':')[1].split(';')[0]
                    
                    # Decode base64
                    decoded = base64.b64decode(encoded)
                    
                    attachment_info.append({
                        'name': name,
                        'mime_type': mime_type,
                        'size': len(decoded),
                        'data_url': data_url,  # Keep original for embedding
                        'preview': decoded[:100].decode('utf-8', errors='ignore') if mime_type.startswith('text') else None
                    })
                except Exception as e:
                    print(f"⚠ Warning: Could not decode attachment {name}: {e}")
                    attachment_info.append({
                        'name': name,
                        'data_url': data_url,
                        'error': str(e)
                    })
        
        return attachment_info
    
    def _build_prompt(self, brief, checks, attachment_info):
        """Build the prompt for Gemini"""
        
        attachment_section = ""
        if attachment_info:
            attachment_section = "\n\n**ATTACHMENTS:**\n"
            for att in attachment_info:
                attachment_section += f"- {att['name']} ({att.get('mime_type', 'unknown')})\n"
                if att.get('preview'):
                    attachment_section += f"  Preview: {att['preview'][:50]}...\n"
                attachment_section += f"  Data URL available: {att['data_url'][:50]}...\n"
        
        checks_section = "\n".join([f"- {check}" for check in checks])
        
        prompt = f"""You are an expert web developer. Generate a complete, production-ready single-page web application.

**REQUIREMENTS:**
{brief}

**EVALUATION CHECKS (your code must pass these):**
{checks_section}
{attachment_section}

**INSTRUCTIONS:**
1. Generate a complete, working HTML file (index.html)
2. Use Bootstrap 5 from CDN for styling
3. Include all necessary JavaScript inline
4. Handle attachments by embedding data URLs directly in the code
5. Make sure all element IDs and checks are satisfied
6. Use modern, clean, professional code
7. Add proper error handling
8. Include comments explaining key functionality
9. Ensure the page is responsive and accessible

**OUTPUT FORMAT:**
Provide your response in this exact format:

```html
<!-- index.html -->
[Your complete HTML code here]
```

Only provide the HTML code. Make it complete and ready to deploy.
"""
        
        return prompt
    
    def _extract_response_text(self, response):
        """
        Extract text from Gemini response, handling both simple and complex responses
        """
        try:
            # Try simple text accessor first
            return response.text
        except:
            # If that fails, extract from parts
            if hasattr(response, 'parts'):
                text_parts = []
                for part in response.parts:
                    if hasattr(part, 'text'):
                        text_parts.append(part.text)
                return ''.join(text_parts)
            elif hasattr(response, 'candidates') and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate.content, 'parts'):
                    text_parts = []
                    for part in candidate.content.parts:
                        if hasattr(part, 'text'):
                            text_parts.append(part.text)
                    return ''.join(text_parts)
            
            # Fallback
            return str(response)
    
    def _parse_response(self, response_text):
        """Parse the LLM response to extract code files"""
        files = {}
        
        # Extract HTML code from markdown code blocks
        if '```html' in response_text:
            # Find the HTML block
            start = response_text.find('```html') + 7
            end = response_text.find('```', start)
            html_code = response_text[start:end].strip()
            files['index.html'] = html_code
        elif '```' in response_text:
            # Try generic code block
            start = response_text.find('```') + 3
            # Skip language identifier if present
            newline = response_text.find('\n', start)
            end = response_text.find('```', newline)
            html_code = response_text[newline:end].strip()
            files['index.html'] = html_code
        else:
            # Use the whole response as HTML
            files['index.html'] = response_text.strip()
        
        return files
    
    def _generate_readme(self, brief, checks, task_id, attachment_info):
        """Generate a professional README.md"""
        
        attachments_section = ""
        if attachment_info:
            attachments_section = "\n### Attachments\n\n"
            for att in attachment_info:
                attachments_section += f"- `{att['name']}` - {att.get('mime_type', 'unknown type')}\n"
        
        checks_list = "\n".join([f"- {check}" for check in checks])
        
        readme = f"""# {task_id or 'Web Application'}

## Summary

{brief}

## Features

This application was automatically generated to meet the following requirements:

{checks_list}

## Setup

This is a static web application that requires no build process.

### Local Development

1. Clone this repository
2. Open `index.html` in a web browser
3. Or serve with a local server:
   ```bash
   python -m http.server 8000
   ```
{attachments_section}

## Usage

Simply open the `index.html` file in a modern web browser. The application includes:
- Bootstrap 5 for responsive design
- Inline JavaScript for functionality
- Embedded data for attachments

## Code Explanation

### HTML Structure
- Uses semantic HTML5 elements
- Bootstrap components for UI
- Responsive design that works on all devices

### JavaScript Functionality
- Handles user interactions
- Processes data from attachments
- Updates DOM elements dynamically
- Includes error handling

### Styling
- Bootstrap 5 framework
- Custom CSS for specific requirements
- Mobile-first responsive design

## Deployment

This application is deployed on GitHub Pages and accessible at the URL provided in the repository settings.

## License

MIT License - See LICENSE file for details

## Auto-Generated

This application was automatically generated using AI-powered code generation.
Generated on: {task_id}
"""
        
        return readme
    
    def _generate_mit_license(self):
        """Generate MIT License text"""
        return """MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    def update_app(self, existing_code, brief, checks, attachments=None):
        """
        Update an existing application based on new requirements
        
        Args:
            existing_code: The current index.html content
            brief: New requirements or modifications needed
            checks: Updated evaluation criteria
            attachments: New attachments if any
        
        Returns:
            dict with updated files
        """
        print(f"\n🔄 Updating existing app")
        print(f"📝 Update brief: {brief[:100]}...")
        
        attachment_info = self._process_attachments(attachments)
        attachment_section = ""
        if attachment_info:
            attachment_section = "\n\n**NEW ATTACHMENTS:**\n"
            for att in attachment_info:
                attachment_section += f"- {att['name']}: {att['data_url'][:50]}...\n"
        
        checks_section = "\n".join([f"- {check}" for check in checks])
        
        prompt = f"""You are updating an existing web application. Here is the current code:

```html
{existing_code}
```

**UPDATE REQUIREMENTS:**
{brief}

**NEW EVALUATION CHECKS (code must pass these):**
{checks_section}
{attachment_section}

**INSTRUCTIONS:**
1. Modify the existing code to meet the new requirements
2. Keep all existing functionality that still applies
3. Add new features as specified
4. Ensure all new checks pass
5. Maintain code quality and comments
6. Keep using Bootstrap 5 and inline JavaScript

**OUTPUT FORMAT:**
Provide the complete updated HTML:

```html
<!-- index.html -->
[Your updated HTML code here]
```

Provide only the complete, updated HTML code.
"""
        
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192,
        }
        
        response = self._generate_with_fallback(
            prompt,
            generation_config=generation_config
        )
        response_text = self._extract_response_text(response)
        updated_files = self._parse_response(response_text)
        
        print(f"✓ Updated {len(updated_files)} files")
        return updated_files
