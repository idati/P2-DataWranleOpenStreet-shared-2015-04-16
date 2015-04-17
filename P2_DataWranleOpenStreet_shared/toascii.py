from unidecode import unidecode
import codecs
# the function toascii exclude all problematic signs from the dataset that could
# create problems for importing into MongoDB, function toascii.py has to run before data.py
# can be started
def toascii():
    z=0
    with open(r'C:\Python27\vienna-bratislava_austria.osm', 'r') as origfile, open(r'C:\Python27\__vienna-bratislava_austria.osm', 'w') as convertfile: 
        for line in origfile:
            if (z>=0):
                line=unidecode(line.decode('utf-8'))
                line=line.replace('n""/','n"/')
                line=line.replace('>>','')
                line=line.replace('<<','')
                line=line.replace(' "K',' K')
                line=line.replace('i""','i"')
                line=line.replace('m""','m"')
                line=line.replace('e""','e"')
                line=line.replace('g""','g"')
                line=line.replace('`s"C','s C')
                line=line.replace('d" i','d i')
                line=line.replace('&amp;','und')
                line=line.replace('e "A','e A')
                line=line.replace(',,','')

                convertfile.write(line)

            z=z+1


if __name__ == "__main__":
    toascii()
