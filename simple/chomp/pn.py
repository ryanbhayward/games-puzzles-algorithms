#http://code.activestate.com/recipes/218332-generator-for-integer-partitions/
#David Eppstein (author) 15 years, 5 months ago  # | flag
#Explanation. Maybe I should explain in a little more detail how this works. If you have a partition of n, you can reduce it to a partition of n-1 in a canonical way by subtracting one from the smallest item in the partition. E.g. 1+2+3 => 2+3, 2+4 => 1+4. This algorithm reverses the process: for each partition p of n-1, it finds the partitions of n that would be reduced to p by this process. Therefore, each partition of n is output exactly once, at the step when the partition of n-1 to which it reduces is considered.

def partitions(n):
	# base case of recursion: zero is the sum of the empty list
	if n == 0:
		yield []
		return
		
	# modify partitions of n-1 to form partitions of n
	for p in partitions(n-1):
		yield [1] + p
		if p and (len(p) < 2 or p[1] > p[0]):
			yield [p[0] + 1] + p[1:]

X = partitions(10)
for j in X:
  print(j)

