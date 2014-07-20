all: docs

docs: doc/source/conf.py
	scons README.md
	sphinx-apidoc -o doc/source modeled
	@ cd doc ; make html

debug:
	scons DEBUG=yes

clean:
	scons -c
	@ cd doc ; make clean

doc/source/conf.py:
	sphinx-quickstart
