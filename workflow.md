## Workflow for batch processing with create_metadata.py
1. Use the project metadata spreadsheet to rename all packages with `=concatenate("rename '", [current folder name], "' ", [SIP name])`. "Short title" is a manually-created field with a keyword from the full work title. "SIP name" is a concatenation of the short title and OCLC number in UW's house style. Paste the highlighted cells into a plaintext document in the same directory as the SIPs, save it as `rename.bat`, and find-and-replace all single quotes to double quotes. (I can't get Excel to concatenate double quotes properly and the batch script doesn't like single quotes in file paths.) Double-click the batch script to run, then remove it.

<img alt="batch-renaming" src=https://user-images.githubusercontent.com/75695487/165340803-e0a69849-7241-49f1-925f-86f9de9a7ff7.PNG>

2. Download the code folder from this repository to your desktop. The Saxon script folder should also be on your desktop. Populate the `input.csv` template with the appropriate metadata. If you're using Excel, be sure to change the data type of the sheet from "General" to "Text" and then paste "match destination formatting" so that the MMSIDs are not reformulated in scientific notation. At this point, also open `create_metadata.py` in a text editor and update the text of the `readme` variable for the project⁠—currently the date, name of the project, and OCLC number of the CONTENTdm collection are just hardcoded into the `readme` variable (could potentially rewrite these as command-line inputs later).

3. Open a command prompt, navigate to the directory containing `create_metadata.py`, and run the script. It will use your first line of data to confirm that the columns have mapped correctly: input `y` to proceed and it will print names of the metadata folders as it creates them in a today-dated directory next to the script. _Note that combining diacritical marks (which Alma titles are full of) will \*not\* combine properly in the terminal—e.g. a floating umlaut after its letter—but they \*will\* print correctly in readme files._

<img width="778" alt="create_metadata" src="https://user-images.githubusercontent.com/75695487/165982398-44ea02a7-d0f0-403b-8600-e1896c48e9e8.png">

4. Depending on the use case, this is a conveneint time to batch-add metadata to these folders. For the Music Library Digital Scores Project, I used the "SIP name" column of `input.csv` plus "metadata" (i.e. the name of the new folders), concatenated with "xcopy,"  to make a batch script that copied the CONTENTdm collection's `itemLevelMetadata.csv` into every metadata folder.

5. At this point, pre-bagging, I used Karen's Directory Printer to do a full subfolders-and-files print, including filetype column, then filtered by filetype to make sure there wasn't any nonsense left in the folders. There were in fact a bunch of `Thumbs.db` files, which I searched in File Explorer at the top folder level to remove.

6. Bag the SIPs by creating a batch file with the following (h/t Moriah Caruso):
```batch
::Change ROOTDIR to full path to the target directories.
::Change SCRIPT to the full path to the bagit python script.
::Copy this file in the same directory as the bags you want to bag,
::and change the rootdir to the full path to the directory the bat file is in.

@echo off
set ROOTDIR="I:\2021\music_manuscripts_reorg\bagging\"
set SCRIPT="C:\Users\emmma\AppData\Local\Programs\Python\Python36\Scripts\bagit.py"

for /d %%F in (%ROOTDIR%*) do (
	echo Full Path : %%F
	echo Rel Path : %%~nF
	python %SCRIPT%  --md5 %%F
)
```

<img width="152" alt="bag" align="right" src="https://user-images.githubusercontent.com/75695487/165988912-93f84100-4381-4636-90e8-14216e77e92b.png">

7. Use Karen's Directory Printer or similar to list the "Full Name (Path + File)" of all the metadata folders and then all the just-bagged SIPs. Paste these into a spreadsheet (a good moment to make sure you have the right number of each and the SIP names match up with their metadata!) and concatenate another "xcopy" command, adding "/metadata" to the SIP path. You should end up with a properly-structured bag that is ready to upload to Archivematica. Spot-check then remove the original metadata folders from the `create_metadata.py` script folder.
