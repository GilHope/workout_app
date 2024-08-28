import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from workout_functions.block_calc.main import calculate_workouts
from app import add_warmup_sets

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

# Test warm-up sets are added correctly
def test_add_warmup_sets():
    """Test the warm-up sets are calculated correctly."""
    result = add_warmup_sets('BENCH', 100)

    # Check that warm-up sets are calculated correctly
    assert result == [
        (5, 40),  # 40% of training max
        (5, 50),  # 50% of training max
        (3, 60)   # 60% of training max
    ]

    # Check correct length
    assert len(result) == 3

