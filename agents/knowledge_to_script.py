"""
Knowledge File to Sales Script Generator
Extract information from uploaded knowledge files (PDF, DOCX, TXT) and generate sales script
"""
import logging
from typing import Dict, Optional
import os

logger = logging.getLogger(__name__)


def extract_text_from_file(file_path: str, file_type: str = None) -> Optional[str]:
    """
    Extract text content from various file types
    
    Args:
        file_path: Path to the file
        file_type: File type (pdf, docx, txt, etc.)
        
    Returns:
        Extracted text or None if failed
    """
    try:
        if not file_type:
            # Auto-detect from extension
            ext = os.path.splitext(file_path)[1].lower()
            file_type = ext.replace('.', '')
        
        # TXT file
        if file_type == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        # PDF file
        elif file_type == 'pdf':
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except ImportError:
                logger.warning("PyPDF2 not installed, cannot read PDF")
                return None
        
        # DOCX file
        elif file_type in ['docx', 'doc']:
            try:
                from docx import Document
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
            except ImportError:
                logger.warning("python-docx not installed, cannot read DOCX")
                return None
        
        else:
            logger.warning(f"Unsupported file type: {file_type}")
            return None
            
    except Exception as e:
        logger.error(f"Error extracting text from file: {e}")
        return None


def parse_knowledge_file_content(content: str) -> Dict:
    """
    Parse knowledge file content and extract structured information
    
    Args:
        content: Raw text content from file
        
    Returns:
        Structured data dictionary
    """
    data = {
        'success': True,
        'company_name': '',
        'description': '',
        'about_text': '',
        'products_services': [],
        'key_features': [],
        'testimonials': [],
        'contact_info': {},
        'pricing_info': []
    }
    
    lines = content.split('\n')
    content_lower = content.lower()
    
    # Extract company name (look for patterns)
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        if len(line) > 3 and len(line) < 100 and not line.startswith('-'):
            # First meaningful line often is company name
            if not data['company_name']:
                data['company_name'] = line
                break
    
    # Extract sections based on keywords
    current_section = None
    section_content = []
    
    section_keywords = {
        'about': ['about us', 'about', 'who we are', 'company overview'],
        'products': ['products', 'services', 'solutions', 'offerings', 'what we do'],
        'features': ['features', 'benefits', 'advantages', 'why choose'],
        'testimonials': ['testimonials', 'reviews', 'customer feedback', 'success stories'],
        'pricing': ['pricing', 'plans', 'packages', 'cost']
    }
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if line is a section header
        section_found = False
        for section_type, keywords in section_keywords.items():
            if any(keyword in line_lower for keyword in keywords):
                # Save previous section
                if current_section and section_content:
                    content_text = '\n'.join(section_content).strip()
                    if current_section == 'about':
                        data['about_text'] = content_text[:1000]
                    elif current_section == 'products':
                        # Try to extract list items
                        items = [l.strip('- •*') for l in section_content if l.strip().startswith(('-', '•', '*'))]
                        for item in items[:10]:
                            if len(item) > 5:
                                data['products_services'].append({
                                    'name': item.split(':')[0] if ':' in item else item[:50],
                                    'description': item
                                })
                    elif current_section == 'features':
                        items = [l.strip('- •*') for l in section_content if l.strip().startswith(('-', '•', '*'))]
                        data['key_features'].extend([item for item in items if len(item) > 5][:10])
                
                current_section = section_type
                section_content = []
                section_found = True
                break
        
        if not section_found and current_section:
            section_content.append(line)
    
    # Process last section
    if current_section and section_content:
        content_text = '\n'.join(section_content).strip()
        if current_section == 'about' and not data['about_text']:
            data['about_text'] = content_text[:1000]
    
    # Use first paragraph as description if not set
    if not data['description']:
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50 and len(para) < 500:
                data['description'] = para
                break
    
    # If still no description, use beginning of content
    if not data['description'] and content:
        data['description'] = content[:300]
    
    return data


def generate_script_from_knowledge_file(file_path: str, agent_name: str = "AI Agent", agent_tone: str = "professional") -> Optional[str]:
    """
    Generate sales script from knowledge file
    
    Args:
        file_path: Path to knowledge file
        agent_name: Name of the agent
        agent_tone: Tone of conversation
        
    Returns:
        Generated sales script or None if failed
    """
    try:
        # Extract text from file
        text = extract_text_from_file(file_path)
        
        if not text:
            logger.warning(f"Could not extract text from file: {file_path}")
            return None
        
        # Parse content
        knowledge_data = parse_knowledge_file_content(text)
        
        if not knowledge_data['success']:
            return None
        
        # Generate script using sales_script_generator
        from agents.sales_script_generator import generate_sales_script
        
        script = generate_sales_script(
            website_data=knowledge_data,
            agent_name=agent_name,
            agent_tone=agent_tone
        )
        
        return script
        
    except Exception as e:
        logger.error(f"Error generating script from knowledge file: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Test with a sample text file
    test_content = """
TechSolutions Inc.

About Us
We are a leading provider of cloud-based software solutions for modern businesses.
Our platform helps companies streamline operations and increase productivity.

Our Products
- Cloud Storage Pro: Unlimited secure storage for your business
- Analytics Dashboard: Real-time insights and reporting
- Team Collaboration: Enhanced communication tools

Key Features
- 99.9% Uptime Guarantee
- 24/7 Customer Support
- Enterprise-grade Security
- Easy Integration with existing tools
- Scalable infrastructure

Contact Us
Email: sales@techsolutions.com
Phone: 1-800-TECH-SOL
"""
    
    print("=" * 80)
    print("🧪 Testing Knowledge File Parser")
    print("=" * 80)
    
    # Parse content
    data = parse_knowledge_file_content(test_content)
    
    print(f"\n📊 Extracted Data:")
    print(f"   Company: {data['company_name']}")
    print(f"   Description: {data['description'][:100]}...")
    print(f"   Products: {len(data['products_services'])} found")
    print(f"   Features: {len(data['key_features'])} found")
    
    # Generate script
    from agents.sales_script_generator import generate_sales_script
    script = generate_sales_script(data, "Sarah", "friendly")
    
    print(f"\n📝 Generated Script Preview:")
    print("-" * 80)
    print(script[:500])
    print("...")
