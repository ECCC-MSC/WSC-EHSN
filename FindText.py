#### Simple script used to search text from multiple python scripts##
import glob
import os
mytext =".xsx.xml"

for file in glob.glob('*.py'):
    with open(file) as f:
        contents = f.read()
    if mytext in contents:
        print file
