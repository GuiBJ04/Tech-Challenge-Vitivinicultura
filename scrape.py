import requests
from bs4 import BeautifulSoup

def get_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip()
        return title
    except Exception as e:
        return f"Error: {e}"
    
def get_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        headers = []
        for header_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for header in soup.find_all(header_tag):
                headers.append(header.get_text(strip=True))

        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        return headers, paragraphs
    except Exception as e:  
        return f"Error: {e}"