CXX = g++
CXXFLAGS = -c -std=c++0x #-stdlib=libc++ -pedantic -Wall -Wextra -g -O0

all: SpaceGroupSymOps

SpaceGroupSymOps: SpaceGroupSymOps.o main.o
	$(CXX) SpaceGroupSymOps.o main.o -o SpaceGroupSymOps

SpaceGroupSymOps.o: SpaceGroupSymOps.cpp
	$(CXX) $(CXXFLAGS) SpaceGroupSymOps.cpp

main.o: main.cpp
	$(CXX) $(CXXFLAGS) main.cpp

clean:
	rm -rf *.o SpaceGroupSymOps
