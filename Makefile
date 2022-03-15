all: docs
	$(MAKE) -C ./ising all

.PHONY:docs
docs:
	sphinx-build -b html docs/source docs/build/html
