
```markdown
# Dynamic Web Scraper with FastAPI and OpenAI

This project is a dynamic web scraper built with FastAPI that leverages OpenAI's GPT-4 to generate Python code for scraping and extracting data from web pages dynamically. The application takes a URL input and dynamically generates a function to extract structured data in JSON format.

## Features

- **Dynamic Web Scraping:** Generate Python functions dynamically using OpenAI's GPT-4 to scrape web pages.
- **FastAPI Integration:** FastAPI is used to create an API endpoint for data extraction.
- **JSON Data Extraction:** Extracts metadata, content, product information, reviews, FAQs, comments, and more from web pages.
- **Environment Configuration:** Uses `dotenv` for managing environment variables, including the OpenAI API key.

## Requirements

- Python 3.8 or higher
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- OpenAI Python Client
- Python-dotenv

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/alinaqi/dynamic_crawler.git
   cd dynamic_crawler
   ```

2. **Create and Activate a Virtual Environment**

   On macOS and Linux:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

   On Windows:
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. **Run the FastAPI Server**

   Start the FastAPI server using Uvicorn:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   This will start the server on `http://localhost:8000`.

2. **API Endpoint**

   - **POST** `/extract-data/`

   Send a POST request to the `/extract-data/` endpoint with a JSON body containing the URL you want to scrape.

   **Request Example:**

   ```json
   {
     "url": "https://www.example.com"
   }
   ```

   **Response Example:**

   ```json
   {
     "url": "https://www.example.com",
     "metadata": {
       "title": "Page Title",
       "description": "A brief description of the page content",
       ...
     },
     "content": {
       "summary": "A brief summary of the page content.",
       ...
     },
     ...
   }
   ```

## How It Works

1. **Data Extraction Prompt:**
   - The app uses OpenAI's GPT-4 to generate a JSON structure for the data to be extracted from the HTML page.

2. **Function Generation Prompt:**
   - Given the JSON structure and the URL, GPT-4 generates a Python function named `scrape_data` to extract data from the provided URL.

3. **Dynamic Execution:**
   - The generated function is executed dynamically using Python's `exec()` function in a controlled environment.

4. **Output:**
   - The output is returned as a structured JSON object containing metadata, content, and other extracted entities from the web page.

## Example Code

Here is an example of the dynamically generated scraping function:

```python
def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    # Make a request to the webpage
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract relevant data (as per the structure defined)
    ...
    return output
```

## Error Handling

The application includes error handling for various scenarios, such as:

- Invalid URLs or failed HTTP requests.
- Errors in dynamically generated code.
- Issues with OpenAI API calls.

If an error occurs, a detailed traceback is printed, and a 500 HTTP response is returned with an error message.

## License

This project is licensed under the free lunch license.. enjoy and spread the joy :)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [OpenAI](https://openai.com/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://docs.python-requests.org/)

## Contact

For any questions or issues contact me :)

```