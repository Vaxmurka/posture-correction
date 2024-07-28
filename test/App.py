import cv2
import mediapipe as mp
import screen_brightness_control as sbc
import time
from PIL import Image, ImageStat
from detectFace import face
from customtkinter import *
import winreg
import subprocess
import sys
import threading

# --------------------------------- НАСТРОЙКИ -----------------------------------------
# Инициализация библиотек
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Инициализация объекта для обнаружения лиц
face_detection = mp_face_detection.FaceDetection()

# Захват видеопотока с камеры
cap = cv2.VideoCapture(0)

# Максимальное время препровождения за компьютером (в секундах)
MAX_time = 5
time_cam = 5


# set_appearance_mode('light')

app = CTk()
app.title("Осанка")
app.geometry('800x450')
app.resizable(False, False)

Setting1 = CTkFrame(master=app, width=580, height=215).place(x=5, y=5)
Setting2 = CTkFrame(master=app, width=200, height=215).place(x=590, y=5)
Settings3 = CTkFrame(master=app, width=790, height=220).place(x=5, y=225)
# -------------------------------------------------------------------------------------

# --------------------------------- ПЕРЕМЕННЫЕ ----------------------------------------
global timeStat
tmr = time.localtime(None).tm_sec
AppOpen = True
global getStartTime
Shape = 0

if get_appearance_mode() == 'Dark':
    mode_var = StringVar(value="on")
else:
    mode_var = StringVar(value="off")
read_var = StringVar(value="off")
read2_var = StringVar(value="on")
MAX_timePC = IntVar()
btn_var = StringVar(value="off")
MTPC = StringVar()
CAM = ["Основная"]
timePC = ["30 минут", "1 час", "1 час 30 минут", "2 часа"]
SettingArr = [0, 0, 0]

STATUS_PATH = "Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default$windows.data.bluelightreduction.bluelightreductionstate\\windows.data.bluelightreduction.bluelightreductionstate"
STATE_VALUE_NAME = "Data"

flagSwCAM = False
# -------------------------------------------------------------------------------------

# ----------------------------------- ФУНКЦИИ -----------------------------------------


def DopFunctions():
    SettingArr[0] = read2_var.get()
    SettingArr[1] = read_var.get()
    Chtenie()


def Chtenie():
    if SettingArr[0] == 'on':
        if SettingArr[1] == 'on':
            def get_night_light_state_data():
                try:
                    hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STATUS_PATH, 0, winreg.KEY_READ)
                    value, regtype = winreg.QueryValueEx(hKey, STATE_VALUE_NAME)
                    winreg.CloseKey(hKey)

                    if regtype == winreg.REG_BINARY:
                        return value
                except:
                    pass
                return False

            def process_night_light_state_data(byte_array):
                night_light_is_on = False
                ch = byte_array[18]
                size = len(byte_array)

                if ch == 0x15:
                    night_light_is_on = True
                    for i in range(10, 15):
                        ch = byte_array[i]
                        if ch != 0xff:
                            byte_array[i] += 1
                            break
                    byte_array[18] = 0x13
                    for i in range(24, 22, -1):
                        for j in range(i, size - 2):
                            byte_array[j] = byte_array[j + 1]
                elif ch == 0x13:
                    night_light_is_on = False
                    for i in range(10, 15):
                        ch = byte_array[i]
                        if ch != 0xff:
                            byte_array[i] += 1
                            break
                    byte_array[18] = 0x15
                    n = 0
                    while n < 2:
                        for j in range(size - 1, 23, -1):
                            byte_array[j] = byte_array[j - 1]
                        n += 1
                    byte_array[23] = 0x10
                    byte_array[24] = 0x00
                    # extend array
                    ba = bytearray(1)
                    ba[0] = 0x00
                    byte_array.extend(ba)
                    byte_array.extend(ba)
                return night_light_is_on

            def write_data_to_registry(byte_array, night_light_state):
                size = len(byte_array)
                retval = False
                try:
                    hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STATUS_PATH, 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(hKey, STATE_VALUE_NAME, 0, winreg.REG_BINARY, byte_array[:size])
                    winreg.CloseKey(hKey)
                    retval = True
                except:
                    pass
                return retval

            if __name__ == '__main__':

                night_light_is_on = False
                value = get_night_light_state_data()
                size = len(value)
                reg_val = bytearray(size)
                reg_val[:] = value
                if get_night_light_state_data():
                    night_light_new_settings = process_night_light_state_data(reg_val)
                    write_data_to_registry(reg_val, night_light_new_settings)
        else:
            def get_night_light_state_data():
                try:
                    hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STATUS_PATH, 0, winreg.KEY_READ)
                    value, regtype = winreg.QueryValueEx(hKey, STATE_VALUE_NAME)
                    winreg.CloseKey(hKey)

                    if regtype == winreg.REG_BINARY:
                        return value
                except:
                    pass
                return False

            def process_night_light_state_data(byte_array):
                night_light_is_on = False
                ch = byte_array[18]
                size = len(byte_array)

                if ch == 0x15:
                    night_light_is_on = True
                    for i in range(10, 15):
                        ch = byte_array[i]
                        if ch != 0xff:
                            byte_array[i] += 1
                            break
                    byte_array[18] = 0x13
                    for i in range(24, 22, -1):
                        for j in range(i, size - 2):
                            byte_array[j] = byte_array[j + 1]
                elif ch == 0x13:
                    night_light_is_on = False
                    for i in range(10, 15):
                        ch = byte_array[i]
                        if ch != 0xff:
                            byte_array[i] += 1
                            break
                    byte_array[18] = 0x15
                    n = 0
                    while n < 2:
                        for j in range(size - 1, 23, -1):
                            byte_array[j] = byte_array[j - 1]
                        n += 1
                    byte_array[23] = 0x10
                    byte_array[24] = 0x00
                    # extend array
                    ba = bytearray(1)
                    ba[0] = 0x00
                    byte_array.extend(ba)
                    byte_array.extend(ba)
                return night_light_is_on

            def write_data_to_registry(byte_array, night_light_state):
                size = len(byte_array)
                retval = False
                try:
                    hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STATUS_PATH, 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(hKey, STATE_VALUE_NAME, 0, winreg.REG_BINARY, byte_array[:size])
                    winreg.CloseKey(hKey)
                    retval = True
                except:
                    pass
                return retval

            if __name__ == '__main__':

                night_light_is_on = False
                value = get_night_light_state_data()
                size = len(value)
                reg_val = bytearray(size)
                reg_val[:] = value
                if get_night_light_state_data():
                    night_light_new_settings = process_night_light_state_data(reg_val)
                    write_data_to_registry(reg_val, night_light_new_settings)


def DopFunctions2():
    SettingArr[0] = read2_var.get()
    SettingArr[2] = mode_var.get()
    Tema()


def Tema():
    if SettingArr[0] == 'on':
        if SettingArr[2] == 'on':
            set_appearance_mode('dark')
            p = subprocess.Popen(["powershell.exe",
                                  "New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 0 -Type Dword -Force; New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 0 -Type Dword -Force"],
                                 stdout=sys.stdout)
            p.communicate()

        else:
            set_appearance_mode('light')
            p = subprocess.Popen(["powershell.exe",
                                  "New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 1 -Type Dword -Force; New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 1 -Type Dword -Force"],
                                 stdout=sys.stdout)
            p.communicate()


stop_threads = False


def statCAM():
    timeStat = 0
    getStartTime = True
    while True:
        # Чтение кадра
        ret, frame = cap.read()

        Shape, timeStat, breakFlag, valueCam, valueDisplay, timeWork, getStartTime = face(cap, face_detection, time,
                                                                                          cv2, Image, ImageStat, sbc,
                                                                                          AppOpen, MAX_time, time_cam,
                                                                                          timeStat, getStartTime)
        print(Shape, breakFlag, valueCam, valueDisplay, timeStat, timeWork, getStartTime)

        # global stop_threads
        # if stop_threads:
        #     break
        if btn_var.get() == "off":
            break

    # Освобождение ресурсов
    # cap.release()
    # cv2.destroyAllWindows()


def switchCAM():
    thread = threading.Thread(target=statCAM)
    if btn_var.get() == "on":
        # stop_threads = False
        thread.start()
    else:
        # stop_threads = True
        thread.join()


def set_brightness(value):
    sbc.set_brightness(value=value)
# -------------------------------------------------------------------------------------

# --------------------------------- ПАНЕЛЬ SETTING1 -----------------------------------
ltimePC = CTkLabel(master=Setting1, width=200, height=30, text='Максимальное время работы', font=('aria', 14, 'bold')).place(x=20, y=20)
timePC1 = CTkComboBox(master=Setting1, width=200, height=30, values=timePC).place(x=300, y=20)


ltimeCAM = CTkLabel(master=Setting1, width=200, height=30, text='Выбор камеры', font=('aria', 14, 'bold')).place(x=20, y=60)
timeCAM = CTkComboBox(master=Setting1, width=200, height=30, values=CAM).place(x=300, y=60)
lslider = CTkLabel(master=Setting1, width=200, height=30, text='Ручная настройка яркости', font=('aria', 14, 'bold')).place(x=20, y=100)
slider = CTkSlider(master=Setting1, width=200, height=20, from_=20, to=100, number_of_steps=40, command=set_brightness)
brightness = sbc.get_brightness()[0]
slider.set(brightness)
slider.place(x=300, y=100)

# -------------------------------------------------------------------------------------

# --------------------------------- ПАНЕЛЬ SETTING2 -----------------------------------
# switchL = CTkButton(master=Setting2, text='д/н', width=50, height=50, corner_radius=25).place(x=680, y=20)

switchL = CTkSwitch(master=Setting2, width=15, height=15, text='Темный режим', command=DopFunctions2, variable=mode_var,
                    onvalue='on', offvalue='off').place(x=600, y=20)
switchR = CTkSwitch(master=Setting2, width=15, height=15, text='Режим чтения', command=DopFunctions, variable=read_var,
                    onvalue='on', offvalue='off').place(x=600, y=50)
switchM = CTkSwitch(master=Setting2, width=15, height=15, text='Телефон / ПК',  variable=read2_var, onvalue='on',
                    offvalue='off').place(x=600, y=80)
button = CTkSwitch(master=Setting2, width=15, height=15, text="вкл./выкл. камера", variable=btn_var, onvalue='on',
                    offvalue='off', command=switchCAM).place(x=600, y=110)
# -------------------------------------------------------------------------------------


# --------------------------------- ПАНЕЛЬ SETTING3 -----------------------------------

# -------------------------------------------------------------------------------------

app.mainloop()
