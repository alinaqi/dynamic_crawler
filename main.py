import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bs4 import BeautifulSoup
import json
import openai
import os
from dotenv import load_dotenv
import traceback

app = FastAPI()
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


example_code = """
def scrap_url(url):
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

prompt_for_data_extraction = """
Given an HTML page, convert it to JSON, separating out all the key entities from the page e.g. main content, images, reviews, etc. Return as json. The example json is given below. Analyze the page and add any additional entities that may be needed:

{
  "url": "https://www.example.com",  // The URL of the webpage
  "metadata": {
    "title": "Page Title",  // The title of the page
    "description": "A brief description of the page content",  // Meta description for SEO
    "keywords": ["keyword1", "keyword2", "keyword3"],  // Keywords related to the page
    "author": "Author Name",  // Author of the content
    "language": "en",  // Language of the content
    "publish_date": "2024-09-09T12:00:00Z",  // Publication date (if applicable)
    "last_updated": "2024-09-10T12:00:00Z",  // Last update date (if applicable)
    "canonical_url": "https://www.example.com",  // Canonical URL for SEO
    "favicon": "https://www.example.com/favicon.ico",  // URL to the site's favicon
    "og_tags": {  // Open Graph tags for social sharing
      "og:title": "Open Graph Title",
      "og:description": "Open Graph Description",
      "og:image": "https://www.example.com/image.jpg",
      "og:type": "website"
    },
    "twitter_tags": {  // Twitter Card tags for social sharing
      "twitter:card": "summary_large_image",
      "twitter:title": "Twitter Title",
      "twitter:description": "Twitter Description",
      "twitter:image": "https://www.example.com/image.jpg"
    }
  },
  "content": {
    "summary": "A brief summary of the page content.",  // A summary or abstract of the page content
    "main_topic": "The primary topic or theme of the page",  // The main topic or theme
    "headings": [  // List of all headings on the page
      {
        "tag": "h1",
        "text": "Main Heading"
      },
      {
        "tag": "h2",
        "text": "Sub Heading 1"
      }
    ],
    "paragraphs": [  // List of all paragraphs on the page
      "Paragraph 1 text...",
      "Paragraph 2 text..."
    ],
    "images": [  // List of images on the page
      {
        "url": "https://www.example.com/image1.jpg",
        "alt_text": "Description of image 1",
        "caption": "Caption for image 1"
      }
    ],
    "videos": [  // List of videos on the page
      {
        "url": "https://www.example.com/video1.mp4",
        "title": "Title of the video",
        "description": "Description of the video",
        "thumbnail": "https://www.example.com/video_thumbnail.jpg"
      }
    ],
    "links": [  // List of internal and external links
      {
        "text": "Link Text",
        "url": "https://www.example.com/some-link",
        "type": "internal"  // Can be 'internal' or 'external'
      }
    ]
  },
  "products": [  // List of products (if any)
    {
      "product_id": "12345",
      "name": "Product Name",
      "description": "Product Description",
      "price": {
        "amount": 99.99,
        "currency": "USD"
      },
      "availability": "In Stock",  // or "Out of Stock"
      "categories": ["Category 1", "Category 2"],
      "images": [
        {
          "url": "https://www.example.com/product_image.jpg",
          "alt_text": "Product Image"
        }
      ],
      "reviews": [  // List of reviews for the product
        {
          "review_id": "98765",
          "author": "Reviewer Name",
          "rating": 4.5,
          "date": "2024-09-09",
          "text": "Review text here..."
        }
      ]
    }
  ],
  "reviews": [  // General reviews (if the page is a review page)
    {
      "review_id": "54321",
      "author": "Reviewer Name",
      "rating": 4.0,
      "date": "2024-09-09",
      "title": "Review Title",
      "text": "Detailed review text...",
      "product_id": "12345"  // ID of the product being reviewed (if applicable)
    }
  ],
  "faqs": [  // Frequently Asked Questions
    {
      "question": "What is the product made of?",
      "answer": "The product is made of high-quality materials."
    }
  ],
  "comments": [  // User comments or discussion (if applicable)
    {
      "comment_id": "23456",
      "author": "Commenter Name",
      "date": "2024-09-09T12:00:00Z",
      "text": "This is a comment text.",
      "replies": [
        {
          "comment_id": "23457",
          "author": "Reply Author",
          "date": "2024-09-10T12:00:00Z",
          "text": "This is a reply to the comment."
        }
      ]
    }
  ],
  "sidebar": {  // Sidebar content (if applicable)
    "related_articles": [  // Related articles or links
      {
        "title": "Related Article 1",
        "url": "https://www.example.com/related-article-1"
      }
    ],
    "advertisements": [  // Advertisements present on the page
      {
        "ad_id": "ad123",
        "image_url": "https://www.example.com/ad.jpg",
        "target_url": "https://www.example.com/ad-target",
        "description": "Ad description"
      }
    ]
  },
  "footer": {  // Footer information
    "links": [  // List of links in the footer
      {
        "text": "Privacy Policy",
        "url": "https://www.example.com/privacy-policy"
      }
    ],
    "contact_info": {  // Contact information if available in the footer
      "email": "contact@example.com",
      "phone": "+1-234-567-8900"
    },
    "social_media": [  // Social media links if available in the footer
      {
        "platform": "Twitter",
        "url": "https://twitter.com/example"
      }
    ]
  }
}

Return as JSON.

"""
@app.post("/extract-data/")
async def extract_data(request: str):
    try:
        # step 1 - generate the initial json
        print("Extracting data from the given URL...")
        completion = openai.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": prompt_for_data_extraction},
                    {"role": "user", "content": f"url: {request}"}
                ]
            )
        
        results = completion.choices[0].message.content
        #cleaning the json
        clean_results = results.strip('`').strip().lstrip('json').strip()


        print("First results: ", clean_results)

        print("generating code.. ")
        # step 2 - given the json and the url, create a function that extracts the data
        function_generator_prompt = f"""
        Given the JSON structure provided, write a python function to extract data from the given url. The function name should be 'scrape_data'

        JSON Structure: {results}
        URL: {request}

        Do not return any additional data. Do not add import files in the returned code. Return only python function ie don't return 'Here is the python function..' etc. 

        Example code is here:
        {example_code}



        """
        completion = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": function_generator_prompt},
                    {"role": "user", "content": f"url: {request}"}
                ]
            )
        
        script = completion.choices[0].message.content

        clean_script = script.strip('`').strip().lstrip('python').strip()

        print("Generated code: ", clean_script)

        # Step 3 - Execute the generated code in a controlled namespace
        print("Executing generated code...")
        local_vars = {}
        exec(clean_script, globals(), local_vars)  # Execute within the global namespace
        
        # Ensure the function is loaded correctly
        scrape_function = local_vars.get('scrape_data')
        if not scrape_function:
            raise ValueError("Generated code does not define a valid function 'scrape_data'.")

        # Execute the generated scraping function
        output = scrape_function(request)
        print("Function executed successfully. Output:", output)
        
        return output
    

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
