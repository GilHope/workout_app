import sys
import os

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

def test_add_warmup_sets():
    """Test the warm-up sets are calculated correctly."""
    result = add_warmup_sets('BENCH', 100)

    # Check that warm-up sets are calculated correctly
    assert result == [
        '5 x 35 lbs',  # 40% of training max (90 lbs training max, so 35 lbs)
        '5 x 45 lbs',  # 50% of training max
        '3 x 55 lbs'   # 60% of training max
    ]

def test_add_fsl_sets():
    """Test that FSL sets are correctly added and formatted."""
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_fsl_sets(workout_plan)

    # Check that FSL sets are correctly appended for each lift
    assert any('<em>3-5 sets of 5-8 reps x' in set for week in result.values() for sets in week.values() for set in sets)

def test_add_bbb_sets():
    """Test that BBB sets are correctly added and formatted."""
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_bbb_sets(workout_plan, orms, unit='lbs')

    # Check that BBB sets are correctly appended and formatted in italics
    assert any('5 sets of 10 x' in set for week in result.values() for sets in week.values() for set in sets)

def test_add_pyramid_sets():
    """Test that Pyramid sets are correctly added and formatted."""
    orms = (100, 200, 300, 400)
    workout_plan = calculate_workouts(orms, unit='lbs', include_deload=True)
    result = add_pyramid_sets(workout_plan)

    # Check that Pyramid sets are correctly appended and formatted in italics
    assert any('<em>' in set for week in result.values() for sets in week.values() for set in sets)

