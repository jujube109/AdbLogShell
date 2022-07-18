import tkinter as tk
from tkinter import messagebox


#port1=''

#run_shell=AdbShell()
class GuiGet:
    def __init__(self):
        self.__IPport = dict(ip=None,port=None)
        self.root_window = tk.Tk()
        self.root_window.title('ADB日志查看器')
        self.root_window.geometry('400x180')
        self.root_window.resizable(0, 0)
        # 创建input控件接收用户输入的端口号，并赋初始值
        port_initial = tk.IntVar()
        port_initial.set(62025)
        ip_initial=tk.StringVar()
        ip_initial.set("127.0.0.1")
        self.port_input = tk.Entry(self.root_window,textvariable =port_initial )
        self.port_input.grid(row=0, column=2, padx=10, pady=5,)
        self.ip_input = tk.Entry(self.root_window, textvariable=ip_initial)
        self.ip_input.grid(row=1, column=2, padx=10, pady=5, )


    # 内置验证方法，点击提交后触发，判断输入值是否为数字
    def chechk(self):
        self.__port = self.port_input.get()
        flag = self.__port.isdigit()

        if flag:
            messagebox.askokcancel ('提示', '提交成功')
            self.root_window.withdraw()
            self.root_window.quit()

        else:
            messagebox.showwarning('提示', "只能输入数字")
            self.port_input.delete(0, tk.END)
            return False
    def input_Ip_port(self):

        #创建label控件
        lable=tk.Label(self.root_window,text='端口号: ')
        #grid方法为通过网格的形式设置布局
        lable.grid(row=0, column=1, padx=10, pady=5)
        # 创建label控件
        Iplable = tk.Label(self.root_window, text='ip地址: ')
        # grid方法为通过网格的形式设置布局
        Iplable.grid(row=1, column=1, padx=10, pady=5)

        button=tk.Button(self.root_window,text="提交",width=10,command=self.chechk)
        button.grid(row=0, column=3, sticky="w", padx=10, pady=5)

        self.root_window.mainloop()
        self.__IPport["ip"]=self.ip_input.get()
        self.__IPport["port"] = self.port_input.get()
        return self.__IPport

    def close_window(self):
        messagebox.showwarning('提示', '连接失败，端口号错误或未找到')
        self.root_window.quit()




