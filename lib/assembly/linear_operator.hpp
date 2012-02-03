// Copyright (C) 2011-2012 by the BEM++ Authors
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

#ifndef bempp_linear_operator_hpp
#define bempp_linear_operator_hpp

#include "../grid/common.hpp"

#include <memory>

namespace arma {
template <typename eT> class Mat;
}

namespace Bempp {

class AssemblyOptions;
class Grid;
template <typename ValueType> class DiscreteScalarValuedLinearOperator;
template <typename ValueType> class DiscreteVectorValuedLinearOperator;
template <typename ValueType> class Space;

/** \brief Linear operator.

  This class template is used as a base class for all implementations of
  various types of linear operators, in particular integral operators.

  A LinearOperator represents a linear mapping \f$L : X \to Y\f$, where \f$X\f$
  is the space of functions \f$F : S \to K^p\f$ and \f$Y\f$ is another space of
  functions \f$G : T \to K^q\f$, with \f$S\f$ standing for an
  \f$n\f$-dimensional surface and \f$T\f$ either equal to \f$S\f$ or to a
  \f$(n+1)\f$-dimensional domain in which \f$S\f$ is embedded. \f$K\f$ denotes
  either the set of real or complex numbers.

  \tparam ValueType      Type used to represent elements of \f$K\f$. This can be
                         one of: float, double, std::complex<float> and
                         std::complex<double>.
*/
template <typename ValueType>
class LinearOperator
{
public:
    virtual ~LinearOperator() {}

    // Ideas for better names for all methods here are very welcome!!!
    /** \brief Number of components of the functions from the trial space \f$X\f$.

      This is equal to \f$p\f$ in the notation above. */
    virtual int domainDimension() const = 0;

    /** \brief Number of components of the functions from trial space \f$Y\f$.

      This is equal to \f$q\f$ in the notation above. */
    virtual int codomainDimension() const = 0;

    /** \brief Assemble the operator's weak form.

      Construct a discrete linear operator representing the matrix \f$W_{jk}\f$
      whose entries have the form

      \f[W_{jk} = \int_S \phi_j L \psi_k,\f]

      where \f$L\f$ is the linear operator represented by this object, \f$S\f$
      denotes the surface that is the domain of the trial space \f$X\f$ and
      which is represented by the grid returned by trialSpace.grid(),
      \f$\phi_j\f$ is a function from the test space \f$Y\f$ and \f$\psi_k\f$ a
      function from \f$X\f$.

      Note: trialSpace.grid() and testSpace.grid() must return a reference to
      the same object. */
    virtual std::auto_ptr<DiscreteScalarValuedLinearOperator<ValueType> >
    assembleWeakForm(
            const Space<ValueType>& testSpace,
            const Space<ValueType>& trialSpace,
            const AssemblyOptions& options) const = 0;

    /** \brief Assemble a discrete representation of the operator.

      Construct a discrete linear operator representing the 3D array
      \f$L_{ijk}\f$ whose entries have the form

      \f[L_{ijk} = [(L \psi_k)(x_j)]_i,\f]

      where \f$L\f$ is the linear operator represented by this object, \f$S\f$
      denotes the surface that is the domain of the trial space \f$X\f$ and
      which is represented by the grid returned by trialSpace.grid(),
      \f$\psi_k\f$ a function from \f$X\f$, and \f$x_j\f$ is a point from the
      space \f$T\f$ that is the domain of the test space \f$Y\f$. The symbol
      \f$[]_i\f$ denotes the \f$i\f$'th component of the quantity in brackets.
      */
    virtual std::auto_ptr<DiscreteVectorValuedLinearOperator<ValueType> >
    assembleOperator(
            const arma::Mat<ctype>& testPoints,
            const Space<ValueType>& trialSpace,
            const AssemblyOptions& options) const = 0;
};

} // namespace Bempp

#endif
