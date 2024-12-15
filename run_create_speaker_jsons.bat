@echo off
REM Activate the virtual environment
call env\Scripts\activate

REM Execute the Python script
python create_speaker_jsons.py

REM Deactivate the virtual environment
call deactivate
