#!/usr/bin/env python3

import tkinter
import customtkinter
from PIL import Image, ImageTk
import os
import shutil
import threading
import winreg
noroot =False

if not os.path.exists('./config.txt'):
    conf = open('./config.txt', 'w')
    conf.write('0')
    conf.close()
    
config = open('./config.txt', "r")
configure = config.read()
config.close()
if (configure == "1"):
    
    path = r'SYSTEM\CurrentControlSet\Control\FileSystem'

    key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, path)
    data, regtype = winreg.QueryValueEx(key, 'LongPathsEnabled')
    winreg.CloseKey(key)
    if not (data == int('1')):
        try:
                key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, path, access=winreg.KEY_WRITE)
                winreg.SetValueEx(key, 'LongPathsEnabled', 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
        except:
            noroot = True
customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  

root_tk = customtkinter.CTk() 
root_tk.geometry("400x240")
root_tk.iconbitmap('./floorp.ico')
root_tk.resizable(0,0)
root_tk.title('Floorp-プロファイル移行')
image = Image.open("./folder.png")
bg_image = ImageTk.PhotoImage(image)
apd = os.getenv('APPDATA')
moving_dir = (apd + "/Ablaze/Floorp")
confirm_chk = False
error = False
default_chk = False
error_ro = ""
error_ro2 = ""
error_ro3 = ""
error_ro4 = ""
default_default_pro = 0
switch_var = tkinter.StringVar(value=configure)
try:
    with open(apd + '/Mozilla/Firefox/profiles.ini') as fin:
        for row, text in enumerate(fin, start=1):
            text = text.rstrip()
            if text == r'Default=1':
                default_pro = row + 1
                break
            
    with open(apd + '/Mozilla/Firefox/profiles.ini') as fin:
        for row, text in enumerate(fin, start=1):
            text = text.rstrip()
            if text == r'Name=default-default':
                default_default_pro = row + 3
                break
        else:
            error = True
except FileNotFoundError as chk_ro:
    err_ro = chk_ro
    error = True
except NameError as chk_ros:
    err_ro2 = chk_ros
    error = True

try:
    profile = open(apd + '/Mozilla/Firefox/profiles.ini')
    default_profiles = profile.read().splitlines()
    profile.close()
    i = (default_pro - 6)
    while i < default_pro:
        chk_prof = default_profiles[i]
        if 'Path' in chk_prof:
            prof_path = default_profiles[i]
        if 'IsRelative=' in chk_prof:
            prof_isrelative = default_profiles[i]
        if 'Name=' in chk_prof:
            if (default_profiles[i] == "Name=default"):
                default_chk = True
            prof_name = default_profiles[i]
        i += 1
    prof_list=['[Profile0]\n', prof_name + '\n', prof_isrelative + '\n', prof_path + '\n', 'Default=1\n\n', '[General]\n', 'Version=2']
    move_path = prof_path.replace("Path=Profiles/", "")
except FileNotFoundError as chk_ross:
    err_ro3 = chk_ross
    error = True
except NameError as chk_rosss:
    err_ro4 = chk_rosss
    error = True
    
if (default_chk):
        i = (default_default_pro - 6)
        while i < default_default_pro:
            chk_prof = default_profiles[i]
            if 'Path' in chk_prof:
                def_prof_path = default_profiles[i]
            if 'IsRelative=' in chk_prof:
                def_prof_isrelative = default_profiles[i]
            if 'Name=' in chk_prof:
                def_prof_name = default_profiles[i]
            i += 1
        prof_list = []
        prof_list = ['[Profile0]\n', def_prof_name + '\n', def_prof_isrelative + '\n', def_prof_path + '\n', 'Default=1\n\n', '[General]\n', 'Version=2']
        move_path = ""
        move_path = def_prof_path.replace("Path=Profiles/", "")


def error_msg():
    label_error = customtkinter.CTkLabel(master=root_tk, text="不明なエラーが発生しました。\n\n以下の項目を確認し、解決できない場合は開発者へご連絡ください。\n\n・プロファイル内部に長過ぎる名前のファイルはありませんか？\n\n・FloorpとFirefoxは終了しましたか？\n\n・別のプロセスでファイルを使用していませんか？\n\n・Floorpはインストールされていますか？", text_font=("", 10))
    label_error.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

def confirm_start():
    global confirm_chk
    label_yet.destroy()
    label_yetmsg.destroy()
    confirm_button.destroy()
    confirm_chk = True
    start()

def start():
    button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    images.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
    switch_reg.place(relx=0.42, rely=0.95, anchor=tkinter.CENTER)
    switch_reg.toggle(configure)
    
def button_function():
    label.destroy()
    images.destroy()
    button.destroy()
    label_warn.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    label_warnmsg.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    last_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    
def chk_copy():
    with open(apd + '/Mozilla/Firefox/Profiles/' + move_path + '/extension-preferences.json') as fis:
        if not 'floorp-system@floorp.ablaze.one' in fis.read():
            label_warn.destroy()
            label_warnmsg.destroy()
            last_button.destroy()
            label_nofloorp.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            nofloorp_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        else:
            label_warn.destroy()
            label_warnmsg.destroy()
            last_button.destroy()
            start_copy()
            
def copy_nofloorp():
    label_nofloorp.destroy()
    nofloorp_button.destroy()
    start_copy()
    
def start_copy():
    progressbar.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    label_copymsg.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    th = threading.Thread(target=copy)
    th.start()
    

def copy():
    if (confirm_chk):
        shutil.rmtree(moving_dir + '/Profiles/' + move_path)
    if not(os.path.exists(moving_dir)):
        os.makedirs(apd + '/Ablaze\Floorp\Profiles', exist_ok=True)
    f = open(moving_dir + '/profiles.ini', 'w')
    f.writelines(prof_list)
    f.close()
    try:
        shutil.copytree(apd + '/Mozilla/Firefox/Profiles/' + move_path, moving_dir + '/Profiles/' + move_path)
    except FileExistsError:
        print("すでにファイルが存在するようです。")
    except  Exception as e:
        es = e
        if (error_ro):
            es = (es + "\n" + error_ro)
        if (error_ro2):
            es = (es + "\n" + error_ro2)
        if (error_ro3):
            es = (es + "\n" + error_ro2)
        if (error_ro4):
            es = (es + "\n" + error_ro2)
        print(es)
        fs = open('./error.log', 'w')
        fs.write(str(es))
        fs.close()
        progressbar.destroy()
        label_copymsg.destroy()
        error_msg()
        return
    progressbar.set(100)
    end_copy()
    
def end_copy():
    label_copymsg.destroy()
    label_endmsg.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    end_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

def end_prog():
    root_tk.destroy()

def switch_event():
    if (switch_var.get() == "<_io.TextIOWrapper name='./config.txt' mode='r' encoding='cp932'>"):
        return
    else:
        confs = open('./config.txt', 'w')
        confs.write(switch_var.get())
        confs.close()
def noroot_msg():
    label_norootmsg.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    
#各種メッセージ、ボタン
switch_reg = customtkinter.CTkSwitch(master=root_tk, text="ファイル長のエラーを修正する(再起動が必要です。)", command=switch_event,
                                   variable= switch_var, onvalue="0", offvalue="1")
label_yet = customtkinter.CTkLabel(master=root_tk, text="警告！", text_font=("", 12), text_color=("red"))
label_yetmsg = customtkinter.CTkLabel(master=root_tk, text="すでにプロファイルが生成されているようです。\n\n続行した場合移行先のプロファイルは破棄されます。", text_font=("", 10))
confirm_button = customtkinter.CTkButton(master=root_tk, text="続行する", command=confirm_start)
label_nofloorp = customtkinter.CTkLabel(master=root_tk, text="これはFloorpのプロファイルではないようです。\n\n続行しますか？", text_font=("", 10))
nofloorp_button = customtkinter.CTkButton(master=root_tk, text="続行する", command=copy_nofloorp)
label_copymsg = customtkinter.CTkLabel(master=root_tk, text="コピーしています...", text_font=("", 10))
label_endmsg = customtkinter.CTkLabel(master=root_tk, text="終了しました。", text_font=("", 10))
label_norootmsg = customtkinter.CTkLabel(master=root_tk, text="現在ファイル長修正モードです。\n\n管理者権限でexeを実行してください。", text_font=("", 10))
label_warn = customtkinter.CTkLabel(master=root_tk, text="警告！", text_font=("", 12), text_color=("red"))
label_warnmsg = customtkinter.CTkLabel(master=root_tk, text="Floorp、Firefoxを終了してからご利用ください。\n\n\nこのプログラムによるプロファイルの破損、損失は保証されません。\n\nそれでもよろしい方は'実行する'を押してください。", text_font=("", 10))
last_button = customtkinter.CTkButton(master=root_tk, text="実行する", command=chk_copy)
button = customtkinter.CTkButton(master=root_tk, text="実行する", command=button_function)
label = customtkinter.CTkLabel(master=root_tk, text="プロファイル移行プログラム", text_font=("", 12))
images = tkinter.Label(master=root_tk, image=bg_image)
images['bg'] = root_tk['bg']
progressbar = customtkinter.CTkProgressBar(master=root_tk)
end_button = customtkinter.CTkButton(master=root_tk, text="終了する", command=end_prog)
if (noroot):
    noroot_msg()
else:
    if (error):
        error_msg()
    else:
        if os.path.exists(moving_dir + '/Profiles/' + move_path):
            label_yet.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
            label_yetmsg.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            confirm_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        else:
            start()

root_tk.mainloop()
