import customtkinter as ctk


class DairyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # 设置窗口
        self.title("My Notebook")
        self.geometry("800x500")
        ctk.set_appearance_mode("light")

        # 设置分栏状况
        self.grid_rowconfigure(0, weight=1)     # 唯一行，全权
        self.grid_columnconfigure(0, weight=0)  # 左栏，无拉伸权
        self.grid_columnconfigure(1,weight=1)   # 右栏，全权

        # 左侧日记列表框架

        # 左侧标题

        # 日记列表 (使用可滚动框架)

if __name__ == "__main__":
    app = DairyApp()
    app.mainloop()