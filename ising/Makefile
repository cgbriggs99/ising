# del vs. rm -rf
include ./src/defs.mk

all:
	# Build subprograms.
	$(MAKE) -C ./src all

# Clean the environment.
.PHONY:clean
clean:
	$(DEL) *.pyc *.pyo *.~
	$(MAKE) -C ./src clean


