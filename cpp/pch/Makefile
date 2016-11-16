all: myprogram

myprogram: mysource.cc precompiled_myheader.h.pch precompiled_myheader.h
	clang++ -include precompiled_myheader.h -o myprogram mysource.cc -std=gnu++11

# http://clang.llvm.org/docs/UsersManual.html#id30
# The command in the doc below does not work.
# http://clang.llvm.org/docs/PCHInternals.html
precompiled_myheader.h precompiled_myheader.h.pch: myheader.h
	clang++ -x c++-header -o precompiled_myheader.h.pch -std=gnu++11 myheader.h
	touch precompiled_myheader.h

clean:
	rm -rf *.h.pch myprogram precompiled_*
