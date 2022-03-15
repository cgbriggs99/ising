include defs.mk
CFLAGS+=-I $(PYHEADER) -Ofast -fPIC
LDLIBS+=-lm -lpthread

.PHONY:all
all: fafb.so fafbmodule.o ising.o

.PHONY:clean
clean:
	$(DEL) -rf *.o *.so

fafb.so: fafbmodule.o ising.o
	$(LD) -o fafb.so $^ -shared $(LDLIBS)

fafbmodule.o: fafbmodule.c ising.h

ising.o: ising.c ising.h

