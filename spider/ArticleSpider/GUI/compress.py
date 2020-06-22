#!usr/bin/env python  
#-*- coding:utf-8 -*-

import tkinter
import tkinter.filedialog
import tkinter.messagebox
import zipfile
import os

class Compress_Soft():
    file_list = []
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.minsize(300,300)
        self.root.title('压缩软件1.0')
        self.windows()
        self.root.mainloop()
    # 界面布局
    def windows(self):
        # 添加按钮
        self.btn_addfile = tkinter.Button(self.root, text='添加文件', command=self.addfile)
        self.btn_addfile.place(x=10, y=16, width=80, height=30)
        # 压缩按钮
        self.btn_compress = tkinter.Button(self.root, text='压缩操作', command=self.compress)
        self.btn_compress.place(x=110, y=16, width=80, height=30)
        # 解压按钮
        self.btn_uncompress = tkinter.Button(self.root, text='解压操作', command=self.uncompress)
        self.btn_uncompress.place(x=210, y=16, width=80, height=30)
        # 信息展示区域
        self.label_info = tkinter.Label(self.root, bg='white', anchor='nw', justify='left')
        self.label_info.place(x=10, y=51, width=280, height=245)
    #添加文件函数
    def addfile(self):
        paths = tkinter.filedialog.askopenfilenames(title='选择要压缩的文件')
        for path in paths:
            self.file_list.append(path)
            self.label_info['text'] = '\n'.join(self.file_list)
    # 压缩
    def compress(self):
        # 设置压缩路径
        compass = tkinter.filedialog.asksaveasfilename(filetypes=(('zip文件','*zip'),))
        zp = zipfile.ZipFile(compass,'a')
        for path in self.file_list:
            zp.write(path,os.path.basename(path))
        zp.close()
        tkinter.messagebox.showinfo(title='操作结果',message='压缩成功')
    # 解压
    def uncompress(self):
        zippath = tkinter.filedialog.askopenfilename()
        # 打开压缩文件
        zp = zipfile.ZipFile(zippath,'r')
        # 解压
        dirpath = tkinter.filedialog.askdirectory()
        zp.extractall(dirpath)
        # 关闭压缩文件
        zp.close()
        tkinter.messagebox.showinfo(title='解压提示',message='解压成功'+dirpath)
compress_sotf = Compress_Soft()
