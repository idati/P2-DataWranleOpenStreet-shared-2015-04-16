import xml.etree.ElementTree as ET
import pprint
import re
import codecs
from xml.dom import pulldom
import json
import pymongo


try:
    conn=pymongo.MongoClient('localhost')
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" %e
conn
from unidecode import unidecode
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


# the function shape_element needs the function toascii.py to cleanup the dataset before
# import to MongoDB, notice the function unidecode is used to transform f.e. ß -> to ss
# the output of the function loos like for example:
#{
#"id": "2406124091",
#"type: "node",
#"visible":"true",
#"created": {
#          "version":"2",
#          "changeset":"17206049",
#          "timestamp":"2013-08-03T16:43:42Z",
#          "user":"linuxUser16",
#          "uid":"1219059"
#        },
#"pos": [41.9757030, -87.6921867],
#"address": {
#          "housenumber": "5157",
#          "postcode": "60625",
#          "street": "North Lincoln Ave"
#        },
#"amenity": "restaurant",
#"cuisine": "mexican",
#"name": "La Cabana De Don Luis",
#"phone": "1 (773)-271-5176"
#}


def shape_element(tree):
    iz=0
    db = conn.lasttry
    collection=db.austria
    node = {}
    logfile=open('tmp.txt', 'w')
    data=list()
    check=0
    last=0
    for event, element in tree:       #new
        if event==pulldom.START_ELEMENT:  #new
	    if (element.tagName=='node' or element.tagName=='way'):
                last=1
            if (element.tagName=='node' or element.tagName=='way') and check==1 and node !={}:
                collection.insert(node)
                node={}
            if element.tagName == "node" or element.tagName == "way":
                node['id']=str(element.getAttribute(str('id')))
                node['type']=str(element.tagName)
                if u'visible' in element.attributes.keys():
                    node['visible']=str(element.getAttribute(('visible')))
                node['created']={'version': str(element.getAttribute((str('version')))), 'changeset':str(element.getAttribute(str('changeset'))),  'timestamp':str(element.getAttribute(str('timestamp'))), 'user': unidecode(element.getAttribute(('user'))), 'uid': str(element.getAttribute(str('uid')))}
                if 'lat' in element.attributes.keys():
                    node['pos']=[float(element.getAttribute('lat')),float(element.getAttribute('lon'))]
             
            check=1
            if element.tagName=='tag':
                if 'k' in element.attributes.keys():
                    if (element.getAttribute('k')=='addr:housenumber'):
                        if 'address' in node and not(node['address'] is None):
                            node['address'].update({'housenumber': unidecode(element.getAttribute('v'))})
                        else:
                            node['address']=({'housenumber': unidecode(element.getAttribute('v'))})
                    if element.getAttribute('k')=='addr:postcode':
                        if 'address' in node and not(node['address'] is None):
                            node['address'].update({'postcode': unidecode(element.getAttribute('v'))})
                        else:
                            node['address']=({'postcode': unidecode(element.getAttribute('v'))})
                    if element.getAttribute('k')=='addr:street':
                        if 'address' in node and not(node['address'] is None):
                            node['address'].update({'street': unidecode((element.getAttribute('v')))})
                        else:
                            node['address']=({'street':unidecode((element.getAttribute('v')))})
                    check=1
                    if element.getAttribute('k')=='amenity':
                        node['amenity']= str(element.getAttribute('v'))
                    if element.getAttribute('k')=='cuisine':
                        node['cuisine']= unidecode(element.getAttribute('v'))
                    if element.getAttribute('k')=='name':                                 
                        node['name']= unidecode(element.getAttribute('v'))
                    if element.getAttribute('k')=='phone':
                        node['phone']= unidecode(element.getAttribute('v'))
            if (element.tagName == "nd"):
                if 'node_refs' in node:
                    node['node_refs'].append(str(element.getAttribute('ref')))
                else:
                    node['node_refs']=[]
                    node['node_refs'].append(str(element.getAttribute('ref')))
    if node !={}:
        collection.insert(node)


def process_map(file_in):
    osm_file = open(file_in, "r")  #new
    tree=pulldom.parse(osm_file)   #new
    shape_element(tree)

def test():
    process_map('__vienna-bratislava_austria.osm')

if __name__ == "__main__":
    test()

