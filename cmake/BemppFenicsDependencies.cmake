include(PythonFiatLookup)

lookup_python_package(instant)
lookup_python_package(six)
lookup_python_package(sympy)
lookup_python_package(ply)
lookup_fiat_package(FIAT)
lookup_python_package(ufl)
lookup_package(Eigen3 REQUIRED)
lookup_package(VTK 6.1 REQUIRED)
lookup_package(Umfpack REQUIRED)
lookup_package(SWIG 3.0.5 REQUIRED)
lookup_package(FFC REQUIRED)
lookup_package(DOLFIN REQUIRED)
