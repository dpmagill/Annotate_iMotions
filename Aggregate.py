# -*- coding: utf-8 -*-
"""                   

Summary
-------

Function file for function Aggregate. This file is intended to be called by 
script "StartHere_Script.py". See this script for details.


Inputs
------

    ExpressionNames  = List of string elements indicating the expressions to be
                       aggregated.
                       
                       Example:
                           
                       ExpressionNames = ['Anger', 'Sadness', 'Disgust', 'Joy',  
                       'Surprise', 'Fear', 'Contempt']
                                                     
    OutputDataFolder = Full path of folder that contains output iMotions data   
                       files. The term "output" is used because the files were
                       output of function Annotate; however, they are now the
                       input to the current function. Class str. 
                       
                       Example: 
                           
                       OutputDataFolder = "C:/Users/user1/Documents"    
                       
    AggregateFile    = Full path of file to which a table of aggregated
                       expressions is to be written. The file extension must be
                       ".csv". Class str.
                       
                       Example: 
                           
                       AggregateFile = "C:/Users/user1/Documents/AggTable.csv"
                       
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
6 February 2021 

""" 


def Aggregate(ExpressionNames, OutputDataFolder, AggregateFile): 

    
    ########################################################
    ##### Import packages and validate input arguments #####
    ########################################################    


    ##### Import packages ##### 
    
    import pandas as pd      
    import numpy as np
    from os.path import exists   
    from os import listdir  
    import re
    
    
    ##### Argument validation ##### 
        
    #Verify types and lengths:
    
    assert( type(OutputDataFolder) == str and \
            type(AggregateFile)    == str), \
    "Error in Aggregate: OutputDataFolder and AggregateFile must be type str."      
    
    assert( type(ExpressionNames) == list), \
    "Error in Aggregate: ExpressionNames must be type list."
    
    assert( len(ExpressionNames) != 0), \
    "Error in Aggregate: ExpressionNames must have length greater than 0."
    
    #Verify that all elements of ExpressionNames are of type str
    AllStr = True
    
    for i in range(0, len(ExpressionNames)):
        
        if not ( type(ExpressionNames[i]) == str ):
            
            AllStr = False
            
            break
            
    assert(AllStr), \
    "Error in Aggregate: Elements of list ExpressionNames must be type str."
    
    #Verify full directories were entered:
        
    f = re.search("/", OutputDataFolder) #find indices of forward slashes 
    b = re.search("\\\\", OutputDataFolder) #find indices of double backward 
                                            #slashes
    
    assert( not (f == None) or not (b == None) ), \
    "Error in Aggregate: OutputDataFolder should be the full path of a" \
    " folder, e.g.,'C:/Users/User1/Documents'."
    
    f = re.search("/", AggregateFile) #find indices of forward slashes 
    b = re.search("\\\\", AggregateFile) #find indices of double backward 
                                         #slashes    
    
    assert( not (f == None) or not (b == None) ), \
    "Error in Aggregate: AggregateFile should be the full path of a file," \
    " e.g., 'C:/Users/User1/Documents/AggFile.csv'."
    
    #Verify existence of directories:
    
    assert( exists(OutputDataFolder) ), \
    "Error in Aggregate: The folder corresponding to OutputDataFolder does" \
    " not appear to exist." 
    
    #Remove the file name from the path to verify whether the path exists
    #This is necessary because the file has not been written yet.
       
    f = re.search("/", AggregateFile) #find indices of forward slashes 
    b = re.search("\\\\", AggregateFile) #find indices of double backward 
                                         #slashes   
    
    if b == None:
        
        pattern = "/"
        
    else:
        
        pattern = "\\\\"
    
    for i in re.finditer(pattern, AggregateFile):
        
        LastMatchIdx = i.start() #index of final "/"     
      
    #Verify existance of path with file name removed
    assert( exists(AggregateFile[: LastMatchIdx]) ), \
    "Error in Aggregate: The folder in which AggregateFile is specified to be"\
    " written does not appear to exist." 
    
    #Verify file extension:
        
    assert(AggregateFile[-3:] == "csv"), \
    "Error in Aggregate: The file extension of AggregateFile must be '.csv'."
      
    #Verify data present:

    filesArrayStr = np.array( listdir(OutputDataFolder) )
    
    assert(filesArrayStr.size != 0), \
    "Error in Aggregate: Folder OutputDataFolder does not appear to contain" \
    " any files to be aggregated."

    
    ##### Column names to use in iMotions data files ##### 
    
    #Also include the "Event" column, which is required for processing.
    ColumnNames = ExpressionNames.copy()
    ColumnNames.insert(0, "Event")   
    
    
    ##### Parse folder names #####

    #Remove trailing path separator if present:
        
    if OutputDataFolder[len(OutputDataFolder) - 1] == "/":
        
        OutputDataFolder = OutputDataFolder[:-1]
        
    if OutputDataFolder[-2:] == "\\":
        
        OutputDataFolder = OutputDataFolder[:-2]
    
    
    ######################################################
    ##### Define function to setup aggregation table #####
    ######################################################
    
    def SetupData(OutputDataFolder, ColumnNames, filesArrayStr): 
    
        
        ##### Remove non-annotated iMotions data files from list #####
        
        #Remove files that are not csv files and files that do not have the
        #columns that an annotated iMotions data file should have.
        
        #Initialize Boolean index of non-annotated iMotions files
        NoniMotionsBoolIdx = np.tile(False, filesArrayStr.size)
        
        #Loop through files
        for i in range(0, filesArrayStr.size):
            
            fileIth = filesArrayStr[i]
            
            #If not a csv file             
            if fileIth[-3 : filesArrayStr.size] != "csv":
                
                #Mark as non-iMotions file
                NoniMotionsBoolIdx[i] = True  
                
            else:    
                
                path = OutputDataFolder + "/" + fileIth              
                
                #Read the first couple rows of the file
                dataIth = \
                    pd.read_csv(path, 
                                nrows = 1,
                                memory_map = True) #default False 
                    
                #Determine whether the columns that should be in an annotated
                #iMotions file are present:
                                    
                ColumnNamesN = len(ColumnNames)            

                for j in range(0, ColumnNamesN):
                    
                    #If any required column is not present
                    if not (ColumnNames[j] in dataIth.columns):
                        
                        #Mark as non-iMotions file
                        NoniMotionsBoolIdx[i] = True
                        
                        break                
        
        #Remove non-annotated iMotions files from array                
        if NoniMotionsBoolIdx.any():             
 
            filesArrayStr = filesArrayStr[~ NoniMotionsBoolIdx]              
       
        #Verify at least one annotated iMotions file present
        assert(filesArrayStr.size != 0), \
        "Error in Aggregate: No annotated iMotions files appear to be present"\
        " in folder OutputDataFolder."
           
        
        ##### Remove file extension ######
        
        #Remove '.csv' from file names
        filesArrayStr = np.char.rstrip(filesArrayStr, chars = ".csv")
                          
        
        ##### Preallocate aggregation table #####
                           
        #Unique events:
         
        path = OutputDataFolder + "/" + filesArrayStr[0] + ".csv"   
         
        dataIth = \
            pd.read_csv(path, 
                        usecols = ['Event'], 
                        memory_map = True) #default False                      
        
        NEvents = len(pd.Categorical(dataIth.Event).categories)   
        
        #ID Column:                  

        #Length is number of events * number of participants
        #Wrap in Pandas categorical series.       
        ID = pd.Categorical( filesArrayStr.repeat(repeats = NEvents) )

        #Events column:                   
        
        #Preallocate categorical object of events, which will be   
        #sorted by chronological order.
        EventsSorted = list(range(NEvents)) 
        
        EventIth = dataIth.Event[0]        
        jj = 0
        EventsSorted[jj] = EventIth
        
        #Sort events by chronological order
        #Do so by determining the order of occurrence in an iMotions data file.
        for j in range(0, len(dataIth.Event)):
            
            if EventIth != dataIth.Event[j]:
                
                jj = jj + 1
                
                EventsSorted[jj] = dataIth.Event[j]
                
                EventIth = dataIth.Event[j]
 
        #Repeat events by number of participants            
        EventsByID = np.tile(EventsSorted, filesArrayStr.size)
        
        #Cast to class categorical
        Event = pd.Categorical(EventsByID, categories = EventsSorted)                       
   
        #Assign table:
                         
        AggregateTable = \
            pd.DataFrame(
                {
                    "ID":       ID,
                    "Event":    Event,
                }
            ) 
            
        #Preallocate expression aggregation columns:    
            
        ExpressionAgg = \
            pd.Series(np.nan, 
                      index = list(range(filesArrayStr.size * NEvents)))                 
      
        #Insert the preallocated column into each of the expression columns
        for i in ColumnNames:
            
            if (i == "Event"):
            
                continue
            
            AggregateTable[i] = ExpressionAgg
  
    
        return [EventsSorted, NEvents, AggregateTable, filesArrayStr] 
                
    
    ########################################
    ##### Define function to aggregate #####
    ######################################## 
    
    def AggregateToTable(OutputDataFolder, ExpressionNames, ColumnNames, 
                         EventsSorted, NEvents, AggregateTable, filesArrayStr):
          
        print("\nAggregating...")  
        
        #Loop across files
        for i in range(0, filesArrayStr.size):
            
            fileIth = filesArrayStr[i]  
            
            print("..." + fileIth)
               
            path = OutputDataFolder + "/" + fileIth + ".csv"
                
            #Extract needed columns from annotated iMotions data file
            dataIth = \
                pd.read_csv(path, 
                            usecols = ColumnNames, 
                            memory_map = True) #default False 
            
            #Loop across events
            for j in range(0, NEvents):
                               
                EventJth = EventsSorted[j]
                
                EventJthBoolIdx = dataIth.Event == EventJth                   
                    
                #Loop across expressions
                for k in range(0, len(ExpressionNames)):
                    
                    ExpressionNameKth = ExpressionNames[k]
                    
                    ExpressionKth = \
                        dataIth.loc[EventJthBoolIdx, ExpressionNameKth]
                    
                    RowBoolIdx = \
                        (AggregateTable.ID == fileIth) & \
                        (AggregateTable.Event == EventJth)
                    
                    AggregateTable.loc[RowBoolIdx, ExpressionNameKth] = \
                        ExpressionKth.mean()
     
        
        return AggregateTable
     
        
    ########################################################
    ##### Aggregate and write aggregation table to csv #####
    ########################################################
    
    #Setup data:
        
    #Function defined previously
    Out = SetupData(OutputDataFolder, ColumnNames, filesArrayStr) 
    
    EventsSorted   = Out[0] 
    NEvents        = Out[1] 
    AggregateTable = Out[2] 
    filesArrayStr  = Out[3]  
    
    #Return aggregation table:
    
    #Function defined previously
    AggregateTable = \
        AggregateToTable(OutputDataFolder, ExpressionNames, ColumnNames, 
                         EventsSorted, NEvents, AggregateTable, filesArrayStr)                        
            
    #Write to csv:
        
    AggregateTable.to_csv(AggregateFile, 
                          index = False) #No row index (default is True)


   ##### Completion message #####

    print("\nAggregation operations completed." + \
          "\nFiles written to " + AggregateFile + ".\n") 
