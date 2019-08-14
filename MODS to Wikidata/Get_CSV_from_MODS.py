import os
import re
import xml.etree.ElementTree as ET

dir = 'MODS'

modsFiles = os.listdir( dir )

ns = {'m': 'http://www.loc.gov/mods/v3' }

with open ('tmp.csv', 'w') as csv:

    csv.write( f"Handle,Title,Name,Shelfmark,Collection,Date,Topic,Geographic\n")

    for m in modsFiles:
           if re.search( 'xml$' , m ):

            record = dict()

            tree = ET.parse( os.path.join( dir, m ) )
            root = tree.getroot()
            #print(root)



            findElement = root.find('m:titleInfo/m:nonSort' , ns )
            if findElement is not None:
                record['nonSort'] = findElement.text

            findElement = root.find('m:titleInfo/m:title' , ns )
            if findElement is not None:
                record['title'] = findElement.text

            findElement = root.find('m:name/m:namePart' , ns )
            if findElement is not None:
                record['name'] = findElement.text

            findElement = root.find('m:identifier[@type="hdl"]' , ns )
            if findElement is not None:
                record['URI'] = findElement.text

                csv.write( f"{ record['URI'] },\"{ record['title'] }\",")


                if 'name' in record:
                    csv.write( f"\"{ record['name'] }\",")

                elif 'name' not in record:
                    csv.write( f",")

                findElement = root.find('m:relatedItem/m:identifier' , ns )
                if findElement is not None:
                    record['shelfmark'] = findElement.text
                    csv.write( f"\"{ record['shelfmark'] }\",Leiden University Library,")

                findElement = root.find('m:relatedItem/m:originInfo/m:publisher' , ns )
                if findElement is not None:
                    record['date'] = findElement.text
                    csv.write( f"\"{ record['date'] }\",")



                    #subject = dict()

                    for subjecttopic in root.findall('./m:subject/m:topic' , ns ):
                        record['topic'] = subjecttopic.find('./m:topic' , ns )
                        record['topic'] = subjecttopic.text
                        csv.write (f"{record['topic']},")
                        csv.write (f"\n,,,,,,")

                    csv.write (f"\n")

                    for geotopic in root.findall('./m:subject/m:geographic' , ns ):
                        record['geographic'] = geotopic.find('./m:geographic' , ns )
                        record['geographic'] = geotopic.text
                        csv.write (f",,,,,,,{record['geographic']},")
                        csv.write (f"\n")



                    csv.write (f"\n")

import csv

with open('tmp.csv') as in_file:
    with open('CSV_from_MODS.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if any(row):
                writer.writerow(row)

os.remove("tmp.csv")
