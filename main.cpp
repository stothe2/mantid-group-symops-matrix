#include "SpaceGroupSymOps.h"

#include <iostream>
#include <sstream>

int main() {

	SpaceGroupSymOps p1bar;
	std::vector<std::vector<int>> v_bases = p1bar.transformSymOp(10, {1,1,0});
	std::vector<int> v_basis;

	for (auto it = v_bases.begin(); it < v_bases.end(); ++it) {
		v_basis = *it;
		for (int i = 0; i < 3; i++) {
			std::cout << v_basis[i] << std::endl;
		}
		std::cout << p1bar.getBasisVector(v_basis, "a") << std::endl;
	}
	
	return 0;
}