all: docs

.PHONY:clean
clean:
	rm -rf *.pyc *.pyo

.PHONY:docs
docs:
	sphinx-build -b html docs/source docs/build/html
