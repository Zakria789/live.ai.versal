"""
Test Website Scraper with Real Hume AI Website
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.website_scraper import scrape_website
from agents.sales_script_generator import generate_sales_script


def main():
    print("=" * 80)
    print("🌐 TESTING WITH REAL WEBSITE: https://platform.hume.ai/")
    print("=" * 80)
    
    # Scrape Hume AI website
    url = "https://platform.hume.ai/"
    print(f"\n📍 Scraping: {url}")
    print("-" * 80)
    
    result = scrape_website(url)
    
    if result['success']:
        print(f"✅ Successfully scraped Hume AI website!")
        print(f"\n📊 Extracted Data:")
        print(f"   Company Name: {result.get('company_name', 'N/A')}")
        print(f"   Title: {result.get('title', 'N/A')}")
        print(f"   Description: {result.get('description', 'N/A')}")
        print(f"   About: {result.get('about_text', 'N/A')[:200]}...")
        print(f"   Products/Services: {len(result.get('products_services', []))} items")
        print(f"   Key Features: {len(result.get('key_features', []))} items")
        
        if result.get('products_services'):
            print(f"\n📦 Products/Services Found:")
            for idx, product in enumerate(result['products_services'][:5], 1):
                print(f"   {idx}. {product.get('name', 'N/A')}")
                if product.get('description'):
                    print(f"      {product['description'][:100]}...")
        
        if result.get('key_features'):
            print(f"\n✨ Key Features Found:")
            for idx, feature in enumerate(result['key_features'][:5], 1):
                print(f"   {idx}. {feature}")
        
        if result.get('contact_info'):
            print(f"\n📞 Contact Info:")
            for key, value in result['contact_info'].items():
                print(f"   {key}: {value}")
        
        # Generate sales script
        print("\n" + "=" * 80)
        print("📝 GENERATING SALES SCRIPT FROM HUME AI DATA")
        print("=" * 80)
        
        script = generate_sales_script(
            website_data=result,
            agent_name="Sarah",
            agent_tone="professional"
        )
        
        print(f"\n✅ Sales Script Generated!")
        print(f"   Length: {len(script)} characters")
        print(f"   Words: {len(script.split())} words")
        
        print(f"\n📄 Generated Sales Script:")
        print("=" * 80)
        print(script)
        print("=" * 80)
        
        # Test with friendly tone
        print("\n" + "=" * 80)
        print("📝 GENERATING WITH FRIENDLY TONE")
        print("=" * 80)
        
        friendly_script = generate_sales_script(
            website_data=result,
            agent_name="Alex",
            agent_tone="friendly"
        )
        
        print(f"\n✅ Friendly Script Generated!")
        print(f"   Length: {len(friendly_script)} characters")
        print(f"\n📄 First 500 characters:")
        print("-" * 80)
        print(friendly_script[:500])
        print("...")
        print("-" * 80)
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        print("\n💡 SUMMARY:")
        print(f"   ✅ Successfully scraped: {result.get('company_name', 'Hume AI')}")
        print(f"   ✅ Extracted {len(result.get('products_services', []))} products/services")
        print(f"   ✅ Extracted {len(result.get('key_features', []))} key features")
        print(f"   ✅ Generated professional sales script ({len(script)} chars)")
        print(f"   ✅ Generated friendly sales script ({len(friendly_script)} chars)")
        
        print("\n🎯 READY TO USE:")
        print("   This feature is now integrated in your Agent creation API")
        print("   Just provide 'website_url' and script will be auto-generated!")
        
    else:
        print(f"❌ Failed to scrape: {result.get('error')}")
        print("\n💡 This might happen if:")
        print("   - Website requires authentication")
        print("   - Website blocks scrapers")
        print("   - Network connectivity issues")
        print("\n🔧 Fallback:")
        print("   System will use generic script template")
        print("   User can manually add custom script")


if __name__ == "__main__":
    main()
