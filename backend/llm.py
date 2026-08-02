import os
import json
from typing import Dict, Any, Optional
from groq import Groq
import requests

class LLMProvider:
    def __init__(self, provider: str = "groq"):
        """Initialize LLM provider"""
        self.provider = provider.lower()
        self.groq_client = None
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        if self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                self.groq_client = Groq(api_key=api_key)
            else:
                print("WARNING: GROQ_API_KEY not set. Using mock responses.")
        elif self.provider == "ollama":
            print(f"Using Ollama at {self.ollama_base_url}")
        else:
            print(f"Unknown provider: {provider}. Using mock responses.")
    
    def generate_response(
        self, 
        prompt: str, 
        response_type: str = "text",
        model: str = "llama-3.3-70b-versatile"
    ) -> Dict[str, Any]:
        """Generate response from LLM"""
        try:
            if self.provider == "groq" and self.groq_client:
                return self._call_groq(prompt, response_type, model)
            elif self.provider == "ollama":
                return self._call_ollama(prompt, response_type, model)
            else:
                return self._mock_response(prompt, response_type)
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._mock_response(prompt, response_type)
    
    def _call_groq(self, prompt: str, response_type: str, model: str) -> Dict[str, Any]:
        """Call Groq API"""
        try:
            # Model selection based on task
            if response_type == "essay":
                model = "llama-3.3-70b-versatile"  # Best for long-form
            elif response_type == "html" or response_type == "markdown":
                model = "llama-3.3-70b-versatile"  # Good for structured output
            else:
                model = model  # Use specified model
            
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,  # Lower temperature for more focused, document-based responses
                max_tokens=1500 if response_type == "essay" else 1000,
                top_p=0.9
            )
            
            content = response.choices[0].message.content
            
            if response_type == "html":
                content = self._format_html(content)
            elif response_type == "markdown":
                content = self._format_markdown(content)
            
            return {"content": content, "type": response_type, "success": True}
            
        except Exception as e:
            print(f"Groq API error: {e}")
            return self._mock_response(prompt, response_type)
    
    def _call_ollama(self, prompt: str, response_type: str, model: str) -> Dict[str, Any]:
        """Call Ollama API"""
        try:
            # Ollama model mapping
            ollama_model = "llama3.2"  # Default
            
            payload = {
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 1500 if response_type == "essay" else 1000,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                content = response.json()["response"]
                
                if response_type == "html":
                    content = self._format_html(content)
                elif response_type == "markdown":
                    content = self._format_markdown(content)
                
                return {"content": content, "type": response_type, "success": True}
            else:
                print(f"Ollama API error: {response.status_code}")
                return self._mock_response(prompt, response_type)
                
        except Exception as e:
            print(f"Ollama connection error: {e}")
            return self._mock_response(prompt, response_type)
    
    def _format_html(self, content: str) -> str:
        """Format content as HTML"""
        # Ensure it's valid HTML
        if not content.strip().startswith("<"):
            content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Article</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }}
        h2 {{ color: #007acc; margin-top: 30px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 10px; }}
        .highlight {{ background-color: #fff3cd; padding: 5px; border-radius: 3px; font-weight: bold; }}
        .takeaway {{ background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <article>
        {content}
    </article>
</body>
</html>"""
        return content
    
    def _format_markdown(self, content: str) -> str:
        """Format content as Markdown"""
        # Ensure it starts with proper markdown
        if not content.strip().startswith("#"):
            content = f"# Generated Article\n\n{content}"
        return content
    
    def _mock_response(self, prompt: str, response_type: str) -> Dict[str, Any]:
        """Generate mock response for demonstration"""
        import random
        
        base_response = "Based on Lenny's Podcast transcripts, I can provide insights about startup growth, product-market fit, and founder stories. "
        
        if "product-market fit" in prompt.lower():
            content = base_response + "Product-market fit is when customers are pulling the product out of your hands rather than you pushing it to them. Founders describe it as feeling like the product is selling itself."
        elif "essay" in response_type:
            content = f"""# The Startup Journey: Finding Product-Market Fit

**Hook:** Every startup founder dreams of that magical moment when their product clicks with the market. But how do you actually get there?

**Key Takeaways:**
1. **Listen to your early users** - They'll tell you what's working and what's not
2. **Measure leading indicators** - Not just revenue, but engagement and retention
3. **Iterate relentlessly** - The first version is rarely the right one
4. **Focus on a specific niche** - Trying to serve everyone means serving no one well

**Actionable Takeaway:** Start by solving a painful problem for a small group of people who desperately need your solution. Obsess over their experience, and growth will follow."""
        elif response_type == "html":
            content = """<!DOCTYPE html>
<html>
<head>
    <title>Startup Insights</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #007acc; }
        .insight { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007acc; }
    </style>
</head>
<body>
    <h1>Key Startup Insights</h1>
    <div class="insight">
        <h2>Product-Market Fit</h2>
        <p>The moment when your product satisfies strong market demand.</p>
    </div>
    <div class="insight">
        <h2>Growth Strategies</h2>
        <p>Focus on retention before acquisition. Happy users bring more users.</p>
    </div>
</body>
</html>"""
        elif response_type == "markdown":
            content = """# Startup Growth Principles

## 1. Start with Problem-Solution Fit
- Identify a painful problem
- Build the simplest solution
- Validate with real users

## 2. Seek Product-Market Fit
- Measure user engagement
- Track retention metrics
- Listen to customer feedback

## 3. Scale with Confidence
- Systematize successful processes
- Hire for cultural fit
- Maintain quality while growing"""
        else:
            content = base_response + "This is a mock response. In the actual application, this would be generated by the LLM based on transcript context."
        
        return {"content": content, "type": response_type, "success": False, "mock": True}

# Example usage
if __name__ == "__main__":
    llm = LLMProvider("groq")
    response = llm.generate_response("What is product-market fit?", "text")
    print(response)