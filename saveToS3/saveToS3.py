#this for now saves to local
from pathlib import Path
from datetime import datetime
from utils.utils import get_old_file_name, is_uploaded

def upload(security_code:str, html_data:bytes) -> None:
    data_directory=Path(__file__).resolve().parent.parent/'DATA'
    data_directory.mkdir(exist_ok=True)
    old_files=list(data_directory.glob("*.html"))
    old_file_name=get_old_file_name(old_files, security_code)
    if is_uploaded(old_file_name):
        return None
    new_file_path=data_directory / f"{security_code }_{datetime.now()}.html"
    file = new_file_path.open('w', encoding='utf-8')
    file.write(html_data.decode('utf-8'))
    file.close()
