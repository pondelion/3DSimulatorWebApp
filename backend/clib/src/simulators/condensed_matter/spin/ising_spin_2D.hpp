#include <chrono>
#include <random>
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <Eigen/Dense>


using namespace Eigen;

namespace p = boost::python;
namespace np = boost::python::numpy;

std::random_device rd;

class IsingSpin2D
{
public:
    IsingSpin2D(int dimX, int dimY, double initTemperature);
    ~IsingSpin2D() {};
    void update(double dt);
    np::ndarray getSpins();
    void setTemperature(double temperature);

private:
    MatrixXd mSpins;
    int mCnt;
    int const mDimX;
    int const mDimY;
    double mTemperature; 
};

BOOST_PYTHON_MODULE(ising_spin_2D) {
    Py_Initialize();
    np::initialize();
    p::class_<IsingSpin2D>("IsingSpin2D", p::init<int, int, double>())
        .def("update", &IsingSpin2D::update)
        .def("getSpins", &IsingSpin2D::getSpins)
        .def("setTemperature", &IsingSpin2D::setTemperature);
}
