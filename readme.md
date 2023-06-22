

**Step 1: Install Python**
- Make sure Python is installed on your system. You can download the latest version of Python from the official website: https://www.python.org/downloads/

**Step 2: Install the Required Packages**
- Open a command prompt or terminal.
- Run the following command to install the required packages:
  ```
  pip install PyPDF2
  ```

**Step 3: Verify tkinter Installation (Windows and macOS)**
- Open a command prompt or terminal.
- Run the following command to check if tkinter is installed:
  ```
  python -m tkinter
  ```
  - If tkinter is already installed, a separate Python shell window will open and you can close it.
  - If tkinter is not installed, you'll receive an error message like `'No module named '_tkinter'`.

**Step 4: Install tkinter (if necessary)**
- Follow the instructions below based on your operating system:

  **For Windows:**
  - Open Command Prompt or PowerShell.
  - Run the following command to install tkinter:
    ```
    py -m pip install tkinter
    ```

  **For macOS:**
  - Open Terminal.
  - Run the following command to install tkinter using Homebrew:
    ```
    brew install python-tk
    ```

  **For Linux:**
  - Open a terminal.
  - Install tkinter using the package manager specific to your distribution. For example, on Ubuntu, run the following command:
    ```
    sudo apt-get install python3-tk
    ```
    Use the appropriate package manager for your Linux distribution.

**Step 5: Save the Script**
- Copy the provided Python script (mentioned in the previous response) and save it in a file with a `.py` extension, such as `pdf_filter.py`.

**Step 6: Run the Script**
- Open a command prompt or terminal.
- Navigate to the directory where you saved the `pdf_filter.py` script.
- Run the following command to execute the script:
  ```
  python pdf_filter.py
  ```

**Step 7: Use the GUI**
- The GUI window will appear.
- Click the "Browse" button to select a folder containing PDF files.
- Enter keywords separated by commas in the "Enter Keywords" field.
- Click the "Process Files" button to perform the filtering operation.
- The inclusion and exclusion files will be displayed in the respective sections of the GUI window.

That's it! You have successfully installed and executed the PDF file filtering script with a GUI using tkinter.