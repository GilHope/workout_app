import pytest
import sys
import os

# Add the project root directory to sys.path to allow imports from the root level
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Importing the functions needed for the tests
from workout_functions.block_calc.main import (
    calculate_workouts,
    add_warmup_sets,
    add_fsl_sets,
    add_pyramid_sets,
    add_bbb_sets
)

# Test the warm-up sets are calculated correctly.
def test_add_warmup_sets():
    result = add_warmup_sets('BENCH', 100, 'lbs')
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
    assert any('<em>3-5 sets of 5-8 reps x' in set for week in result.values() for sets in week.values() for set in sets)

# Test that BBB sets are correctly added and formatted.
def test_add_bbb_sets():
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_bbb_sets(workout_plan, orms, unit='lbs')
    assert any('5 sets of 10 x' in set for week in result.values() for sets in week.values() for set in sets)

# Test that Pyramid sets are correctly added and formatted.
def test_add_pyramid_sets():
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_pyramid_sets(workout_plan)
    assert any('<em>' in set for week in result.values() for sets in week.values() for set in sets)

# Test that 1RM values outside of the 0-1000 range get a ValueError.
def test_invalid_1rm_values():
    with pytest.raises(ValueError, match="Bench 1RM must be between 0 and 1000."):
        calculate_workouts((-10, 200, 300, 400), unit='lbs')
    with pytest.raises(ValueError, match="Squat 1RM must be between 0 and 1000."):
        calculate_workouts((100, 2000, 300, 400), unit='lbs')
    with pytest.raises(ValueError, match="OHP 1RM must be between 0 and 1000."):
        calculate_workouts((100, 200, -5, 400), unit='lbs')
    with pytest.raises(ValueError, match="Deadlift 1RM must be between 0 and 1000."):
        calculate_workouts((100, 200, 300, 1500), unit='lbs')

# Test missing 1RM values.
def test_missing_input_values():
    with pytest.raises(ValueError, match="Bench 1RM values cannot be None."):
        calculate_workouts((None, 200, 300, 400), unit='lbs')
    with pytest.raises(ValueError, match="Squat 1RM values cannot be None."):
        calculate_workouts((100, None, 300, 400), unit='lbs')

# Test that 1RM values exactly at the boundaries (0 and 1000) are processed correctly.
def test_edge_case_1rm_values():
    orms = (0, 1000, 500, 250)  # Edge case values
    result = calculate_workouts(orms, unit='lbs', include_deload=True)
    assert 'WEEK 1:' in result
    assert 'WEEK 2:' in result
    assert 'WEEK 3:' in result
    assert 'WEEK 4:' in result  # Deload week should be included

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
