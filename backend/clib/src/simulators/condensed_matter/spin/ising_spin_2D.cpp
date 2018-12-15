#include "ising_spin_2D.hpp"


IsingSpin2D::IsingSpin2D(int dimX, int dimY, double initTemperature) : 
    mDimX(dimX),
    mDimY(dimY),
    mTemperature(initTemperature),
    mSpins(MatrixXd::Zero(dimX, dimY))
{
};

void IsingSpin2D::update(double dt)
{
    using namespace std;

    chrono::system_clock::time_point start;
    double elapsed;
    start = chrono::system_clock::now();
    while (elapsed < dt)
    {
        mCnt++;
        for (auto i = 0; i < mDimX; ++i) {
            for (auto j = 0; j < mDimY; ++j) {
                if (0.5 < (rd()+1)/RAND_MAX) {
                    mSpins(i, j) = 1;
                } else {
                    mSpins(i, j) = 0;
                }
            }
        }
        elapsed = static_cast<double>(chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now() - start).count() / 1000.0);
    }
};


np::ndarray IsingSpin2D::getSpins()
{
    Py_intptr_t shape[2] = {mDimX, mDimY};
    np::ndarray result = np::zeros(2, shape, np::dtype::get_builtin<double>());
    std::copy(&mSpins(0, 0), &mSpins(mDimX-1, mDimY-1)+1, reinterpret_cast<double*>(result.get_data()));
    return result;
};


void IsingSpin2D::setTemperature(double temperature)
{
    mTemperature = temperature;
};
