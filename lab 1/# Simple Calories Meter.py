

print(" Daily Calorie Tracker")

meals = []  
calories = []

while True:
    meal = input("\nEnter meal name (or type 'done' to finish): ")
    if meal.lower() == "done":
        break
    cal = float(input("Enter calories for this meal: "))
    meals.append(meal)
    calories.append(cal)

total = sum(calories)
average = total / len(calories)

limit = 2000
if total > limit:
    print("\n⚠️ Warning: You exceeded your daily limit of", limit, "calories!")

print("\n----- Summary Report -----")
for m, c in zip(meals, calories):
    print(f"{m:15} : {c} kcal")

print(f"\nTotal Calories  : {total} kcal")
print(f"Average per meal: {average:.2f} kcal")

with open("calorie_log.txt", "w") as f:
    f.write("Daily Calorie Tracker Log\n")
    for m, c in zip(meals, calories):
        f.write(f"{m}: {c} kcal\n")
    f.write(f"\nTotal: {total} kcal\nAverage: {average:.2f} kcal\n")

print("\nData saved to 'calorie_log.txt'")
