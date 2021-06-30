import cv2
import json
import pytesseract
import screen_search
import subprocess
import sys
import time
from pynput.keyboard import Key, Controller
import win32api, win32con, win32gui
from PIL import Image, ImageGrab

print('Program telah dijalankan\nVersi 1.6.1\n--------------')

with open('config.json', 'r') as f:
    config = json.load(f)

tesseract_loc = config['tesseract']
interval = config['interval']
precision = config['precision']

precision = precision / 100

arguments = sys.argv

pytesseract.pytesseract.tesseract_cmd = tesseract_loc

keyboard = Controller()

previous_loc = None
already_run = False

skip_delay = False

def click(x,y):
    x = x + 10
    y = y + 12
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def cari_tombol_jual():
    search = screen_search.Search('img/sell_button.png', precision=precision)

    pos = search.imagesearch()

    if pos[0] != -1:
        print(pos[0], pos[1], '- Tombol jual hasil pancing')
        return (pos[0], pos[1])
    else:
        print('tombol "Jual Hasil Pancing" tidak ditemukan, mencoba lagi...')
        return False

def cari_tombol_jual_auto():
    search = screen_search.Search('img/auto_sell_button.png', precision=precision)

    pos = search.imagesearch()

    if pos[0] != -1:
        global previous_loc
        previous_loc = (pos[0], pos[1])
        print(pos[0], pos[1], '- Tombol jual otomatis')
        return (pos[0], pos[1])
    else:
        print('tombol "Sell Otomatis" tidak ditemukan, mencoba lagi...')
        return False

def klik_tombol_jual():
    position = cari_tombol_jual()
    if position:
        click(*position)
        return True
    else:
        return False

def tutup_window_jual():
    search = screen_search.Search('img/cancel1.png', precision=precision)
    
    pos = search.imagesearch()

    if pos[0] != -1:
        print(pos[0], pos[1], '- Tutup window jual (batal)')
        click(pos[0], pos[1])
        return False

    search = screen_search.Search('img/cancel2.png', precision=precision)

    pos = search.imagesearch()

    if pos[0] != -1:
        print(pos[0], pos[1], '- Tutup window jual (tutup)')
        click(pos[0], pos[1])
        return False

    return True
    
def check_item():
    search = screen_search.Search('img/no_item.png', precision=precision)

    pos = search.imagesearch()

    if pos[0] != -1:
        wildcard_close()
        return True
    
    return False

def wildcard_close():
    search = screen_search.Search('img/cancel3.png', precision=precision)

    pos = search.imagesearch()

    if pos[0] != -1:
        print(pos[0], pos[1], '- Wildcard X')
        click(pos[0], pos[1])
        return False

    return True

def close_all_wildcard():
    while True:
        search = screen_search.Search('img/mtk_window.png', precision=precision)

        pos = search.imagesearch()

        if pos[0] != -1:
            wildcard_close()
        else:
            break

def check_succeed():
    search = screen_search.Search('img/accept_button.png', precision=precision)

    pos = search.imagesearch()

    if pos[0] != -1:
        print(pos[0], pos[1], '- Gagal MTK')
        click(pos[0], pos[1])
        return False
    
    return True

def cleanup_screen():
    a = False
    b = False
    c = False
    d = False
    e = False
    f = False
    g = False
    h = False
    time.sleep(1)
    search = screen_search.Search('img/retrieve_quest_button.png', precision=precision)

    pos = search.imagesearch()
    
    if pos[0] != -1:
        print(pos[0], pos[1], '- Quest selesai (event)')
        click(pos[0], pos[1])
    else:
        b = True

    time.sleep(.75)

    search = screen_search.Search('img/accept_quest_button.png', precision=precision)

    pos = search.imagesearch()
    
    if pos[0] != -1:
        print(pos[0], pos[1], '- Terima quest (event)')
        click(pos[0], pos[1])
    else:
        c = True

    time.sleep(.75)

    search = screen_search.Search('img/accept_quest_button2.png', precision=precision)

    pos = search.imagesearch()
    
    if pos[0] != -1:
        print(pos[0], pos[1], '- Selesai quest (default)')
        click(pos[0], pos[1])
    else:
        d = True

    time.sleep(.75)

    search = screen_search.Search('img/accept_button.png', precision=precision)

    pos = search.imagesearch()
    
    if pos[0] != -1:
        print(pos[0], pos[1], '- Terima quest (default)')
        click(pos[0], pos[1])
    else:
        e = True
    
    time.sleep(.75)

    search = screen_search.Search('img/unique_close.png', precision=precision)

    pos = search.imagesearch()
    
    if pos[0] != -1:
        print(pos[0], pos[1], '- Wildcard X (pink)')
        click(pos[0], pos[1])
    else:
        f = True
    
    time.sleep(.75)

    search = screen_search.Search('img/close_button.png', precision=precision)

    pos = search.imagesearch()
    
    if pos[0] != -1:
        print(pos[0], pos[1], '- Wildcard X (default)')
        click(pos[0], pos[1])
    else:
        g = True
    
    time.sleep(.75)

    a = tutup_window_jual()
    h = wildcard_close()
    print((a, b, c, d, e, f, g, h))
    return (a, b, c, d, e, f, g, h)

def crop_center(img, w, h):
    im_w, im_h = img.size
    return img.crop(((im_w - w) // 2,
                         (im_h - h) // 2,
                         (im_w + w) // 2,
                         (im_h + h) // 2))

def get_win_ss():
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    lso = [(hwnd, title) for hwnd, title in winlist if 'lost saga in time' in title.lower()]
    lso = lso[0]
    hwnd = lso[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    if img:
        return img
    else:
        return False

def ocr():
    img = cv2.imread("img/text.png")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                     cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cropped = im2[y:y + h, x:x + w]

        text = pytesseract.image_to_string(cropped, config='-c tessedit_char_whitelist=0123456789+- --psm 6 digits')

    return text
# print('Jangan lupa juga untuk join discord gblso (discord.link/gblso) jika belum join\nUntuk minta bantuan tentang script juga bisa ditanyakan disana\n-------------')
def ocr_check(result):
    global already_run
    result = result
    while True:
        filtered = result.split('+')
        try:
            num1 = filtered[0]
            int(num1)
            num2 = filtered[1]
            int(num2)
        except (ValueError, IndexError):
            print('OCR gagal mengindentifikasi seluruh nomor, mencoba ulang')

            if not already_run:
                res = ocr_retry()
                result = res
                if isinstance(result, bool):
                    return result
                continue
            else:
                return False

        if len(num1) >= 3:
            num1 = num1[2]
            return (num1, num2)
        else:
            return (num1, num2)

def ocr_retry():
    global already_run
    global skip_delay
    already_run = True
    while True:
        search = screen_search.Search('img/mtk_window.png', precision=precision)
        pos = search.imagesearch()
        if pos[0] == -1:
            print('Window mtk gagal muncul, memulai ulang dari awal')
            skip_delay = True
            break
        
        wildcard_close()
        time.sleep(2)
        click(previous_loc[0], previous_loc[1])
        time.sleep(2)
        step_2()
        result = ocr()
        print(result)
        if result:
            already_run = False
            break
        time.sleep(.3)

    if skip_delay:
        return False
    return result

def type_and_enter(text):
    if arguments[1] == 'k' or arguments[1] == 'km':
        subprocess.Popen(['python', './ext/jitbit_keyboard.py', str(text)])
        return
    keyboard.type(str(text))
    time.sleep(.2)
    keyboard.press(Key.enter)
    time.sleep(.2)
    keyboard.release(Key.enter)

def press_key(key):
    keyboard.press(key)
    time.sleep(.2)
    keyboard.release(key)

def step_1():
    """ Klik tombol jual, lalu klik tombol jual auto
        Kalo tidak muncul, coba tutup, dan pencet tombol juat lagi
        Kadang tidak muncul karena tombol juat otomatis di blok oleh elemen lain
    """
    print('step 1')
    while True:
        result = klik_tombol_jual()
        if result:
            time.sleep(1.5)
            res = check_item()
            if res is True:
                return False
            position = cari_tombol_jual_auto()
            if position:
                click(*position)
                break

        time.sleep(1)
        while True:
            res = cleanup_screen()
            if all(res):
                break
        time.sleep(2)

    return True

def step_2():
    """ Seteleah mtk muncul, ambil layar lalu crop bagian pentingnya saja dan save
    """
    print('step 2')
    while True:
        im = get_win_ss()
        if im:
            break
        time.sleep(1)

    im = crop_center(im, 250, 177)
    im = im.crop((33, 70, 41+33, 15+70))
    w, h = im.size
    im = im.resize((w*5, h*5), resample=Image.LANCZOS)
    im.save('img/text.png')

def step_3():
    """ Setelah file di save, dimasukkan kedalam ocr lalu di filter
        Jika ocr gagal, maka ulang supaya dapet nomor baru
        Lalu input mtk
    """
    print('step 3')
    result = ocr()
    print(result)

    ans = ocr_check(result)
    if isinstance(ans, bool):
        return ans

    ans = sum(tuple(map(int, ans)))
    type_and_enter(ans)
    res = check_succeed()
    return res

def step_3_retry():
    print('step 3 retry')
    global skip_delay
    while True:
        res = cleanup_screen()
        if not all(res):
            continue

        search = screen_search.Search('img/fish_button.png', precision=precision)

        pos = search.imagesearch()

        if pos[0] != -1:
            print(pos[0], pos[1], '- Tombol mancing')
            click(pos[0], pos[1])

        time.sleep(.5)

        skip_delay = False

        time.sleep(2)

        while True:
            res = cleanup_screen()
            if all(res):
                break

        result = step_1()

        if result is False:
            print('Tidak ada item untuk dijual, selesai')
            return True

        time.sleep(2) # tunggu window mtk muncul

        step_2()

        res = step_3()
        if res is False and skip_delay:
            continue

        if res is False:
            while True:
                res = step_3_retry()
                if res:
                    break
                time.sleep(1)
                
        if skip_delay == True:
            continue

        return True

while True:
    if not skip_delay:
        time.sleep(interval) # tunggu setiap 5 menit untuk jual otomatis
    skip_delay = False

    print('Script akan dimulai, harap fokuskan window ke lost saga dan diamkan mouse hingga selesai')
    time.sleep(5)

    while True:
        res = cleanup_screen()
        if all(res):
            break

    result = step_1()

    if result is False:
        print('Tidak ada item untuk dijual, selesai')
        continue

    time.sleep(2) # tunggu window mtk muncul

    step_2()

    res = step_3()
    if res is False and skip_delay:
        continue

    if res is False:
        while True:
            res = step_3_retry()
            if res:
                break
            time.sleep(1)

    if skip_delay == True:
        continue

    print('Selesai')
