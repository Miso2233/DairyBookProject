import customtkinter as ctk


class DairyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # 模拟笔记数据
        self.diaries = {
            "2023-10-01": "今天是国庆节，天气晴朗，和家人一起去了公园...",
            "2023-10-05": "项目进展顺利，解决了几个关键的技术难题...",
            "2023-10-12": "读完了《百年孤独》，感触颇深...",
            "2023-10-18": "尝试了新的菜谱，味道还不错...",
            "2023-10-25": "参加了技术分享会，学到了很多新知识..."
        }

        # 设置窗口
        self.title("My Notebook")
        self.geometry("800x500")
        ctk.set_appearance_mode("light")

        # 设置分栏状况
        self.grid_rowconfigure(0, weight=1)     # 唯一行，全权
        self.grid_columnconfigure(0, weight=0)  # 左栏，无拉伸权
        self.grid_columnconfigure(1,weight=1)   # 右栏，全权

        # 左侧日记列表框架
        self.sidebar_frame = ctk.CTkFrame(master=self, width=200, corner_radius=0) # 创建一个框架
        self.sidebar_frame.grid(row=0, column=0, rowspan=1, sticky="nsew") # 绑定到主体网格，并使之扩展
        self.sidebar_frame.grid_rowconfigure(0, weight=0) # 左栏设置0号行，无拉伸权
        self.sidebar_frame.grid_rowconfigure(1, weight=1) # 左栏设置1号行，全权

        # 左侧标题
        self.sidebar_lable = ctk.CTkLabel(
            master=self.sidebar_frame,
            text="所有笔记",
            font=ctk.CTkFont(size=20, weight="bold")
        ) # 构建左侧标题标签
        self.sidebar_lable.grid(row=0, column=0, padx=20, pady=20) # 绑定到左栏网格，并设置大小

        # 笔记列表 (使用可滚动框架)
        self.sidebar_list = ctk.CTkScrollableFrame(
            master=self.sidebar_frame
        ) # 构造左侧可滚动列表
        self.sidebar_list.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew") # 绑定到左栏网格，并设置大小

if __name__ == "__main__":
    app = DairyApp()
    app.mainloop()