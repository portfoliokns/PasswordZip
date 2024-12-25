import os
from tkinter import Tk, messagebox, simpledialog, Label, Entry, Entry, END
from tkinter.filedialog import askdirectory
import pyzipper
from pathlib import Path
import re

def is_hankaku(password):
    return any(re.match(r'[^\x00-\x7F]', char) for char in password)

class passwordDialog(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.ok_button_text = "登録"
        self.cancel_button_text = "キャンセル"
        self.isCancel = True
        super().__init__(parent, title)

    layout_row = {
        "password": 0,
        "re_password": 1,
        "announce": 2,
        "repletion1": 3,
        "repletion2": 4,
        "repletion3": 5
    }

    def body(self, master):
        self.password = Entry(master, show="*")
        self.password.grid(row=self.layout_row["password"], column=0, columnspan=2)

        self.re_password = Entry(master, show="*")
        self.re_password.grid(row=self.layout_row["re_password"], column=0, columnspan=2)

        Label(master, text="zipファイルへパスワードを設定してください。").grid(row=self.layout_row["announce"], column=0, columnspan=2)
        Label(master, text="※同じパスワードを2回入力してください。").grid(row=self.layout_row["repletion1"], column=0, columnspan=2)
        Label(master, text="※必ず半角英数字記号で入力してください。").grid(row=self.layout_row["repletion2"], column=0, columnspan=2)
        Label(master, text="※パスワードは忘れないようにしてください。").grid(row=self.layout_row["repletion3"], column=0, columnspan=2)

        return self.password

    def validate(self):
        password = self.password.get()
        re_password = self.re_password.get()

        if not password or not re_password:
            messagebox.showerror("エラー", "パスワードを入力してください。")
            self.reset()
            return False

        if is_hankaku(password) :
            messagebox.showerror("エラー", "全角が含まれています。全角で入力しないでください")
            self.reset()
            return False

        if password != re_password:
            messagebox.showerror("エラー", "パスワードが一致しません。")
            self.reset()
            return False

        return True

    def reset(self):
        self.password.focus_set()
        self.password.delete(0, END)
        self.re_password.delete(0, END)

    def apply(self, event=None):
        self.zip_pass = self.password.get()
        self.isCancel = False

    def cancel(self, event=None):
        if self.isCancel:
            self.zip_pass = None
        self.destroy() 

    def get_password(self):
        return self.zip_pass

def create_zip(full_file_path, password):
    output_dir = os.path.expanduser("~/ZipPassword")
    os.makedirs(output_dir, exist_ok=True)
    zip_file_name = output_dir / Path(full_file_path.name + ".zip")
    with pyzipper.AESZipFile(zip_file_name, 'w', encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password)
        zipf.write(full_file_path, arcname=os.path.basename(full_file_path))

def getPassword():
    root = Tk()
    root.withdraw()
    dialog = passwordDialog(root, title="パスワード登録")
    password = dialog.get_password()
    return password

def startZip():
    root = Tk()
    root.withdraw()

    folder_path = askdirectory()
    if not folder_path:
        exit()

    password = getPassword()
    if password == None:
        exit()

    result = messagebox.askyesno('圧縮を実行しますか？','次のフォルダにあるファイルをzipファイルに変換しますか\n' + folder_path)
    if not result:
        exit()

    files = os.listdir(folder_path)
    files.sort()
    for file in files:
        full_file_path = Path(os.path.join(folder_path, file))
        create_zip(full_file_path, password.encode())

    messagebox.showinfo("圧縮が完了しました", "すべてのファイルの圧縮に成功しました")

if __name__ == "__main__":
    startZip()