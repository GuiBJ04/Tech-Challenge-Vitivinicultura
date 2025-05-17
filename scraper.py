import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url: str):
        try: 
            self.response = requests.get(url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except Exception as e:
            raise Exception(f"Erro ao inicializar Scraper: {e}")
        
    def get_title(self):
        try:
            title = self.soup.title.string.strip()
            return title
        except Exception as e:
            return f"Error: {e}"
        
    def get_headers(self):
        try:
            headers = []
            for header_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                for header in self.soup.find_all(header_tag):
                    headers.append(header.get_text(strip=True))
            return headers
        except Exception as e:
            return f"Error: {e}"
        

    def get_content(self):
        try:
            headers = self.get_headers()
            paragraphs = [p.get_text(strip=True) for p in self.soup.find_all('p')]
            return headers, paragraphs
        except Exception as e:  
            return f"Error: {e}"
        

    def get_table(self):
        try: 
            table = self.soup.find("table", class_="tb_base tb_dados")
            if not table:
                raise ValueError("Tabela com calsse 'tb_base tb_dados' não encontrada")
            rows = table.find_all("tr")
            header_row = rows[0]            
            headers = [
                cell.get_text(strip=True) for cell in header_row.find_all(["th", "td"])
            ]
            data_rows = rows[1:]
            data = []
            for row in data_rows:
                cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
                if len(cells) == len(headers):
                    data.append(cells)
            return data
        except Exception as e:
            return f"Error: {e}"
    
    def get_paragraphs(self):
        try:
            paragraphs = [p.get_text(strip=True) for p in self.soup.find_all('p')]
            return paragraphs
        except Exception as e:
            return f"Error: {e}"
        
    
        
    