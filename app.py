# app.py
import streamlit as st
import pandas as pd
from lp_solver import solve_lp_problem # Import the solver function

# --- Application Configuration ---
st.set_page_config(
    page_title="Wyndor Glass Co. Product-Mix Optimizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Streamlit UI ---

st.title("🪟 Wyndor Glass Co. Product-Mix Optimizer")
st.markdown("A template for solving Linear Programming Product-Mix problems by **maximizing profit**.")
st.markdown(
    "Use the sidebar to input the profit, capacity, and production time required for each product (Door $x_1$ and Window $x_2$).")

# --- Sidebar Input ---
st.sidebar.header("Input Data")
st.sidebar.markdown("---")

# --- Profit Input ---
st.sidebar.subheader("💰 Unit Profit (Objective Function Coeffs)")
doors_profit = st.sidebar.number_input("Doors ($x_1$)", value=300, min_value=1, step=10, key='p_door')
windows_profit = st.sidebar.number_input("Windows ($x_2$)", value=500, min_value=1, step=10, key='p_window')
st.sidebar.markdown("---")

# --- Capacity Input ---
st.sidebar.subheader("🏭 Plant Capacity (RHS of Constraints)")
plant1_capacity = st.sidebar.number_input("Plant 1 (Aluminum/Hardware)", value=4, min_value=1, key='c_p1')
plant2_capacity = st.sidebar.number_input("Plant 2 (Wood Frames)", value=12, min_value=1, key='c_p2')
plant3_capacity = st.sidebar.number_input("Plant 3 (Glass/Assembly)", value=18, min_value=1, key='c_p3')
st.sidebar.markdown("---")


# --- Production Time Input ---
st.sidebar.subheader("⏱️ Time Used Per Unit (LHS of Constraints)")
# Plant 1 (P1)
st.sidebar.write("##### Plant 1 Time (Capacity: {} hrs)".format(plant1_capacity))
plant1_doors_time = st.sidebar.number_input("Doors time in P1", value=1, min_value=0, key='t_p1_door')
plant1_windows_time = st.sidebar.number_input("Windows time in P1", value=0, min_value=0, key='t_p1_window')

# Plant 2 (P2)
st.sidebar.write("##### Plant 2 Time (Capacity: {} hrs)".format(plant2_capacity))
plant2_doors_time = st.sidebar.number_input("Doors time in P2", value=0, min_value=0, key='t_p2_door')
plant2_windows_time = st.sidebar.number_input("Windows time in P2", value=2, min_value=0, key='t_p2_window')

# Plant 3 (P3)
st.sidebar.write("##### Plant 3 Time (Capacity: {} hrs)".format(plant3_capacity))
plant3_doors_time = st.sidebar.number_input("Doors time in P3", value=3, min_value=0, key='t_p3_door')
plant3_windows_time = st.sidebar.number_input("Windows time in P3", value=2, min_value=0, key='t_p3_window')


# --- Run the Model ---
if st.button("Solve for Optimal Mix"):
    
    # Collect all inputs and run the solver function from lp_solver.py
    results = solve_lp_problem(
        doors_profit, windows_profit,
        plant1_doors_time, plant2_windows_time,
        plant3_doors_time, plant3_windows_time,
        plant1_capacity, plant2_capacity, plant3_capacity
    )

    st.header("✅ Optimization Results")
    st.markdown("---")

    if results['status'] == 'Optimal':
        col1, col2, col3 = st.columns(3)
        
        # Optimal Production Mix
        with col1:
            st.metric(label="Optimal Doors ($x_1$)", 
                      value=f"{results['doors_units']:.2f} units/wk")
        with col2:
            st.metric(label="Optimal Windows ($x_2$)", 
                      value=f"{results['windows_units']:.2f} units/wk")
        with col3:
            st.metric(label="Maximum Total Profit", 
                      value=f"${results['max_profit']:,.2f}/wk", 
                      delta=f"Status: {results['status']}",
                      delta_color="normal")

        st.subheader("🏭 Plant Capacity Analysis (Constraints)")
        
        # Display Constraint Analysis
        constraints_data = {
            "Plant": ["Plant 1", "Plant 2", "Plant 3"],
            "Constraint": [
                f"{plant1_doors_time}x₁ + {plant1_windows_time}x₂ ≤ {plant1_capacity}",
                f"{plant2_doors_time}x₁ + {plant2_windows_time}x₂ ≤ {plant2_capacity}",
                f"{plant3_doors_time}x₁ + {plant3_windows_time}x₂ ≤ {plant3_capacity}",
            ],
            "Capacity (hrs)": [plant1_capacity, plant2_capacity, plant3_capacity],
            "Time Used (hrs)": [
                results['constraints']['Plant 1']['time_used'],
                results['constraints']['Plant 2']['time_used'],
                results['constraints']['Plant 3']['time_used'],
            ],
        }
        
        # Calculate Slack and Status
        constraints_data["Slack (hrs)"] = [
            constraints_data["Capacity (hrs)"][i] - constraints_data["Time Used (hrs)"][i] 
            for i in range(len(constraints_data["Plant"]))
        ]
        
        constraints_data["Status"] = [
            "Binding (Fully Used)" if abs(s) < 0.001 else "Remaining Capacity"
            for s in constraints_data["Slack (hrs)"]
        ]

        df = pd.DataFrame(constraints_data)
        st.dataframe(df.style.format({
            "Time Used (hrs)": "{:.2f}",
            "Slack (hrs)": "{:.2f}"
        }))

    else:
        st.error(f"The optimization failed. Status: {results['status']}")
        st.info("Check your input values. The problem might be infeasible (no solution) or unbounded.")
