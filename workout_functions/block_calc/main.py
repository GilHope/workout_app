import sys

def calculate_workouts(orms):
    """
    Calculate the workout program based on the given 1RMs.

    :param orms: A tuple containing the 1RM for squat, bench, deadlift, overhead press
    :return: A dictionary with the workout plan for each week
    """
    workout_plan = {}

    training_maxes = {lift: max * 0.9 for lift, max in zip(["SQUAT", "BENCH", "DEADLIFT", "OHP"], orms)}

    # Define the rep schemes and percentages for each week
    rep_schemes = {
        "WEEK 1": [(5, 0.65), (5, 0.75), (5, 0.85)],
        "WEEK 2": [(3, 0.70), (3, 0.80), (3, 0.90)],
        "WEEK 3": [(5, 0.75), (3, 0.85), (1, 0.95)],
        "WEEK 4": [(5, 0.40), (5, 0.50), (5, 0.60)]
    }

    # Calculate the weights for each set
    for week, reps_and_percs in rep_schemes.items():
        formatted_week = f'{week}:' 
        workout_plan[formatted_week] = {}

        for lift, training_max in training_maxes.items():
            workout_plan[formatted_week][lift] = [
                (f'{reps} reps', f'{round(training_max * perc / 5) * 5}lbs') for reps, perc in reps_and_percs
            ]

    return workout_plan


#######################################################################################################
#######################################################################################################


## Test Call ##

if __name__ == "__main__":
    # Default 1RM values
    default_1rms = (315, 225, 405, 135) # <--- Change these default values here!
    
    # If no command-line arguments are provided, use default values
    if len(sys.argv) == 1:
        my_1rms = default_1rms
    elif len(sys.argv) == 5:
        try:
            # Parse command-line arguments to integers
            my_1rms = tuple(int(arg) for arg in sys.argv[1:])
        except ValueError as e:
            print("Error: Please provide four integer values for the 1RMs.")
            print(f"Exception message: {e}")
            sys.exit(1)
    else:
        print("Usage: python3 wendler_func_4.py [squat_1rm bench_1rm deadlift_1rm ohp_1rm]")
        sys.exit(1)
    
    workout_plan = calculate_workouts(my_1rms)
    
    # Output the workout plan
    for week in workout_plan:
        print(f"{week}")
        for lift in workout_plan[week]:
            formatted_lift = lift.upper()
            print(f"{formatted_lift}: ")
            formatted_sets = ', '.join(f"({reps}, {weight})" for reps, weight in workout_plan[week][lift])
            print(formatted_sets)
        print()  


#######################################################################################################
#######################################################################################################

# The program can be called from the terminal as follows:

# Example:

# python3 wendler_func_3.py 315 225 405 135  # Replace these arguments with your actual 1RMs