# Windows and linux removals.
include defs.mk

all: test_ising

test_ising: test_ising.c ising.c
test_ising: CFLAGS+=-I $(PYHEADER) -g3 -ggdb -Og -lm -lpthread -DNO_PYTHON

.PHONY:clean
clean:
	$(DEL) -rf *.o *.so test_ising
