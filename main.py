import os
import shelve
from datetime import datetime
from typing import Dict

import customtkinter as ctk


class DairyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # 初始化本地存档
        os.makedirs("data", exist_ok=True)

        # 读取笔记数据
        with shelve.open("data/notes") as notes:
            self.notes:dict = notes.get("Miso",{})

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
        self.sidebar_frame.grid_rowconfigure(1, weight=0) # 左栏设置1号行，无拉伸权
        self.sidebar_frame.grid_rowconfigure(2, weight=1) # 左栏设置1号行，全权

        # 左侧标题
        self.sidebar_lable = ctk.CTkLabel(
            master=self.sidebar_frame,
            text="📚笔记库",
            font=ctk.CTkFont(family="微软雅黑", size=20, weight="bold")
        ) # 构建左侧标题标签
        self.sidebar_lable.grid(row=0, column=0, padx=20, pady=(20,0)) # 绑定到左栏网格，并设置大小

        # 新建笔记按钮
        self.new_button = ctk.CTkButton(
            master=self.sidebar_frame,
            height=40,
            width=180,
            fg_color="#66CCFF",
            text="新建笔记",
            font=ctk.CTkFont(family="微软雅黑", size=14, weight="bold"),
            text_color="#FFFFFF",
            command=self.new_note
        )
        self.new_button.grid(row=1, padx=10, pady=(20,0))

        # 笔记列表框架 (使用可滚动框架)
        self.sidebar_list = ctk.CTkScrollableFrame(
            master=self.sidebar_frame,
            fg_color="#FFFFFF"
        ) # 构造左侧可滚动列表
        self.sidebar_list.grid(row=2, column=0, padx=10, pady=(20,10), sticky="nsew") # 绑定到左栏网格，并设置大小

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
                command=lambda idx=index:[self.show_note(idx),self.text_modified.set(False)]
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
        self.note_title.bind("<KeyRelease>",command=self.on_text_modified)

        # 笔记内容文本框
        self.note_content = ctk.CTkTextbox(
            master=self.content_frame,
            wrap="word",
            font=ctk.CTkFont(family="微软雅黑", size=16),
            state="normal"
        )
        self.note_content.grid(row=1, column=0, sticky="nswe", padx=30, pady=10)
        self.note_content.bind("<KeyRelease>",command=self.on_text_modified) # 每次键盘输入触发一次比较函数，可能触发self.text_modified的写入

        # 编辑栏按钮
        self.button_frame = ctk.CTkFrame(
            master=self.content_frame,
            fg_color="#FFFFFF"
        )
        self.button_frame.grid(row=2, padx=30, pady=20, sticky="we")

        self.save_button = ctk.CTkButton(
            master=self.button_frame,
            text="保存",
            width=100,
            height=40,
            text_color="#FFFFFF",
            font=ctk.CTkFont(family="微软雅黑", size=14, weight="normal"),
            command=self.save_note
        )
        self.save_button.pack(side="right", padx=(10, 0))

        self.optimize_button = ctk.CTkButton(
            master=self.button_frame,
            text="自动排版",
            width=100,
            height=40,
            text_color="#FFFFFF",
            fg_color="#009666", # 按钮颜色 自动排版
            font=ctk.CTkFont(family="微软雅黑", size=14, weight="normal"),
            command=self.optimize_text
        )
        self.optimize_button.pack(side="right", padx=(10, 0))

        self.current_index = None

        self.text_modified = ctk.BooleanVar(value=False)
        self.text_modified.trace_add("write", lambda *args: self.update_save_button()) # 对变量添加【写入】侦听

        self.update_save_button()


    def update_save_button(self):
        if self.text_modified.get():
            self.save_button.configure(
                fg_color="#009666" # 按钮颜色 保存 激活
            )
        else:
            self.save_button.configure(
                fg_color="#9E9F9E" # 按钮颜色 保存 未激活
            )            
    
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

        with shelve.open("data/notes") as notes:
            notes["Miso"] = self.notes

        self.text_modified.set(False)

    def new_note(self):
        self.save_note()
        new_index = max(self.notes.keys()) + 1
        self.current_index = new_index
        self.notes[new_index] = {
            'metadata': {
                'title': '新的笔记',
                'date': datetime.now().strftime("%Y-%m-%d"),
                'tags': []
            }, 
            'content': ''
        }
        btn = ctk.CTkButton(
            master=self.sidebar_list,
            fg_color="#FFFFFF",
            hover_color="#66CCFF",
            text=self.notes[new_index]["metadata"]["title"],
            text_color="#000000",
            width=180,
            height=40,
            anchor="w",
            font=ctk.CTkFont(family="微软雅黑", size=14),
            command=lambda idx=new_index:[self.show_note(idx),self.text_modified.set(False)]
        )
        self.button_list[new_index] = btn
        btn.pack(pady=5, padx=5) # 使用pack自动进行排列
        self.text_modified.set(False)
        self.show_note(new_index)


    def optimize_text(self):
        if not self.current_index: 
            return
        raw = self.note_content.get("1.0","end")
        raw_list = raw.split("\n")
        indent_list = []
        for line in raw_list:
            if line.startswith("        "):
                indent_list.append(line)
            elif line != "":
                indent_list.append("        "+line)
        output_txt = "\n" + "\n\n".join(indent_list)

        self.note_content.delete("1.0","end")
        self.note_content.insert("1.0",output_txt)

        self.on_text_modified() # 触发一次文本比较函数

    # 比较文本框更改
    def on_text_modified(self,event=None):
        if not self.current_index:
            return
        self.text_modified.set(
            self.note_content.get("1.0","end") != self.notes[self.current_index]["content"] or self.note_title.get("1.0","end") != self.notes[self.current_index]["metadata"]["title"]
        )

class AnimateTools:

    # 颜色转换函数
    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb):
        return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'
    
    


if __name__ == "__main__":
    app = DairyApp()
    print(app.notes)
    app.mainloop()