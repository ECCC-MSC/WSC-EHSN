# WSC-EHSN
# LICENSE

All works in this repository have been curated by ECCC and licensed under the GNU General Public License v3.0. Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

# ENVIRONMENT

Python 3.8.2

Packages:  
wxPython (Phoenix, version 4.0.7)  
matplotlib (version 3.5.1)  
requests (version 2.27.1)  
qrcode (version 7.3.1)  
lxml (version 4.7.1)  
suds-jurko (version 0.6)  
XlsxWriter (version 3.0.2)  
pywin32 (version 303)  
reportlab (version 3.6.5)  
PyQt5 (version 5.15.6)  
PyQtWebEngine (version 5.15.5)  

See requirements.txt for full package list.  
Note: An older version of wxPython (4.0.7) is required as later versions cause an error related to unknown locales.  
Note: The most up-to-date version of pip (22.0.2 or higher) is required to download PyQt5 sucessfully.

# EXCLUDED FILES

This repository does not include the Rating Extraction Tool which extracts data from Aquarius as we have agreed with Aqutic Informatics not to distribute it at this time.

Rating curves can still be exported manually from Aquarius and imported using the provided sample format.

# CONFIGURATION FILE

A configuration file template (config.xml) is included in which you can specify: Aquarius Server and Login Information for some
# RUNNING IT

Once the environment is created, the file 1_ElectronicFieldNotes.py runs the program.
# COMPILING IT

We use pyinstaller but of course you can use whatever you like.

If using pyinstaller, navigate to your local clone of WSC-EHSN and use the command:   
pyinstaller 1_ElectronicFieldNotes.py  

Move the image files:  
"downarrow.png"  
"backarrow.png"  
"icon_transparent.ico"   
into the "1_ElectronicFieldNotes" folder (found in the newly created "dist" folder)

You can now run the program using 1_ElectronicFieldNotes.exe
# MANUAL

User manual is available upon request.
