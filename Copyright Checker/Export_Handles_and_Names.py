import os
import re
import xml.etree.ElementTree as ET

dir = 'MODS'

modsFiles = os.listdir( dir )

ns = {'m': 'http://www.loc.gov/mods/v3' }

with open ('handles_and_names.csv', 'w') as csv:

    for m in modsFiles:
        if re.search( 'xml$' , m ):

            record = dict()

            tree = ET.parse( os.path.join( dir, m ) )
            root = tree.getroot()
            #print(root)

            findElement = root.find('m:name/m:namePart' , ns )
            if findElement is not None:
                record['name'] = findElement.text

            findElement = root.find('m:identifier[@type="hdl"]' , ns )
            if findElement is not None:
                record['URI'] = findElement.text

            if 'name' in record:
                csv.write( f"{ record['URI'] },\"{ record['name'] }\"\n" )
