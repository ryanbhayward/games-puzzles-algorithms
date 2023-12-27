############## board cells      rbh 2024 ###############

class Cell: 
  e, b, w, io_ch = 0, 1, 2, '.*@'  # empty, black, white

  def ch_to_cell(ch):
    return Cell.io_ch.index(ch)

  def opponent(c): 
    return 3 - c

  def test():
    io_ch = Cell.io_ch
    for ch in io_ch:
      c = Cell.ch_to_cell(ch)
      print(ch, c, io_ch[c])
    print()
    for j in range(1,3):
      print(j, Cell.opponent(j))

Cell.test()
