import os
import sys
import getpass

#(?=\s).*(?=\(.*\)) 

FUNCTION_END = 0
MEMBER_OPERATOR = "::"
FILE_PATH_OPERATOR = ":\\"
PATH_TO_GITHUB = "C:\\Users\\{}\\Documents\\GitHub\\".format(getpass.getuser())
LIST_OF_TYPES = ['void', 'uint8_t', 'uint16_t', 'uint32_t', 'byte',
                        'int' , 'const', 'volatile', 'char', 'char16_t',
                        'char32_t', 'float', 'double']  

STRING_FLAIR = "=================================="

def error_out(error):

    if error == 0:
        sys.exit("Incorrect path to the parent directory.")

def get_path_to_src_par_dir():
    
    if len(sys.argv) > 1:

        userDir = sys.argv[1]

        if FILE_PATH_OPERATOR in userDir and os.path.isdir(userDir):
            if (verify_parent_directory(userDir)):
                    return userDir  

        elif os.path.isdir(PATH_TO_GITHUB + userDir):
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
        if "src" in file:
            return True

def get_path_to_header(pathToSrc):

    for file in os.listdir(pathToSrc):
        if file.endswith(".h"):
            if(confirm_header_file(pathToSrc + os.sep + file)):
                return pathToSrc + os.sep + file
            

def confirm_header_file(filePath):
    
    with open(filePath, 'r') as h:
        for line in h:
            if "class" in line:
                return True
                                 
def get_class_name(headerPath):

    print("Checking for Class Name....")
    with open(headerPath, 'r') as h: 
        for line in h:
            if "class" in line:
                words = line.split(' ')
                className = words[1] 
                return className

def get_functions(pathToheader, functionList):
    
   with open(pathToheader) as h:
       for line in h:

           if "Private:" in line:
                return 

           for type in LIST_OF_TYPES:
               if type in line:
                   functionLine = line.split(' ')
                   functionName = functionLine[1]
                   functionList.append(functionName)


def check_if_keywords_exists(pathToParent):

    for file in os.listdir(pathToParent):
        if file == "keywords.txt":
            print("Found") 
            return True

    print("Existing Keywords.txt file not found, creating new one!")

def format_keyword_file(libPath, className, functions):

    print("Checking if keywords.txt already exists.")
    if check_if_keywords_exists(libPath):
        os.chdir(libPath)
        with open("keywords.txt", 'a+') as k:
            for line in k:
                if className in line:
                    break
                else:
                    k.write("{}\tKEYWORD1\n".format(className))
            k.seek(0)
            for line in k:
                for function in functions: 
                    if function in line:
                        k.seek(0)
                        continue
                    else:
                        k.write("{}\tKEYWORD2\n".format(function))

    else:
        os.chdir(libPath)
        print("Keywords.txt file created.")
        with open("keywords.txt", 'w') as k:
            k.write("Class {} \n".format(STRING_FLAIR))
            k.write("{}\tKEYWORD1\n".format(className))
            k.write("Functions {} \n".format(STRING_FLAIR))
            for function in functions: 
                k.write("{}\tKEYWORD2\n".format(function))
            


def create_keyword_file():
    
    parPath     = get_path_to_src_par_dir()
    srcPath     = parPath + "\src"
    print("Arduino Library Path:\n{}".format(parPath))

    headerFilePath = get_path_to_header(srcPath)
    print("Header File Path:\n{}".format(headerFilePath))

    className      = get_class_name(headerFilePath)
    print("Class name found in header:\n{}".format(className))

    print("Getting Functions....")
    functionList = list()
    get_functions(headerFilePath, functionList)
    print("Functions gathered.")

    format_keyword_file(parPath, className, functionList)


print("Arduino Keywords.txt File Creator")
create_keyword_file()
