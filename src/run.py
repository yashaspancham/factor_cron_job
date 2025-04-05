import pandas
import requests
from bs4 import BeautifulSoup
import time
from memory_profiler import profile
from pathlib import Path
from saveToS3.saveToS3 import upload
from utils.utils import get_old_file_name, is_uploaded

start_point=time.time()
stock_list = pandas.read_csv("./Equity.csv")
security_code_list = stock_list.index.to_list()
number_of_stocks = 0
failed_number_of_stocks=0

for security_code in security_code_list:
    security_code = str(security_code)
    if (number_of_stocks % 50) == 0:
        print(f"Number of files downloaded: {number_of_stocks}")
    try:
        if number_of_stocks == 20:
            end_point=time.time()
            print(f"The total number of stocks that were attempted to downloaded: {number_of_stocks}")
            print(f"The total number of stocks failed to dowmload: {failed_number_of_stocks}")
            print(f"The total time taken: {end_point-start_point} seconds")
            exit(0)
        data_directory=Path(__file__).resolve().parent.parent/'DATA'
        data_directory.mkdir(exist_ok=True)
        old_files=list(data_directory.glob("*.html"))
        old_file_name=get_old_file_name(old_files, security_code)
        if is_uploaded(old_file_name):
            number_of_stocks += 1
            continue
        print("This will webscrape")
        old_files=list(data_directory.glob("*.html"))
        address = "https://www.screener.in/company/" + security_code + "/"
        request = requests.get(address)
        soup = BeautifulSoup(request.content, 'html.parser')
        html_data = request.content
        upload(security_code, html_data)
        
    except Exception as error:
        print(f"unable to download: {security_code}, error: {error}")
        failed_number_of_stocks+=1
    number_of_stocks += 1
    
end_point=time.time()
print(f"The total number of stocks that were attempted to downloaded: {number_of_stocks}")
print(f"The total number of stocks failed to dowmload: {failed_number_of_stocks}")
print(f"The total time taken: {end_point-start_point} seconds")