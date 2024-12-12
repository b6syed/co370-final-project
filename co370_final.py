import os
import pandas as pd
from gurobipy import Model, GRB, quicksum

# Change this to your csv files location
os.chdir('documents/CO370/Final Project')

# Load data from CSV files
contractors = pd.read_csv('contractors.csv', skiprows=1)
demand = pd.read_csv('demand.csv', skiprows=1)
distances = pd.read_csv('distances.csv', skiprows=1)

# Extract parameters
fixed_costs = contractors['fixed_cost'].tolist() # fc
cost_rates = contractors['cost_rate'].tolist() # fv
contractor_capacities = contractors['capacity'].tolist() # CCv
vehicle_capacities = contractors['vehicle_capacity'].tolist() # CVv
risk_scores = contractors['risk_score'].tolist() # RCv

#Max distance parameter
MaxDist = 100


# Convert distances to a dictionary for fast lookups
distance_dict = {(row['node_id'], row['contractor_id']): row['distance'] for _, row in distances.iterrows()} # dij

# Create sets dynamically based on input data
N = demand['node_id']  # Set of nodes (demand points)
V = contractors['capacity'].index.tolist()  # Set of vehicles/contractors

# Create model
model = Model("Transportation_Problem")

# Create variables
x = model.addVars(N, V, vtype=GRB.BINARY, name="x")  # Route assignment
y = model.addVars(V, vtype=GRB.BINARY, name="y")     # Contractor assignment

# Objective 1: Minimize Total Cost (Z1)
total_cost = quicksum(cost_rates[v] * distance_dict[i, v] * x[i, v] for i in N for v in V) + \
             quicksum(fixed_costs[v] * y[v] for v in V)
model.setObjectiveN(total_cost, 0, priority=2, name="Cost", weight=1.0)

# Objective 2: Minimize Risk Exposure (Z2)
risk = quicksum(risk_scores[v] * x[i, v] for i in N for v in V)
model.setObjectiveN(risk, 1, priority=1, name="Risk", weight=1.0)

# Constraints
# Flow conservation at demand nodes (3)
for i in N:
    for v in V:
        model.addConstr(quicksum(x[j, v] for j in N if j != i) == quicksum(x[i, v] for j in N if j != i))

# Flow conservation at demand nodes (4)
for i in N:
    model.addConstr(quicksum(x[i, v] for v in V) == 1)  # Ensure each node is visited by one contractor

# Vehicle capacity (5)
for v in V:
    model.addConstr(quicksum(x[i, v] * demand.loc[demand['node_id'] == i, 'demand'].values[0] for i in N) <= vehicle_capacities[v])

# Distance constraint (6).
for v in V:
    model.addConstr(quicksum(distance_dict[i, v] * x[i, v] for i in N) <= MaxDist)

# Flow conservation at disposal nodes (7)
for v in V:
    model.addConstr(quicksum(x[i, v] for i in N) == quicksum(x[j, v] for j in N))

# Binary variable constraints
for i in N:
    for v in V:
        model.addConstr(x[i, v] <= y[v])  # A vehicle can only be assigned to a route if its contractor is assigned

# Optimize
model.optimize()

# Display results
if model.Status == GRB.OPTIMAL:
    print("Optimal solution found:")
    for i in N:
        for v in V:
            if x[i, v].X > 0.5:
                print(f"Node {i} is serviced by Contractor {v}")
    for v in V:
        if y[v].X > 0.5:
            print(f"Contractor {v} is assigned")
else:
    print("No optimal solution found.")
