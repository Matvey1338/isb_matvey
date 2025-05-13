import json
import os

def load_constants():
    """Load constants from JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    constants_path = os.path.join(current_dir, 'constants.json')
    
    try:
        with open(constants_path, 'r') as f:
            constants = json.load(f)
        return constants
    except FileNotFoundError:
        raise FileNotFoundError(f"Constants file not found at {constants_path}. Please ensure constants.json exists in the handlers directory.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {constants_path}. Please check the file contents.")

# Load all constants
CONSTANTS = load_constants()

# Export constants as module variables
SEQUENCE_LENGTH = CONSTANTS['SEQUENCE_LENGTH']
SIGNIFICANCE_LEVEL = CONSTANTS['SIGNIFICANCE_LEVEL']
BLOCK_SIZE = CONSTANTS['BLOCK_SIZE']
THEORETICAL_PROBABILITIES = CONSTANTS['THEORETICAL_PROBABILITIES'] 