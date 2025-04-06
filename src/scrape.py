import requests
from bs4 import BeautifulSoup

def webscrape(security_code:str)->str:
    address = "https://www.screener.in/company/" + security_code + "/"
    request = requests.get(address)
    soup = BeautifulSoup(request.content, 'html.parser')
    html_data = request.content
    return html_data