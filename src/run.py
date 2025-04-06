import pandas
import time
from memory_profiler import profile
from pathlib import Path
from saveToS3.saveToS3 import upload
from datetime import datetime
from utils.utils import get_old_file_name, is_uploaded
from .scrape import webscrape
from .send_email import send_email

start_point=time.time()
stock_list = pandas.read_csv("./Equity.csv")
security_code_list = stock_list.index.to_list()
number_of_stocks = 0
failed_number_of_stocks=0

start_of_cron_job_datetime=datetime.now()

for security_code in security_code_list:
    security_code = str(security_code)
    if (number_of_stocks % 50) == 0:
        print(f"Number of files downloaded: {number_of_stocks}")
    try:
        if number_of_stocks == 20:
            end_point=time.time()
            subject="Test Factor_cron_job is done"
            message_text=f"""The total number of stocks that were attempted to downloaded: {number_of_stocks}.\n\n
            The total number of stocks failed to dowmload: {failed_number_of_stocks}\n\n
            The total time taken: {end_point-start_point} seconds or {(end_point-start_point)/3600} hours\n\n
            The cron_job started at {start_of_cron_job_datetime} and finished at {datetime.now()}\n\n
            """
            send_email(subject,message_text)
            print(message_text)
            exit(0)
        data_directory=Path(__file__).resolve().parent.parent/'DATA'
        data_directory.mkdir(exist_ok=True)
        old_files=list(data_directory.glob("*.html"))
        old_file_name=get_old_file_name(old_files, security_code)
        if is_uploaded(old_file_name):
            number_of_stocks += 1
            continue
        html_data = webscrape(security_code)
        upload(security_code, html_data)
        
    except Exception as error:
        print(f"unable to download: {security_code}, error: {error}")
        failed_number_of_stocks+=1
    number_of_stocks += 1
    
end_point=time.time()
subject="Factor_cron_job is done"
message_text=f"""The total number of stocks that were attempted to downloaded: {number_of_stocks}.\n\n
The total number of stocks failed to dowmload: {failed_number_of_stocks}\n\n
The total time taken: {end_point-start_point} seconds or {(end_point-start_point)/3600} hours\n\n
The cron_job started at {start_of_cron_job_datetime} and finished at {datetime.now()}\n\n
"""
send_email(subject,message_text)
print(message_text)