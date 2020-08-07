none:
	echo "No default make target."

rstslide-light:
	echo "Not implementated yet"

rstslide-full:
	if [ ! -e "resources/mini-mathjax/README.md" ]; then cd resources; git clone "https://github.com/electricbookworks/mini-mathjax"; fi
	if [ ! -e "resources/reveal.js/README.md" ]; then cd resources; git clone "https://github.com/hakimel/reveal.js.git"; fi

build:
	mkdir -p build
	test -e "resources/mini-mathjax/README.md" || exit 1
	( if [ ! -e resources/build/mathjax ]; then \
		mkdir -p build/mathjax; \
		cp -rp resources/mini-mathjax/build/extensions build/resources/mathjax/.; \
		cp -rp resources/mini-mathjax/build/jax build/resources/mathjax/.; \
		cp -rp resources/mini-mathjax/build/MathJax.js build/resources/mathjax/.; \
		cp -rp resources/mini-mathjax/build/LICENSE build/resources/mathjax/.; \
          fi \
	)
	test -e "resources/reveal.js/README.md" || exit 1
	( if [ ! -e  resources/build/reveal.js ]; then \
		cp -rp reveal.js build/resources/reveal.js; \
	  fi \
	)
	( if [ ! -e  build/resources/reveal-plugins ]; then \
		cp -rp resources/reveal-plugins build/resources/reveal-plugins; \
	  fi \
	)

clean:
	rm -rf build

autopep8:
	autopep8 --ignore=E501,E401,E402,W291,W293,W391,E265,E266,E226 --aggressive --in-place -r src/

