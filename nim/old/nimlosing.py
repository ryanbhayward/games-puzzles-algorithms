from operator import xor

count = 0
for a in range(3):
  for b in range(3):
    for c in range(3):
      for d in range(3):
        for e in range(3):
          for f in range(3):
            if 0 == a^b^c^d^e^f:
              count += 1
print(count)
