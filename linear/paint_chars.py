# display some characters in color

class Paint:
  esc       = '\033[' 
  endcolor  =  esc + '0m'
  textcolor =  esc + '0;37m'
  color_of  = (esc + '0;35m', esc + '0;32m', esc + '0;34m')
  
############ colored output ######################

def paint(s, chars):  # replace with colored characters
  p = ''
  for c in s:
    x = chars.find(c)
    if x >= 0 and x < 2:
      p += Paint.color_of[x] + c + Paint.endcolor
    elif x >= 0 or c.isalnum():
      p += Paint.textcolor + c + Paint.endcolor
    else: p += c
  return p

def paint3(s, chars):  # replace with colored characters
  p = ''
  for c in s:
    x = chars.find(c)
    if x >= 0 and x < 3:
      p += Paint.color_of[x] + c + Paint.endcolor
    elif x >= 0 or c.isalnum():
      p += Paint.textcolor + c + Paint.endcolor
    else: p += c
  return p
