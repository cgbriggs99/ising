# Where to find Python headers.
ifeq ($(CONDA_PREFIX),)
	PYHEADER=/usr/include/python3.6
else
	PYHEADER=$(wildcard $(CONDA_PREFIX)/include/python3.*)
endif

# Set the command to delete things.
ifeq ($(OS),Windows_NT)
	DEL=del
else
	DEL=rm -rf
endif
