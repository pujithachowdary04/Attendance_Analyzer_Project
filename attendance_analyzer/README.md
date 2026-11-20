# Attendance Analyzer

A beginner-friendly Python terminal application based on the supplied StudentLife Hack project brief.

## Features
- Menu-driven terminal interface
- Input validation and duplicate roll-number checks
- Attendance percentage calculation and low-attendance warnings
- Persistent local storage in JSON and CSV
- Student search
- Executive summary
- Matplotlib attendance chart
- CSV bulk import with invalid-row handling

## Requirements
- Python 3.10+
- Matplotlib (only needed for charts)

## Run
1. Extract the ZIP file.
2. Open a terminal in the extracted `attendance_analyzer` folder.
3. Optional: install chart dependency:
   `pip install -r requirements.txt`
4. Start the application:
   `python main.py`

The application creates `data/attendance.json` and `data/attendance.csv` automatically.
The default required attendance threshold is 75%. You can change it from the menu.

## CSV import format
The CSV file must contain these headers:
`roll_no,name,classes_held,classes_attended`
