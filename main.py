import json
import os
import pynput
import signal
import subprocess
import tkinter as tk
import webbrowser
from pyparsing import ParseException
from tkinter import filedialog, ttk
from ext.nsp import NumericStringParser as NSP

script_pid = None
toggle = False

with open('config.json', 'r') as f:
    config: dict = json.load(f)

current = set()

def on_press(key):
    combination = {pynput.keyboard.Key.ctrl, '\x03', 'c'}

    if key == pynput.keyboard.Key.f6:
        toggle_script()
    elif key in combination:
        current.add(key)
        if all(k in current for k in combination):
            listener.stop()
            raise KeyboardInterrupt

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

def web(url):
    webbrowser.open_new(url)

def highlight_text(event):
    note_label1.config(state=tk.NORMAL)
    note_label1.focus()
    note_label1.config(state=tk.DISABLED)

def tesseract_set():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select A File",filetype = (("exe","*.exe"),("All Files","*.*")))
    if filename:
        tesseract_loc.set(filename)

def toggle_script():
    global script_pid
    global toggle
    global toggle_button
    global tesseract_loc
    global delay_input
    global precision_input
    global config
    global fix_select
    global selected_version
    global input_select
    global window_select

    if not toggle:
        tesseract_loc.set(tesseract_entry.get())
        delay_input.set(delay_entry.get())
        precision_input.set(precision_entry.get())

        if not all((tesseract_loc.get(), delay_input.get(), precision_input.get(), fix_select.get(), selected_version.get(), input_select.get(), window_select.get())):
            tk.messagebox.showerror(title='Invalid', message='Satu atau lebih pilihan tidak dipilih')
            return False

        if fix_select.get() == 'm' or fix_select.get() == 'km':
            tk.messagebox.showwarning(title='Notice', message='Versi 2.2 tidak memadai fix untuk mouse')
            return False

        if not tesseract_loc.get():
            tk.messagebox.showerror(title='Invalid', message='Lokasi Tesseract tidak bisa kosong')
            return False

        if not tesseract_loc.get().lower().endswith('.exe'):
            tk.messagebox.showerror(title='Invalid', message='Lokasi Tesseract seharusnya memiliki akhiran \'.exe\'')
            return False

        try:
            delay_num = NSP().eval(delay_input.get())
        except ParseException:
            tk.messagebox.showerror(title='Invalid', message='Interval harus berupa integer, float, atau ekspresi matematika')
            return False

        if not delay_input.get():
            tk.messagebox.showerror(title='Invalid', message='Interval tidak bisa kosong')
            return False
            
        try:
            precision_input.get()
        except tk.TclError:
            tk.messagebox.showerror(title='Invalid', message='Precision harus berupa angka antara 1-100 atau tidak bisa kosong')
            return False
        
        if precision_input.get() < 1 or precision_input.get() > 100:
            tk.messagebox.showerror(title='Invalid', message='Precision harus berupa angka di antara 1-100')
            return False

        config['tesseract'] = tesseract_loc.get().replace('/', '\\')
        config['interval'] = delay_num
        config['precision'] = precision_input.get()
        config['fix'] = fix_select.get()
        config['version'] = selected_version.get()
        config['input'] = input_select.get()
        config['screen'] = window_select.get()

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        toggle = True
        toggle_button.config(text='...', state=tk.DISABLED)
        p = subprocess.Popen(['python', f'./script/{selected_version.get()}', fix_select.get(), input_select.get()])
        script_pid = p.pid
        toggle_button.config(text='Stop', state=tk.NORMAL)
    else:
        if script_pid:
            toggle = False
            toggle_button.config(text='...', state=tk.DISABLED)
            try:
                os.kill(script_pid, signal.SIGTERM)
                print('Script telah dihentikan')
            except ProcessLookupError:
                pass
            script_pid = None
            toggle_button.config(text='Mulai', state=tk.NORMAL)
        else:
            tk.messagebox.showerror(title='Unknown Error', message='Error tidak diketahui. script_pid berupa NoneType, tombol telah diubah ke False')
            toggle = False

window = tk.Tk()
s = ttk.Style(window)

try:
    s.theme_use('vista')
except Exception:
    pass

window.iconbitmap('img/sire icon.ico')
window.title('Auto Sell Mancing')
tk.Grid.columnconfigure(window, 0, weight=1)
tk.Grid.rowconfigure(window, 0, weight=1)

mainframe = tk.Frame(window)
mainframe.grid(column=0, row=0, sticky=tk.N+tk.W+tk.E+tk.S)

for row_index in range(14):
    tk.Grid.rowconfigure(mainframe, row_index, weight=1)
    for col_index in range(5):
        tk.Grid.columnconfigure(mainframe, col_index, weight=1)

ttk.Frame(mainframe).grid(row=3, column=1)

tesseract_label = ttk.Label(mainframe, compound=tk.RIGHT, text='Lokasi Tesseract')
tesseract_label.grid(row=1, column=1, sticky=tk.E)

tesseract_loc = tk.StringVar(value=config.get('tesseract', ''))

tesseract_entry = ttk.Entry(mainframe, width=50, textvariable=tesseract_loc)
tesseract_entry.grid(row=1, column=2, sticky=tk.W)


browse = ttk.Button(mainframe, text='Browse',width=15, command=lambda:tesseract_set())
browse.grid(row=1, column=3, sticky=tk.W)

delay_input = tk.StringVar(value=config.get('interval', '60*5'))

delay_label = ttk.Label(mainframe, text='Interval Auto Sell (dalam detik)')
delay_label.grid(row=2, column=1, sticky=tk.E)
delay_entry = ttk.Entry(mainframe, width=5, textvariable=delay_input)
delay_entry.grid(row=2, column=2, sticky=tk.W)

precision_input = tk.IntVar(value=config.get('precision', 80))

precision_label = ttk.Label(mainframe, text='Precision (ketepatan, 1-100)')
precision_label.grid(row=3, column=1, sticky=tk.E)
precision_entry = ttk.Entry(mainframe, width=5, textvariable=precision_input)
precision_entry.grid(row=3, column=2, sticky=tk.W)

ttk.Label(mainframe, text='').grid(row=4, column=2)

future_row1 = 5
available_fix = {
    'Keyboard': 'k',
    'Mouse': 'm',
    'Keyboard + Mouse': 'km',
    'None': 'n'
}

fix_select = tk.StringVar()

fix_label = ttk.Label(mainframe, text='Fix (untuk yang tidak work di script namum work di jitbit)')
fix_label.grid(row=5, column=2)

input_select = tk.StringVar()

input_types_label = ttk.Label(mainframe, text='Tipe input')
input_types_label.grid(row=5, column=3)

ttk.Radiobutton(mainframe, text='Default (pynput)', value='default', variable=input_select).grid(row=6, column=3)
ttk.Radiobutton(mainframe, text='DirectInput', value='directinput', variable=input_select).grid(row=7, column=3)

input_note = ttk.Label(mainframe, text='Note: setting ini tidak ada efek\njika fix keyboard digunakan')
input_note.grid(row=8, column=3)

input_select.set(config.get('input', 'directinput'))

window_select = tk.StringVar()

windows_types_label = ttk.Label(mainframe, text='Mode window')
windows_types_label.grid(row=5, column=4)

ttk.Radiobutton(mainframe, text='Fullscreen', value='full', variable=window_select).grid(row=6, column=4)
ttk.Radiobutton(mainframe, text='Window', value='window', variable=window_select).grid(row=7, column=4)

window_select.set(config.get('screen', 'window'))

ttk.Label(mainframe, text=' ').grid(row=1, column=5)

for k, v in available_fix.items():
    future_row1 += 1
    fix_entry = ttk.Radiobutton(mainframe, text=k, value=v, variable=fix_select)
    fix_entry.grid(row=future_row1, column=2)

fix_select.set(config.get('fix', 'n'))
future_row2 = 5

version_label = ttk.Label(mainframe, text='Versi script')
version_label.grid(row=5, column=1)

selected_version = tk.StringVar()
for x in os.listdir('script/'):
    if not x.endswith('.py'):
        continue
    future_row2 += 1
    version_entry = ttk.Radiobutton(mainframe, text=x[:-3], value=x, variable=selected_version)
    version_entry.grid(row=future_row2, column=1)

selected_version.set(config.get('version', '1.8.py'))

if future_row1 > future_row2:
    available_row = future_row1
else:
    available_row = future_row2

available_row += 1
ttk.Label(mainframe, text='').grid(row=available_row, column=2)

available_row +=1
toggle_button = ttk.Button(mainframe, text='Mulai', width=15, command=lambda:toggle_script())
toggle_button.grid(row=available_row, column=2, sticky=tk.N)
toggle_label = ttk.Label(mainframe, text='F6 shortcut untuk mulai/stop', foreground='green')
toggle_label.grid(row=available_row, column=3, sticky=tk.W)

available_row += 1
ttk.Label(mainframe, text='').grid(row=available_row, column=2)

available_row += 1
note_label1 = tk.Label(mainframe, text='Creator: K·#4963 (discord)\nUntuk minta bantuan/pertanyaan\nbisa langsung tanya di DM.')
note_label1.grid(row=available_row, column=1, sticky=tk.W)
note_label2 = ttk.Label(mainframe, text='')
note_label2.grid(row=available_row, column=2)
note_label3 = ttk.Label(mainframe, text='Script ini gratis dan tidak untuk diperjualbelikan.')
note_label3.grid(row=available_row, column=3, sticky=tk.E)

available_row += 1
ttk.Label(mainframe, text='Versi 2.2', foreground='green').grid(row=available_row, column=1, sticky=tk.W+tk.S)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=2, pady=5)

listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

window.mainloop()
