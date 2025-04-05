import pandas
import requests
from bs4 import BeautifulSoup
import time
from memory_profiler import profile


start_point=time.time()
stock_list = pandas.read_csv("./Equity.csv")
Security_Code_list = stock_list.index.to_list()
number_of_stocks = 0
failed_number_of_stocks=0

for Security_Code in Security_Code_list:
    Security_Code = str(Security_Code)
    if (number_of_stocks % 50) == 0:
        print(f"Number of files downloaded: {number_of_stocks}")
    try:
        if number_of_stocks == 100:
            end_point=time.time()
            print(f"The total number of stocks that were attempted to downloaded: {number_of_stocks}")
            print(f"The total number of stocks failed to dowmload: {failed_number_of_stocks}")
            print(f"The total time taken: {end_point-start_point} seconds")
            exit(0)
        address = "https://www.screener.in/company/" + Security_Code + "/"
        request = requests.get(address)
        soup = BeautifulSoup(request.content, 'html.parser')
        html_data = request.content
        with open('./DATA/' + Security_Code + '.html', "w") as file:
            file.write(html_data.decode("utf-8"))
        
    except Exception:
        print(f"unable to download: {Security_Code}")
        failed_number_of_stocks+=1
    time.sleep(1)
    number_of_stocks += 1
    
end_point=time.time()
print(f"The total number of stocks that were attempted to downloaded: {number_of_stocks}")
print(f"The total number of stocks failed to dowmload: {failed_number_of_stocks}")
print(f"The total time taken: {end_point-start_point} seconds")