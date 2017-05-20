# Split XML containing many <mods> elements into invidual files
# Modified from script found here: http://stackoverflow.com/questions/36155049/splitting-xml-file-into-multiple-at-given-tags
# by Bill Levay for California Historical Society

import lxml.etree as ET
# comment out below modules if working on NEW collections
import codecs, json

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
parser = ET.XMLParser(remove_blank_text=True, remove_comments=True)
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

# getting islandora IDs for existing collections
# comment this out if preparing to ingest new collections!
item_list = []

with codecs.open('C:\\mods\\wagner\\data.json', encoding='utf-8') as filename:
    item_list = json.load(filename)

#close the file
filename.close

# find the <mods> nodes
for event, elem in cleanxml:
    if elem.tag == '{http://www.loc.gov/mods/v3}mods':

        # the filenames of the resulting xml files will be based on the <identifier> element
        identifier = elem.find('{http://www.loc.gov/mods/v3}identifier').text
        # filename = format(identifier + ".xml")

        # look through the list of object metadata and get the islandora ID by matching the digital object ID
        # comment this out if preparing to ingest new collections and use the filenaming line above instead
        for item in item_list:
            local_ID = item['identifier-type:local']
            islandora_ID = item['PID']

            if identifier == local_ID:
                filename = format(islandora_ID + ".xml")

        # write out to new file
        with open(filename, 'wb') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write(ET.tostring(elem, pretty_print = True))
        print "Writing", filename
print "All done!"