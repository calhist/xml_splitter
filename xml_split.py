# Split XML containing many <mods> elements into invidual files
# Modified from script found here: http://stackoverflow.com/questions/36155049/splitting-xml-file-into-multiple-at-given-tags

import xml.etree.ElementTree as ET

# register the namespaces
ET.register_namespace('', "http://www.loc.gov/mods/v3")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
ET.register_namespace('xsi:schemaLocation', "http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd")

# parse
context = ET.iterparse('source.xml', events=('end', ))

for event, elem in context:
    if elem.tag == '{http://www.loc.gov/mods/v3}mods':

        # the filenames of the resulting xml files will be based on the <identifier> element
        title = elem.find('{http://www.loc.gov/mods/v3}identifier').text
        filename = format(title + ".xml")
        with open(filename, 'wb') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write(ET.tostring(elem))
        print "Writing", filename
print "All done"