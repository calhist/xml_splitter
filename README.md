# XML Splitter

Python script to clean up and split an XML file with many MODS records into individual MODS XML files. After exporting OpenRefine metadata to MODS XML using the templating feature, you'll need to run this script to split into component files.

The kernel of this script was [found here](http://stackoverflow.com/questions/36155049/splitting-xml-file-into-multiple-at-given-tags).

## For splitting OpenRefine XML output
Save the OpenRefine output as source.xml in the same directory as the script.

The script is assuming you have a MODS element for the object identifier with the attribute type="local", e.g., 

    <identifier type="local">CHS_PC001_001</identifier>

And it will use this unique value as the filename for each subsequent MODS record, e.g.,

    CHS_PC001_001.xml

Assuming you've named your digital object with the same string, e.g., CHS_PC001_001.tif, you'll be able to easily create a batch for Islandora ingestion.

You can set your output directory in line 9:

    output_path = ''

The script will run through the OpenRefine output, doing its best to clean up the XML by removing elements with no text value or children, removing attributes with null values, etc. It will produce an intermediate file called clean.xml.

It will then output well-formed and pretty-printed XML for each object record in the source.xml document. Now you can QC the records and prepare your batch ingest.

## For cleaning existing MODS records exported from Islandora
The following procedure was devised in order to regenerate and replace MODS records for assets already in Islandora. Thus the resulting XML docs must be named with the Islandora ID instead of the local ID. And since we're not saving the Islandora ID in the MODS record itself, we need to be able to look up the Islandora ID of an object by referencing its local ID.

*Note: We needed to do this in order to clean up the MODS XML for our first two Islandora collections. Hopefully you won't need to do this going forward, and will be able to make any necessary changes to datastreams using Islandora Find & Replace. But if you really need to make some serious changes to a whole collection or collections of MODS, then you'll probably need to use this method or something similar.*

To do this, we first run a different script over the exported Islandora MODS XML. It's called mods2json.py and lives in [this repo](https://github.com/calhist/mods_xml). (Note to self: Perhaps move all these MODS tools into a single repo?) This produces a JSON file which contains all the XML values, most importantly these two IDs.

You can then import the JSON into OpenRefine, do your cleanup there, then follow the [spreadsheet-to-MODS workflow](https://github.com/calhist/documentation/wiki/Spreadsheet-Data-to-MODS-XML): export from OpenRefine using templating and run this script to split the results. You'll then have clean MODS XML with the same filenames as the exported Islandora datastreams, which you can replace en masse.

But first you'll have to uncomment some lines of code in order to read the JSON file and match the IDs.

Uncomment line 7 to enable the codecs and json modules.

    import codecs, json

Uncomment lines 65-71 and specify the path to your JSON file in order load the data as a list of dictionaries.

    item_list = []

    json_path = 'C:\\mods\\maps\\data.json'

    with codecs.open(json_path, encoding='utf-8') as filename:
        item_list = json.load(filename)
    filename.close

Comment out line 81, since we'll be using the Islandora ID as the filename

    # filename = format(identifier + ".xml")

Uncomment lines 87-92 to format the filenames

        for item in item_list:
            local_ID = item["identifier-type:local"]
            islandora_ID = item["PID"]

            if identifier == local_ID:
                filename = format(islandora_ID + "_MODS.xml")

And that should do it!
