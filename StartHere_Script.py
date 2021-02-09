# -*- coding: utf-8 -*-
"""                   

Summary
-------
 
This script aggregates emotion expressions from iMotions "raw data" files.
Aggregation is by participant and event. The events to be aggregated are
specified by an Excel file that lists the participant IDs and the timestamps 
that correspond to the beginning of the events.

The aggregation method is the mean.
      
Inputs:

 - A batch of iMotions data files (one file per participant) (see example 
   below).
 - A single Excel file that lists the participant IDs and the timestamps that 
   correspond to the beginning of the events (see example below).
 - A variable indicating the emotion expressions to aggregage.

Outputs:
             
 - A batch of iMotions data files (one file per participant) with a new "Event"
   column that specifies the correspondence between events and timestamps (see 
   example below). Note that this batch of files will not overwrite the batch 
   of original iMotions files.
 - A single csv file that contains the aggregated emotion expressions by 
   participant and event (see example below).                                   


Example Input and Output File Layout
------------------------------------

Excel Annotations File Input (One File for All Participants):

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

An iMotions Data File Input (One per Participant):

_____________________________
| "MediaTime" | "Joy" | ... |
|_____________|_______|_____|
| 100         | 2.2   | ... |  
| 133         | 40.5  | ... | 
| 166         | 20.7  | ... |    
| .           | .     | .   |   
| .           | .     | .   |    
| .           | .     | .   |
| 2000        | 0.7   | ... | 
| 2033        | 0.2   | ... |    
| 2066        | 0.1   | ... |
|_____________|_______|_____|
  ^                     ^
  Timestamp in          Additional expression columns.
  milliseconds.

An iMotions Data File Output (One per Participant):

______________________________________________________
| "Event"                | "MediaTime" | "Joy" | ... |    
|________________________|_____________________|_____|
| "Webcam Start"         | 100         | 0.2   | ... | <- Start time of "Webcam  
| "Webcam Start"         | 133         | 0.4   | ... |    Start". This 
| "Webcam Start"         | 166         | 4.0   | ... |    annotation continues
| .                      | .           | .     | .   |    until the start time 
| .                      | .           | .     | .   |    of the next event.
| .                      | .           | .     | .   | <- Other event rows.
| "Start of interaction" | 2000        | 5.2   | ... | <- Start time of "Start 
| "Start of interaction" | 2033        | 80.2  | ... |    of interaction".
| "Start of interaction" | 2066        | 1.5   | ... |
|________________________|_____________|_______|_____|
  ^                           ^                  ^                                    
  Annotation from column      Timestamp in       Additional expression columns.
  header of Excel annotation  milliseconds.
  file.

Aggregated Expression File Output  (One File for All Participants):

_____________________________________
"ID" | "Event"        | "Joy" | ... |
_____|________________|_______|_____|
4001 | "Webcam Start" | 4.5   | ... | <- Joy aggregated (mean) across all 
4001 | "Start of ..." | 2.3   | ... |    timestamps within event "Webcam
   . | .              | .     | .   |    Start" for participant 4001.
   . | .              | .     | .   | <- Additional aggregated events.
   . | .              | .     | .   |
4005 | "Webcam Start" | 40.5  | ... |
4005 | "Start of ..." | 4.2   | ... | 
_____|________________|_______|_____|
^        ^                      ^                               
ID       Event                  Additional expression columns.
column.  annotations. 
                                          

Instructions
------------

1. Edit the variable "FunFolder" below to the location of the Python files 
   "Annotate.py" and "Aggregate.py". These files can be located in any folder.

2. Import the functions within these files.
                                                                              
3. Place all iMotions data files (one per participant) into the same folder, 
   which can be any name. Then, edit the variable "InputDataFolder" below to   
   the location of the folder.

   Note that each data file name should match the name in header "Participant  
   #" of the Excel annotation file. For example, if file 4001.txt is included,   
   then there should be a participant with name "4001" in the Excel annotation  
   file. Also note that not all iMotions data files need to be included in the  
   folder; that is, there can be fewer files than names in the Excel file.  
   Fewer files may be included if it is desired to annotate only a subset of
   files.

   Note that the original copies of the iMotions data sets will not be 
   modified. That is, the annotations will be written to new copies of the 
   files.
   
4. Edit the variable "ExcelFile" below to the path of the Excel file that has 
   the annotations. The Excel file can be located in any folder. 

   Regarding the contents of the file, see the example table above for 
   specifications. Note that this file must be an Excel file (i.e., have file
   extension .xlsx). 

5. Edit the variable "OutputDataFolder" below to the desired path of the folder
   that will be written to hold the output (annotated) iMotions data files.      

6. Edit the variable "ExpressionNames" below to the desired expressions to be
   aggregated. 

7. Edit the variable "AggregateFile" below to the desired path of the file that
   will be written with the aggregated expressions. 
   

Requires
--------

- Python 3
- Pandas 
- NumPy
- Annotate.py (custom file)
- Aggregate.py (custom file)


Author
------

Douglas Magill
dpm59@uakron.edu
Suarez Behavioral Labs, College of Business, The University of Akron
25 January 2021 

"""


##### Import Python code #####

#Specify location of Python files Annotate.py and Aggregate.py
FunFolder = "G:/My Drive/U Akron/CBA RA/Hamdani/Code"

#Add location to Python path
import sys
sys.path.append(FunFolder)

#Import functions
from Annotate import Annotate
from Aggregate import Aggregate


##### Write annotated iMotions files #####

#Specify location of the input iMotions data files
InputDataFolder = "G:/My Drive/U Akron/CBA RA/Hamdani/Input/iMotions"

#Specify Excel file containing annotations to insert. Must have file extension 
#".xlsx". Class str.
ExcelFile = "G:/My Drive/U Akron/CBA RA/Hamdani/Input/Timestamps/2020 lab timestamps imotion.xlsx"

#Specify location where the annotated iMotions data files will be written to
OutputDataFolder = "G:/My Drive/U Akron/CBA RA/Hamdani/Output/iMotions"

#Run annotation code
#This may take about an hour to run if using the data of about 100 
#participants.
Annotate(ExcelFile, InputDataFolder, OutputDataFolder)


##### Write file containing aggregated events #####

#List of string elements indicating the expressions to be aggregated.
ExpressionNames = \
    ['Anger', 'Sadness', 'Disgust', 'Joy', 'Surprise', 'Fear', 'Contempt']

#Full path of file to which a table of aggregated expressions is to be written. 
#The file extension must be ".csv". Class str.
AggregateFile = "G:/My Drive/U Akron/CBA RA/Hamdani/Output/Aggregated/AggTable.csv"

#Run aggregation code
Aggregate(ExpressionNames, OutputDataFolder, AggregateFile)

