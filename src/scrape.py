import requests

def webscrape(security_code:str)->bytes:
    address = "https://www.screener.in/company/" + security_code + "/"
    request = requests.get(address)
    html_data = request.content
    return html_data