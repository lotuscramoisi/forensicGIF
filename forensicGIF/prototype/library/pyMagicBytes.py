# Autor : FanaticPythoner.
# Please read the "LICENSE" file before doing anything.

from os.path import abspath
from requests import get
import os

def _getAllFileTypes():
    return open('./library/DB','r').readlines()

class FileObject:
    def __init__(self, filePath):
        self.allFileTypes = _getAllFileTypes()
        self.fileStream = open(abspath(filePath),'rb')

    def getPossibleTypes(self, ReturnArray=True):
        typesFound = []
        for row in self.allFileTypes:
            matchedCurrentFileType = True
            size, offs, sign, ext, desc = row.split('|')
            size = int(size)
            offsArr = offs.split('..')
            for off in offsArr:
                self.fileStream.seek(int(off))
                redBytesString = self.fileStream.read(size).hex().upper()
                for byteHex, hexByteSign in zip(redBytesString, sign):
                    if hexByteSign != '?':
                        if hexByteSign != byteHex:
                            matchedCurrentFileType = False
                            break
            if matchedCurrentFileType:
                typesFound.append([('Bytes Offsets', offs.replace('..',' and ')), ('File Signature', sign), ('File Extension', ext), ('Description', desc.replace('\n',''))])
        if ReturnArray:
            return typesFound
        else:
            newTypeFound = [''] * len(typesFound)
            for item in typesFound:
                tempItemFromTuples = ''
                for tuples in item:
                    if tempItemFromTuples != '':
                        tempItemFromTuples = tempItemFromTuples + ' -> ' + tuples[0] + ' : ' + str(tuples[1])
                    else:
                        tempItemFromTuples = tuples[0] + ' : ' + str(tuples[1])
                newTypeFound.append(tempItemFromTuples)
            newTypeFound = [x for x in newTypeFound if x != '']
            return str(newTypeFound).replace("', '", ",\n").replace("['Bytes Offsets :","Bytes Offsets :").replace("']","")

class HexStringObject:
    def __init__(self, hexString):
        # Ensure the hex string is in uppercase
        self.hexString = hexString.upper()
        self.allFileTypes = _getAllFileTypes()

    def getPossibleTypes(self, ReturnArray=True):
        typesFound = []
        for row in self.allFileTypes:
            matchedCurrentFileType = True
            size, offs, sign, ext, desc = row.split('|')
            size = int(size)
            offsArr = offs.split('..')

            # Iterate over offset ranges
            for off in offsArr:
                start_offset = int(off) * 2  # Multiply by 2 for hex string indexing (2 chars per byte)
                end_offset = start_offset + size * 2  # Account for the size in bytes
                redBytesString = self.hexString[start_offset:end_offset]

                for byteHex, hexByteSign in zip(redBytesString, sign):
                    if hexByteSign != '?':
                        if hexByteSign != byteHex:
                            matchedCurrentFileType = False
                            break
            if matchedCurrentFileType:
                typesFound.append([
                    ('Bytes Offsets', offs.replace('..', ' and ')),
                    ('File Signature', sign),
                    ('File Extension', ext),
                    ('Description', desc.replace('\n', ''))
                ])
        if ReturnArray:
            return typesFound
        else:
            newTypeFound = [''] * len(typesFound)
            for item in typesFound:
                tempItemFromTuples = ''
                for tuples in item:
                    if tempItemFromTuples != '':
                        tempItemFromTuples = tempItemFromTuples + ' -> ' + tuples[0] + ' : ' + str(tuples[1])
                    else:
                        tempItemFromTuples = tuples[0] + ' : ' + str(tuples[1])
                newTypeFound.append(tempItemFromTuples)
            newTypeFound = [x for x in newTypeFound if x != '']
            return str(newTypeFound).replace("', '", ",\n").replace("['Bytes Offsets :", "Bytes Offsets :").replace("']", "")
