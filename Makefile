default: clean
	python3 -m build

clean:
	rm -rf build dist src/simpleshell.egg-info

install:
	python3 -m pip install simpleshell

uninstall:
	python3 -m pip uninstall simpleshell

publish:
	python3 -m twine upload dist/*
