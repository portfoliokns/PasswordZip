import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
import zipfile
from pathlib import Path

def create_zip(full_file_path):
    zip_file_name = Path(full_file_path.name + ".zip")
    output_dir = "./zip/"
    os.makedirs(output_dir, exist_ok=True)
    zip_file_name = output_dir / (zip_file_name)
    with zipfile.ZipFile(zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(full_file_path, arcname=os.path.basename(full_file_path))

def startZip():
    root = Tk()
    root.withdraw()
    folder_path = askdirectory()
    if not folder_path:
        print('処理を中止します。')
        exit()

    files = os.listdir(folder_path)
    for file in files:
        full_file_path = Path(os.path.join(folder_path, file))
        create_zip(full_file_path)

if __name__ == "__main__":
    startZip()