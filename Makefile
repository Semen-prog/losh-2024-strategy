CC=gcc
CXX=g++
CFLAGS=-Wall -Wextra -Wshadow -O2 -march=native
CXXFLAGS=-std=gnu++20

CXX_VERSION := $(shell $(CXX) -dumpversion)
ifeq ($(shell expr $(CXX_VERSION) '<' 13), 1)
$(error You have to install at least g++ version 13 to build this project)
endif

BUILDDIR=$(CURDIR)/binaries

all: $(BUILDDIR)/interactor $(BUILDDIR)/validate $(BUILDDIR)/fieldgen

$(BUILDDIR)/interactor: sources/interactor.c | $(BUILDDIR)
	${CC} $< -o $@ ${CFLAGS}

$(BUILDDIR)/validate: sources/s_validate.cpp | $(BUILDDIR)
	${CXX} $< -o $@ ${CFLAGS} ${CXXFLAGS}

$(BUILDDIR)/fieldgen: sources/fieldgen.cpp | $(BUILDDIR)
	${CXX} $< -o $@ ${CFLAGS} ${CXXFLAGS}

$(BUILDDIR):
	mkdir $(BUILDDIR)
