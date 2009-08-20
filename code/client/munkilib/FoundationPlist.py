#!/usr/bin/env python
# encoding: utf-8
#
"""FoundationPlist.py -- a tool to generate and parse MacOSX .plist files.

This is intended as a drop-in replacement for Python's included plistlib,
with a few caveats:
    - readPlist() and writePlist() operate only on a filepath, 
        not a file object.
    - there is no support for the deprecated functions:
        readPlistFromResource()
        writePlistToResource()
    - there is no support for the deprecated Plist class.

The Property List (.plist) file format is a simple XML pickle supporting
basic object types, like dictionaries, lists, numbers and strings.
Usually the top level object is a dictionary.

To write out a plist file, use the writePlist(rootObject, filepath)
function. 'rootObject' is the top level object, 'filepath' is a
filename.

To parse a plist from a file, use the readPlist(filepath) function,
with a file name. It returns the top level object (again, usually a 
dictionary).

To work with plist data in strings, you can use readPlistFromString()
and writePlistToString().
"""

from Foundation import NSData, NSPropertyListSerialization, NSPropertyListMutableContainers, NSPropertyListXMLFormat_v1_0

class NSPropertyListSerializationException(Exception):
    pass

def readPlist(filepath):
    """
    Read a .plist file from filepath.  Return the unpacked root object
    (which usually is a dictionary).
    """
    plistData = NSData.dataWithContentsOfFile_(filepath)
    dataObject, plistFormat, error = NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistData, NSPropertyListMutableContainers, None, None)
    if error:
        raise NSPropertyListSerializationException(error)
    else:
        return dataObject


def readPlistFromString(data):
    '''Read a plist data from a string. Return the root object.'''
    plistData = buffer(data)
    dataObject, plistFormat, error = NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistData, NSPropertyListMutableContainers, None, None)
    if error:
        raise NSPropertyListSerializationException(error)
    else:
        return dataObject


def writePlist(dataObject, filepath):
    '''
    Write 'rootObject' as a plist to filepath.
    '''
    plistData, error = NSPropertyListSerialization.dataFromPropertyList_format_errorDescription_(dataObject, NSPropertyListXMLFormat_v1_0, None)
    if error:
        raise NSPropertyListSerializationException(error)
    else:
        if plistData.writeToFile_atomically_(filepath, True):
            return
        else:
            raise Exception("Failed to write plist data to %s" % filepath)


def writePlistToString(rootObject):
    '''Return 'rootObject' as a plist-formatted string.'''
    plistData, error = NSPropertyListSerialization.dataFromPropertyList_format_errorDescription_(rootObject, NSPropertyListXMLFormat_v1_0, None)
    if error:
        raise NSPropertyListSerializationException(error)
    else:
        return str(plistData)

