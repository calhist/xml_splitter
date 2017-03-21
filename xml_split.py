# Split XML containing many <mods> elements into invidual files
# Modified from script found here: http://stackoverflow.com/questions/36155049/splitting-xml-file-into-multiple-at-given-tags

import lxml.etree as ET 

# parse source.xml with lxml
tree = ET.parse('source.xml')

# start cleanup
# remove any element tails
for element in tree.iter():
    element.tail = None

# remove any line breaks or tabs in element text
    if element.text:
        if '\n' in element.text:
            element.text = element.text.replace('\n', '') 
        if '\t' in element.text:
            element.text = element.text.replace('\t', '')

# remove any remaining whitespace
parser = ET.XMLParser(remove_blank_text=True)
treestring = ET.tostring(tree)
clean = ET.XML(treestring, parser)

# remove empty nodes
for element in tree.xpath(".//*[not(node())]"):
	element.getparent().remove(element)

# remove nodes with text "null"
for element in tree.xpath(".//*[text()='null']"):
	element.getparent().remove(element)

# remove nodes with attribute "null"
for element in tree.xpath(".//*[@*='null']"):
    element.getparent().remove(element)

# finished cleanup
# write out to intermediate file
with open('clean.xml', 'wb') as f:
    f.write(ET.tostring(clean))
print "XML is now clean"

# parse the clean xml
cleanxml = ET.iterparse('clean.xml', events=('end', ))

# find the <mods> nodes
for event, elem in cleanxml:
    if elem.tag == '{http://www.loc.gov/mods/v3}mods':

        # the filenames of the resulting xml files will be based on the <identifier> element
        title = elem.find('{http://www.loc.gov/mods/v3}identifier').text
        filename = format(title + ".xml")

        # write out to new file
        with open(filename, 'wb') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write(ET.tostring(elem, pretty_print = True))
        print "Writing", filename
print "All done!"