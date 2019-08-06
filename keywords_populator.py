import os
import sys

def get_class_name(headerPath):

    with open(headerPath, 'r') as h: 
        for line in h:
            for word in line: 
                if word == "class": 
                    className = line[len("class"):]
                    return className


def get_path_to_header():

    if len(sys.argv) > 1:
        if verify_path_to_header(sys.argv[0]) == True:
            return(sys.argv[0])

    else:
        if verify_path_to_header(os.getcwd()) == True:
            for file in os.listdir():
                if (file.endswith(".h")):
                  return(file)

    check = check_if_close_enough(sys.argv[0])
    if(check):
        return check
    else:
        return false

def verify_path_to_header(pathToFile):
                                 
    if pathToFile.endswith("src"):  
        return True 

def check_if_close_enough(pathToFile):

    for file in os.listdir():
        if file == "src":
            return (os.getcwd() + os.sep() + "src")
        else:
            return False
        
def get_functions(className):
    
   headerPath = get_path_to_header() 
   if not headerPath:
       return

   className = get_class_name(headerPath, 'r')
   with open(header) as h:
       for line in h:
           for word in line:
               if word.contains(className + "::"):
                   position = h.tell()



