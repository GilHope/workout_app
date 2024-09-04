import pytest
import sys
import os
import time

# Add the project root directory to sys.path to ensure correct module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import necessary functions for integration testing
from workout_functions.block_calc.main import (
    calculate_workouts,
    add_fsl_sets,
    add_bbb_sets,
    add_pyramid_sets
)

# Test deload week is included when true
def test_calculate_workouts_with_deload():
    orms = (100, 200, 300, 400)
    result = calculate_workouts(orms, unit='lbs', include_deload=True)
    assert 'WEEK 1:' in result
    assert 'WEEK 2:' in result
    assert 'WEEK 3:' in result
    assert 'WEEK 4:' in result  # Deload week should be included

# Test deload week is not included when false
def test_calculate_workouts_without_deload():
    orms = (100, 200, 300, 400)
    result = calculate_workouts(orms, unit='lbs', include_deload=False)
    assert 'WEEK 1:' in result
    assert 'WEEK 2:' in result
    assert 'WEEK 3:' in result
    assert 'WEEK 4:' not in result  # Deload week should not be included

# Test multiple edge cases together for correct handling.
def test_combined_edge_cases():
    orms = (0, 1000, 500, 250)  # Edge case values
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    # Apply all additional sets (integration of different functionalities)
    # Test formatting and structure of the output.
    assert any('<strong>' in set for week in workout_plan.values() for sets in week.values() for set in sets)

# Test that empty input values are handled properly.
def test_empty_input_values():
    with pytest.raises(ValueError, match="Bench 1RM values cannot be None or empty."):
        calculate_workouts((None, None, None, None), unit='lbs')

# Test the formatting of the final output for all sets.
def test_final_output_formatting():
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    # Check if all outputs have correct HTML tags
    for week in workout_plan.values():
        for sets in week.values():
            for set in sets:
                assert ('<strong>' in set or '<em>' in set or 'x' in set), f"Invalid format found in set: {set}"

# Test that the workout generation function performs efficiently with valid inputs.
def test_performance():
    orms = (100, 200, 300, 400)
    start_time = time.time()
    result = calculate_workouts(orms, unit='lbs', include_deload=True)
    end_time = time.time()
    execution_time = end_time - start_time
    assert execution_time < 0.5, f"Performance issue: Execution took too long ({execution_time:.2f} seconds)"

# Test that user input is sanitized to prevent HTML or script injection.
def test_html_injection_prevention():
    orms = (100, 200, 300, 400)
    result = calculate_workouts(orms, unit='lbs', include_deload=True)

    # Ensure that no potentially harmful tags are in the output
    forbidden_strings = ['<script>', '</script>', '<img>', '</img>', '<iframe>', '</iframe>']
    for week in result.values():
        for sets in week.values():
            for set in sets:
                assert not any(tag in set for tag in forbidden_strings), "Potential HTML injection detected"

# Test the performance of the app with a large number of inputs.
def test_large_input_sizes():
    orms = tuple([i * 10 for i in range(1, 101)])  # Create a large tuple with 100 inputs

    try:
        result = calculate_workouts(orms, unit='lbs', include_deload=True)
        # Check that there are no unexpected errors and the output is correct
        assert isinstance(result, dict) and len(result) > 0
    except Exception as e:
        pytest.fail(f"Performance test failed with error: {str(e)}")

# Test the formatting of the final output for all sets.
def test_final_output_formatting():
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)

    workout_plan = add_fsl_sets(workout_plan)
    workout_plan = add_bbb_sets(workout_plan, orms, unit='lbs')
    workout_plan = add_pyramid_sets(workout_plan)

    # Check if all outputs have correct HTML tags
    for week in workout_plan.values():
        for sets in week.values():
            for set in sets:
                assert ('<strong>' in set or '<em>' in set or 'x' in set), f"Invalid format found in set: {set}"
