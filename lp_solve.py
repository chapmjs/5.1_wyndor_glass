# lp_solver.py
from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, value

def solve_lp_problem(doors_profit, windows_profit,
                     plant1_doors_time, plant2_windows_time,
                     plant3_doors_time, plant3_windows_time,
                     plant1_capacity, plant2_capacity, plant3_capacity):
    """
    Formulates and solves the Linear Programming product-mix problem using PuLP.
    
    Returns: A dictionary containing status, optimal variables, max profit, and constraint details.
    """
    
    # 1. Create the Problem
    prob = LpProblem("Product Mix Optimization", LpMaximize)

    # 2. Define Decision Variables
    x1 = LpVariable("Doors", lowBound=0, cat='Continuous')
    x2 = LpVariable("Windows", lowBound=0, cat='Continuous')

    # 3. Define the Objective Function (Maximize Total Profit)
    # Z = Profit_Door * x1 + Profit_Window * x2
    prob += doors_profit * x1 + windows_profit * x2, "Total_Profit"

    # 4. Define Constraints (Available Production Capacity)
    
    # Plant 1 Constraint: Time_P1_Door * x1 + Time_P1_Window * x2 <= Capacity_P1
    prob += plant1_doors_time * x1 + plant1_windows_time * x2 <= plant1_capacity, "Plant_1_Capacity"

    # Plant 2 Constraint: Time_P2_Door * x1 + Time_P2_Window * x2 <= Capacity_P2
    prob += plant2_doors_time * x1 + plant2_windows_time * x2 <= plant2_capacity, "Plant_2_Capacity"

    # Plant 3 Constraint: Time_P3_Door * x1 + Time_P3_Window * x2 <= Capacity_P3
    prob += plant3_doors_time * x1 + plant3_windows_time * x2 <= plant3_capacity, "Plant_3_Capacity"

    # 5. Solve the Problem
    prob.solve()
    
    # 6. Prepare Results Dictionary
    results = {
        "status": LpStatus[prob.status],
        "doors_units": 0,
        "windows_units": 0,
        "max_profit": 0,
        "constraints": {}
    }

    if prob.status == LpStatus.Optimal:
        results["doors_units"] = value(x1)
        results["windows_units"] = value(x2)
        results["max_profit"] = value(prob.objective)
        
        # Calculate utilization for the output table
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
