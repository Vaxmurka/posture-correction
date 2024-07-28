import cv2
import mediapipe as mp
import time
from PIL import Image, ImageStat
import screen_brightness_control as sbc
from customtkinter import *
import pyautogui
import winreg
import ctypes
import subprocess
import sys

# --------------------------------- НАСТРОЙКИ -----------------------------------------
# Инициализация библиотек
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Инициализация объекта для обнаружения лиц
face_detection = mp_face_detection.FaceDetection()

# Захват видеопотока с камеры
cap = cv2.VideoCapture(0)

Shape = 0
# cap.set(3, 640)   # Ширина
# cap.set(4, 480)   # Высота
# cap.set(10, 100)  # Яркость

# Максимальное время препровождения за компьютером (в секундах)
MAX_time = 0
time_cam = 5
tmr = time.localtime(None).tm_sec

set_appearance_mode('light')

app = CTk()
app.title("Осанка")
app.geometry('800x450')
app.resizable(False, False)
# -------------------------------------------------------------------------------------

# --------------------------------- ПЕРЕМЕННЫЕ ----------------------------------------
# FPS time
pTime, cTime = 0, 0
# Переменная, отвечающая за наличие человека (есть - True, нет - False)
Is_face = False
timeStat, timeFinal, timeWork = 0, 0, 0
f_stat = True
f_final = False
AppOpen = True

mode_var = StringVar(value="off")
read_var = StringVar(value="off")
read2_var = StringVar(value="off")
MAX_timePC = IntVar()
MTPC = StringVar()
CAM = ["Основная"]
timePC = ["30 минут", "1 час", "1 час 30 минут", "2 часа"]
SettingArr= [0, 0, 0]


STATUS_PATH = "Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default$windows.data.bluelightreduction.bluelightreductionstate\\windows.data.bluelightreduction.bluelightreductionstate"
STATE_VALUE_NAME = "Data"

command1 = "Write-Host 'New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 1 -Type Dword -Force; New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 1 -Type Dword -Force'"
command2 = "Write-Host 'New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 0 -Type Dword -Force; New-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 0 -Type Dword -Force'"

# -------------------------------------------------------------------------------------

Setting1 = CTkFrame(master=app, width=630, height=215).place(x=5, y=5)
Setting2 = CTkFrame(master=app, width=150, height=215).place(x=640, y=5)
Settings3 = CTkFrame(master=app, width=790, height=220).place(x=5, y=225)

# ----------------------------------- ФУНКЦИИ -----------------------------------------


def DopFunctions():
    SettingArr[0] = read2_var.get()
    SettingArr[1] = read_var.get()
    Chtenie()

def DopFunctions2():
    SettingArr[0] = read2_var.get()
    SettingArr[2] = mode_var.get()
    Tema()
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

###
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
###

def contrast(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.imwrite('cam.png', image)
    screen = Image.open('cam.png').convert('L')
    screen = ImageStat.Stat(screen)

    valueCam = int(screen.rms[0])
    valueDisplay = sbc.get_brightness()[0]

    if valueCam < 25: valueCam = 10
    elif 25 <= valueCam < 51: valueCam = 20
    elif 51 <= valueCam < 76: valueCam = 30
    elif 76 <= valueCam < 102: valueCam = 40
    elif 102 <= valueCam < 127: valueCam = 50
    elif 127 <= valueCam < 153: valueCam = 60
    elif 153 <= valueCam < 178: valueCam = 70
    elif 178 <= valueCam < 204: valueCam = 80
    elif 204 <= valueCam < 229: valueCam = 90
    elif valueCam >= 229: valueCam = 100


    return valueCam, valueDisplay


def face(Shape, MAX_time, time_cam, tmr, pTime, cTime, Is_face, timeStat, timeFinal, timeWork, f_stat, f_final):
    while cap.isOpened():
        # Чтение кадра
        ret, frame = cap.read()
        if not ret:
            break

        # Преобразование кадра в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Обнаружение лиц с помощью Mediapipe
        results = face_detection.process(frame)

        if results.detections:
            Is_face = True  # Человек появился
            if f_stat:
                timeStat = time.localtime(None).tm_sec
                f_stat = False
                f_final = True
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)

                # Отрисовка рамки вокруг обнаруженного лица
                cv2.rectangle(frame, bbox, (255, 0, 255), 2)

                # Определение расстояния от экрана до глаз(очень сильно округленная площадь прямоугольника)
                Shape = (bboxC.width * iw) * int(bboxC.height * ih)
                print(int(Shape) // 1000)
        else:
            Is_face = False  # Человек пропал
            if f_final:
                timeFinal = time.localtime(None).tm_sec
                f_final = False
                f_stat = True

        timeWork = time.localtime(None).tm_sec - timeStat
        if timeWork >= 0: pass  # print(time.localtime(None).tm_sec - timeStat)
        if timeWork > MAX_time: print('stop')

        if Is_face:
            if time.localtime(None).tm_sec - tmr >= time_cam:
                valueCam, valueDisplay = contrast(frame)
                # print(valueCam, valueDisplay)
                tmr = time.localtime(None).tm_sec

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)  # ФреймРейт

        # Отображение кадра
        cv2.imshow('Face Detection', frame)

        # Выход из цикла по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождение ресурсов
    cap.release()
    cv2.destroyAllWindows()


def statCAM():
    face(Shape, MAX_time, time_cam, tmr, pTime, cTime, Is_face, timeStat, timeFinal, timeWork, f_stat, f_final)
# -------------------------------------------------------------------------------------

# --------------------------------- ПАНЕЛЬ SETTING1 -----------------------------------
ltimePC = CTkLabel(master=Setting1, textvariable=MTPC ,width=200, height=30, text='Максимальное время работы', font=('aria', 14, 'bold')).place(x=20, y=20)
timePC1 = CTkComboBox(master=Setting1, width=200, height=30, values=timePC).place(x=300, y=20)


ltimeCAM = CTkLabel(master=Setting1, width=200, height=30, text='Выбор камеры', font=('aria', 14, 'bold')).place(x=20, y=60)
timeCAM = CTkComboBox(master=Setting1, width=200, height=30, values=CAM).place(x=300, y=60)

# -------------------------------------------------------------------------------------

# --------------------------------- ПАНЕЛЬ SETTING2 -----------------------------------
# switchL = CTkButton(master=Setting2, text='д/н', width=50, height=50, corner_radius=25).place(x=680, y=20)

switchL = CTkSwitch(master=Setting2, width=15, height=15, text='Темный режим', command=DopFunctions2, variable=mode_var, onvalue='on', offvalue='off').place(x=650, y=20)
switchR = CTkSwitch(master=Setting2, width=15, height=15, text='Режим чтения', command=DopFunctions, variable=read_var, onvalue='on', offvalue='off').place(x=650, y=50)
switchM = CTkSwitch(master=Setting2, width=15, height=15, text='Телефон / ПК',  variable=read2_var, onvalue='on', offvalue='off').place(x=650, y=80)
button = CTkButton(master=Setting2, width=100, height=50, text="вкл./выкл. камера", command=statCAM).place(x=650, y=110)

# -------------------------------------------------------------------------------------


# --------------------------------- ПАНЕЛЬ SETTING3 -----------------------------------

# -------------------------------------------------------------------------------------

app.mainloop()