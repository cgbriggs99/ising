# Get the differing Windows vs. Linux remove commands.
include ./ising/src/defs.mk

all:
	echo "Made all"

# Clean up the environment.
.PHONY:clean
clean:
	$(DEL) *.o *.so *~
	$(MAKE) -C ./ising clean

# Build the docs.
#.PHONY:docs
#docs:
#	sphinx-build -b html docs/source docs/build/html
