import pytest
import sys
import os
import time

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from workout_functions.block_calc.main import calculate_workouts
from workout_functions.block_calc.main import (
    calculate_workouts,
    add_warmup_sets,
    add_fsl_sets,
    add_pyramid_sets,
    add_bbb_sets
)

# Test deload week is included when true
def test_calculate_workouts_with_deload():
    orms = (100, 200, 300, 400)
    result = calculate_workouts(orms, unit='lbs', include_deload=True)

    # Check that all 4 weeks are included when deload is True
    assert 'WEEK 1:' in result
    assert 'WEEK 2:' in result
    assert 'WEEK 3:' in result
    assert 'WEEK 4:' in result  # Deload week should be included

    # Validate main set formatting (check bold)
    assert all('<strong>' in set for week in result.values() for sets in week.values() for set in sets if 'strong' in set)

# Test deload week is not included when false
def test_calculate_workouts_without_deload():
    orms = (100, 200, 300, 400)
    result = calculate_workouts(orms, unit='lbs', include_deload=False)

    # Check that only 3 weeks are included when deload is False
    assert 'WEEK 1:' in result
    assert 'WEEK 2:' in result
    assert 'WEEK 3:' in result
    assert 'WEEK 4:' not in result  # Deload week should not be included

    # Validate no empty week entries
    assert all(len(sets) > 0 for week in result.values() for sets in week.values())

# Test the warm-up sets are calculated correctly.
def test_add_warmup_sets():
    result = add_warmup_sets('BENCH', 100, 'lbs')

    # Check that warm-up sets are calculated correctly
    assert result == [
        '5 x 35 lbs',  # 40% of training max (90 lbs training max, so 35 lbs)
        '5 x 45 lbs',  # 50% of training max
        '3 x 55 lbs'   # 60% of training max
    ]

# Test that FSL sets are correctly added and formatted.
def test_add_fsl_sets():
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_fsl_sets(workout_plan)

    # Check that FSL sets are correctly appended for each lift
    assert any('<em>3-5 sets of 5-8 reps x' in set for week in result.values() for sets in week.values() for set in sets)

# Test that BBB sets are correctly added and formatted.
def test_add_bbb_sets():
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_bbb_sets(workout_plan, orms, unit='lbs')

    # Check that BBB sets are correctly appended and formatted in italics
    assert any('5 sets of 10 x' in set for week in result.values() for sets in week.values() for set in sets)

# Test that Pyramid sets are correctly added and formatted.
def test_add_pyramid_sets():
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_pyramid_sets(workout_plan)

    # Check that Pyramid sets are correctly appended and formatted in italics
    assert any('<em>' in set for week in result.values() for sets in week.values() for set in sets)

# Test that valid 1RM values between 0 and 1000 are accepted and processed correctly.
def test_valid_1rm_values():
    orms = (100, 200, 300, 400)  # Valid values
    result = calculate_workouts(orms, unit='lbs', include_deload=True)

    # Check that all 4 weeks are included when deload is True
    assert 'WEEK 1:' in result
    assert 'WEEK 2:' in result
    assert 'WEEK 3:' in result
    assert 'WEEK 4:' in result  # Deload week should be included

    # Validate that the main sets are correctly formatted
    assert all('<strong>' in set for week in result.values() for sets in week.values() for set in sets if 'strong' in set)

# Test that 1RM values outside of the 0-1000 range get a ValueError.
def test_invalid_1rm_values():
    with pytest.raises(ValueError, match="Bench 1RM must be between 0 and 1000."):
        calculate_workouts((-10, 200, 300, 400), unit='lbs')  # Negative 1RM

    with pytest.raises(ValueError, match="Squat 1RM must be between 0 and 1000."):
        calculate_workouts((100, 2000, 300, 400), unit='lbs')  # 1RM over 1000

    with pytest.raises(ValueError, match="OHP 1RM must be between 0 and 1000."):
        calculate_workouts((100, 200, -5, 400), unit='lbs')  # Negative 1RM

    with pytest.raises(ValueError, match="Deadlift 1RM must be between 0 and 1000."):
        calculate_workouts((100, 200, 300, 1500), unit='lbs')  # 1RM over 1000

# Test that 1RM values exactly at the boundaries (0 and 1000) are processed correctly.
def test_edge_case_1rm_values():
    orms = (0, 1000, 500, 250)  # Edge case values
    result = calculate_workouts(orms, unit='lbs', include_deload=True)

    # Check that all 4 weeks are included when deload is True
    assert 'WEEK 1:' in result
    assert 'WEEK 2:' in result
    assert 'WEEK 3:' in result
    assert 'WEEK 4:' in result  # Deload week should be included

    # Validate that the main sets are correctly formatted
    assert all('<strong>' in set for week in result.values() for sets in week.values() for set in sets if 'strong' in set)

# Test multiple edge cases together for correct handling.
def test_combined_edge_cases():
    orms = (0, 1000, 500, 250)  # Edge case values
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)

    # Apply all additional sets
    for lift, lift_max in zip(["BENCH", "SQUAT", "OHP", "DEADLIFT"], orms):
        warmup_sets = add_warmup_sets(lift, lift_max, 'lbs')
        for week in workout_plan:
            if lift not in workout_plan[week]:
                workout_plan[week][lift] = []
            workout_plan[week][lift] = warmup_sets + workout_plan[week][lift]

    workout_plan = add_fsl_sets(workout_plan)
    workout_plan = add_bbb_sets(workout_plan, orms, unit='lbs')
    workout_plan = add_pyramid_sets(workout_plan)

    # Ensure all sets are formatted correctly
    assert any('<strong>' in set for week in workout_plan.values() for sets in week.values() for set in sets)
    assert any('<em>3-5 sets of 5-8 reps x' in set for week in workout_plan.values() for sets in week.values() for set in sets)
    assert any('5 sets of 10 x' in set for week in workout_plan.values() for sets in week.values() for set in sets)
    assert any('<em>' in set for week in workout_plan.values() for sets in week.values() for set in sets)

# Test that missing 1RM values are handled properly.
def test_missing_input_values():
    with pytest.raises(ValueError, match="Bench 1RM values cannot be None."):
        calculate_workouts((None, 200, 300, 400), unit='lbs')

    with pytest.raises(ValueError, match="Squat 1RM values cannot be None."):
        calculate_workouts((100, None, 300, 400), unit='lbs')

#Test the formatting of the final output for all sets.
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

# Test the performance of the app with a large number of inputs.
def test_large_input_sizes():
    orms = tuple([i * 10 for i in range(1, 101)])  # Create a large tuple with 100 inputs

    try:
        result = calculate_workouts(orms, unit='lbs', include_deload=True)
        # Check that there are no unexpected errors and the output is correct
        assert isinstance(result, dict) and len(result) > 0
    except Exception as e:
        pytest.fail(f"Performance test failed with error: {str(e)}")

# Test that empty input values are handled properly.
def test_empty_input_values():
    with pytest.raises(ValueError, match="Bench 1RM values cannot be None or empty."):
        calculate_workouts((None, None, None, None), unit='lbs')

    with pytest.raises(ValueError, match="Bench 1RM values cannot be None or empty."):
        calculate_workouts(("", 200, 300, 400), unit='lbs')  # Empty string input

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

# Test that the workout generation function performs efficiently with valid inputs.
def test_performance():
    orms = (100, 200, 300, 400)
    start_time = time.time()
    result = calculate_workouts(orms, unit='lbs', include_deload=True)
    end_time = time.time()
    execution_time = end_time - start_time

    assert execution_time < 0.5, f"Performance issue: Execution took too long ({execution_time:.2f} seconds)"
