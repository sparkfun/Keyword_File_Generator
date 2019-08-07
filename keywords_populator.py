import os
import sys
import getpass

FUNCTION_END = 0
MEMBER_OPERATOR = "::"
FILE_PATH_OPERATOR = ":\\"
PATH_TO_GITHUB = "C:\\Users\\Documents\\{}\\Github\\".format(getpass.getuser())

def error_out(error):

    if error == 0:
        sys.exit("Incorrect path to the parent directory.")

def get_path_to_src_par_dir():

    if len(sys.argv) > 1:

        userDir = sys.argv[1]

        if userDir.contains(FILE_PATH_OPERATOR) and os.is_dir(userDir):
            if (verify_parent_directory(userPath)):
                    return userPath

        elif os.is_dir(PATH_TO_GITHUB + userDir):
            if (verify_parent_directory(PATH_TO_GITHUB + userDir)):
                return PATH_TO_GITHUB + userDir
        else:
            error_out(0)

    else:
        if verify_parent_directory(os.getcwd()): 
            return os.getcwd()
        else:
            error_out(0)

        

def verify_parent_directory(pathToParent):

    for file in os.listdir(pathToParent):
        if file.contains("src"):
            return True

def get_path_to_header(pathToSrc):

    for file in os.listdir(pathToSrc):
        if file.endswith(".h"):
            if(confirm_header_file(pathToSrc + os.sep + file)):
                return pathToSrc + os.sep + file
            

def confirm_header_file(filePath):
    
    with open(filePath, 'r') as h:
        for line in h:
            if line.contains("class"):
                return True
                                 
def get_class_name(headerPath):

    with open(headerPath, 'r') as h: 
        for line in h:
            for word in line: 
                if word == "class": 
                    className = line[len("class"):]
                    return className

def get_functions(pathToheader, className):
    
   with open(pathToheader) as h:
       for line in h:
           if line.contains("Public:"):
               if line.contains("def"):
                   for word in line:
                       position = h.tell()
                       return line[position: 

           elif line.contains("Private:"):
                return FUNCTION_END

           else:
                return FUNCTION_END


def create_keyword_file():
    
    srcFilePath = get_path_to_src_par_dir()
    headerFilePath = get_path_to_header(srcFilePath)
    className = get_class_name(headerFilePath)
    functions = get_functions(headerFilePath)

     
