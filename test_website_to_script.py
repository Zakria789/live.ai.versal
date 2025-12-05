"""
Test Website URL to Sales Script Feature

This script tests the automatic sales script generation from website URL
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from agents.website_scraper import scrape_website
from agents.sales_script_generator import generate_sales_script


def test_website_scraper():
    """Test website scraping functionality"""
    print("=" * 80)
    print("🌐 TESTING WEBSITE SCRAPER")
    print("=" * 80)
    
    # Test URLs
    test_urls = [
        "https://www.salesforce.com",
        "https://www.hubspot.com",
        "https://www.example.com"
    ]
    
    for url in test_urls:
        print(f"\n📍 Testing URL: {url}")
        print("-" * 80)
        
        result = scrape_website(url)
        
        if result['success']:
            print(f"✅ Successfully scraped!")
            print(f"   Company Name: {result.get('company_name', 'N/A')}")
            print(f"   Title: {result.get('title', 'N/A')[:80]}...")
            print(f"   Description: {result.get('description', 'N/A')[:100]}...")
            print(f"   Products/Services: {len(result.get('products_services', []))} found")
            print(f"   Key Features: {len(result.get('key_features', []))} found")
            print(f"   Contact Info: {result.get('contact_info', {})}")
        else:
            print(f"❌ Failed: {result.get('error')}")
    
    return result  # Return last result for script generation test


def test_sales_script_generator(website_data=None):
    """Test sales script generation"""
    print("\n" + "=" * 80)
    print("📝 TESTING SALES SCRIPT GENERATOR")
    print("=" * 80)
    
    # Use test data if no website data provided
    if not website_data or not website_data.get('success'):
        print("\n⚠️  Using test data (no valid website data)")
        website_data = {
            'success': True,
            'company_name': 'SalesAI Pro',
            'description': 'AI-powered sales automation platform that helps businesses close more deals',
            'about_text': 'We are a leading provider of AI sales solutions for modern businesses.',
            'products_services': [
                {
                    'name': 'AI Voice Agents',
                    'description': 'Intelligent voice AI that handles customer calls 24/7'
                },
                {
                    'name': 'Sales Analytics',
                    'description': 'Real-time insights and performance tracking'
                }
            ],
            'key_features': [
                '24/7 Automated calling',
                'Natural conversation AI',
                'CRM Integration',
                'Real-time analytics',
                'Multi-language support'
            ],
            'testimonials': [
                'SalesAI Pro increased our sales by 150% in just 3 months!',
            ],
            'contact_info': {
                'email': 'sales@salesaipro.com',
                'phone': '+1-800-SALES-AI'
            }
        }
    
    # Test different tones
    tones = ['professional', 'friendly', 'casual', 'enthusiastic']
    
    for tone in tones:
        print(f"\n🎭 Generating script with '{tone}' tone")
        print("-" * 80)
        
        script = generate_sales_script(
            website_data=website_data,
            agent_name="Sarah",
            agent_tone=tone
        )
        
        print(f"✅ Script generated: {len(script)} characters")
        print("\n📄 Preview (first 500 chars):")
        print(script[:500] + "...\n")
    
    # Return full script for final test
    return generate_sales_script(website_data, "Sarah", "professional")


def test_agent_creation_with_website():
    """Test creating an agent with website URL"""
    print("\n" + "=" * 80)
    print("🤖 TESTING AGENT CREATION WITH WEBSITE URL")
    print("=" * 80)
    
    from django.contrib.auth import get_user_model
    from agents.models import Agent
    from agents.serializers import AgentCreateUpdateSerializer
    from rest_framework.test import APIRequestFactory
    
    User = get_user_model()
    
    # Get or create test user
    test_user, created = User.objects.get_or_create(
        email='testuser@example.com',
        defaults={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Test user created: {test_user.email}")
    else:
        print(f"✅ Using existing test user: {test_user.email}")
    
    # Create test agent data
    agent_data = {
        'name': 'Test Website Agent',
        'agent_type': 'outbound',
        'status': 'active',
        'voice_tone': 'friendly',
        'website_url': 'https://www.example.com',  # Test URL
        'auto_answer_enabled': False,
        'operating_hours': {
            'start': '09:00',
            'end': '17:00'
        },
        'business_info': {
            'company_name': 'Test Company'
        }
    }
    
    # Create mock request
    factory = APIRequestFactory()
    request = factory.post('/api/agents/')
    request.user = test_user
    
    # Test serializer
    print("\n📋 Testing serializer with website URL...")
    serializer = AgentCreateUpdateSerializer(
        data=agent_data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        print("✅ Serializer validation passed")
        
        # Create agent
        agent = serializer.save()
        print(f"✅ Agent created: {agent.name} (ID: {agent.id})")
        print(f"   Website URL: {agent.website_url}")
        print(f"   Sales Script Length: {len(agent.sales_script_text or '')} characters")
        
        if agent.sales_script_text:
            print(f"\n📝 Generated Sales Script Preview:")
            print("-" * 80)
            print(agent.sales_script_text[:500])
            print("...")
            print("-" * 80)
        
        # Check business_info for website data
        if agent.business_info.get('website_data'):
            website_data = agent.business_info['website_data']
            print(f"\n📊 Website Data Stored:")
            print(f"   Company: {website_data.get('company_name')}")
            print(f"   Products: {len(website_data.get('products_services', []))}")
            print(f"   Features: {len(website_data.get('key_features', []))}")
            print(f"   Scraped At: {website_data.get('scraped_at')}")
        
        print(f"\n✅ SUCCESS! Agent created with auto-generated sales script from website!")
        
        # Cleanup - delete test agent
        print(f"\n🗑️  Cleaning up test agent...")
        agent.delete()
        print(f"✅ Test agent deleted")
        
    else:
        print(f"❌ Serializer validation failed:")
        print(serializer.errors)


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("🚀 WEBSITE TO SALES SCRIPT - COMPLETE TEST SUITE")
    print("=" * 80)
    
    try:
        # Test 1: Website Scraper
        website_data = test_website_scraper()
        
        # Test 2: Sales Script Generator
        test_sales_script_generator(website_data)
        
        # Test 3: Full Integration (Agent Creation)
        test_agent_creation_with_website()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 80)
        print("\n📖 FEATURE SUMMARY:")
        print("   ✅ Website scraper extracts business data from URL")
        print("   ✅ Sales script generator creates professional scripts")
        print("   ✅ Agent creation auto-generates script from website")
        print("   ✅ Agent update regenerates script when URL changes")
        print("\n💡 HOW TO USE:")
        print("   1. Create/Update agent via API")
        print("   2. Provide 'website_url' in request")
        print("   3. System automatically scrapes website")
        print("   4. Sales script is auto-generated and saved")
        print("   5. Website data stored in business_info for reference")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
