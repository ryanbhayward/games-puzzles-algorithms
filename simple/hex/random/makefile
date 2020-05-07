LATEX = latex
DVIPS = dvips -Ppdf -t letter
PPR = randomwin

pdf: 
	$(LATEX) $(PPR)
	$(DVIPS) -D 1000 $(PPR) -o
	ps2pdf $(PPR).ps
	cp $(PPR).pdf ~
	-@rm $(PPR).dvi $(PPR).aux $(PPR).log $(PPR).ps 

clean: 
	-@rm $(PPR).pdf
