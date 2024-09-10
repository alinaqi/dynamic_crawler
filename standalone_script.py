import requests
from bs4 import BeautifulSoup
import json

# Example generated code stored as a string
generated_code = """
def scrape_amazon_product(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    # Make a request to the Amazon product page
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract metadata and product details
    metadata = {
        "title": soup.find('title').text.strip() if soup.find('title') else None,
        "description": soup.find('meta', {'name': 'description'})['content'].strip() if soup.find('meta', {'name': 'description'}) else None,
        "keywords": soup.find('meta', {'name': 'keywords'})['content'].strip().split(", ") if soup.find('meta', {'name': 'keywords'}) else [],
        "author": soup.find('meta', {'name': 'author'})['content'].strip() if soup.find('meta', {'name': 'author'}) else None,
        "language": soup.find('html')['lang'] if soup.find('html') else None,
        "favicon": soup.find('link', {'rel': 'icon'})['href'] if soup.find('link', {'rel': 'icon'}) else None,
        "og_tags": {tag['property'][3:]: tag['content'] for tag in soup.find_all('meta', property=lambda x: x and x.startswith('og:'))},
        "twitter_tags": {tag['name'][8:]: tag['content'] for tag in soup.find_all('meta', {'name': lambda x: x and x.startswith('twitter:')})},
    }

    # Extract main content
    content = {
        "summary": soup.find('meta', {'name': 'description'})['content'].strip() if soup.find('meta', {'name': 'description'}) else None,
        "headings": [{"tag": heading.name, "text": heading.get_text(strip=True)} for heading in soup.find_all(['h1', 'h2', 'h3'])],
        "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
        "images": [{"url": img['src'], "alt_text": img.get('alt', ''), "caption": img.get('alt', '')} for img in soup.find_all('img', src=True)],
        "videos": [],  # Assuming no direct video links on the page
        "links": [{"text": a.get_text(strip=True), "url": a['href'], "type": "external" if a['href'].startswith('http') else "internal"} for a in soup.find_all('a', href=True)],
    }

    # Product information (example for demonstration; more work needed for extracting details)
    product_info = {
        "product_id": url.split('/dp/')[-1],
        "name": metadata['title'],
        "description": metadata['description'],
        "price": None,  # Extract price dynamically
        "availability": None,  # Extract availability dynamically
        "categories": ["Electronics", "Monitors", "Computers"],  # Example data; may need to adjust
        "images": content['images'],
        "reviews": [],  # Extract reviews dynamically
    }

    # Combine data into the final dictionary
    output = {
        "url": url,
        "metadata": metadata,
        "content": content,
        "products": [product_info],
        "reviews": [],  # Reviews extraction logic needed
        "faqs": [],  # FAQs extraction logic needed
        "comments": [],  # Comments extraction logic needed
        "sidebar": {},  # Sidebar content extraction logic needed
        "footer": {},  # Footer content extraction logic needed
    }

    # Return or save the extracted data
    return output
"""

# Execute the generated code
print("Executing generated code...")
exec(generated_code)

# Now, the function scrape_amazon_product is available for use
print("Function loaded successfully.")
url = "https://www.amazon.de/Samsung-Odyssey-LC49G95TSSUXEN-Monitor-UltraWide/dp/B0866C4BM7"
result = scrape_amazon_product(url)

# Print or save the result as JSON
print(json.dumps(result, indent=4, ensure_ascii=False))
