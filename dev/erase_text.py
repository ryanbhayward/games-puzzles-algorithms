from time import sleep

text = 'erase this message'

def pause():
  sleep(.2)

def erase(k):
  for j in range(k):
    print('\b', end='', flush=True)
    pause()
    print(' ', end='', flush=True)
    pause()
    print('\b', end='', flush=True)
    pause()

print(text, end='', flush=True)
sleep(1)
erase(3)
pause()
print('y mess')
