PYHEADER=/usr/include/python3.6

ifeq ($(OS),Windows_NT)
	DEL=del
else
	DEL=rm -rf
endif
