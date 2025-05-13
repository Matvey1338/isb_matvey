from .constants import SIGNIFICANCE_LEVEL

def process_test_result(test_name, p_value, additional_data=None):
    """
    Process test results and determine success/failure
    Args:
        test_name: Name of the test
        p_value: P-value from the test
        additional_data: Dictionary with additional test data (optional)
    Returns:
        Dictionary with processed test results
    """
    if p_value is None:
        return {
            'success': False,
            'message': f'{test_name} cannot be applied',
            'p_value': None
        }
    
    result = {
        'success': p_value >= SIGNIFICANCE_LEVEL,
        'message': f'{test_name} {"passed" if p_value >= SIGNIFICANCE_LEVEL else "failed"}',
        'p_value': p_value
    }
    
    if additional_data:
        result.update(additional_data)
        
    return result 