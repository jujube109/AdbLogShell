import subprocess
from Gui import GuiGet


class AdbShell:
    def execute_cmd(self):
        # 实例化窗口创建类，输入要连接的adb设备端口号，代码例子中的以夜神为例62025
        gui = GuiGet()
        iplist = gui.input_Ip_port()
        print(iplist)
        address = iplist["ip"] + ":" + iplist["port"]
        # 将gui窗口获取到的端口号与adb命令拼接
        connect_str = "adb connect " + address
        print(connect_str)
        # 获取命令的输出结果
        try:
            cmd_connect = subprocess.getoutput(connect_str)
        except UnicodeDecodeError:
            gui.close_window()
            exit(0)
        # flag标志用于判断连接命令是否成功连接
        flag = "connected" in cmd_connect or "successfully" in cmd_connect

        '''
        可以通过遍历命令结果的stdout输出属性获取yjt包的进程的pid，注意获取到的stdout信息是byte流。需要再通过遍历stdout字符转换
        
        也可以直接使用communicate
        '''
        pack_pid = str()
        # 先判断flag是否为真，连接是否成功
        if flag:
            cmd = subprocess.Popen(f"adb -s {address} shell top -n 1| grep xx", stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
            top_byte = cmd.communicate()
            top_str = str(top_byte)
            pack_pid = top_str.split(" ")[1]
            print(pack_pid)
            # time.sleep(1)
            # for line in cmd_yjt.stdout:
            #     yjt_pid=line

        # flag为假直接关闭窗口退出程序
        else:
            gui.close_window()
            exit(0)
        # 再通过遍历stdout流

        # yjt_top_str=str()
        # for i in yjt_pid:
        #   yjt_top_str=yjt_top_str+chr(i)
        # yjt_pid=yjt_top_str.split(" ")[1]

        log_command = f"adb -s {address} logcat --pid={pack_pid}"
        # if yjt_pid:
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


if __name__ == '__main__':
    a = AdbShell()
    a.execute_cmd()
