pres:
	env/bin/ipython3 nbconvert presentation.ipynb --to slides --template output_toggle 

test:
	env/bin/nosetests

ipython:
	env/bin/ipython3 notebook

serve: reveal.js
	echo "browse to http://localhost:2000/presentation.slides.html"
	env/bin/python -m http.server 2000

env: reveal.js
	virtualenv --python=python3 env
	env/bin/pip install -r requirements.txt
	

reveal.js:
	git clone https://github.com/hakimel/reveal.js.git

clear:
	rm -rf env
	rm -rf reveal.js
