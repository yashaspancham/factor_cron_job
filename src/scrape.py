import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL=os.getenv("BASE_URL")
def webscrape(security_code:str)->bytes:
    address = f"{BASE_URL}/company/" + security_code + "/"
    request = requests.get(address)
    html_data = request.content
    return html_data