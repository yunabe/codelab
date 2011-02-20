all: pyramid.html population.html

pyramid.html: calc.py
	python calc.py pyramid > pyramid.html || rm -f pyramid.html

population.html: calc.py
	python calc.py population > population.html || rm -f population.html

clean:
	rm -f *.html
