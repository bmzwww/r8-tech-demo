## About
This project provides two solutions to the same Python Developer Recruitment Exercise. The first solution (`advanced.py`) utilizes classes, while the second (`optimized.py`) employs dictionaries with field names.

## How to Start

1. **Clone or Download the Repository**
   - Access the project at [this address](https://github.com/bmzwww/r8-tech-demo/).
   - Clone the repository or download the files.

2. **Install Python**
   - Download and install the latest version of Python.
   - Optionally, set up a separate Python environment to run this app by creating a `.venv` environment with the latest Python version.
   - To activate the virtual environment on Windows, use the following commands:
     - `.\.venv\Scripts\activate.bat`
     - `.\.venv\Scripts\Activate.ps1` (for PowerShell)

3. **Install Dependencies**
   - After installing Python, update the Python packages by running:
     - `pip install -r .\requirements.txt`

4. **Configure Environment Variables**
   - The application uses `demo.env` to read default environmental variables. You can rename `demo.env` to `.env` to override these values.

5. **Run the Application**
   - Use the following commands to start the application:
     - `python run.py`
     - `python .\src\optimized.py` (uses dictionaries with field names)
     - `python .\src\advanced.py` (uses classes)

6. **Run Tests**
   - Project test cases for pytest are located in the `tests` folder. Run them using the command:
     - `pytest`