products = {"Bubblegum": 202, "Toffee": 118, "Ice cream": 2250, "Milk chocolate": 1680, "Doughnut": 1075,
         "Pancake": 80}

print("Earned amount:")

for item in products:
    print(f"{item}: ${products[item]}")

print()
total_revenue = sum(products.values())
print(f"Income: ${total_revenue}")

staff_expenses = int(input("Staff expenses: \n"))
other_expenses = int(input("other expenses: \n"))

print(f"Net income: ${total_revenue - staff_expenses - other_expenses}")
