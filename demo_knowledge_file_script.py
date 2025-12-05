"""
Demo: Knowledge File to Sales Script Feature
"""

def demo_knowledge_file_feature():
    print("=" * 80)
    print("📚 KNOWLEDGE FILE TO SALES SCRIPT FEATURE")
    print("=" * 80)
    
    print("\n✨ THREE WAYS TO GENERATE SALES SCRIPT:")
    print("-" * 80)
    print("""
1️⃣  FROM WEBSITE URL:
    {
      "website_url": "https://company.com"
    }
    → Scrapes website → Generates script

2️⃣  FROM KNOWLEDGE FILE:
    {
      "knowledge_files_upload": [file.pdf]
    }
    → Extracts text from file → Generates script

3️⃣  CUSTOM SCRIPT + WEBSITE/FILE:
    {
      "sales_script_text": "My intro...",
      "website_url": "https://company.com"
    }
    → Combines both → Complete script
""")
    
    print("\n📁 SUPPORTED FILE FORMATS:")
    print("-" * 80)
    print("""
✅ PDF (.pdf)         - Product catalogs, brochures
✅ Word (.docx, .doc) - Company documents, proposals  
✅ Text (.txt)        - Simple text files, scripts
✅ CSV (.csv)         - Feature lists, pricing tables
""")
    
    print("\n🔄 PROCESSING WORKFLOW:")
    print("-" * 80)
    print("""
Step 1: Upload Knowledge File
  ├─ File saved to: agents/{agent_id}/knowledge/
  └─ File type detected automatically

Step 2: Extract Text Content
  ├─ PDF → PyPDF2 extraction
  ├─ DOCX → python-docx extraction
  └─ TXT → Direct read

Step 3: Parse Structured Data
  ├─ Find company name (first lines)
  ├─ Extract sections (About, Products, Features)
  ├─ Parse lists and bullet points
  └─ Extract contact information

Step 4: Generate Sales Script
  ├─ Use sales_script_generator
  ├─ Create complete script structure
  └─ Save to agent.sales_script_text
""")
    
    print("\n📋 PRIORITY ORDER:")
    print("-" * 80)
    print("""
When creating agent, script is generated from:

1. Custom sales_script_text (if provided)        → Use as-is
2. Website URL (if provided)                     → Scrape & generate
3. Knowledge files (if uploaded)                 → Extract & generate
4. None of above                                 → Generic template

If BOTH custom script + URL/file provided:
→ Custom script FIRST + Generated script SECOND = Combined!
""")
    
    print("\n💡 EXAMPLE USE CASES:")
    print("-" * 80)
    print("""
📄 Use Case 1: Company Brochure PDF
   Upload: company_brochure.pdf
   Contains: About us, products, features
   Result: Professional sales script generated!

📊 Use Case 2: Product Catalog
   Upload: product_catalog.docx
   Contains: Product list, specs, pricing
   Result: Detailed product-focused script!

📝 Use Case 3: Sales Template
   Upload: sales_template.txt
   Contains: Your custom template
   Result: Uses your template as-is!

🌐 Use Case 4: Website + Custom Intro
   Provide: website_url + sales_script_text
   Result: Your intro + Website details combined!
""")
    
    print("\n🎯 API REQUEST EXAMPLES:")
    print("-" * 80)
    print("""
Example 1: Only Knowledge File
POST /api/agents/
Content-Type: multipart/form-data

{
  "name": "Product Sales Agent",
  "agent_type": "outbound",
  "knowledge_files_upload": [file.pdf],
  "voice_tone": "professional"
}

→ Script generated from PDF content!

---

Example 2: Knowledge File + Custom Intro
POST /api/agents/
Content-Type: multipart/form-data

{
  "name": "Premium Agent",
  "sales_script_text": "SPECIAL: 50% OFF!",
  "knowledge_files_upload": [brochure.pdf],
  "voice_tone": "enthusiastic"
}

→ Custom intro + PDF content combined!

---

Example 3: All Three Sources!
POST /api/agents/

{
  "sales_script_text": "Limited offer!",
  "website_url": "https://company.com",
  "knowledge_files_upload": [details.pdf]
}

→ Custom + Website + PDF = Super comprehensive!
""")
    
    print("\n⚙️ CONFIGURATION:")
    print("-" * 80)
    print("""
Required packages (already in requirements.txt):
✅ PyPDF2==3.0.1          - For PDF extraction
✅ python-docx==1.1.0     - For DOCX extraction

File size limits:
- Max file size: Configured in Django settings
- Recommended: < 10MB per file
- Multiple files: Supported!
""")
    
    print("\n" + "=" * 80)
    print("✅ FEATURE COMPLETE!")
    print("=" * 80)
    print("""
Now your agents can generate sales scripts from:
✅ Website URLs (automatic scraping)
✅ Knowledge files (PDF, DOCX, TXT)
✅ Custom text (manual input)
✅ Any combination of above!

Maximum flexibility for your sales team! 🚀
""")


if __name__ == "__main__":
    demo_knowledge_file_feature()
