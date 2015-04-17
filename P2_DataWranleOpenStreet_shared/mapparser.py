#!/usr/bin/python
import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict  
from xml.etree.ElementTree import iterparse  #like in course
from xml.dom import pulldom                  #used variante - better performance

# the function count_tags counts all different tags in the dataset
def count_tags(filename):
    tags={}
    tree=pulldom.parse(filename)  
    for event, node in tree:
        if event==pulldom.START_ELEMENT: 
            if node.tagName in tags:
                tags[node.tagName]+=1
            else:
                tags[node.tagName]=1


   # tree=ET.parse(filename)
    #for elem in iterparse(filename):
    #    tree=ET.parse(elem)
    #    print tree.getroot() 
       # if elem[1].tag in tags:
       #     tags[elem[1].tag]+=1
       # else:
       #     tags[elem[1].tag]=1
           
    return tags


def test():
    tags=count_tags('vienna-bratislava_austria.osm')
    pprint.pprint(tags)


if __name__ == "__main__":
    test()