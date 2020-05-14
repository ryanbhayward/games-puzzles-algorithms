CC  = gcc -Wall -O3
PROG = display3
OBJ = $(PROG).o

$(PROG): $(OBJ)
	$(CC) -o  $(PROG) $(OBJ)

$(PROG).o: $(PROG).c 
	$(CC) -c  $(PROG).c

clean: 
	rm $(OBJ)
