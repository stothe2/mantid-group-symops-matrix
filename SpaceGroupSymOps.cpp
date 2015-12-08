#include "SpaceGroupSymOps.h"
#include <iostream>

SpaceGroupSymOps::SpaceGroupSymOps() {}

// Returns a vector of all symmetry operations in matrix form that
// correspond to the given space group number.
std::vector<intMatrix>
SpaceGroupSymOps::getGeneratorMatrices(size_t number) const {
	std::vector<intMatrix> m_generators;

	auto keyPair = m_sg.equal_range(number);

	for (auto it = keyPair.first; it != keyPair.second; ++it) {
		m_generators.push_back(it->second);
	}

	return m_generators;
}

// Returns a vector of all translation columns of the symmetry
// operations matrices of the given space group number.
std::vector<std::vector<float>>
SpaceGroupSymOps::getTranslationMatrices(size_t number) const {
	std::vector<std::vector<float>> v_translations;

	auto keyPair = m_t.equal_range(number);

	for (auto it = keyPair.first; it != keyPair.second; ++it) {
		v_translations.push_back(it->second);
	}

	return v_translations;
}


// Returns a vector containing all "transformed" bases vectors by
// running through all symmetry operations of the given space group
// number and performing matrix multiplication.
std::vector<std::vector<int>>
SpaceGroupSymOps::transformSymOp(size_t number, std::vector<int> v_cut) {
	std::vector<int> v_basis(3);
	std::vector<std::vector<int>> v_bases; // contains all v_basis
	intMatrix m_mat;
	int sum;

	// TODO: size check; and, best way to implement matrix multiplication?
	std::vector<intMatrix> generatorList = getGeneratorMatrices(number);

	for (auto it = generatorList.begin(); it < generatorList.end(); ++it) {
		m_mat = *it;
		for (int i = 0; i < 3 ; ++i) {
			sum = 0;
			for (int j = 0; j < 3; ++j) {
				sum += m_mat[i][j] * v_cut[j];
			}
			v_basis[i] = sum;
		}
		v_bases.push_back(v_basis);
	}

	return v_bases;
}

// "Stringifies" the given basis vector so it can be used as an input to BinMD.
std::string
SpaceGroupSymOps::getBasisVector(std::vector<int> v_basis, std::string name) {
	std::string basis;

	basis.append(name);
	basis.append(",unit");
	for (int i = 0; i < 3; ++i) {
		basis.append(",");
		basis.append(std::to_string(v_basis[i]));
	}
	basis.append(",0");

	return basis;
}