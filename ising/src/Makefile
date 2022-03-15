include defs.mk

CFLAGS+=-I $(PYHEADER) -pthread -Og -ggdb -g3 -fPIC
LDLIBS+=-lm -lpthread

.PHONY:all
all: fafb.so fafbmodule.o ising.o

.PHONY:clean
clean:
	$(DEL) *.o *.so

fafb.so: fafbmodule.o ising.o
	$(LD) -o fafb.so $^ -shared $(LDLIBS)
fafbmodule.o: ising.o

