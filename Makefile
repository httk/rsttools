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
	autopep8 --ignore=E501,E401,E402,W391,E265,E266,E226 --aggressive --in-place -r src/

tests: unittests2 unittests3

unittests:
	(cd tests; TEST_EXPECT_PYVER=ignore python all.py)

unittests2: link_python2
	echo "Running unittests with Python 2"
        # Avoid mkdir -p in case this is run not in the right directory.
	(cd tests; TEST_EXPECT_PYVER=2 PATH="$$(pwd -P)/python_versions/ver2:$$PATH" python all.py)

unittests3: link_python3
	echo "Running unittests with Python 3"
	(cd tests; TEST_EXPECT_PYVER=3 PATH="$$(pwd -P)/python_versions/ver3:$$PATH" python all.py)

pytest:
	(cd tests; TEST_EXPECT_PYVER=ignore py.test)

pytest2: link_python2
	echo "Running pytest with Python 2"
	(cd tests; TEST_EXPECT_PYVER=2 PATH="$$(pwd -P)/python_versions/ver2:$$PATH" py.test)

pytest3: link_python3
	echo "Running pytest with Python 3"
	(cd tests; TEST_EXPECT_PYVER=3 PATH="$$(pwd -P)/python_versions/ver3:$$PATH" py.test-3)

link_python2:
	if [ ! -e tests/python_versions ]; then mkdir tests/python_versions; fi
	if [ ! -e tests/python_versions/ver2 ]; then mkdir tests/python_versions/ver2; fi
	if [ ! -e tests/python_versions/ver2/python ]; then ln -sf /usr/bin/python2 tests/python_versions/ver2/python; fi

link_python3:
	if [ ! -e tests/python_versions ]; then mkdir tests/python_versions; fi
	if [ ! -e tests/python_versions/ver3 ]; then mkdir tests/python_versions/ver3; fi
	if [ ! -e tests/python_versions/ver3/python ]; then ln -sf /usr/bin/python3 tests/python_versions/ver3/python; fi

relink_python:
	rm -f tests/python_versions/ver2/python
	rmdir tests/python_versions/ver2
	rm -f tests/python_versions/ver3/python
	rmdir tests/python_versions/ver3

release:
	( \
		echo "Present release: $$(git describe --always)"; \
		echo "Enter new tag:"; \
		read tag; \
		echo "$$tag" | awk '{printf("__version__ = '"'%s'"'\n",$$0)}' > src/rstslide/_version.py; \
		git add src/rstslide/_version.py; \
		git commit -m "Release $$tag"; \
		git tag -s "$$tag" -m "Release $$tag"; \
		git push -u origin "$$tag"; \
	)

