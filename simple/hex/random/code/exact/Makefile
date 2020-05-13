CC  = gcc -Wall -O3
PROG = oddprob
OBJ = $(PROG).o

$(PROG): $(OBJ)
	$(CC) -o  $(PROG) $(OBJ)

$(PROG).o: $(PROG).c 
	$(CC) -c  $(PROG).c

clean: 
	rm $(OBJ)
