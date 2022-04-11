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
xhtml2pdf (version 0.2.5)  

See requirements.txt for full package list.  
Note: An older version of wxPython (4.0.7) is required as later versions cause an error related to unknown locales.  
Note: The pytz and pyRFC3339 packages are also required to properly use the Aquarius Python Wrapper created by Doug Schmidt.  

# EXCLUDED FILES

This repository does not include the Rating Extraction Tool which extracts data from Aquarius as we have agreed with Aqutic Informatics not to distribute it at this time.

Rating curves can still be exported manually from Aquarius and imported using the provided sample format.

# CONFIGURATION FILE

A configuration file template (config.xml) is included in which you can specify: Aquarius Server and Login Information for some
# RUNNING IT

Once the environment is created, the file 1_ElectronicFieldNotes.py runs the program.
# COMPILING IT

We use pyinstaller but of course you can use whatever you like.

If using pyinstaller to create a testing exe, navigate to your local clone of WSC-EHSN and use the command:   
pyinstaller create_ehsn_exe.spec  

This will create a single executable in the "dist" folder called WSC_eHSN_Python_test.exe with all required files included.  
If your virtual environment where the packages are installed is not called 'env', then you must modify the pathex variable in create_ehsn_exe.spec.  
You will have to copy the Aquarius Python Wrapper code (timeseries_client.py) created by Doug Schmidt into your local clone of WSC-EHSN as well.  


# MANUAL

User manual is available upon request.
