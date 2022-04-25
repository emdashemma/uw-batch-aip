import sys
import csv
import os
import os.path
import subprocess
from datetime import datetime

# confirm structure of input.csv
with open('input.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    column_names = next(reader) # removes the header row
    row1 = next(reader)
    lines = len(list(reader)) + 1
    test_sip, test_title, test_mmsid, test_digital, test_oclc = row1[0], row1[1], row1[2], row1[3], row1[4]
    print(f"""Your input file has been parsed as:
	SIP name: {test_sip}
	Title: {test_title}
	MMSID: {test_mmsid}
	Digital OCLC (if applicable): {test_digital}
	OCLC: {test_oclc}
A readme.txt file and metadata.csv file will be created for {lines} item(s).
Enter "y" to confirm that your data is structured correctly.""")

if input("> ") != "y":
	print("Not confirmed. Exiting...")
	sys.exit(0)

# create a batch folder with today's date
today = datetime.today().strftime("%Y-%m-%d")
if os.path.isdir(f"{today}-SIPs"):
	print("Batch folder already exists. Exiting...")
	sys.exit(0)
else:
	os.mkdir(f"{today}-SIPs")

# wayfinding
working_dir = os.path.abspath(f"{today}-SIPs") # absolute path of batch folder
here = os.getcwd() # level above batch folder i.e. where script + inputs are
desktop = os.path.dirname(here) # level above "here" is assumed to be the desktop
saxon_dir = os.path.join(desktop, "SaxonHE9-8-0-1J") # assumes Saxon folder is on the desktop

csvfile = open('input.csv', newline='', encoding='utf-8-sig')
reader = csv.reader(csvfile)
remove_header = next(reader) # removes the header row before looping
for row in csv.reader(csvfile):
	sip_name, title, mmsid, digital_oclc, oclc = row[0], row[1], row[2], row[3], row[4]

	# create a subfolder for this row of the csv, go into it
	os.chdir(f"{working_dir}")
	os.mkdir(f"{sip_name} metadata")
	os.chdir(f"{sip_name} metadata")

	print(f"Created \"{sip_name} metadata\"")

	# define text for readme.txt
	readme = f"""This Information Package was constructed in the Preservation Department of the University of Washington Libraries in April 2022.

The "objects" folder contains objects associated with \"{title}\", OCLC # {oclc}.

This folder ("metadata") includes metadata files that have not been incorporated into the Information Package's master METS file.

The METS file draws from the metadata.csv file found in this folder, which reflects descriptive metadata for the collection derived from the bibliographic MARC record.

The other metadata files contain descriptive information as follows:

itemLevelMetadata.csv
Metadata originally submitted to the Libraries' CONTENTdm access platform. Note that this file includes metadata for the entire CONTENTdm collection, not just the item associated with this package.

Curation notes:
The physical object represented by this package was digitized for inclusion in the Music Library Digital Scores Collection on CONTENTdm, OCLC # 670750165.
"""

	# add line about digital OCLC # if that value is present
	readme_digital = readme + f"That digital surrogate has been cataloged separately by the UW Libraries, with OCLC # {digital_oclc}."

	# create readme.txt in the metadata folder with appropriate template
	with open("readme.txt", "w", encoding="UTF-8", errors="replace") as f:
		if digital_oclc:
			f.write(readme_digital)
		else:
			f.write(readme)

	# define variables needed to write the Saxon template xml file
	xml_path = os.getcwd() # we're in the metadata folder rn
	xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<mmsids>
    <row>
        <MMSID>{mmsid}</MMSID>
        <path>{xml_path}\</path>
    </row>
</mmsids>"""

	# navigate to Saxon folder to create xml
	os.chdir(saxon_dir)

	# write xml
	with open(f"{mmsid}.xml", "w") as f:
		f.write(xml)

	# run Saxon script then remove xml template
	subprocess.call(["java", "-jar", "saxon9he.jar", "-xsl:mms2dc.xsl", "-o:dummyResult4.xml", "-s:dummy.xml", f"path2xmlMms={mmsid}.xml", "--suppressXsltNamespaceCheck:on"])
	os.remove(f"{mmsid}.xml")

	os.chdir(desktop)
	os.chdir(f"{working_dir}") # back up and do it again

count = len(next(os.walk(working_dir))[1])
print(f"Success! Created {count} metadata folders in \"{today}-SIPS\"")
