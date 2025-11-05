# gradebook.py
# ANKIT MAITY
# Date: 5 November 2023

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    scores = sorted(marks_dict.values())
    n = len(scores)
    if n % 2 == 0:
        return (scores[n//2 - 1] + scores[n//2]) / 2
    else:
        return scores[n//2]

def find_max_score(marks_dict):
    name = max(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def find_min_score(marks_dict):
    name = min(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def assign_grades(marks_dict):
    grades = {}
    for name, mark in marks_dict.items():
        if mark >= 90:
            grades[name] = 'A'
        elif mark >= 80:
            grades[name] = 'B'
        elif mark >= 70:
            grades[name] = 'C'
        elif mark >= 60:
            grades[name] = 'D'
        else:
            grades[name] = 'F'
    return grades

def count_grades(grades):
    counts = {}
    for g in grades.values():
        counts[g] = counts.get(g, 0) + 1
    return counts

def display_table(marks, grades):
    print("\nName\t\tMarks\tGrade")
    print("-" * 30)
    for name in marks:
        print(f"{name:<10}\t{marks[name]:<5}\t{grades[name]}")
    print("-" * 30)

def main():
    print(" Welcome to the GradeBook Analyzer ")
    print("--------------------------------------")

    while True:
        marks = {}
        n = int(input("\nEnter number of students: "))
        for i in range(n):
            name = input(f"Enter name of student {i+1}: ")
            score = float(input(f"Enter marks of {name}: "))
            marks[name] = score

        
        avg = calculate_average(marks)
        med = calculate_median(marks)
        max_name, max_score = find_max_score(marks)
        min_name, min_score = find_min_score(marks)

        print("\n STATISTICS ")
        print(f"Average Marks: {avg:.2f}")
        print(f"Median Marks: {med}")
        print(f"Highest Score: {max_score} ({max_name})")
        print(f"Lowest Score: {min_score} ({min_name})")

        
        grades = assign_grades(marks)
        counts = count_grades(grades)
        print("\n GRADE DISTRIBUTION ")
        for g, c in counts.items():
            print(f"Grade {g}: {c} student(s)")

        
        passed = [name for name, m in marks.items() if m >= 40]
        failed = [name for name, m in marks.items() if m < 40]

        print("\n Passed Students:", passed)
        print(" Failed Students:", failed)

        print("\n Final Report ")
        display_table(marks, grades)

        again = input("\nDo you want to analyze again? (yes/no): ").lower()
        if again != "yes":
            print("\nThank you for using GradeBook Analyzer! ")
            break

if __name__ == "__main__":
    main()
