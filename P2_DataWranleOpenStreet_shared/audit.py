#!/usr/bin/python
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from xml.dom import pulldom
import codecs

OSMFILE = "vienna-bratislava_austria.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road","Trail", "Parkway", "Commons"]


mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road"
            }
# the used dataset (german and slovacian language) we cannot find this kind of problems
# shortcuts of street names but we have the problem that the dataset uses ä, ü, ...
# in the function audit_street_type we change that f.e. from ä -> a
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[str(street_type.encode('utf8'))].add(str(street_name.encode('utf8')))


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    tree=pulldom.parse(osm_file)
    for event, node in tree:
        if event==pulldom.START_ELEMENT:
            if node.tagName == "tag":
                if node.getAttribute('k')=="addr:street":
                    audit_street_type(street_types, node.getAttribute('v'))
           
    return street_types


def update_name(name, mapping):
    tmp=[]
    tmp=name.split(' ')
    tmp[-1]= mapping[name.split(' ')[-1]]
    name=  " ".join(tmp )

    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    logFile=open('streetname_v2.txt','w')
    pprint.pprint(dict(st_types),logFile)


if __name__ == '__main__':
    test() 