# del vs. rm -rf
include ./src/defs.mk

all:
	$(MAKE) -C src all

# Clean the environment.
.PHONY:clean
clean:
	$(DEL) *.pyc *.pyo *.~ *.so
	$(MAKE) -C ./src clean


