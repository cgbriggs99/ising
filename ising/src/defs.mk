# Where to find Python headers.
ifeq ($(PYHEADER),)
	PYHEADER=/usr/include/python3.6
endif

# Set the command to delete things.
ifeq ($(OS),Windows_NT)
	DEL=del
else
	DEL=rm -rf
endif
