# co370-final-project
CO370 Fall 2024 Final Project

demand.csv
\nThis file contains the demand parameters (Di) for each node:
\nnode_id: Represents both demand nodes (Nd) and hospital nodes (H)
\ndemand: The quantity needed at each location
\nRegular nodes (0-4) have positive demand values
\nHospital nodes (5-6) have zero demand as they are service points

contractors.csv
This file combines several parameters for each contractor (C):
contractor_id: Unique identifier for each contractor
fixed_cost: The Fi parameter representing fixed cost for using a contractor
cost_rate: The Gi parameter for cost per unit
capacity: The CCi parameter showing contractor's total capacity
vehicle_capacity: The CVi parameter indicating how much each vehicle can carry
risk_score: The Ri parameter representing risk exposure score

distances.csv
This file contains the distance matrix (Aij) showing:
node_id: Source location (includes both demand nodes and hospitals)
contractor_id: Destination contractor
distance: The Aij parameter representing distance between node i and contractor j
This matrix is used in the distance constraint ensuring routes don't exceed maximum allowed distance M
