import os
from tkinter import Tk, messagebox, simpledialog, Toplevel
from tkinter.filedialog import askdirectory
import pyzipper
from pathlib import Path
import re

def is_hankaku(password):
    return any(re.match(r'[^\x00-\x7F]', char) for char in password)

def create_zip(full_file_path, password):
    output_dir = os.path.expanduser("~/ZipPassword")
    os.makedirs(output_dir, exist_ok=True)
    zip_file_name = output_dir / Path(full_file_path.name + ".zip")
    with pyzipper.AESZipFile(zip_file_name, 'w', encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password)
        zipf.write(full_file_path, arcname=os.path.basename(full_file_path))

def getPassword():
    exit_range = 3
    for counter in range(exit_range):
        password = simpledialog.askstring("パスワード入力","パスワードを入力してください\n必ず半角英数字記号で入力してください")
        re_password = simpledialog.askstring("パスワード再入力","パスワードをもう一度入力してください\n必ず半角英数字記号で入力してください")

        if password != re_password:
            messagebox.showerror("パスワード不一致", "パスワードが一致しません\n2回同じパスワードを設定してください")
        elif password == "":
            messagebox.showerror("パスワード未入力", "パスワードが空になっています\nパスワードを入力してください")
        elif is_hankaku(password):
            messagebox.showerror("全角は登録できません", "パスワードに全角が含まれています\n半角で入力してください")
        elif password == re_password:
            return password.encode()
        else:
            messagebox.showerror("パスワード不一致", "パスワードが一致しません")

def startZip():
    root = Tk()
    root.withdraw()

    folder_path = askdirectory()
    if not folder_path:
        exit()

    password = getPassword()
    if password == None:
        messagebox.showerror("エラー", "パスワードの入力に失敗しました\n終了します")
        exit()

    result = messagebox.askyesno('圧縮を実行しますか？','次のフォルダにあるファイルをzipファイルに変換しますか\n' + folder_path)
    if not result:
        exit()

    files = os.listdir(folder_path)
    files.sort()
    for file in files:
        full_file_path = Path(os.path.join(folder_path, file))
        create_zip(full_file_path, password)

    messagebox.showinfo("圧縮が完了しました", "すべてのファイルの圧縮に成功しました")

if __name__ == "__main__":
    startZip()