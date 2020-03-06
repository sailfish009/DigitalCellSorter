'''Ggeneral functions for conveniece of use
'''

import os
import pickle
import zipfile
import gzip
import shutil
import time
import numpy as np

def write(data, fileName):
    
    '''Pickle object into a (binary) file
        
    Parameters:
        data: any Pyhton object, e.g. list, dictionary, file, method, variable, etc.
        fileName: path and name of the file to store binary data in

    Returns:
        None
        
    Usage:
        data = [['A', 'B', 'C'], pd.DataFrame()]
        write(data, os.path.join('some dir 1', 'some dir 2', 'File with my data'))
    '''

    with gzip.open(fileName + '.pklz','wb') as temp_file:
        pickle.dump(data, temp_file, protocol=4)

    return None

def read(fileName):

    '''Unpickle object from a (binary) file

    Parameters:
        fileName: path and name of the file with binary data stored in

    Returns:
        Data stored in the provided file
        
    Usage:
        read(os.path.join('some dir 1', 'some dir 2', 'File with my data'))
    '''

    with gzip.open(fileName + '.pklz','rb') as temp_file:
        data = pickle.load(temp_file)
        return data

    return None

def timeMark():

    '''Print total time elapsed from the beggining of the process
    from which the function is called
        
    Parameters:
        None

    Returns:
        None

    Usage:
        timeMark()
    '''
        
    return print('--> Total elapsed time: %s min' % (np.round(time.thread_time() / 60., 1)), '\n')

def getStartTime():

    '''Get time (in seconds) elapsed from the epoch
    
    Parameters:
        None

    Returns:
        Time (in seconds)

    Usage:
        start = getStartTime()
    '''

    return time.time()
    
def getElapsedTime(start):

    '''Print total elapsed time (in minutes) elapsed from the reference point
    
    Parameters:
        start: float or int 
            Reference time (in seconds)

    Returns:
        None

    Usage:
        getElapsedTime(start)
    '''

    return print('Elapsed time: ' + str(np.round((time.time() - start) / 60.,1)) + ' min' + '\n')

def extractFromZipOfGz(filepath, removeDownloadedZipFile=False):

    print('Extracting files at:', filepath)

    extractPath = os.path.join(os.path.dirname(filepath), os.path.splitext(os.path.basename(filepath))[0])

    filename = os.path.basename(filepath)
    filepath = os.path.dirname(filepath)

    if not os.path.exists(extractPath):
        os.makedirs(extractPath)

    with zipfile.ZipFile(os.path.join(filepath, filename), "r") as zipFile:

        for finfo in zipFile.infolist():

            ifile = zipFile.open(finfo)
            zipFile.extract(ifile.name, path=filepath)

            with gzip.open(os.path.join(filepath, ifile.name), "r") as fileIn:
                extractName = os.path.join(extractPath, os.path.splitext(os.path.basename(fileIn.name))[0])
                
                print("Extracting to:", extractName)

                with open(extractName, 'wb') as fileOut:
                    shutil.copyfileobj(fileIn, fileOut)

            shutil.rmtree(os.path.join(filepath, os.path.dirname(ifile.name)))

    if removeDownloadedZipFile:

        print('Removing the downloaded ZIP file')

        try:
            os.remove(os.path.join(filepath, filename))
        except:
            print('Could not remove the file')

    return extractPath