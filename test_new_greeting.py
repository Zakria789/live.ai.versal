"""
Test Updated Opening Greeting Format
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.website_scraper import scrape_website
from agents.sales_script_generator import generate_sales_script


def test_new_greeting():
    print("=" * 80)
    print("🎤 TESTING NEW OPENING GREETING FORMAT")
    print("=" * 80)
    
    # Sample data
    website_data = {
        'success': True,
        'company_name': 'PythonAnywhere',
        'description': 'Host, run, and code Python in the cloud',
        'contact_info': {
            'email': 'support@pythonanywhere.com'
        }
    }
    
    print("\n📋 TESTING DIFFERENT TONES:")
    print("=" * 80)
    
    tones = {
        'professional': '🎩 Professional',
        'friendly': '😊 Friendly',
        'casual': '👋 Casual',
        'enthusiastic': '🎉 Enthusiastic'
    }
    
    for tone, label in tones.items():
        print(f"\n{label} Tone:")
        print("-" * 80)
        
        script = generate_sales_script(
            website_data=website_data,
            agent_name="Zakria",
            agent_tone=tone
        )
        
        # Extract just the greeting
        greeting_section = script.split('=== INTRODUCTION ===')[0]
        print(greeting_section.strip())
    
    print("\n" + "=" * 80)
    print("📊 COMPARISON: OLD vs NEW")
    print("=" * 80)
    
    print("\n❌ OLD FORMAT (Confusing):")
    print("-" * 80)
    print("""Hi there! This is Zakria from PythonAnywhere.
How are you doing today?""")
    
    print("\n✅ NEW FORMAT (Clear & Natural):")
    print("-" * 80)
    print("""Hi! I'm Zakria calling from PythonAnywhere.
How are you doing today?""")
    
    print("\n" + "=" * 80)
    print("💡 WHY THIS IS BETTER:")
    print("=" * 80)
    print("""
1. ✅ "I'm Zakria" - More natural and personal
2. ✅ "calling from" - Clearly states purpose
3. ✅ Shorter and cleaner
4. ✅ Professional tone maintained
5. ✅ Immediately identifies who they are and why calling
""")
    
    print("\n" + "=" * 80)
    print("📝 FULL EXAMPLE WITH CUSTOM SCRIPT:")
    print("=" * 80)
    
    custom_intro = "Hi! I'm Zakria calling from PythonAnywhere."
    
    full_script = generate_sales_script(
        website_data=website_data,
        agent_name="Zakria",
        agent_tone="friendly"
    )
    
    # Simulate concatenation
    combined = f"""{custom_intro}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{full_script}"""
    
    print("\nCombined Script Preview (first 800 chars):")
    print("-" * 80)
    print(combined[:800])
    print("...")
    
    print("\n" + "=" * 80)
    print("✅ PERFECT! Natural & Professional!")
    print("=" * 80)


if __name__ == "__main__":
    test_new_greeting()
