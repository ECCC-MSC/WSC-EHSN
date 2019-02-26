# WSC-EHSN
# LICENSE

All works in this repository have been curated by ECCC and licensed under the GNU General Public License v3.0. Read more: https://www.gnu.org/licenses/gpl-3.0.en.html

# ENVIRONMENT

Python 2.7.14

Packages:  
wxpython (this is the pheonix version)  
matplotlib  
requests  
qrcode  
lxml  
html2pdf (version 0.0.6)  
suds-jurko (version 0.7)  
html5lib (version 1.0b8)

Upon downloading the repository, execute the following command to install all python modules: pip install -r requirements.txt  

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
