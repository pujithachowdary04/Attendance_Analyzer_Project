import csv
import json
import os
from statistics import mean

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "attendance.csv")
JSON_FILE = os.path.join(DATA_DIR, "attendance.json")
CHART_FILE = "attendance_chart.png"
DEFAULT_THRESHOLD = 75.0

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["roll_no", "name", "classes_held", "classes_attended"])
            writer.writeheader()
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

def load_records():
    ensure_files()
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            print("Warning: JSON data format is invalid. Starting with an empty list.")
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read JSON data. Starting with an empty list.")
    return []

def save_records(records):
    ensure_files()
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        fields = ["roll_no", "name", "classes_held", "classes_attended"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in records:
            writer.writerow({key: r.get(key, "") for key in fields})

def read_int(prompt, minimum=0, maximum=None):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number < minimum or (maximum is not None and number > maximum):
                print(f"Enter a number from {minimum} to {maximum if maximum is not None else 'above'}.")
                continue
            return number
        except ValueError:
            print("Please enter a valid whole number.")

def attendance_percent(record):
    held = record["classes_held"]
    return (record["classes_attended"] / held * 100) if held else 0.0

def add_record(records):
    print("\n--- Add Student Attendance ---")
    roll = input("Roll number: ").strip()
    if not roll:
        print("Roll number cannot be blank.")
        return
    if any(r["roll_no"].lower() == roll.lower() for r in records):
        print("A student with this roll number already exists.")
        return
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be blank.")
        return
    held = read_int("Total classes held: ", 1)
    attended = read_int("Classes attended: ", 0, held)
    records.append({
        "roll_no": roll,
        "name": name,
        "classes_held": held,
        "classes_attended": attended
    })
    save_records(records)
    print("Attendance record saved successfully.")

def show_records(records, threshold):
    print("\n--- Attendance Records ---")
    if not records:
        print("No records found.")
        return
    print(f"{'Roll No':<12} {'Name':<22} {'Held':>6} {'Attended':>9} {'Percent':>9} {'Status':>12}")
    print("-" * 76)
    for r in records:
        pct = attendance_percent(r)
        status = "LOW" if pct < threshold else "OK"
        print(f"{r['roll_no']:<12} {r['name'][:21]:<22} {r['classes_held']:>6} "
              f"{r['classes_attended']:>9} {pct:>8.2f}% {status:>12}")

def search_records(records):
    keyword = input("Enter roll number or student name to search: ").strip().lower()
    matches = [r for r in records if keyword in r["roll_no"].lower() or keyword in r["name"].lower()]
    if not matches:
        print("No matching students found.")
    else:
        show_records(matches, DEFAULT_THRESHOLD)

def summary(records, threshold):
    print("\n--- Executive Summary ---")
    if not records:
        print("No attendance data available.")
        return
    percentages = [attendance_percent(r) for r in records]
    low = [r for r in records if attendance_percent(r) < threshold]
    print(f"Students recorded       : {len(records)}")
    print(f"Average attendance     : {mean(percentages):.2f}%")
    print(f"Students below {threshold:.0f}%      : {len(low)}")
    print(f"Students meeting target : {len(records) - len(low)}")
    if low:
        print("\nStudents requiring attention:")
        for r in low:
            print(f"- {r['name']} ({r['roll_no']}): {attendance_percent(r):.2f}%")

def plot_chart(records):
    if not records:
        print("No data available to plot.")
        return
    try:
        import matplotlib.pyplot as plt
        names = [r["name"] for r in records]
        values = [attendance_percent(r) for r in records]
        plt.figure(figsize=(10, 5))
        plt.bar(names, values)
        plt.axhline(DEFAULT_THRESHOLD, linestyle="--", label=f"{DEFAULT_THRESHOLD:.0f}% threshold")
        plt.ylabel("Attendance (%)")
        plt.title("Student Attendance Analysis")
        plt.ylim(0, 105)
        plt.xticks(rotation=35, ha="right")
        plt.legend()
        plt.tight_layout()
        plt.savefig(CHART_FILE)
        plt.close()
        print(f"Chart saved as {CHART_FILE}")
    except ImportError:
        print("Matplotlib is not installed. Run: pip install -r requirements.txt")

def import_csv(records):
    path = input("CSV file path to import: ").strip()
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            added = 0
            for row in reader:
                try:
                    roll = row["roll_no"].strip()
                    name = row["name"].strip()
                    held = int(row["classes_held"])
                    attended = int(row["classes_attended"])
                    if not roll or not name or held <= 0 or attended < 0 or attended > held:
                        raise ValueError
                    if any(r["roll_no"].lower() == roll.lower() for r in records):
                        continue
                    records.append({"roll_no": roll, "name": name,
                                    "classes_held": held, "classes_attended": attended})
                    added += 1
                except (KeyError, ValueError, TypeError):
                    print(f"Skipped invalid row: {row}")
        save_records(records)
        print(f"Imported {added} valid record(s).")
    except OSError as e:
        print(f"Could not open file: {e}")

def main():
    ensure_files()
    records = load_records()
    threshold = DEFAULT_THRESHOLD
    while True:
        print("\n========== ATTENDANCE ANALYZER ==========")
        print(f"Required attendance threshold: {threshold:.0f}%")
        print("1. Add attendance record")
        print("2. View all records")
        print("3. Search student")
        print("4. Executive summary")
        print("5. Generate attendance chart")
        print("6. Import records from CSV")
        print("7. Change attendance threshold")
        print("8. Exit")
        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            add_record(records)
        elif choice == "2":
            show_records(records, threshold)
        elif choice == "3":
            search_records(records)
        elif choice == "4":
            summary(records, threshold)
        elif choice == "5":
            plot_chart(records)
        elif choice == "6":
            import_csv(records)
        elif choice == "7":
            try:
                new_value = float(input("Enter threshold percentage (1-100): ").strip())
                if 1 <= new_value <= 100:
                    threshold = new_value
                else:
                    print("Threshold must be between 1 and 100.")
            except ValueError:
                print("Enter a valid number.")
        elif choice == "8":
            print("Thank you for using Attendance Analyzer!")
            break
        else:
            print("Invalid option. Please choose 1-8.")

if __name__ == "__main__":
    main()
