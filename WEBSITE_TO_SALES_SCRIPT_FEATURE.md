# 🌐 Website URL to Sales Script - Feature Documentation

## ✨ Overview
Automatically generate professional sales scripts from website URLs when creating or updating AI agents.

## 🎯 Features

### 1. **Website Data Extraction**
- Scrapes business information from any website URL
- Extracts:
  - Company name
  - Description & About text
  - Products/Services
  - Key features/benefits
  - Testimonials
  - Contact information
  - Pricing details

### 2. **Smart Sales Script Generation**
- Converts website data into structured sales scripts
- Multiple tone options:
  - **Professional** - Formal and business-oriented
  - **Friendly** - Warm and approachable
  - **Casual** - Relaxed and conversational
  - **Enthusiastic** - Energetic and excited

### 3. **Complete Script Structure**
Generated scripts include:
- Opening greeting
- Introduction
- Value proposition
- Products/Services presentation
- Key benefits
- Social proof (testimonials)
- Objection handling guidelines
- Call to action
- Professional closing

## 🚀 How to Use

### Creating Agent with Website URL

**API Endpoint:** `POST /api/agents/`

**Request Example:**
```json
{
  "name": "My Sales Agent",
  "agent_type": "outbound",
  "status": "active",
  "voice_tone": "friendly",
  "website_url": "https://yourcompany.com",
  "operating_hours": {
    "start": "09:00",
    "end": "17:00"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Outbound agent 'My Sales Agent' created successfully",
  "agent": {
    "id": "uuid-here",
    "name": "My Sales Agent",
    "website_url": "https://yourcompany.com",
    "sales_script_text": "=== OPENING GREETING ===\nHi there! This is...",
    "business_info": {
      "website_data": {
        "company_name": "Your Company",
        "description": "...",
        "products_services": [...],
        "scraped_at": "2025-11-13T10:30:00Z"
      }
    }
  }
}
```

### Updating Agent Website URL

**API Endpoint:** `PUT /api/agents/{agent_id}/`

**Request Example:**
```json
{
  "website_url": "https://newcompany.com"
}
```

**Behavior:**
- If website URL changes → Sales script is automatically regenerated
- If custom `sales_script_text` is provided → Custom script is preserved
- Website data is always updated in `business_info`

## 📁 Files Created

### 1. `agents/website_scraper.py`
**Purpose:** Extracts business data from website URLs

**Main Function:**
```python
from agents.website_scraper import scrape_website

result = scrape_website("https://example.com")
# Returns: {
#   'success': True,
#   'company_name': 'Company Name',
#   'description': '...',
#   'products_services': [...],
#   'key_features': [...],
#   ...
# }
```

**Features:**
- Handles invalid URLs gracefully
- Extracts structured data
- Timeout protection (10 seconds)
- Error handling

### 2. `agents/sales_script_generator.py`
**Purpose:** Generate sales scripts from website data

**Main Function:**
```python
from agents.sales_script_generator import generate_sales_script

script = generate_sales_script(
    website_data=website_data,
    agent_name="Sarah",
    agent_tone="friendly"
)
```

**Features:**
- Multiple tone options
- Complete script structure
- Fallback for missing data
- Professional formatting

### 3. Updated `agents/serializers.py`
**Changes:**
- Added imports for scraper and generator
- Modified `create()` method - auto-generate script from website_url
- Modified `update()` method - regenerate when URL changes
- Store website data in `business_info` field

## 🔄 Workflow

```
User Creates Agent
       ↓
Provides website_url
       ↓
AgentCreateUpdateSerializer.create()
       ↓
Scrape Website (website_scraper.py)
       ↓
Extract Business Data
       ↓
Generate Sales Script (sales_script_generator.py)
       ↓
Save to agent.sales_script_text
       ↓
Store data in agent.business_info
       ↓
Agent Ready for Calls! 🎉
```

## 📊 Data Storage

### `sales_script_text` Field
Stores the complete generated sales script as text.

### `business_info` Field (JSON)
Stores extracted website data:
```json
{
  "website_data": {
    "company_name": "Company Name",
    "description": "Company description",
    "products_services": [
      {"name": "Product 1", "description": "..."},
      {"name": "Product 2", "description": "..."}
    ],
    "key_features": ["Feature 1", "Feature 2"],
    "contact_info": {
      "email": "contact@company.com",
      "phone": "+1-800-XXX-XXXX"
    },
    "scraped_at": "2025-11-13T10:30:00Z"
  }
}
```

## 🧪 Testing

### Test Files Created

**1. `test_website_scraper_simple.py`**
Simple standalone test without Django dependencies.

**Run:**
```bash
python test_website_scraper_simple.py
```

**Tests:**
- Website scraping functionality
- Sales script generation with multiple tones
- Full output preview

**2. `test_website_to_script.py`**
Full integration test with Django (requires setup).

## ⚙️ Configuration

### Required Packages
Added to `requirements.txt`:
```
beautifulsoup4==4.12.3
requests==2.31.0  # Already present
```

### Installation
```bash
pip install beautifulsoup4==4.12.3
```

## 🎨 Tone Examples

### Professional
```
Good [morning/afternoon/evening]. My name is Sarah, and I'm calling from Company Name. 
How are you today?
```

### Friendly
```
Hi there! This is Sarah from Company Name. How are you doing today?
```

### Casual
```
Hey! Sarah here from Company Name. How's it going?
```

### Enthusiastic
```
Hello! This is Sarah from Company Name! I hope you're having a great day!
```

## 🛡️ Error Handling

### Invalid URL
- Returns error message
- Agent creation continues
- User can add script manually

### Website Unreachable
- Logs warning
- Agent creation continues
- No script generated

### Partial Data
- Generates script with available data
- Uses fallback content for missing sections
- Always creates complete script structure

## 🔧 Customization

### Adding New Sections
Edit `sales_script_generator.py`:

```python
def _generate_custom_section(self) -> str:
    """Generate custom section"""
    section = "=== CUSTOM SECTION ===\n"
    section += "Your custom content here\n"
    return section
```

Add to `generate_script()`:
```python
script_parts.append(self._generate_custom_section())
```

### Modifying Extraction
Edit `website_scraper.py` methods:
- `_extract_company_name()`
- `_extract_products_services()`
- `_extract_key_features()`
- etc.

## 📈 Benefits

1. **Time Saving** - No manual script writing
2. **Consistency** - Professional format every time
3. **Customization** - Adapts to company data
4. **Flexibility** - Multiple tones available
5. **Automation** - Works seamlessly with agent creation

## 🎯 Use Cases

1. **Quick Agent Setup** - Get agents running fast
2. **Multi-Client Agencies** - Generate unique scripts per client
3. **Template Generation** - Use as starting point, edit as needed
4. **A/B Testing** - Try different tones automatically
5. **Bulk Agent Creation** - Script hundreds of agents efficiently

## 📝 Notes

- **Manual Override:** Users can still provide custom `sales_script_text`
- **Data Preservation:** Website data stored for future reference
- **Update Behavior:** Script regenerates only when URL changes
- **Fallback:** Generic script if website scraping fails

## 🚦 Status

✅ **COMPLETE AND TESTED**

- Website scraper working
- Sales script generator working
- Integration with serializers complete
- Test files created and verified
- Documentation complete

## 📞 Support

For issues or questions:
1. Check logs for scraping errors
2. Verify website URL is accessible
3. Test with `test_website_scraper_simple.py`
4. Review generated script in agent details

---

**Last Updated:** November 13, 2025
**Feature Version:** 1.0
**Status:** ✅ Production Ready
