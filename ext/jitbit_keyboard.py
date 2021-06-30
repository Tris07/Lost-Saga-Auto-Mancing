import os
import subprocess
import sys
import time
from pynput.keyboard import Controller, Key

arguments = sys.argv

inputs = []
inputs.append('DELAY : 500\n')

for x in arguments[1]:
    inputs.append(f'Keyboard : D{x} : KeyDown\n')
    inputs.append('DELAY : 50\n')
    inputs.append(f'Keyboard : D{x} : KeyUp\n')
    inputs.append('DELAY : 150\n')

inputs.extend([
    'Keyboard : Enter : KeyDown\n',
    'DELAY : 50\n',
    'Keyboard : Enter : KeyUp\n'
    ])

with open('macro/input.mcr', 'w+') as f:
    f.writelines(inputs)

subprocess.Popen(['macro\\input.mcr'], shell=True)

time.sleep(5)

keyboard = Controller()

with keyboard.pressed(Key.ctrl):
    keyboard.press('p')
    time.sleep(.2)
    keyboard.release('p')

time.sleep(2)

os.system('TASKKILL /F /IM MacroRecorder.exe')