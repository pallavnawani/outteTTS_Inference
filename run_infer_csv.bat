@echo off
REM Activate the virtual environment (adjust the path to your environment if necessary)
call env\Scripts\activate.bat

REM Run the Python script with the CSV file as an argument
python infer_csv.py --csv_file outtsinput.csv

REM Deactivate the virtual environment
call deactivate
