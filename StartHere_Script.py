# -*- coding: utf-8 -*-
"""                   

Summary
-------
                                                       
This script produces a new copy of each iMotions data file (there is one file   
per participant) with an event annotations column (named "Event") inserted.  
These new copies are written to a new folder named "Annotated", which will be  
located in the same folder in which the iMotions data files are located (this  
new folder will be generated automatically). Note that the original iMotions
data files will not be modified. Also note that the iMotions data files are not 
combined into a single file because of the large size of each file (~ 50 MB).

The annotations for all participants are taken from a single specified Excel 
file. The column headers of this Excel file serve as the text of the 
annotations, and the rows of the file indicate the timestamps at which the 
annotations are to be inserted into the new iMotions files. The column headers
or rows of the Excel file can be modified as long as they stay within the  
constraints noted in the example table below. 

Processing time can be rather long. Plan on the function writing about 2 to 3
iMotions files per minute. To test/experiment with the function, consider only 
including a few iMotions data files to save time; the function allows fewer 
data files to present compared to the number of participants listed on the 
Excel annotation files.

Excel Annotations File used as Input:

_______________________________________________________________________
"Participant #" | ... | "Webcam Start" | "Start of interaction" | ... |
________________|_____|________________|________________________|_____|
           4001 | ... | HH:MM:SS AM/PM |         HH:MM:SS AM/PM | ... |
           4002 | ... | HH:MM:SS AM/PM |         HH:MM:SS AM/PM | ... |
              . | .   | .              |         .              | .   |
              . | .   | .              |         .              | .   |
              . | .   | .              |         .              | .   |
________________|_____|________________|________________________|_____|
^                ^           ^                    ^                     
Participant ID   Any number  The first annotation There should be exactly 10  
column. This     of misc.    must be labelled     annotations (as columns) in  
column must be   columns     "Webcam Start".      addition to "Webcam Start".  
named            (not used).                      These columns should be   
"Participant #"                                   positioned from left to right  
                                                  in chronological order. Other 
                                                  columns can be placed to the
                                                  right of these columns, but
                                                  they will not be used.

iMotions Data File to be Written (One per Participant):

__________________________________________________
... | "Event"                | "MediaTime" | ... |
____|________________________|____________________
... | "Webcam Start"         | 100         | ... | <- Start time of  
... | "Webcam Start"         | 133         | ... |    "Webcam Start". This
... | "Webcam Start"         | 166         | ... |    annotation continues
.   | .                      | .           | .   |    until the start time of
.   | .                      | .           | .   |    the next annotation.
.   | .                      | .           | .   |
... | "Start of interaction" | 2000        | ... | <- Start time of "Start of
... | "Start of interaction" | 2033        | ... |    interaction".
... | "Start of interaction" | 2066        | ... |
____|________________________|_____________|_____|
     ^                           ^
     Annotation from column      Timestamp in 
     header of Excel annotation  milliseconds.
     file.


Setup
-----
                                                                              
1. Place all iMotions data files (one per participant) into the same folder, 
   which can be any name. Then, edit the variable "DataFolder" below to the  
   path of the folder.

   Note that each data file name should match the name in header "Participant  
   #" of the Excel annotation file. For example, if file 4001.txt is included,   
   then there should be a participant with name "4001" in the Excel annotation  
   file. Also note that not all iMotions data files need to be included in the  
   folder; that is, there can be fewer files than names in the Excel file.  
   Fewer files may be included if it is desired to annotate only a subset of
   files. 
   
2. Edit the variable "ExcelFile" below to the path of the Excel file that has 
   the annotations. The Excel file can be located in any folder. 

   Regarding the contents of the file, see the example table above for 
   specifications. Note that this file must be an Excel file (i.e., have file
   extension .xlsx). 

3. Edit the variable "FunFolder" below to the path of the Python file 
   "Annotator.py". The python file can be located in any folder.

   "Annotator.py" is a custom function used to annotate the iMotions data 
   files.

4. Import the function code for "Annotator.py" and run the code.

   Annotated copies of the iMotion data sets will be written to a new folder, 
   "Annotated". This folder will be written within the folder specified to
   hold the iMotions data files (as specified by variable "DataFolder"). 
   Original copies of the iMotions data sets will not be modified.


Requires
--------

- Python 3
- Pandas 
- NumPy
- Annotator.py


Author
------

Douglas Magill
dpm59@uakron.edu
Suarez Behavioral Labs, College of Business, The University of Akron
25 January 2021 

"""


##### Specify data locations #####

#Specify location of data without annotations
DataFolder = "G:/My Drive/U Akron/CBA RA/Hamdani/Data"

#Specify location of file with annotations to insert
ExcelFile = "G:/My Drive/U Akron/CBA RA/Hamdani/Timestamps/2020 lab timestamps imotion.xlsx"


##### Specify annotation code location #####

#Specify location of annotation code
FunFolder = "G:/My Drive/U Akron/CBA RA/Hamdani/Code"


##### Run annotation code #####

#Add function location to Python path
import sys
sys.path.append(FunFolder)

#Import function code
from Annotator import Annotator

#Run annotation code
#This may take about an hour to run if using the data of about 100 
#participants.
Annotator(ExcelFile, DataFolder)


