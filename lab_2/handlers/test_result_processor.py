from .constants import SIGNIFICANCE_LEVEL

def process_test_result(test_name, p_value, additional_data=None):
    """
    Process test results and determine success/failure
    Args:
        test_name: Name of the test
        p_value: P-value from the test
        additional_data: Dictionary with additional test data
    Returns:
        Dictionary with processed test results
    """
    match p_value:
        case None:
            return {
                'success': False,
                'message': f'{test_name} cannot be applied',
                'p_value': None
            }
        case value if value >= SIGNIFICANCE_LEVEL:
            result = {
                'success': True,
                'message': f'{test_name} passed',
                'p_value': value
            }
        case _:
            result = {
                'success': False,
                'message': f'{test_name} failed',
                'p_value': p_value
            }
    
    if additional_data:
        result.update(additional_data)
        
    return result 