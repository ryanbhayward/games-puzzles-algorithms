CC  = gcc -Wall -O3
#CC  = gcc -DNDEBUG
PROG = cellminl
OBJ = $(PROG).o board.hex.o 

$(PROG): $(OBJ)
	$(CC) -o  $(PROG) $(OBJ)

$(PROG).o: $(PROG).c board.hex.h
	$(CC) -c  $(PROG).c

board.hex.o: board.hex.h board.hex.c
	$(CC) -c board.hex.c

clean: 
	rm $(OBJ)

cleanup: 
	rm $(OBJ) 
	rm $(PROG) 

tst: tst.c
	$(CC) -o $@ $<

estwin: estwin.c
	$(CC) -o $@ $<
