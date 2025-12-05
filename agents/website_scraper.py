"""
Website Scraper Utility
Extract business information and data from website URL for sales script generation
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import json
import logging

logger = logging.getLogger(__name__)


class WebsiteScraper:
    """Extract business information from website URL"""
    
    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout
        self.soup = None
        self.text_content = ""
        
    def scrape(self):
        """Main scraping function"""
        try:
            # Validate URL
            if not self._validate_url(self.url):
                return {
                    'success': False,
                    'error': 'Invalid URL format'
                }
            
            # Fetch webpage content
            response = requests.get(
                self.url, 
                timeout=self.timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response.raise_for_status()
            
            # Parse HTML
            self.soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract all relevant information
            data = {
                'success': True,
                'url': self.url,
                'company_name': self._extract_company_name(),
                'title': self._extract_title(),
                'description': self._extract_description(),
                'about_text': self._extract_about_section(),
                'products_services': self._extract_products_services(),
                'contact_info': self._extract_contact_info(),
                'key_features': self._extract_key_features(),
                'testimonials': self._extract_testimonials(),
                'pricing_info': self._extract_pricing_info(),
                'main_content': self._extract_main_content(),
                'meta_keywords': self._extract_meta_keywords(),
            }
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return {
                'success': False,
                'error': f'Failed to fetch website: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return {
                'success': False,
                'error': f'Error scraping website: {str(e)}'
            }
    
    def _validate_url(self, url):
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_company_name(self):
        """Extract company/business name"""
        # Try multiple sources
        sources = [
            # Logo alt text
            self.soup.find('img', {'class': re.compile(r'logo', re.I)}),
            # Site name in header
            self.soup.find('meta', {'property': 'og:site_name'}),
            # Title tag (first part)
            self.soup.find('title'),
            # H1 in header
            self.soup.find('header', recursive=True),
        ]
        
        for source in sources:
            if source:
                if source.name == 'img' and source.get('alt'):
                    return source['alt'].strip()
                elif source.name == 'meta' and source.get('content'):
                    return source['content'].strip()
                elif source.name == 'title':
                    # Get first part before separator
                    title = source.get_text().strip()
                    for sep in ['-', '|', '–']:
                        if sep in title:
                            return title.split(sep)[0].strip()
                    return title
                elif source.find('h1'):
                    return source.find('h1').get_text().strip()
        
        # Fallback to domain name
        domain = urlparse(self.url).netloc
        return domain.replace('www.', '').split('.')[0].title()
    
    def _extract_title(self):
        """Extract page title"""
        title_tag = self.soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        return ""
    
    def _extract_description(self):
        """Extract meta description"""
        meta_desc = self.soup.find('meta', {'name': 'description'}) or \
                   self.soup.find('meta', {'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        return ""
    
    def _extract_about_section(self):
        """Extract About Us section content"""
        about_sections = []
        
        # Look for about sections by ID or class
        patterns = [
            {'id': re.compile(r'about', re.I)},
            {'class': re.compile(r'about', re.I)},
            {'id': re.compile(r'company', re.I)},
            {'class': re.compile(r'company', re.I)},
        ]
        
        for pattern in patterns:
            sections = self.soup.find_all(['section', 'div', 'article'], pattern)
            for section in sections:
                text = section.get_text(separator=' ', strip=True)
                if len(text) > 50:  # Meaningful content
                    about_sections.append(text)
        
        if about_sections:
            # Return first meaningful about section
            return about_sections[0][:1000]  # Limit to 1000 chars
        
        return ""
    
    def _extract_products_services(self):
        """Extract products/services information"""
        products = []
        
        # Look for product/service sections
        patterns = [
            {'id': re.compile(r'product|service|solution|feature', re.I)},
            {'class': re.compile(r'product|service|solution|feature', re.I)},
        ]
        
        for pattern in patterns:
            sections = self.soup.find_all(['section', 'div', 'article'], pattern)
            for section in sections:
                # Find product/service items
                items = section.find_all(['div', 'article', 'li'], 
                                        class_=re.compile(r'item|card|box', re.I),
                                        limit=10)
                
                for item in items:
                    # Extract heading and description
                    heading = item.find(['h2', 'h3', 'h4', 'h5'])
                    if heading:
                        title = heading.get_text(strip=True)
                        desc = item.get_text(separator=' ', strip=True)
                        products.append({
                            'name': title,
                            'description': desc[:200]  # Limit description
                        })
        
        return products[:10]  # Return top 10 products/services
    
    def _extract_contact_info(self):
        """Extract contact information"""
        contact = {}
        
        # Extract email
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, str(self.soup))
        if emails:
            # Filter out common false positives
            valid_emails = [e for e in emails if not any(x in e.lower() for x in ['example', 'domain', 'test'])]
            if valid_emails:
                contact['email'] = valid_emails[0]
        
        # Extract phone
        phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, self.soup.get_text())
        if phones:
            contact['phone'] = phones[0]
        
        # Extract address
        address_section = self.soup.find(['div', 'section'], 
                                        class_=re.compile(r'address|contact', re.I))
        if address_section:
            address_text = address_section.get_text(separator=' ', strip=True)
            if len(address_text) > 10:
                contact['address'] = address_text[:200]
        
        return contact
    
    def _extract_key_features(self):
        """Extract key features or benefits"""
        features = []
        
        # Look for features/benefits lists
        feature_sections = self.soup.find_all(['ul', 'ol'], 
                                             class_=re.compile(r'feature|benefit|advantage', re.I),
                                             limit=5)
        
        for section in feature_sections:
            items = section.find_all('li', limit=10)
            for item in items:
                text = item.get_text(strip=True)
                if len(text) > 10 and len(text) < 200:
                    features.append(text)
        
        return features[:10]
    
    def _extract_testimonials(self):
        """Extract customer testimonials"""
        testimonials = []
        
        # Look for testimonial sections
        testimonial_sections = self.soup.find_all(['div', 'section', 'article'],
                                                  class_=re.compile(r'testimonial|review|feedback', re.I),
                                                  limit=5)
        
        for section in testimonial_sections:
            items = section.find_all(['div', 'article', 'blockquote'], limit=5)
            for item in items:
                text = item.get_text(separator=' ', strip=True)
                if len(text) > 20 and len(text) < 500:
                    testimonials.append(text)
        
        return testimonials[:5]
    
    def _extract_pricing_info(self):
        """Extract pricing information"""
        pricing = []
        
        # Look for pricing sections
        pricing_sections = self.soup.find_all(['div', 'section', 'article'],
                                              class_=re.compile(r'pric|plan|package', re.I),
                                              limit=5)
        
        for section in pricing_sections:
            # Find price tags
            prices = section.find_all(string=re.compile(r'\$\d+|\€\d+|£\d+'))
            if prices:
                text = section.get_text(separator=' ', strip=True)
                pricing.append(text[:300])
        
        return pricing[:3]
    
    def _extract_main_content(self):
        """Extract main content from page"""
        # Remove script and style elements
        for element in self.soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get main content
        main = self.soup.find('main') or self.soup.find('article') or self.soup.find('body')
        
        if main:
            text = main.get_text(separator=' ', strip=True)
            # Clean up multiple spaces
            text = re.sub(r'\s+', ' ', text)
            return text[:2000]  # Limit to 2000 chars
        
        return ""
    
    def _extract_meta_keywords(self):
        """Extract meta keywords"""
        meta_keywords = self.soup.find('meta', {'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            return [k.strip() for k in meta_keywords['content'].split(',')]
        return []


def scrape_website(url):
    """
    Convenience function to scrape website
    
    Args:
        url (str): Website URL to scrape
        
    Returns:
        dict: Extracted website data
    """
    scraper = WebsiteScraper(url)
    return scraper.scrape()


# Example usage
if __name__ == "__main__":
    # Test the scraper
    test_url = "https://example.com"
    result = scrape_website(test_url)
    
    if result['success']:
        print(f"✅ Successfully scraped: {result['company_name']}")
        print(f"📝 Description: {result['description']}")
    else:
        print(f"❌ Error: {result['error']}")
