from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

import sys
import os
from os import chdir
from os.path import dirname


class Test():
    def __init__(self, *args, **kwargs):
        chdir(dirname(sys.argv[0]))
        # determine if application is a script file or frozen exe
        config_path = "config.xml"
        # os.path.dirname(os.path.realpath(sys.argv[0]))
        print os.getcwd()
        if hasattr(sys, '_MEIPASS'):
            config_path = os.path.join(sys._MEIPASS, config_path)
        else:
            config_path = os.getcwd() + "\\" + config_path

        print config_path    
        configFile = ElementTree.parse(config_path).getroot()


        stage1 = configFile.find('stage1').text
        product2 = configFile.find('product2').text
        product = configFile.find('product').text
        #         self.TitleHeaderFromXML(TitleHeader)
        # enteredInHWSCB = TitleHeader.find('enteredInHWS').text
        #     titleHeaderManager.enteredInHWSCB = False if enteredInHWSCB is None else (False if enteredInHWSCB == "False" else True)

        print stage1
        print product2
        print product


def main():
    Test()

if __name__ == '__main__':
    main()