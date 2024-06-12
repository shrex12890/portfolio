from pulp import LpMinimize, LpProblem, LpVariable, lpSum
from itertools import combinations_with_replacement

# Define lengths and quantities
lengths = [3650, 4200, 4900, 5700, 7300, 7800, 8300, 9500, 11650]
quantities = [140, 128, 140, 64, 224, 176, 224, 256, 272]
bar_length = 12000

# Define the problem
problem = LpProblem("Cutting_Stock", LpMinimize)

# Generate patterns and variables
patterns = []
variables = []

# Generate all feasible cutting patterns
for i in range(1, len(lengths) + 1):
    for combo in combinations_with_replacement(lengths, i):
        if sum(combo) <= bar_length:
            patterns.append(combo)

# Create a variable for each pattern
for i, pattern in enumerate(patterns):
    variables.append(LpVariable(f'pattern_{i}', lowBound=0, cat='Integer'))

# Add objective function to minimize the number of bars
problem += lpSum(variables)

# Add constraints to meet the required quantities
for j, length in enumerate(lengths):
    problem += lpSum(variables[i] * patterns[i].count(length) for i in range(len(patterns))) >= quantities[j]

# Solve the problem
problem.solve()

# Output the results
total_bars_used = sum(var.varValue for var in variables)
total_wastage = total_bars_used * bar_length - sum(sum(pattern) * var.varValue for pattern, var in zip(patterns, variables))
print(f"Total bars used: {total_bars_used}")
print(f"Total wastage: {total_wastage}")

for var in variables:
    if var.varValue > 0:
        pattern_index = int(var.name.split('_')[1])
        print(f"{var.name}: {var.varValue}, Pattern: {patterns[pattern_index]}")
