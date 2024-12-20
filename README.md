
README: MySQL Backup Tool
This project is a Python-based MySQL backup tool with a graphical user interface (GUI) built using the tkinter library. The tool allows users to back up their MySQL database at specified intervals.

Requirements
Python Version:
Ensure you have Python 3.12 installed on your system.
Download Python

Required Python Libraries:
The following libraries are required to run the application. Install them using pip:

mysql-connector-python
tkinter (comes pre-installed with Python)
Installation
Clone or Download the Repository:

git clone https://github.com/your-repo/mysql-backup-tool.git
cd mysql-backup-tool
Install Dependencies:
Run the following command to install the required libraries:

pip install mysql-connector-python
Verify Python Version:
Ensure you are running the correct version of Python:

python --version
Run the Application:
Execute the script using the following command:

python backup_tool.py
Features
Backup Scheduling: Automatically back up your database at specified intervals.
Graphical Interface: Easy-to-use GUI for configuring the backup process.
Dynamic Backup: Save database tables and data into a .sql file.
Usage
Input Configuration:

Enter your MySQL host, username, password, and database name in the corresponding fields.
Select a directory to save the backup files.
Specify the backup interval in seconds.
Start Backup:
Click the Start Backup button to initiate the process. The tool will run in the background and create backups at the defined interval.

Troubleshooting
MySQL Connection Error:
Ensure the MySQL server is running and your credentials are correct.

Permission Error:
Verify that the selected backup directory has write permissions.

Library Import Errors:
Ensure all required libraries are installed. Reinstall them using:

pip install mysql-connector-python
Contributing
Feel free to fork this repository and contribute. Pull requests are welcome!

License
This project is licensed under the MIT License.
