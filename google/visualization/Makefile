all: pyramid.html population.html ratio.html eligibility.html

pyramid.html: calc.py
	python calc.py pyramid > pyramid.html || rm -f pyramid.html

population.html: calc.py
	python calc.py population > population.html || rm -f population.html

ratio.html: calc.py
	python calc.py ratio > ratio.html || rm -f ratio.html

eligibility.html: calc.py
	python calc.py eligibility > eligibility.html || rm -f eligibility.html

clean:
	rm -f *.html
