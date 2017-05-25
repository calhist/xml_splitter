# Split XML containing many <mods> elements into invidual files
# Modified from script found here: http://stackoverflow.com/questions/36155049/splitting-xml-file-into-multiple-at-given-tags
# by Bill Levay for California Historical Society

import lxml.etree as ET
# uncomment below modules if doing MODS cleanup on existing Islandora objects
# import codecs, json

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
parser = ET.XMLParser(remove_blank_text=True, remove_comments=True, recover=True)
treestring = ET.tostring(tree)
clean = ET.XML(treestring, parser)

# remove recursively empty nodes
# found here: https://stackoverflow.com/questions/12694091/python-lxml-how-to-remove-empty-repeated-tags
def recursively_empty(e):
   if e.text:
       return False
   return all((recursively_empty(c) for c in e.iterchildren()))

context = ET.iterwalk(clean)
for action, elem in context:
    parent = elem.getparent()
    if recursively_empty(elem):
        parent.remove(elem)

# remove nodes with blank attribute
for element in clean.xpath(".//*[@*='']"):
    element.getparent().remove(element)

# remove nodes with attribute "null"
for element in clean.xpath(".//*[@*='null']"):
    element.getparent().remove(element)

# finished cleanup
# write out to intermediate file
with open('clean.xml', 'wb') as f:
    f.write(ET.tostring(clean))
print "XML is now clean"

# parse the clean xml
cleanxml = ET.iterparse('clean.xml', events=('end', ))

###
# uncomment this section if doing MODS cleanup on existing Islandora objects
# getting islandora IDs for existing collections
# item_list = []

# json_path = 'C:\\mods\\maps\\data.json'

# with codecs.open(json_path, encoding='utf-8') as filename:
#     item_list = json.load(filename)

# filename.close
###

# find the <mods> nodes
for event, elem in cleanxml:
    if elem.tag == '{http://www.loc.gov/mods/v3}mods':

        # the filenames of the resulting xml files will be based on the <identifier> element
        # edit the specific element or attribute if necessary
        identifier = elem.find('{http://www.loc.gov/mods/v3}identifier[@type="local"]').text
        filename = format(identifier + ".xml")

        ### 
        # uncomment this section if doing MODS cleanup on existing Islandora objects
        # look through the list of object metadata and get the islandora ID by matching the digital object ID
        # for item in item_list:
        #     local_ID = item['identifier-type:oclc']
        #     islandora_ID = item['PID']

        #     if identifier == local_ID:
        #         filename = format(islandora_ID + "_MODS.xml")
        ###

        # write out to new file
        with open(filename, 'wb') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write(ET.tostring(elem, pretty_print = True))
        print "Writing", filename
print "All done!"