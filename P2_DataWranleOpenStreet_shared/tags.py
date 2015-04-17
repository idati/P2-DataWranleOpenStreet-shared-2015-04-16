#!/usr/bin/python
import xml.etree.ElementTree as ET
import pprint
import re
from xml.dom import pulldom

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# the function key_type checks what kind of character are used in the dataset, we have 
# three types of character, lower, lower_colon and problemchars
def key_type(element, keys):
    check=0
    if element.tagName == 'tag':
        if lower.findall(element.getAttribute('k')):
            keys['lower']+=1
            check=1
        if lower_colon.findall(element.getAttribute('k')):  
            keys['lower_colon']+=1
            #print element.attrib['k']
            check=1

        if problemchars.findall(element.getAttribute('k')):
            keys['problemchars']+=1
            check=1
        if check==0:
            keys['other']+=1
        pass
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    tree=pulldom.parse(filename)
    for event, node in tree:
        if event==pulldom.START_ELEMENT:
            keys = key_type(node, keys)


    return keys


def test():
    keys = process_map('vienna-bratislava_austria.osm')
    pprint.pprint(keys)

if __name__ == "__main__":
    test() 