%{
#include "assembly/laplace_3d_single_layer_potential_operator.hpp"
#include "assembly/laplace_3d_double_layer_potential_operator.hpp"
%}

%inline %{
namespace Bempp
{

template <typename BasisFunctionType, typename ResultType>
boost::shared_ptr<PotentialOperator<BasisFunctionType, ResultType> >
laplace3dSingleLayerPotentialOperator()
{
    typedef Bempp::Laplace3dSingleLayerPotentialOperator<BasisFunctionType, ResultType> Type;
    return boost::shared_ptr<Type>(new Type);
}

template <typename BasisFunctionType, typename ResultType>
boost::shared_ptr<PotentialOperator<BasisFunctionType, ResultType> >
laplace3dDoubleLayerPotentialOperator()
{
    typedef Bempp::Laplace3dDoubleLayerPotentialOperator<BasisFunctionType, ResultType> Type;
    return boost::shared_ptr<Type>(new Type);
}

} // namespace Bempp
%}

namespace Bempp
{
BEMPP_INSTANTIATE_SYMBOL_TEMPLATED_ON_BASIS_AND_RESULT(laplace3dSingleLayerPotentialOperator);
BEMPP_INSTANTIATE_SYMBOL_TEMPLATED_ON_BASIS_AND_RESULT(laplace3dDoubleLayerPotentialOperator);
}
%pythoncode %{

def _constructLaplacePotentialOperator(className, context):
    basisFunctionType = context.basisFunctionType()
    resultType = context.resultType()
    result = constructObjectTemplatedOnBasisAndResult(
        className, basisFunctionType, resultType )
    result._context = context
    return result

	  %}
