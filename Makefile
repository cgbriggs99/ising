# Get the differing Windows vs. Linux remove commands.
include ./ising/src/defs.mk

# Clean up the environment.
.PHONY:clean
clean:
	$(DEL) *.o *.so *~ build
	$(MAKE) -C ./ising clean
	$(MAKE) -C ./docs clean

# Build the docs.
.PHONY:docs
docs:
	$(MAKE) -C source_docs html
