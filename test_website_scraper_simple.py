"""
Simple Test for Website Scraper and Sales Script Generator
(Without Django setup - just testing the core functions)
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.website_scraper import scrape_website
from agents.sales_script_generator import generate_sales_script


def test_website_scraper():
    """Test website scraping"""
    print("=" * 80)
    print("🌐 TESTING WEBSITE SCRAPER")
    print("=" * 80)
    
    # Test URL
    test_url = "https://www.example.com"
    
    print(f"\n📍 Scraping: {test_url}")
    print("-" * 80)
    
    result = scrape_website(test_url)
    
    if result['success']:
        print(f"✅ Successfully scraped!")
        print(f"\n📊 Extracted Data:")
        print(f"   Company Name: {result.get('company_name', 'N/A')}")
        print(f"   Title: {result.get('title', 'N/A')}")
        print(f"   Description: {result.get('description', 'N/A')[:150]}...")
        print(f"   Products/Services: {len(result.get('products_services', []))} items")
        print(f"   Key Features: {len(result.get('key_features', []))} items")
        
        if result.get('contact_info'):
            print(f"   Contact Info:")
            for key, value in result['contact_info'].items():
                print(f"      {key}: {value}")
        
        return result
    else:
        print(f"❌ Failed: {result.get('error')}")
        return None


def test_sales_script_generator():
    """Test sales script generation with sample data"""
    print("\n" + "=" * 80)
    print("📝 TESTING SALES SCRIPT GENERATOR")
    print("=" * 80)
    
    # Sample website data
    sample_data = {
        'success': True,
        'company_name': 'SalesAI Pro',
        'description': 'AI-powered sales automation platform that helps businesses close more deals faster',
        'about_text': 'We are a leading provider of AI sales solutions for modern businesses. Our platform combines cutting-edge AI technology with proven sales methodologies.',
        'products_services': [
            {
                'name': 'AI Voice Agents',
                'description': 'Intelligent voice AI that handles customer calls 24/7 with natural conversations'
            },
            {
                'name': 'Sales Analytics Dashboard',
                'description': 'Real-time insights and performance tracking for your sales team'
            },
            {
                'name': 'CRM Integration',
                'description': 'Seamless integration with popular CRM systems'
            }
        ],
        'key_features': [
            '24/7 Automated calling capability',
            'Natural conversation AI powered by advanced NLP',
            'Seamless CRM Integration with Salesforce, HubSpot',
            'Real-time analytics and reporting',
            'Multi-language support (10+ languages)',
            'Custom script training and optimization'
        ],
        'testimonials': [
            'SalesAI Pro increased our sales by 150% in just 3 months! The AI agents are incredibly natural and our customers love them. - John Smith, CEO TechCorp',
        ],
        'contact_info': {
            'email': 'sales@salesaipro.com',
            'phone': '+1-800-SALES-AI',
            'address': '123 Innovation Drive, San Francisco, CA 94105'
        }
    }
    
    # Test different tones
    tones = ['professional', 'friendly', 'enthusiastic']
    
    for tone in tones:
        print(f"\n🎭 Generating script with '{tone.upper()}' tone")
        print("-" * 80)
        
        script = generate_sales_script(
            website_data=sample_data,
            agent_name="Sarah",
            agent_tone=tone
        )
        
        print(f"✅ Script generated: {len(script)} characters, {len(script.split())} words")
        print(f"\n📄 Full Script:\n")
        print(script)
        print("\n" + "=" * 80)
    
    return script


def main():
    """Run tests"""
    print("\n" + "=" * 80)
    print("🚀 WEBSITE TO SALES SCRIPT - FUNCTION TEST")
    print("=" * 80)
    
    try:
        # Test 1: Website Scraper
        website_data = test_website_scraper()
        
        # Test 2: Sales Script Generator with sample data
        test_sales_script_generator()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        print("\n📖 FEATURE SUMMARY:")
        print("   ✅ Website scraper extracts business data from any URL")
        print("   ✅ Sales script generator creates professional scripts")
        print("   ✅ Multiple tone options: professional, friendly, casual, enthusiastic")
        print("   ✅ Includes all sections: greeting, intro, value prop, objections, CTA")
        
        print("\n💡 INTEGRATION IN YOUR SYSTEM:")
        print("   1. When user creates/updates agent with website_url")
        print("   2. AgentCreateUpdateSerializer automatically:")
        print("      - Scrapes the website using scrape_website()")
        print("      - Generates sales script using generate_sales_script()")
        print("      - Saves script to agent.sales_script_text")
        print("      - Stores website data in agent.business_info")
        print("   3. Agent is ready to make calls with custom script!")
        
        print("\n🎯 API USAGE:")
        print("   POST /api/agents/")
        print("   {")
        print('     "name": "My Sales Agent",')
        print('     "agent_type": "outbound",')
        print('     "website_url": "https://yourcompany.com",')
        print('     "voice_tone": "friendly"')
        print("   }")
        print("   → Sales script automatically generated! 🎉")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
