from pathlib import Path
from datetime import datetime, timedelta

def get_old_file_name(old_files:list[Path],security_code:str)->str:
    old_file_name=""
    for i in old_files:
        if i.name.split("_")[0]==security_code:
            old_file_name=i.name    
    return old_file_name

def is_uploaded(old_file_name:str)->bool:
    if old_file_name=="":
        return False
    temp=old_file_name.split("_")[-1]
    old_datetime=temp.split(".")[0]
    file_time = datetime.strptime(old_datetime, "%Y-%m-%d %H:%M:%S")
    seven_days=datetime.now()-timedelta(days=7)
    if file_time<seven_days:
        return False
    return True
