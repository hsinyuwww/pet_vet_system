# PetVet Portal System - Installation Guide

### Required Software
1. MySQL Server & Tools
   - Version: 8.0 or later
   - Download: https://dev.mysql.com/downloads/mysql/
   - Components needed:
     * MySQL Server
     * MySQL Workbench
   - Default installation paths:
     * Windows: C:\Program Files\MySQL\MySQL Server 8.0\
     * macOS: /usr/local/mysql/
     * Linux: /var/lib/mysql/

2. Python
   - Version: 3.8 or later
   - Download: https://www.python.org/downloads/
   - Installation verification:
     ```bash
     python --version
     ```
   - Default installation paths:
     * Windows: C:\Users\YourUsername\AppData\Local\Programs\Python\
     * macOS: /usr/local/bin/python3
     * Linux: /usr/bin/python3

### Required Python Libraries
#### Built-in Libraries
The following libraries are included with Python installation:
```python
import datetime  # For date and time handling
import sys      # For system-specific parameters
```

#### External Libraries
Install the following using pip:
```python
pip install mysql-connector-python==8.0.32
pip install pandas==1.5.3
pip install ipython==8.12.0
```
