CC  = gcc -Wall -O3
#CC  = gcc -DNDEBUG

estwin: estwin.c
	$(CC) -o $@ $<

estwin.stack: estwin.stack.c
	$(CC) -o $@ $<

clean: 
	rm estwin estwin.stack
