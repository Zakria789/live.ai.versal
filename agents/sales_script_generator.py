"""
Sales Script Generator
Generate professional sales scripts from website data
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SalesScriptGenerator:
    """Generate sales script from website data"""
    
    def __init__(self, website_data: dict, agent_name: str = "AI Agent", agent_tone: str = "professional"):
        """
        Initialize script generator
        
        Args:
            website_data: Extracted website data from scraper
            agent_name: Name of the agent
            agent_tone: Tone of the conversation (friendly, professional, casual, etc.)
        """
        self.data = website_data
        self.agent_name = agent_name
        self.agent_tone = agent_tone.lower()
        
    def generate_script(self) -> str:
        """Generate complete sales script"""
        
        if not self.data.get('success'):
            return self._generate_fallback_script()
        
        script_parts = []
        
        # 1. Opening/Greeting
        script_parts.append(self._generate_greeting())
        
        # 2. Introduction
        script_parts.append(self._generate_introduction())
        
        # 3. Value Proposition
        script_parts.append(self._generate_value_proposition())
        
        # 4. Products/Services
        if self.data.get('products_services'):
            script_parts.append(self._generate_products_section())
        
        # 5. Key Features/Benefits
        if self.data.get('key_features'):
            script_parts.append(self._generate_features_section())
        
        # 6. Social Proof (Testimonials)
        if self.data.get('testimonials'):
            script_parts.append(self._generate_testimonials_section())
        
        # 7. Objection Handling
        script_parts.append(self._generate_objection_handling())
        
        # 8. Call to Action
        script_parts.append(self._generate_call_to_action())
        
        # 9. Closing
        script_parts.append(self._generate_closing())
        
        # Combine all parts
        full_script = "\n\n".join(script_parts)
        
        return full_script
    
    def _generate_greeting(self) -> str:
        """Generate opening greeting"""
        company_name = self.data.get('company_name', 'our company')
        
        greetings = {
            'friendly': f"Hi there! I'm {self.agent_name} calling from {company_name}. How are you doing today?",
            'professional': f"Good [morning/afternoon/evening]. I'm {self.agent_name} calling from {company_name}. How are you today?",
            'casual': f"Hey! I'm {self.agent_name} from {company_name}. How's it going?",
            'enthusiastic': f"Hello! I'm {self.agent_name} from {company_name}! I hope you're having a great day!",
        }
        
        greeting = greetings.get(self.agent_tone, greetings['professional'])
        
        return f"""=== OPENING GREETING ===
{greeting}

[Wait for response and acknowledge]

Great! I appreciate you taking the time to speak with me today."""
    
    def _generate_introduction(self) -> str:
        """Generate introduction section"""
        company_name = self.data.get('company_name', 'our company')
        description = self.data.get('description', '')
        about = self.data.get('about_text', '')
        
        intro = f"""=== INTRODUCTION ===
I'm reaching out because {company_name} specializes in """
        
        if description:
            intro += description
        elif about:
            # Use first sentence of about text
            first_sentence = about.split('.')[0] + '.'
            intro += first_sentence
        else:
            intro += "providing exceptional solutions to help businesses like yours succeed."
        
        intro += "\n\nI'd love to share how we can help you [achieve specific goal/solve specific problem]."
        
        return intro
    
    def _generate_value_proposition(self) -> str:
        """Generate value proposition"""
        company_name = self.data.get('company_name', 'We')
        
        value_prop = f"""=== VALUE PROPOSITION ===
Here's what makes {company_name} different:

"""
        
        # Add key differentiators
        if self.data.get('key_features'):
            features = self.data['key_features'][:3]  # Top 3 features
            for idx, feature in enumerate(features, 1):
                value_prop += f"{idx}. {feature}\n"
        else:
            # Generic value points
            value_prop += """1. Proven track record of success with clients like you
2. Innovative approach that delivers real results
3. Dedicated support every step of the way"""
        
        value_prop += "\n\n[Pause for questions or comments]"
        
        return value_prop
    
    def _generate_products_section(self) -> str:
        """Generate products/services section"""
        products = self.data.get('products_services', [])
        
        section = "=== OUR SOLUTIONS ===\n"
        section += "Let me tell you about our key solutions that could benefit you:\n\n"
        
        for idx, product in enumerate(products[:5], 1):  # Top 5 products
            name = product.get('name', f'Solution {idx}')
            desc = product.get('description', '')
            
            section += f"{idx}. {name}\n"
            if desc:
                # Get first sentence or first 150 chars
                short_desc = desc.split('.')[0] if '.' in desc else desc[:150]
                section += f"   {short_desc}\n\n"
        
        section += "[Ask: Which of these solutions interests you most?]"
        
        return section
    
    def _generate_features_section(self) -> str:
        """Generate features/benefits section"""
        features = self.data.get('key_features', [])
        
        section = "=== KEY BENEFITS ===\n"
        section += "When you work with us, you'll enjoy:\n\n"
        
        for idx, feature in enumerate(features[:5], 1):
            section += f"✓ {feature}\n"
        
        section += "\n[Ask: Which of these benefits is most important to you?]"
        
        return section
    
    def _generate_testimonials_section(self) -> str:
        """Generate social proof section"""
        testimonials = self.data.get('testimonials', [])
        
        section = "=== WHAT OUR CLIENTS SAY ===\n"
        section += "Don't just take my word for it. Here's what some of our satisfied clients have shared:\n\n"
        
        # Use first testimonial
        if testimonials:
            testimonial = testimonials[0][:200]  # Limit length
            section += f'"{testimonial}..."\n\n'
        
        section += "We have many more success stories like this.\n"
        section += "[Ask: Would you like to hear more about how we've helped businesses similar to yours?]"
        
        return section
    
    def _generate_objection_handling(self) -> str:
        """Generate objection handling guidelines"""
        section = """=== HANDLING COMMON CONCERNS ===

If they say "I'm not interested":
- I understand. Many of our best clients said the same thing initially. Can I ask what specifically doesn't interest you? That way I can better understand if there's a fit.

If they say "Send me information":
- I'd be happy to! But to send you the most relevant information, may I ask just 2-3 quick questions about your current situation?

If they say "I'm busy":
- I completely understand. When would be a better time to call you back? I only need 5 minutes of your time.

If they say "Too expensive":
- I appreciate your concern about cost. Can I show you how the ROI typically covers the investment within [timeframe]? Many clients find it actually saves them money.

If they say "Already have a provider":
- That's great! Who are you currently working with? [Listen] Many of our clients used [competitor] before switching to us because [key differentiator].
"""
        
        return section
    
    def _generate_call_to_action(self) -> str:
        """Generate call to action"""
        contact = self.data.get('contact_info', {})
        
        cta = """=== CALL TO ACTION ===
Based on what we've discussed, I believe we could really help you [achieve specific goal].

Here's what I'd like to propose:
"""
        
        if self.agent_tone == 'friendly':
            cta += "How about we schedule a quick 15-minute demo where I can show you exactly how this works for your situation? Does [specific day/time] work for you?"
        else:
            cta += "I'd like to schedule a brief consultation to discuss your specific needs in detail. Would [specific day/time] work for you?"
        
        cta += "\n\n[If yes: Confirm details and next steps]"
        cta += "\n[If no: Offer alternative times or ask about concerns]"
        
        return cta
    
    def _generate_closing(self) -> str:
        """Generate closing section"""
        company_name = self.data.get('company_name', 'our company')
        contact = self.data.get('contact_info', {})
        
        closing = f"""=== CLOSING ===
Thank you so much for your time today. I'm excited about the possibility of working together!

Just to confirm:
- [Recap any commitments made]
- [Confirm next steps]
- [Confirm contact information]
"""
        
        if contact.get('email'):
            closing += f"\nI'll send you a confirmation email at {contact['email']} with all the details we discussed."
        
        if contact.get('phone'):
            closing += f"\nAnd you can always reach us at {contact['phone']} if you have any questions."
        
        closing += f"\n\nHave a wonderful [day/evening], and I look forward to speaking with you again soon!"
        
        return closing
    
    def _generate_fallback_script(self) -> str:
        """Generate fallback script when website data is unavailable"""
        return f"""=== OPENING GREETING ===
Good [morning/afternoon/evening]. My name is {self.agent_name}. How are you today?

[Wait for response]

=== INTRODUCTION ===
I'm calling to introduce our services and see if we might be able to help you with [specific need/goal].

=== VALUE PROPOSITION ===
We specialize in providing solutions that help businesses succeed and grow.

=== QUALIFICATION ===
To make sure I'm offering you the most relevant information:
- What are your main priorities right now?
- What challenges are you currently facing?
- What solutions have you tried in the past?

=== CALL TO ACTION ===
Based on what you've shared, I believe we could help. Would you be interested in scheduling a brief consultation to discuss your needs in more detail?

=== CLOSING ===
Thank you for your time. I'll follow up with you [specific timeframe]. Have a great day!
"""


def generate_sales_script(website_data: dict, agent_name: str = "AI Agent", agent_tone: str = "professional") -> str:
    """
    Generate sales script from website data
    
    Args:
        website_data: Data extracted from website
        agent_name: Name of the agent
        agent_tone: Tone of conversation
        
    Returns:
        str: Generated sales script
    """
    generator = SalesScriptGenerator(website_data, agent_name, agent_tone)
    return generator.generate_script()


# Example usage
if __name__ == "__main__":
    # Test data
    test_data = {
        'success': True,
        'company_name': 'TechSolutions Inc.',
        'description': 'We provide innovative software solutions for modern businesses',
        'products_services': [
            {'name': 'Cloud Platform', 'description': 'Scalable cloud infrastructure for your business'},
            {'name': 'Analytics Suite', 'description': 'Advanced data analytics and insights'}
        ],
        'key_features': [
            '24/7 Customer Support',
            '99.9% Uptime Guarantee',
            'Easy Integration'
        ]
    }
    
    script = generate_sales_script(test_data, agent_name="Sarah", agent_tone="friendly")
    print(script)
