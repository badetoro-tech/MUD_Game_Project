@ECHO OFF

:: Activating Virtual Environment
py -m venv venv
venv\Scripts\activate

:: Installing packages if required
py -m pip install -r requirements.txt

:: Running the main program
python main.py
