# -*- coding: utf-8 -*-
"""                   

Summary
-------

Function file for function Annotate. This file is intended to be called by 
script "StartHere_Script.py". See this script for details.


Inputs
------

    ExcelFile        = Full path of annotations file with extension "xlsx". 
                       Class str.
                       
                       Example: 
                           
                       ExcelFile = \
                           'C:/Users/User1/Documents/Timestamps.xlsx' 
                           
    InputDataFolder  = Full path of folder that contains input iMotion data  
                       files. Class str.   
                       
                       Example: 
                           
                       InputDataFolder = \
                           'C:/Users/User1/Documents/iMotionsInputs'                        
                       
    OutputDataFolder = Full path of folder to which annotated iMotions data
                       files will be written. Class str.
                       
                       Example: 
                           
                       OutputDataFolder = \
                           'C:/Users/User1/Documents/iMotionsOutputs'   
                       
                       
Requires
--------

- Python 3
- Pandas 
- NumPy


Author
------

Douglas Magill
dpm59@uakron.edu
Suarez Behavioral Labs, College of Business, The University of Akron
25 January 2021 

"""  

def Annotate(ExcelFile, InputDataFolder, OutputDataFolder):
        
    ##### Import packages #####
    
    import pandas as pd      
    import numpy as np
    from pathlib import Path
    from os.path import exists 
    import re
      
    
    ##### Argument validation #####
        
    #Verify types:
    
    assert( type(ExcelFile)        == str and \
            type(InputDataFolder)  == str and \
            type(OutputDataFolder) == str), \
    "Error in Annotate: ExcelFile, InputDataFolder, and OutputDataFolder" \
    " must be type str."
           
    #Verify full directories were entered:
 
    f = re.search("/", ExcelFile) #find indices of forward slashes 
    b = re.search("\\\\", ExcelFile) #find indices of double backward 
                                         #slashes    
    
    assert( not (f == None) or not (b == None) ), \
    "Error in Annotate: ExcelFile should be the full path of a file, e.g.," \
    " 'C:/Users/User1/Documents/Timestamps.xlsx'."       
 
    f = re.search("/", InputDataFolder) #find indices of forward slashes 
    b = re.search("\\\\", InputDataFolder) #find indices of double backward 
                                           #slashes
    
    assert( not (f == None) or not (b == None) ), \
    "Error in Annotate: InputDataFolder should be the full path of a folder," \
    " e.g., 'C:/Users/User1/Documents/iMotionsInputs'."    
 
    f = re.search("/", OutputDataFolder) #find indices of forward slashes 
    b = re.search("\\\\", OutputDataFolder) #find indices of double backward 
                                            #slashes
    
    assert( not (f == None) or not (b == None) ), \
    "Error in Annotate: OutputDataFolder should be the full path of a" \
    " folder, e.g., 'C:/Users/User1/Documents/iMotionsOutputs'."
    
    #Verify file extension:
    
    assert( ExcelFile[-4:] == "xlsx" ), \
    "Error in Annotate: ExcelFile must have file extension '.xlsx'."    
        
    #Verify existence of directories:    
    
    assert( exists(ExcelFile) ), \
    "Error in Annotate: The file specified by ExcelFile does not appear to" \
    " exist." 
    
    assert( exists(InputDataFolder) ), \
    "Error in Annotate: The folder specified by InputDataFolder does not" \
    " appear to exist."    
    
    assert( exists(OutputDataFolder) ), \
    "Error in Annotate: The folder specified by OutputDataFolder does not" \
    " appear to exist."   
    
    
    ##### Parse folder names #####

    #Remove trailing path separator if present:
        
    if OutputDataFolder[len(OutputDataFolder) - 1] == "/":
        
        OutputDataFolder = OutputDataFolder[:-1]
        
    if OutputDataFolder[-2:] == "\\":
        
        OutputDataFolder = OutputDataFolder[:-2]
        
    if InputDataFolder[len(InputDataFolder) - 1] == "/":
        
        InputDataFolder = InputDataFolder[:-1]
        
    if InputDataFolder[-2:] == "\\":
        
        InputDataFolder = InputDataFolder[:-2]
  

    #################################################################
    ##### Import and modify Excel sheet containing timestamps #######
    #################################################################
    
    #Import Excel file with the timestamps that correspond to the start  
    #times of events.
    #E.g., for participant 4001, the first task begins at 10:41 AM and the 
    #second task begins at 10:49 AM.
    Annotations = \
        pd.read_excel(ExcelFile)
     
    ##### Select columns to use for annotations ######

    #Start at either column "Webcam Start.1" or "Webcam Start" 
    #Note: there may be two columns with the heading "Webcam Start". If two,   
    #the second will be automatically relabelled "Webcam Start.1" when  
    #imported. If there are two, use the second column ("Webcam Start.1"). 
    FirstColumnLabel = "Webcam Start.1"
    
    if not any(Annotations.columns == "Webcam Start.1"):
        
        FirstColumnLabel = "Webcam Start"
       
    #Determine the index of the starting column
    Idx = Annotations.columns.get_loc(FirstColumnLabel)
    
    #Vector of columns labels to be used
    #These columns correspond to the 11 events, each of which represents an 
    #annotation. Start at "Webcam Start.1" (or "Webcam Start"). 
    HeadingList = Annotations.columns[range(Idx, Idx + 11)]
          
    ##### Modify elements in HH:MM:SS format to millisecond format #####
    
    #Modify the format of elements in the columns to be used from HH:MM:SS 
    #format to millisecond format. This will match the format of the iMotions 
    #data sets, allowing annotations to be added to the iMotions data sets 
    #later. 
    #Note: each element represents the start time of the event by participant. 
    
    #Loop across columns to be used
    for i in range(0, len(HeadingList)):
        
        #Extract column
        Col = Annotations.loc[:, HeadingList[i]].copy(deep = False)   
        
        #Loop across rows 
        for j in range(0, len(Col)): 
            
            #If a HH:MM:SS element present
            #Determined by checking whether a datetime.time type is present.
            if str(type(Col[j])) == "<class 'datetime.time'>":
            
                #Convert HH:MM:SS to milliseconds
                #Type int.
                Col[j] = \
                    (Col[j].hour * 60 * 60 + \
                     Col[j].minute * 60 + \
                     Col[j].second) * \
                    1000
            
            #If not, the element may be blank or have another non-time entry
            else:
                
                #Overwrite with NaN
                #Type float.
                Col[j] = np.nan
         
        #Overwrite column
        Annotations.loc[:, HeadingList[i]] = Col
               
    ##### Adjust milliseconds to start at webcam start #####    
    
    #In other words, milliseconds will equal time elapsed since webcam start 
    #rather than equal clock time. Doing so will make the format of the start 
    #times correspond to the format of iMotions data. 
       
    #Vector of webcam start times
    #Note: it is necessary to use a "deep copy".   
    WebcamStart = Annotations.loc[:, "Webcam Start.1"].copy(deep = True)
        
    #Loop across start columns
    for i in range(0, len(HeadingList)):
        
        #Extract column
        Col = Annotations.loc[:, HeadingList[i]].copy(deep = False)
        
        #Subtract webcam start time to receive elapsed time
        TimeFromStart = Col - WebcamStart
        
        #Overwrite column with adjusted time
        Annotations.loc[:, HeadingList[i]] = TimeFromStart
    
        
    #############################################
    ##### Import and annotate iMotions data #####
    #############################################   
    
    #Insert a column labeled "Event" into each iMotions data set. This column 
    #will hold all annotations to be inserted. Note that there is a separate  
    #iMotions data set for each participant; this is because each data set is  
    #quite large (~ 50 MB). As a result, the loop below loops through the 
    #individual data sets to insert annotations. The annotated iMotion data  
    #sets are then written to new files (rather than overwriting the   
    #originals). These files are saved to a new folder, the path of which is  
    #specified by OutputDataFolder.
    
    #The annotations inserted into an iMotions data set are actually the 
    #column headers of the Excel annotations file. That is, the set of
    #possible annotations are comprised of these headers. An annotation is
    #inserted starting where the event started up the point where the next
    #event started. That is, every cell is filled.
            
    ##### Make new folder for output (annotated) iMotions data sets #####   
    
    #Make new folder
    #Note: function mkdir is set not to overwrite an existing folder.
    #Requires function Path.
    Path(OutputDataFolder).mkdir(parents = True, exist_ok = True) 

    ##### Determine participants to loop through #####       
        
    #This is determined based upon the entries in the Excel annotations 
    #file in column 'Participant #'. Later, the folder specified by 
    #InputDataFolder will be inspected for iMotions data files that match the 
    #ID found in this column. For each matching file found, an output file will 
    #be written. 
  
    #Preallocate participant ID vector
    ParticipantID = np.zeros(Annotations.index.stop, dtype = int)
    
    #Only retain participant IDs that are integers
    #This is intended to exclude blank rows, strings, or other non-ID entries. 
    for i in range(0, Annotations.index.stop):
        
        El = Annotations.loc[i, 'Participant #']
        
        #If an integer type
        if type(El) == int:
        
            ParticipantID[i] = El
    
    #Remove unfilled (i.e., preallocated as zero) or non-unique rows        
    ParticipantID = np.unique( ParticipantID[ParticipantID != 0] )   
    
    ##### Specify annotation text #####
    
    #As mentioned previously, the annotation text is the same as the column
    #headers. However, if "Webcam Start.1" is present rather than 
    #"Webcam Start", use "Webcam Start" instead as this is the text used in the 
    #Excel annotations file.
    
    HeadingListAnnt = list(HeadingList)
    HeadingListAnnt[0] = "Webcam Start"      
  
    ##### Define function to annotate iMotions data files #####
    
    def AnnotateInsert(i, InputDataFolder, Annotations, HeadingList,  
                 HeadingListAnnt, OutputDataFolder):         
            
        #Import txt file with iMotions data: 
       
        #File name of an iMotions data set
        path = ''.join([InputDataFolder, "/", str(i), ".txt"])
      
        #If the specified data file exists
        #Requires function "exists".
        if exists(path):
            
            #Read data
            Data = \
                pd.read_table(path,
                              sep = '\t', 
                              skiprows = 5, #to read the data correctly 
                              memory_map = True) #Import into memory   
                                                 #for decreased I/O  
                                                 #(default false).
             
            #Confirm that column "MediaTime" is present in file
            assert( any(Data.columns == "MediaTime") ), \
            "Error in Annotate: Column 'MediaTime', which is required, not" \
            " present in iMotions input file " + str(path)                                                  
             
            #Insert column for event labels
            Data.insert(
                loc = 1, #column index
                column = 'Event', #column label
                value = '') #values              
            
            ##### Loop across columns of times to insert annotation #####    
        
            #Vector of time (and other columns) for the ith participant 
            #from the annotation Excel file.
            #Deep copy to avoid reindexing.
            LogIdx_IDith = Annotations.loc[:, "Participant #"] == i #log index 
            Times_IDith = \
                Annotations.loc[LogIdx_IDith, :].copy(deep = True) 
        
            #Vector time from iMotions data
            #Deep copy to avoid reindexing.
            MediaTime = Data.loc[:, 'MediaTime'].copy(deep = True)
            
            #Initalize time of previous column
            tOld = int(0)            
        
            #Loop across columns in iMotions data set
            for j in range(1, len(HeadingList)):           
           
                #Start time of jth column and j + 1th column
                t = Times_IDith.loc[:, HeadingList[j]].copy(deep = True)     
                
                #Convert start time from pandas series to integer for 
                #comparison.
                t = t.reset_index(drop = True) #start dataframe index at 0
                t = t[0] #extract as integer
            
                #Logical index of timestamps for previous condition 
                #(Greater than start time of previous condition and   
                #less than start time of current condition).
                LogIdx = MediaTime.ge(tOld) & MediaTime.le(t) 
                
                #Insert label for previous condition to "Event" column
                Data.loc[LogIdx, 'Event'] = \
                    HeadingList[j - 1]                               
                    
                #If the final column
                if j == len(HeadingList) - 1: 
                    
                    #Logical index of timestamps for current condition
                    LogIdx = MediaTime.ge(t)    
                    
                    #Insert label for current condition to "Event" 
                    #column.
                    Data.loc[LogIdx, 'Event'] = \
                        HeadingList[j]   
                
                #Assign time of current column as time of previous 
                #column for the next iteration.
                tOld = t 
                                                  
            ##### Write dataframe to csv file #####  
            
            #File name for annotated data set
            OutputDataFile = \
                ''.join([OutputDataFolder, "/", str(i), ".csv"])
            
            #Write data file with annotations
            Data.to_csv(OutputDataFile)

        #If the specified data file does not exist
        else:
            
            #Display message
            message = \
                ''.join(["...iMotions data file not present for ID ", \
                         str(i), ".", \
                         " Skipping to next file."])    
                
            print(message)             
                  
    ##### Loop through participant data sets and add annotations #####      
            
    print("Annotating...")  
    
    for i in ParticipantID:  
  
        #Progress notification
        print("..." + str(i))           
  
        try:  
            
            #Annotate and write output (annotated) iMotions data file for 
            #ith participant.
            AnnotateInsert(i, InputDataFolder, Annotations, HeadingList,  
                     HeadingListAnnt, OutputDataFolder)
                        
        except:
            
            #Display message
            message = \
                ''.join(["Unknown error while processing ID ", str(i), \
                         ".", " Skipping to next file."])    
                
            print(message)
            
            #Continue to data set of next participant
            continue   
      
    ##### Completion message #####

    print("\nAnnotation operations completed." + \
          "\nFiles written to " + OutputDataFolder + ".\n")  
         
 