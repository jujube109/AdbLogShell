import tkinter as tk
from tkinter import messagebox


#port1=''

#run_shell=AdbShell()
class get_port:
    def __init__(self):
        self.__port = None
        self.root_window = tk.Tk()
        self.root_window.title('test')
        self.root_window.geometry('400x180')
        self.root_window.resizable(0, 0)
        # 创建input控件接收用户输入的端口号，并赋初始值
        initial = tk.IntVar()
        initial.set(62025)
        self.input = tk.Entry(self.root_window,textvariable =initial )
        self.input.grid(row=0, column=2, padx=10, pady=5,)


    # 内置验证方法，点击提交后触发，判断输入值是否为数字
    def chechk(self):
        self.__port = self.input.get()
        flag = self.__port.isdigit()

        if flag:
            messagebox.askokcancel ('提示', '提交成功')
            self.root_window.withdraw()
            self.root_window.quit()

        else:
            messagebox.showwarning('提示', "只能输入数字")
            self.input.delete(0, tk.END)
            return False
    def input_key(self):

        #创建label控件
        lable=tk.Label(self.root_window,text='端口号: ')
        #grid方法为通过网格的形式设置布局
        lable.grid(row=0, column=1, padx=10, pady=5)

        button=tk.Button(self.root_window,text="提交",width=10,command=self.chechk)
        button.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        self.root_window.mainloop()
        return self.__port
    def close_window(self):
        messagebox.showwarning('提示', '连接失败，端口号错误或未找到')
        self.root_window.quit()
# if __name__ == '__main__':
#     a=get_port()
#     print(a.input_key())



