import requests
from bs4 import BeautifulSoup

def amonatbank():
    """Returns a list of required data about amonatbank"""
    
    url = 'https://www.amonatbonk.tj/en/personal/loans/potrebitelskiy-kredit/'

    site = requests.get(url)

    soup = BeautifulSoup(site.text, "html.parser")

    result = []
    for i in soup.find_all('h3'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)

    return [int(result[2]), int(result[0]), int(result[1])]