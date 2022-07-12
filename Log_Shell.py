import subprocess

from  main import  AdbShell


connect_str="adb connect 127.0.0.1:62025"
cmd_connect=subprocess.getoutput(connect_str)
cmd_yjt = subprocess.Popen("adb -s 127.0.0.1:62025 shell top -n 1 | grep yjt",
                           stdout=subprocess.PIPE)


out=cmd_yjt.communicate()
print(out)
str_out=str(out)
print(str_out,type(str_out))
#yjt_pid=bytes()
# for line in out:
#      print(line,type(line))
#      a=line
# print(a)
# b=str()
# for i in str_out:
#     b=b+chr(i)
c= str_out.split(" ")[1]

print(c)
#print(out,type(out))


