from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs


def get_category_name(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if "subopcao" in params:
        subopcao_valor = params["subopcao"][0]
        nome_tabela = soup.find("button", value=subopcao_valor)

        if not nome_tabela:
            return ''

        return nome_tabela.get_text(strip=True)
    
    return ''