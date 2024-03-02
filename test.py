from itertools import combinations

# Data
drivers = [
    {"name": "VER", "cost": 30, "points": 1014},
    {"name": "GAS", "cost": 7.8, "points": 230},
    {"name": "PER", "cost": 20.8, "points": 579},
    {"name": "HAM", "cost": 19.3, "points": 506},
    {"name": "ALO", "cost": 15.8, "points": 403},
    {"name": "STR", "cost": 10.7, "points": 231},
    {"name": "SAI", "cost": 18.5, "points": 394},
    {"name": "RUS", "cost": 18.8, "points": 384},
    {"name": "NOR", "cost": 23, "points": 438},
    {"name": "ALB", "cost": 7, "points": 126},
    {"name": "LEC", "cost": 19.1, "points": 335},
    {"name": "OCO", "cost": 7.8, "points": 120},
    {"name": "PIA", "cost": 19, "points": 279},
    {"name": "RIC", "cost": 9, "points": 90}
]

constructors = [
    {"name": "Red Bull", "cost": 27.9, "points": 1847},
    {"name": "Mercedes", "cost": 20.1, "points": 1060},
    {"name": "Ferrari", "cost": 19.3, "points": 1007},
    {"name": "Mclaren", "cost": 23.2, "points": 899},
    {"name": "Aston Martin", "cost": 13.6, "points": 757},
    {"name": "Alpine", "cost": 8.4, "points": 467},
    {"name": "Williams", "cost": 6.3, "points": 151},
    {"name": "Sauber", "cost": 6.6, "points": 222},
    {"name": "RB", "cost": 8.5, "points": 308},
    {"name": "Haas", "cost": 6.3, "points": 215}
]

# Budget
budget = 100

# Function to calculate the score and cost of a combination
def calculate_score_and_cost(driver_combo, constructor_combo):
    total_cost = sum(d['cost'] for d in driver_combo) + sum(c['cost'] for c in constructor_combo)
    total_points = sum(d['points'] for d in driver_combo) + sum(c['points'] for c in constructor_combo)
    
    # Double the points of the highest-scoring driver
    highest_scoring_driver_points = max(d['points'] for d in driver_combo)
    total_points += highest_scoring_driver_points
    
    return total_cost, total_points

# Search for the best combination
best_score = 0
best_combination = None

for driver_combo in combinations(drivers, 5):
    for constructor_combo in combinations(constructors, 2):
        total_cost, total_points = calculate_score_and_cost(driver_combo, constructor_combo)
        
        if total_cost <= budget and total_points > best_score:
            best_score = total_points
            best_combination = (driver_combo, constructor_combo)

# Extract names for readability
best_drivers = [d['name'] for d in best_combination[0]]
best_constructors = [c['name'] for c in best_combination[1]]

print(best_drivers, best_constructors, best_score)
