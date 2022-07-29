import subprocess
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import re


# port1=''

# run_shell=AdbShell()
class GuiGet:

    def __init__(self, master):
        self.__pack_pid = None
        self.__select_text = None
        self.__address = None
        self.__connectFlag = False
        self.__IPport = dict(ip=None, port=None)
        self.root_window = master
        self.root_window.title('ADB日志查看器')
        self.root_window.geometry('400x180')
        self.root_window.resizable(0, 0)
        # 创建input控件接收用户输入的端口号，并赋初始值
        port_initial = tk.IntVar()
        port_initial.set(62025)
        ip_initial = tk.StringVar()
        ip_initial.set("127.0.0.1")
        self.port_input = tk.Entry(self.root_window, textvariable=port_initial)
        self.port_input.grid(row=0, column=2, padx=10, pady=5 )
        self.ip_input = tk.Entry(self.root_window, textvariable=ip_initial)
        self.ip_input.grid(row=1, column=2, padx=10, pady=5, )
        self.cbox = ttk.Combobox(self.root_window)
        self.comfir_button = tk.Button(self.root_window, text="提交", width=10)

    '''
     内置验证方法，点击提交后触发，判断输入值是否为数字
    def chechk(self):
        self.__port = self.port_input.get()
        flag = self.__port.isdigit()

        if flag:
            messagebox.askokcancel('提示', '提交成功')
            self.root_window.withdraw()
            self.root_window.quit()

        else:
            messagebox.showwarning('提示', "只能输入数字")
            self.port_input.delete(0, tk.END)
            return False

'''
    #adb connect链接成功后显示“连接成功”字样
    def show_pack(self):
        if self.__connectFlag:
            suceeStr = tk.StringVar()
            suceeStr.set("连接成功")
            resultLabel = tk.Label(self.root_window, textvariable=suceeStr, width=6,
                                   fg='red')
            resultLabel.grid(row=1, column=3, padx=20, pady=10)

        def show_packname(event):
            self.__select_text = self.cbox.get()
            if self.__select_text != "请选择":
                self.varLabel.set(self.__select_text)
                self.comfir_button.grid(row=3, column=3, sticky="w", padx=10, pady=5)
            else:
                self.varLabel.set(None)
                self.comfir_button.grid_forget()

        cmd = subprocess.Popen(f"adb -s {self.__address} shell pm list package -3", stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
        top_byte = cmd.communicate()
        top_str = str(top_byte)
        packlist = re.findall(":(.+?)\\\\", top_str)
        packlist.insert(0, "请选择")
        self.cbox.grid(row=2, column=2, padx=10, pady=5)
        packNamelable = tk.Label(self.root_window, text='请选择包名: ')
        packNamelable.grid(row=2, column=1, padx=10, pady=5)
        self.cbox['value'] = packlist
        self.cbox.current(0)
        self.varLabel = tk.StringVar()
        self.select_label = tk.Label(self.root_window, textvariable=self.varLabel, width=23, bg='lightblue', fg='red')
        self.select_label.grid(row=3, column=2, padx=20, pady=10)
        self.cbox.bind("<<ComboboxSelected>>", show_packname, add="+")

        def log_show(event):
            pid_str = f"adb -s {self.__address} shell top -n 1| grep {self.__select_text}"
            print(pid_str)
            find_pid_cmd = subprocess.Popen(pid_str, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE)
            top_byte = find_pid_cmd.communicate()
            top_str = str(top_byte)
            print(top_str)
            self.__pack_pid = top_str.split(" ")[1]
            print(self.__pack_pid)

            log_command = f"adb -s {self.__address} logcat --pid={self.__pack_pid}"
            print(log_command)
            if "None" in self.__pack_pid :
                messagebox.showinfo('提示', "找不到所选的包或软件包未运行")
                self.cbox.delete(0, tk.END)
            cmd_yjt_log = subprocess.Popen(log_command, stdout=subprocess.PIPE)
            # 只要日志命令没有终止，就循环打印出没行新增的日志信息
            try:
                while not cmd_yjt_log.poll():
                    line = cmd_yjt_log.stdout.readline()
                    if line:
                        formatted_line = str(line, encoding="utf-8")
                        print(formatted_line)
                    else:
                        break
            except  KeyboardInterrupt:
                exit(0)

        self.comfir_button.bind("<Button-1>", log_show)
        # self.cbox.current(0)

    def input_Ip_port(self):

        # 创建label控件
        lable = tk.Label(self.root_window, text='端口号: ')
        # grid方法为通过网格的形式设置布局
        lable.grid(row=0, column=1, padx=10, pady=5)
        # 创建label控件
        Iplable = tk.Label(self.root_window, text='ip地址: ')
        # grid方法为通过网格的形式设置布局
        Iplable.grid(row=1, column=1, padx=10, pady=5)

        # button.bind("<Button-1>",show_pack,add="+")

        # 将gui窗口获取到的端口号与adb命令拼接
        self.__IPport["ip"] = self.ip_input.get()
        self.__IPport["port"] = self.port_input.get()
        self.__address = self.__IPport["ip"] + ":" + self.__IPport["port"]

        def adb__connect_exece(event):
            connect_str = "adb connect " + self.__address
            try:
                cmd_connect = subprocess.getoutput(connect_str)
            except UnicodeDecodeError:
                self.root_window.close_window()
                exit(0)
            self.__connectFlag = "connected" in cmd_connect or "successfully" in cmd_connect

        button = tk.Button(self.root_window, text="连接", width=10, command=self.show_pack)
        button.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        button.bind("<Button-1>", adb__connect_exece, add="+")
        # self.root_window.mainloop()

    # def log_show(self):

    def close_window(self):
        messagebox.showwarning('提示', '连接失败，端口号错误或未找到')
        self.root_window.quit()


if __name__ == '__main__':
    master = tk.Tk()
    a = GuiGet(master)
    a.input_Ip_port()
    master.mainloop()
