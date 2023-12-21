# countdown.py

from time import sleep

def flush_print(text):
    print(text, end='  ', flush=True)

def erase():
    print('\b \b\b ', end='', flush=True)

print('\n')
flush_print('    ')

for j in range(3):
    flush_print(j)
    sleep(1)

for __ in range(9):
    erase()
    sleep(1)

for __ in range(3):
    flush_print(' ')
    sleep(1)

flush_print('     ')
sleep(1)
print('\b\b\b\b\b boom \n')
