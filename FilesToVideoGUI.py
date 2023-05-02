import os
import tkinter as tk
import time
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import concurrent.futures
import threading
import FilesToVideo as ftv

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("FilesToVideo")
        self.master.geometry("800x600")
        self.master.resizable(True, True)
        
        self.file_list = []
        self.selected_files = []
        self.converted_files = []
        self.file_path = []
        
        self.frame1 = tk.Frame(self.master)
        self.frame1.pack(fill=tk.BOTH, expand=True)

        self.label1 = tk.Label(self.frame1, text="FilesToVideo", font=("Calibri", 16))
        self.label1.pack(pady=10)

        self.button1 = tk.Button(self.frame1, text="選取檔案", command=self.add_file,font=("Calibri", 12))
        self.button1.pack(pady=10)


        self.button3 = tk.Button(self.frame1, text="刪除選取的檔案", command=self.remove_file)
        self.button3.pack(pady=10)

        self.treeview1 = ttk.Treeview(self.frame1, columns=("name", "size", "mtime"), show="headings",height=5)
        self.treeview1.column("name", width=400, minwidth=400)
        self.treeview1.column("size", width=150, minwidth=150)
        self.treeview1.column("mtime", width=200, minwidth=200)
        self.treeview1.heading("name", text="檔案名稱")
        self.treeview1.heading("size", text="檔案大小")
        self.treeview1.heading("mtime", text="修改時間")
        self.treeview1.pack(fill=tk.BOTH, expand=True)

        self.button2 = tk.Button(self.frame1, text="開始轉檔", command=threading.Thread(target=self.convert_files).start)
        self.button2.pack(pady=10)
        
        self.frame2 = tk.Frame(self.master)
        self.frame2.pack(fill=tk.BOTH, expand=True)

        self.label2 = tk.Label(self.frame2, text="選取轉檔儲存資料夾", font=("Calibri", 16))
        self.label2.pack(pady=10)


        self.treeview2 = ttk.Treeview(self.frame2, columns=("name", "size", "mtime"), show="headings",height=5)
        self.treeview2.column("name", width=400)
        self.treeview2.column("size", width=150)
        self.treeview2.column("mtime", width=200)
        self.treeview2.heading("name", text="檔案名稱")
        self.treeview2.heading("size", text="檔案大小")
        self.treeview2.heading("mtime", text="修改時間")
        self.treeview2.pack(fill=tk.BOTH, expand=True)

        self.button4 = tk.Button(self.frame2, text="開啟儲存資料夾",font=("Calibri", 12) , command=self.open_folder)
        self.button4.pack(pady=10)

        self.update_treeview2()

    def add_file(self):
        files = filedialog.askopenfilenames()
        if not files:
            return
        file_set = set(files)
        for file in file_set:
            file_stat = os.stat(file)
            file_size = self.convert_size(file_stat.st_size)
            file_mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_stat.st_mtime))
            if (file, file_size, file_mtime) not in self.file_list:
                self.file_list.append((file, file_size, file_mtime))
                self.file_path.append(file)
                
        self.update_treeview1()

    def remove_file(self):
        selected_items = self.treeview1.selection()
        for item in selected_items:
            values = self.treeview1.item(item, "values")
            self.file_list.remove((values[0], values[1], values[2]))
            self.file_path.remove(values[0])
        self.update_treeview1()

    def convert_size(self, size_bytes):
        units = ["B", "KB", "MB", "GB", "TB"]
        index = 0
        while size_bytes >= 1024 and index < len(units) - 1:
            size_bytes /= 1024
            index += 1
        return f"{size_bytes:.2f} {units[index]}"
    def update_treeview1(self):
        self.treeview1.delete(*self.treeview1.get_children())
        for file in self.file_list:
            self.treeview1.insert("", "end", values=file)

    def convert_files(self):
        self.button1.config(state=tk.DISABLED)
        self.button2.config(state=tk.DISABLED)
        self.button3.config(state=tk.DISABLED)
        if len(self.file_path) == 0:
            messagebox.showerror("錯誤", "請先選取檔案！")
            self.button1.config(state=tk.NORMAL)
            self.button2.config(state=tk.NORMAL)
            self.button3.config(state=tk.NORMAL)
            return
        items = self.file_path
        print(items)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(ftv.FTV,items)

        self.file_list = []
        self.file_path = []


        messagebox.showinfo("執行結果","全部執行完成")
        self.update_treeview1()
        self.update_treeview2()
        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.NORMAL)
        self.button3.config(state=tk.NORMAL)

    def update_treeview2(self):
        # 先清空treeview2內容
        for row in self.treeview2.get_children():
            self.treeview2.delete(row)

        # 取得特定資料夾內的所有檔案
        
        folder_path = "C:/ISG/FilesToVideo/videos"
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
        else:
            os.makedirs(folder_path)
            files = os.listdir(folder_path)

        # 將每個檔案加入到treeview2中
        for file in files:
            file_path = os.path.join(folder_path, file)
            file_stat = os.stat(file_path)
            file_size = self.convert_size(file_stat.st_size)
            file_mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime))
            self.treeview2.insert("", "end", values=(file, file_size, file_mtime))
    
    def open_folder(self):
        p="C:/ISG/FilesToVideo/videos"
        if not os.path.exists(p):
            messagebox.showerror("錯誤: 資料夾不存在", "NOFOUND : C:/ISG/FilesToVideo/videos")
            return
        else:
            os.startfile(p)

        



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
