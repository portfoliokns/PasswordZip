import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
import pyzipper
import getpass
from pathlib import Path
import re

def is_hankaku(password):
    return any(re.match(r'[^\x00-\x7F]', char) for char in password)

def create_zip(full_file_path, password):
    output_dir = "./zip/"
    os.makedirs(output_dir, exist_ok=True)
    zip_file_name = output_dir / Path(full_file_path.name + ".zip")
    print('圧縮中：' + str(full_file_path.name))
    with pyzipper.AESZipFile(zip_file_name, 'w', encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password)
        zipf.write(full_file_path, arcname=full_file_path)

def getPassword():
    
    exit_range = 3
    for counter in range(exit_range):
        print('パスワードを入力してください')
        password = getpass.getpass()
        print('確認のためもう一度同じパスワードを入力してください')
        re_password = getpass.getpass()

        if password != re_password:
            print('パスワードが一致しません  2回同じパスワードを設定してください')
        elif password == "":
            print('パスワードが未入力です')
        elif is_hankaku(password):
            print('パスワードに全角が含まれています  半角で入力してください')
        elif password == re_password:
            print('パスワードが一致しました  パスワードは忘れないようにしてください')
            return password.encode()
        else:
            print('パスワードが一致しません')

        print('----------------------------------------------------------')

def startZip():
    root = Tk()
    root.withdraw()
    folder_path = askdirectory()
    if not folder_path:
        print('処理を中止します。')
        exit()

    password = getPassword()
    if password == None:
        print('パスワードの入力に失敗しました  終了します')
        exit()

    print('圧縮を開始します')
    files = os.listdir(folder_path)
    files.sort()
    for file in files:
        full_file_path = Path(os.path.join(folder_path, file))
        create_zip(full_file_path, password)
    print('圧縮を終了します')

if __name__ == "__main__":
    startZip()