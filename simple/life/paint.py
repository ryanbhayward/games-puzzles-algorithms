# paint text characters

escape_ch = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')

def paint(s, chars):  # s   a string
  pt = ''
  for j in s:
    if j in chars:      pt += stonecolors[chars.find(j)] + j + colorend
    elif j.isalnum():   pt += textcolor + j + colorend
    else:               pt += j
  return pt
