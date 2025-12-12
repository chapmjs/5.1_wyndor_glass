# lp_solver.py
from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, value
import numpy as np # Adding numpy for robust float comparisons if needed

def solve_lp_problem(
    doors_profit, windows_profit,
    
    # 6 Production Time Coefficients:
    plant1_doors_time, plant1_windows_time,  # <--- plant1_windows_time ADDED
    plant2_doors_time, plant2_windows_time,  # <--- plant2_doors_time ADDED
    plant3_doors_time, plant3_windows_time,
    
    # 3 Capacity Values:
    plant1_capacity, plant2_capacity, plant3_capacity
):
    """
    Formulates and solves the Linear Programming product-mix problem using PuLP.
    ...
    """
    
    # ... rest of the function remains the same ...

    # 4. Define Constraints (Available Production Capacity)
    
    # Plant 1 Constraint: (1x1 + 0x2 <= 4 in the initial problem)
    prob += plant1_doors_time * x1 + plant1_windows_time * x2 <= plant1_capacity, "Plant_1_Capacity"
    #                                ^^^^^^^^^^^^^^^^^^^  <-- Now defined!

    # Plant 2 Constraint: (0x1 + 2x2 <= 12 in the initial problem)
    prob += plant2_doors_time * x1 + plant2_windows_time * x2 <= plant2_capacity, "Plant_2_Capacity"
    #         ^^^^^^^^^^^^^^^^^^  <-- Now defined!
    
    # Plant 3 Constraint
    prob += plant3_doors_time * x1 + plant3_windows_time * x2 <= plant3_capacity, "Plant_3_Capacity"

    # ... and you'll need to update the time_used calculation in the results section too:
    if prob.status == LpStatus.Optimal:
        # ...
        results["constraints"] = {
            "Plant 1": {
                "capacity": plant1_capacity,
                "time_used": (plant1_doors_time * results['doors_units'] + plant1_windows_time * results['windows_units'])
            },
            "Plant 2": {
                "capacity": plant2_capacity,
                "time_used": (plant2_doors_time * results['doors_units'] + plant2_windows_time * results['windows_units'])
            },
            "Plant 3": {
                "capacity": plant3_capacity,
                "time_used": (plant3_doors_time * results['doors_units'] + plant3_windows_time * results['windows_units'])
            }
        }
            
    return results

if __name__ == '__main__':
    # Example usage for testing the solver function directly
    # Data from Table 5.1:
    # Doors Profit=$300, Windows Profit=$500
    # P1 Time: (1, 0), P2 Time: (0, 2), P3 Time: (3, 2)
    # Capacity: (4, 12, 18)
    test_results = solve_lp_problem(
        300, 500, 1, 0, 3, 2, 4, 12, 18
    )
    print(f"Test Status: {test_results['status']}")
    print(f"Test Doors: {test_results['doors_units']:.2f}")
    print(f"Test Max Profit: ${test_results['max_profit']:,.2f}")
