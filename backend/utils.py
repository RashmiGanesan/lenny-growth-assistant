import uuid
import datetime
import json
from typing import Dict, Any

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.datetime.now().isoformat()

def format_chat_response(
    content: str, 
    response_type: str = "text", 
    session_id: str = None
) -> Dict[str, Any]:
    """Format a standardized chat response"""
    return {
        "content": content,
        "type": response_type,
        "session_id": session_id,
        "timestamp": get_current_timestamp()
    }

def clean_response(text: str) -> str:
    """Clean and sanitize response text"""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    # Remove any potential HTML/JS injection
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    return text

def format_essay_prompt(user_question: str, context: str) -> str:
    """Format prompt for essay generation that deeply uses document knowledge"""
    return f"""You are analyzing Lenny's Podcast transcripts to provide expert startup insights. Write a structured mini-essay (300-500 words) that answers the user's question using ONLY information from the provided transcript extracts.

DOCUMENT KNOWLEDGE FROM TRANSCRIPTS:
{context}

USER QUESTION TO ADDRESS:
{user_question}

STRUCTURED ESSAY FORMAT (STRICT ADHERENCE TO TRANSCRIPT CONTENT):

**Introduction** (1 paragraph)
- Start with an engaging hook statement directly related to transcript insights
- Clearly state what the transcripts reveal about the user's question
- Mention 1-2 specific startups or founders referenced in the extracts

**Core Transcript Analysis** (2 paragraphs)
- Paragraph 1: Explain the primary concept or framework from the transcripts
- Paragraph 2: Detail specific examples, data points, or quotes from the extracts
- MUST cite specific transcript excerpts (e.g., "According to Extract 2...")

**Practical Applications** (1-2 paragraphs)
- Convert transcript insights into actionable advice
- Provide step-by-step recommendations based on successful patterns observed
- Include measurable outcomes mentioned in the transcripts

**Conclusion** (1 paragraph)
- Summarize the key transcript-based insights
- State the most important takeaway for founders
- End with a forward-looking statement based on transcript learnings

FORMATTING REQUIREMENTS:
1. **Paragraph structure**: Each paragraph must be separated by a blank line
2. **Bullet points**: Use bullet points only for lists within paragraphs
3. **Citations**: Reference extracts by number in parentheses after relevant claims
4. **Headings**: Use bold headers for each section (Introduction, Core Analysis, etc.)
5. **Word count**: Aim for 400 words total
6. **Line breaks**: Ensure proper spacing between paragraphs and sections

DOCUMENT-BASED WRITING RULES:
1. Every claim MUST be supported by transcript extracts
2. Reference specific extracts by number (Extract 1, Extract 2, etc.)
3. Include direct quotes or paraphrases from transcripts when available
4. If certain information is missing from transcripts, acknowledge this limitation
5. Do NOT add external knowledge beyond what's in the transcripts

SAMPLE ESSAY STRUCTURE:
**Introduction**
[First paragraph with hook and thesis statement]

**Core Transcript Analysis**  
[First paragraph explaining primary concept from transcripts (Extract 1)]
[Second paragraph detailing specific examples (Extract 2, Extract 3)]

**Practical Applications**
[Paragraph with actionable recommendations based on transcript evidence]

**Conclusion**
[Final paragraph summarizing key insights and takeaways]

The essay should demonstrate deep understanding and synthesis of the specific transcript content provided with clear, properly formatted paragraphs."""

def format_rag_prompt(user_question: str, context: str) -> str:
    """Format prompt for RAG-based Q&A that strictly uses document knowledge"""
    return f"""You are a startup growth expert analyzing Lenny's Podcast transcripts. Answer the user's question by analyzing and synthesizing ONLY the provided transcript extracts.

TRANSCRIPT ANALYSIS CONTEXT:
{context}

USER QUESTION:
{user_question}

RESPONSE STRUCTURE (MUST USE TRANSCRIPT EVIDENCE):

**Direct Answer Based on Transcripts**
Start with a concise answer that summarizes what the transcripts reveal about this question. Reference at least 2 specific extracts.

**Evidence-Based Analysis**
Organize the transcript evidence into clear categories with proper paragraph structure:

Key Concepts:
Identify 2-3 main frameworks or principles from the extracts. Use clear paragraphs with specific extract references.

Specific Examples:
Mention concrete startups, founders, or metrics discussed in the transcripts. Each example should be in its own paragraph or bullet point.

Patterns Observed:
Describe recurring themes across multiple extracts. Use clear paragraph structure.

**Transcript-Based Recommendations**
Provide 3 actionable recommendations derived DIRECTLY from transcript content:
1. [Recommendation 1] - Based on [specific extract reference]
2. [Recommendation 2] - Supported by [evidence from transcripts]
3. [Recommendation 3] - Drawing from [transcript pattern]

**Transcript Limitations & Next Steps**
Acknowledge what information might be missing from these specific extracts.
Suggest what additional questions would help get more complete insights.

FORMATTING REQUIREMENTS:
1. Use bold headers for each section (Direct Answer, Evidence-Based Analysis, etc.)
2. Separate paragraphs with blank lines
3. Use bullet points only within sections, not for entire response
4. Keep response length: 250-350 words
5. Each paragraph should focus on one main idea
6. Include line breaks between sections for readability

STRICT GUIDELINES:
1. Base EVERY claim on transcript extracts
2. Reference extracts by number when citing evidence
3. Use exact quotes from transcripts when possible
4. If transcripts don't cover a specific aspect, explicitly say so
5. Do NOT add knowledge beyond the provided transcript extracts
6. Maintain objective, evidence-based tone

Your primary goal is to demonstrate how well you can extract, synthesize, and apply knowledge from the specific transcript documents provided with clear, structured formatting."""


def format_html_prompt(user_question: str, context: str) -> str:
    """Format prompt for HTML output that integrates transcript knowledge"""
    return f"""Create an HTML document that presents transcript-based analysis of the user's question. The HTML should clearly cite and reference specific transcript extracts.

TRANSCRIPT ANALYSIS CONTEXT:
{context}

USER QUESTION TO ADDRESS IN HTML:
{user_question}

HTML STRUCTURE REQUIREMENTS:

1. **Document Header**: Include proper HTML5 doctype, meta tags, and a title mentioning transcript analysis

2. **Evidence Section**: 
   - Create a dedicated section showing key transcript extracts with similarity scores
   - Use <blockquote> or <div class="quote"> for direct transcript quotes
   - Include <span class="extract-ref"> for source references (Extract 1, Extract 2, etc.)

3. **Analysis Section**:
   - Organize findings into categories based on transcript evidence
   - Use semantic HTML: <section>, <article>, <h2>, <h3> tags
   - Include tables for metrics mentioned in transcripts

4. **Recommendations Section**:
   - Present actionable steps as ordered/unordered lists
   - Link each recommendation to specific transcript evidence
   - Include implementation timeline based on transcript patterns

5. **Visual Elements**:
   - Use CSS classes for styling evidence boxes, quotes, and highlights
   - Include appropriate semantic markup for emphasis and structure
   - Ensure the document is readable and well-organized

STYLE & CITATION REQUIREMENTS:
1. Every claim must cite specific transcript extracts
2. Include similarity percentages for referenced extracts
3. Use bold (<strong>) for key concepts mentioned in transcripts
4. Add tooltips or footnotes for transcript references
5. Create responsive design with clear visual hierarchy

The HTML should demonstrate rigorous document analysis while being visually appealing and easy to navigate."""

def format_markdown_prompt(user_question: str, context: str) -> str:
    """Format prompt for Markdown output that integrates transcript knowledge"""
    return f"""Create a Markdown document that presents transcript-based analysis of the user's question. Use proper Markdown formatting with clear transcript citations.

TRANSCRIPT ANALYSIS CONTEXT:
{context}

USER QUESTION TO ADDRESS IN MARKDOWN:
{user_question}

MARKDOWN STRUCTURE REQUIREMENTS:

1. **Header Section**:
   - Main title with query focus
   - Summary of transcript sources and similarity scores
   - Table showing extract references

2. **Evidence Presentation**:
   - Use blockquote formatting for direct transcript quotes
   - Include inline citations like `[Extract 1, 85% similarity]`
   - Create numbered lists for sequential recommendations

3. **Analysis Organization**:
   - Use headers (##, ###) for clear section hierarchy
   - Include tables for comparative data from transcripts
   - Use bold (**text**) for key concepts and metrics

4. **Actionable Framework**:
   - Create checklists using `- [ ]` syntax
   - Include timelines based on transcript implementation patterns
   - Add code blocks for any measurement formulas mentioned

5. **References Section**:
   - List all transcript extracts referenced
   - Include similarity scores and source files
   - Add cross-references to specific recommendations

MARKDOWN FORMATTING RULES:
1. Use `> quote` for transcript excerpts
2. Include `**bold**` for transcript-emphasized concepts
3. Create tables with pipe `|` syntax for data
4. Use `- [ ] task` syntax for actionable items
5. Add `~~~` code blocks for metrics or formulas

The Markdown should be ready for publication while maintaining strict adherence to transcript evidence and clear attribution."""