from typing import Any, Dict

import customtkinter as ctk


class DairyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # 模拟笔记数据
        self.notes: Dict[int, Dict[str, Any]] = {
            1001: {
                "metadata": {
                    "title": "国庆日记",
                    "date": "2023-10-01",
                    "tags": ["家庭", "假日"]
                },
                "content": "今天是国庆节，天气晴朗，和家人一起去了公园..."
            },
            1002: {
                "metadata": {
                    "title": "项目进展报告",
                    "date": "2023-10-05",
                    "tags": ["工作", "技术"]
                },
                "content": "项目进展顺利，解决了几个关键的技术难题..."
            },
            1003: {
                "metadata": {
                    "title": "读书笔记",
                    "date": "2023-10-12",
                    "tags": ["阅读", "文学"]
                },
                "content": "读完了《百年孤独》，感触颇深..."
            },
            1004: {
                "metadata": {
                    "title": "烹饪实验",
                    "date": "2023-10-18",
                    "tags": ["美食", "生活"]
                },
                "content": "尝试了新的菜谱，味道还不错..."
            },
            1005: {
                "metadata": {
                    "title": "技术分享会总结",
                    "date": "2023-10-25",
                    "tags": ["学习", "技术"]
                },
                "content": "参加了技术分享会，学到了很多新知识..."
            }
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
        self.sidebar_frame = ctk.CTkFrame(master=self, width=200, corner_radius=0, fg_color="#EBF6FC") # 创建一个框架
        self.sidebar_frame.grid(row=0, column=0, rowspan=1, sticky="nsew") # 绑定到主体网格，并使之扩展
        self.sidebar_frame.grid_rowconfigure(0, weight=0) # 左栏设置0号行，无拉伸权
        self.sidebar_frame.grid_rowconfigure(1, weight=1) # 左栏设置1号行，全权

        # 左侧标题
        self.sidebar_lable = ctk.CTkLabel(
            master=self.sidebar_frame,
            text="All Notes",
            font=ctk.CTkFont(family="微软雅黑", size=20, weight="bold")
        ) # 构建左侧标题标签
        self.sidebar_lable.grid(row=0, column=0, padx=20, pady=20) # 绑定到左栏网格，并设置大小

        # 笔记列表框架 (使用可滚动框架)
        self.sidebar_list = ctk.CTkScrollableFrame(
            master=self.sidebar_frame,
            fg_color="#FFFFFF"
        ) # 构造左侧可滚动列表
        self.sidebar_list.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew") # 绑定到左栏网格，并设置大小

        # 构建按钮列表
        self.button_list:Dict[int,ctk.CTkButton] = {}
        for index in self.notes:
            btn = ctk.CTkButton(
                master=self.sidebar_list,
                fg_color="#FFFFFF",
                hover_color="#66CCFF",
                text=self.notes[index]["metadata"]["title"],
                text_color="#000000",
                width=180,
                height=40,
                anchor="w",
                font=ctk.CTkFont(family="微软雅黑", size=14),
                command=lambda idx=index:self.show_note(idx)
            )
            btn.pack(pady=5, padx=5) # 使用pack自动进行排列
            self.button_list[index] = btn


        # 右侧笔记内容框架
        self.content_frame = ctk.CTkFrame(master=self,corner_radius=0,fg_color="#FFFFFF")
        self.content_frame.grid(row=0, column=1, sticky="nsew") #绑定到右栏网格
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=0) # 构建行与列

        # 笔记标题
        self.note_title = ctk.CTkTextbox(
            self.content_frame,
            font=ctk.CTkFont(family="微软雅黑", size=24, weight="normal"),
            height=40,
            width=100,
            wrap="none",
            fg_color="#FFFFFF"
        )
        self.note_title.insert("1.0","👋Morning! | Select a note & get started!")
        self.note_title.grid(row=0, column=0, padx=30, pady=30, sticky="we")

        # 笔记内容文本框
        self.note_content = ctk.CTkTextbox(
            master=self.content_frame,
            wrap="word",
            font=ctk.CTkFont(family="微软雅黑", size=16),
            state="normal"
        )
        self.note_content.grid(row=1, column=0, sticky="nswe")

        # 编辑栏按钮
        self.save_button = ctk.CTkButton(
            master=self.content_frame,
            text="Save",
            width=100,
            height=40,
            text_color="#FFFFFF",
            fg_color="#1F883D",
            font=ctk.CTkFont(family="微软雅黑", size=14, weight="normal"),
            command=self.save_note
        )
        self.save_button.grid(row=2, padx=30, pady=20, sticky="e")

        self.current_index = None

    def show_note(self,index):
        assert index in self.notes
        self.current_index = index
        self.note_title.delete("1.0","end")
        self.note_title.insert("1.0",self.notes[index]["metadata"]["title"])# 修改标题
        self.note_content.delete("1.0","end")
        self.note_content.insert("1.0",self.notes[index]["content"]) # 修改内容

    def save_note(self):
        if not self.current_index: 
            return
        new_content = self.note_content.get("1.0","end")
        self.notes[self.current_index]["content"] = new_content
        new_title = self.note_title.get("1.0","end").strip()
        self.notes[self.current_index]["metadata"]["title"] = new_title
        self.button_list[self.current_index].configure(text=new_title)



if __name__ == "__main__":
    app = DairyApp()
    app.mainloop()