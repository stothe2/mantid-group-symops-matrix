#ifndef SPACE_GROUP_SYM_OPS_H_
#define SPACE_GROUP_SYM_OPS_H_

#include <map>
#include <vector>
#include <string>
#include <cstdlib>

// A matrix of ints
typedef std::vector<std::vector<int>> intMatrix;

/** C++11 multimaps maintain a weak-order of insertion. Howevever, use
of this is precarious since we're giving precedent to the compiler.
May not be the best practice.

Another C++11 feature used is thread-safe static initialization.
*/
typedef std::multimap<size_t, std::vector<std::vector<int>>> vecVecMap;
typedef std::multimap<size_t, std::vector<float>> vecMap;

// Space group matrices without translation column
static vecVecMap m_sg {
	// Triclinic
	{1, {{1,0,0}, {0,1,0}, {0,0,1}}},
	{2, {{-1,0,0}, {0,-1,0}, {0,0,-1}}},

	// Monoclinic
	{3, {{-1,0,0}, {0,1,0}, {0,0,-1}}},
	{4, {{-1,0,0}, {0,1,0}, {0,0,-1}}},
	{5, {{-1,0,0}, {0,1,0}, {0,0,-1}}},
	{6, {{1,0,0}, {0,-1,0}, {0,0,1}}},
	{7, {{1,0,0}, {0,-1,0}, {0,0,1}}},
	{8, {{1,0,0}, {0,-1,0}, {0,0,1}}},
	{9, {{1,0,0}, {0,-1,0}, {0,0,1}}},
	{10, {{-1,0,0}, {0,1,0}, {0,0,-1}}},
	{10, {{-1,0,0}, {0,-1,0}, {0,0,-1}}}

	// TODO: initialize all space groups.
};

// Translation vectors
static vecMap m_t {
	// Triclinic
	{1, {0,0,0,0}},
	{2, {0,0,0,0}},

	// Monoclinic
	{3, {0,0,0,0}},
	{4, {0,0.5,0,0}},
	{5, {0,0,0,0}},
	{6, {0,0,0,0}},
	{7, {0,0,0.5,0}},
	{8, {0,0,0,0}},
	{9, {0,0,0.5,0}},
	{10, {0,0,0,0}},
	{10, {0,0,0,0}}

};

/**
 * @class SpaceGroupSymOps
 */
class SpaceGroupSymOps {
public:
	SpaceGroupSymOps();
	~SpaceGroupSymOps() {}

	std::vector<intMatrix> getGeneratorMatrices(size_t number) const;
	std::vector<std::vector<float>> getTranslationMatrices(size_t number) const;

	std::vector<std::vector<int>> transformSymOp(size_t number, std::vector<int> v_cut);
	std::string getBasisVector(std::vector<int> v_basis, std::string name);
};

#endif /* SPACE_GROUP_SYM_OPS_H_ */