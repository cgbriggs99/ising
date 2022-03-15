include ./ising/src/defs.mk

all: docs
	$(MAKE) -C ./ising all

.PHONY:clean
clean:
	$(DEL) *.o *.so *~
	$(MAKE) -C ./ising clean

.PHONY:docs
docs:
	sphinx-build -b html docs/source docs/build/html
