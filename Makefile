build: clean
	python3 -m build

clean:
	rm -rf build dist src/simpleshell.egg-info

install:
	python3 -m pip install dist/simpleshell-*-py3-none-any.whl

uninstall:
	python3 -m pip uninstall simpleshell

reinstall: clean build uninstall install

publish: clean build
	python3 -m twine upload dist/*
