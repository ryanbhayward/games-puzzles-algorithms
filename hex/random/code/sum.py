# sum integers from stdin
import sys

sum = 0
for line in sys.stdin:
  list = map(int, line.split())
  for x in list:
    sum += x
print sum
