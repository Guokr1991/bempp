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

#ifndef bempp_preconditioner_factory_hpp
#define	bempp_preconditioner_factory_hpp

#include "../common/common.hpp"

#include "bempp/common/config_trilinos.hpp"

#ifdef WITH_TRILINOS

#include "Teuchos_RCP.hpp"
#include "Thyra_PreconditionerBase.hpp"
#include "../assembly/discrete_boundary_operator.hpp"

namespace Bempp
{

template<typename ValueType>
class PreconditionerFactory
{
public:
    static Teuchos::RCP<const Thyra::PreconditionerBase<ValueType> >
    acaOperatorToPreconditioner
    (const DiscreteBoundaryOperator<ValueType>& discreteOperator, const double delta=0.1);
};

} // namespace Bempp

#endif /* WITH_TRILINOS */

#endif

