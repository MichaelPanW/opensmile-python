import os
import numpy as np
import csv
import sys


def excuteCMD(_pathExcuteFile, _pathConfig, _pathAudio, _pathOutput):
    cmd = _pathExcuteFile + " -C " + _pathConfig + \
        " -I " + _pathAudio + " -O " + _pathOutput + \
        ".txt -csvoutput " + _pathOutput + ".csv "
    print(cmd)
    return cmd
def coverTextToNumpy(nameFront):
    _pathOutput = os.path.join(pathOutputRoot, nameFront + ".txt")
    if(not os.path.exists(_pathOutput)):
        return 
    f = open(_pathOutput, "r")
    text = f.read()
    dataBox = text.split(',')
    dataList = []
    countRow = 0
    for i in range(len(dataBox)):
        #print(dataBox[i])
        if("'" in dataBox[i] ):
            dataList.append([])
        else:
            if("?" not in dataBox[i]):
                #print(len(dataList))
                #print((dataBox[i]))
                if('0.0' in dataBox[i]):
                    continue
                dataList[len(dataList) - 1].append(dataBox[i])
    '''
    for i in range(len(dataList)):
        print(len(dataList[i]),dataList[i][len(dataList[i])-1])
    '''

    npList = np.array(dataList)
    print(npList.shape)
    np.save(os.path.join(pathOutputRoot, nameFront + ".npy"), npList)


def coverCsvToNumpy(nameFront):
    _pathOutput = os.path.join(pathOutputRoot, nameFront + ".csv")
    if(not os.path.exists(_pathOutput)):
        return 
    csvfile = open(_pathOutput,'r')
    reader = [each for each in csv.DictReader(csvfile, delimiter=';')]
    dataList = []
    for row in reader:
        dataList.append([])
        for i in row:
            if(i in 'name' or i in 'frameTime'):
                continue
            dataList[len(dataList) - 1].append(row[i])
    csvfile.close()
    npList = np.array(dataList)
    print(npList.shape)
    np.save(os.path.join(pathOutputRoot, nameFront + ".npy"), npList)

pathExecute = ""
pathModel = sys.argv[1]
pathExcuteFile = pathExecute + "bin\\Win32\\" + "SMILExtract_Release"
pathConfig = pathExecute + "config\\" + pathModel + ".conf"
pathAudioRoot = "audio"
pathOutputRoot = "output"

for i in os.listdir(pathAudioRoot):
    nameBehind = os.path.splitext(i)[1]
    nameFront = os.path.splitext(i)[0]
    if nameBehind == '.wav':
        print(i)
        _pathOutput = os.path.join(pathOutputRoot, pathModel + nameFront)
        _pathAudio = os.path.join(pathAudioRoot, i)
        os.system(excuteCMD(pathExcuteFile, pathConfig, _pathAudio, _pathOutput))
        coverTextToNumpy(pathModel+nameFront)
        coverCsvToNumpy(pathModel + nameFront)
