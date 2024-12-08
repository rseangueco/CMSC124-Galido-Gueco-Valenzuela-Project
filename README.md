# CMSC124-Galido-Gueco-Valenzuela-Project: LOLCODE Interpreter  

## Program Description  
A lightweight LOLCODE interpreter built in Python, capable of lexically, syntactically, and semantically analyzing LOLCODE files. The interpreter comes with an intuitive GUI that integrates essential tools such as a text editor, symbol table, lexemes table, and a makeshift console for easy testing and debugging.  

---

## Project Features  
- **Lexical Analysis**: Identifies tokens and categorizes them with classifications.  
- **Syntactic Analysis**: Ensures correct LOLCODE syntax structure.  
- **Semantic Analysis**: Validates logic and meaning of LOLCODE statements.  
- **Graphical User Interface (GUI)**:  
  - Integrated text editor for writing LOLCODE programs.  
  - Displays symbol table and lexemes table for better debugging.  
  - Built-in console for output display and error logs.  

---

## Installation Guide  

1. **Download the Project**  
   - Download the `.zip` file of the project and extract it to your desired location.  

2. **Ensure Python is Installed**  
   - Download and install Python from [python.org](https://www.python.org/).  
   - After installation, verify it using the command:  
     ```bash  
     python --version  
     ```  
     or  
     ```bash  
     python3 --version  
     ```  

3. **Ensure Tkinter is Installed**  
   - Tkinter is usually included in standard Python installations. To confirm, run:  
     ```bash  
     python -m tkinter  
     ```  
     or  
     ```bash  
     python3 -m tkinter  
     ```  
   - If Tkinter is not installed, use the following commands based on your operating system:  
     - **Windows**: Reinstall Python and ensure "Tkinter" is selected during installation.  
     - **Linux**:  
       ```bash  
       sudo apt-get install python3-tk  
       ```  
     - **MacOS**: Tkinter should come pre-installed with Python.  

---

## How to Run  

1. Open a terminal.  
2. Navigate to the project directory using:  
   ```bash  
   cd /path/to/project-directory
3. Execute the GUI file:
   ```bash
   python gui.py
   
   # or
   
   python3 gui.py  
