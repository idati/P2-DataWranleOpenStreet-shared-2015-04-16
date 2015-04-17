#!/usr/bin/python
import xml.etree.ElementTree as ET
import pprint
import re
from xml.dom import pulldom

def get_user(element):
    return

# the function process_map checks the number of nodes, relation ands ways in the dataset
def process_map(filename):
    users = set()
    tree=pulldom.parse(filename)
    for event, node in tree:
        if event==pulldom.START_ELEMENT:
            if node.tagName=='node' or node.tagName=='relation'or node.tagName=='way':
                users|={int(node.getAttribute('uid'))}


#   for _, element in ET.iterparse(filename):
#        #print element.findall('tag')
#        if element.tag=='node' or element.tag=='relation'or element.tag=='way':
#            users|={element.attrib['uid']}
#        element.clear()
        pass

    return users



def test():

    users = process_map('vienna-bratislava_austria.osm')
    pprint.pprint(users)
    logFile=open('mylogfile.txt', 'w')
    pprint.pprint(users, logFile)
#    assert len(users) == 6



if __name__ == "__main__":
    test()
