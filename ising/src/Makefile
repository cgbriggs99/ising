# Windows and linux removals.
include defs.mk

# Flags. We want fast. -fPIC is to make it work.
CFLAGS+=-I $(PYHEADER) -Ofast -fPIC
LDLIBS+=-lm -lpthread

.PHONY:all
all: fafb.so fafbmodule.o ising.o

.PHONY:clean
clean:
	$(DEL) -rf *.o *.so

fafb.so: fafbmodule.o ising.o
	$(LD) -o fafb.so $^ $(LDLIBS)

# Depends on ising.h so that if it changes, the program will need to be redone.
fafbmodule.o: fafbmodule.c ising.h

ising.o: ising.c ising.h

