# Windows and linux removals.
include defs.mk

# Flags. We want fast. -fPIC is to make it work.
CFLAGS+=-I $(PYHEADER) -Ofast -fPIC
LDLIBS+=-lpthread

.PHONY:all
all: fafb.so fafbmodule.o ising.o

.PHONY:clean
clean:
	$(DEL) -rf *.o *.so

fafb.so: fafbmodule.o ising.o
ifeq ($(shell uname -s),Darwin)
	$(LD) -o fafb.so $^ $(LDLIBS) -lSystem
else
	$(LD) -o fafb.so $^ $(LDLIBS) -shared -lm
endif

# Depends on ising.h so that if it changes, the program will need to be redone.
fafbmodule.o: fafbmodule.c ising.h

ising.o: ising.c ising.h

