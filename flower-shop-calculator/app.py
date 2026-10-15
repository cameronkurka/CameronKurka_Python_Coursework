# Constants
BOUQUET_COST = 17.00
EXTRA_FLOWER_COST = 0.35
TIP_EXPENSE = 0.15
SALES_TAX = 0.18

# Prompt user for the number of bouquets purchased
bouquets = int(input("How many bouquets were purchased? "))

# Prompt user for the number of extra flowers
extras = int(input("How many extra flowers were added? "))

# Calculate costs
total_bouquet_cost = bouquets * BOUQUET_COST
total_extra_flower_cost = extras * EXTRA_FLOWER_COST

# Calculate total
total_order_cost = (1+ TIP_EXPENSE)* (total_bouquet_cost + total_extra_flower_cost) + (bouquets * SALES_TAX)

print("The total cost of the order is:",total_order_cost)

