import os
import sys
import getpass
import CppHeaderParser

#(?=\s).*(?=\(.*\)) 

FUNCTION_END = 0
MEMBER_OPERATOR = "::"
FILE_PATH_OPERATOR = ":\\"
PATH_TO_GITHUB = "C:\\Users\\{}\\Documents\\GitHub\\".format(getpass.getuser())
STRING_FLAIR = "=================================="
ERROR_FLAIR = "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
SUCCESS_FLAIR = "*********************"
SEPERATOR = "-----"
libData = dict.fromkeys(["Arduino Path", "Source Path", "Header File",
                         "Header Path", "Class Name"])

def error_out(error, libData):

    if error == 0:
        print(ERROR_FLAIR)
        sys.exit("Incorrect path to the Arduino Library.")
    elif error == 1:
        print(ERROR_FLAIR)
        sys.exit("No 'src' file found in Arduino Library Directory")
    elif error == 2:
        print(ERROR_FLAIR)
        sys.exit("Incorrect Arduino Library location was given, try again.")
    elif error == 3:
        print(ERROR_FLAIR)
        sys.exit("No Header File found in the 'src' file.")
    elif error == 4:
        print(ERROR_FLAIR)
        sys.exit("No class defined in {}.".format(libData["Header File"]))
    elif error == 5:
        print(ERROR_FLAIR)
        sys.exit("No functions defined in {} class of the {} file.".format(libData["Class Name"],
                                                                           libData["Header File"]))
    elif error == 6:
        print(ERROR_FLAIR)
        sys.exit("No additional functions to add to {} file!".format(libData["Header File"]))

def get_path_to_arduino_dir():
    
    if len(sys.argv) > 1:

        userDir = sys.argv[1]

        if FILE_PATH_OPERATOR in userDir and os.path.isdir(userDir):
            if (verify_arduino_directory(userDir)):
                    return userDir  

        elif os.path.isdir(PATH_TO_GITHUB + userDir):
            if (verify_arduino_directory(PATH_TO_GITHUB + userDir)):
                return PATH_TO_GITHUB + userDir
        else:
            error_out(0)

    else:
        if verify_arduino_directory(os.getcwd()): 
            return os.getcwd() 
        else:
            error_out(0)

        
def get_path_to_src_dir(pPath):
    
    for file in os.listdir(pPath):
        if "src" in file:
            return pPath + os.sep + file
    
    error_out(1)

def verify_arduino_directory(arPath):
    for file in os.listdir(arPath):
        if "src" in file:
            return True
    
    error_out(2)

def get_path_to_header(sPath):

    for file in os.listdir(sPath):
        if file.endswith(".h"):
            if(confirm_header_file(sPath + os.sep + file)):
                return sPath + os.sep + file
            

def confirm_header_file(fPath):
    
    with open(fPath, 'r') as h:
        for line in h:
            if "class" in line:
                return True
    
    error_out(3)
                               
def get_header_file_name(sPath):
    
    for file in os.listdir(sPath):
        if file.endswith(".h"):
            headerFile = file
            return headerFile

def get_class_name(headerPath):

    with open(headerPath, 'r') as h: 
        for line in h:
            if "class" in line:
                words = line.split(' ')
                className = words[1] 
                if "\n" in className:
                    className = className.rstrip('\n')
                return className
    
    error_out(4)

def get_functions(sPath, hName, cName, fList):
   
    os.chdir(sPath)

    header = CppHeaderParser.CppHeader(hName)
    classInfo = header.classes[cName]

    for i in range(len(classInfo["methods"]["public"])):
        funcName = classInfo["methods"]["public"][i]["name"]
        if funcName == cName:
            continue
        elif funcName in fList:
            continue
        else:
            fList.append(funcName)

    if len(fList) == 0:
        error_out(5, libData)
    else:
        return fList

        

def check_if_keywords_exists(arPath):

    for file in os.listdir(arPath):
        if file == "keywords.txt":
            print("Keywords.txt file found.")
            return True

    print("Existing Keywords.txt file not found, creating new one!")

def format_keyword_file(lPath, cName, functions, hFile):

    os.chdir(lPath)
    exists = False
    fExists = False
    appendList = list()
    
    print("Checking if keywords.txt already exists.")
    if check_if_keywords_exists(lPath):
        with open("keywords.txt", 'a+') as k:
            k.seek(0)
            for line in k:
                if cName in line:
                    exists = True
                    break

            if exists == False:
                k.seek(0)
                k.write("Class {} \n".format(STRING_FLAIR))
                k.write("{}\tKEYWORD1\n".format(cName))
         
        with open("keywords.txt", 'r') as k:
            for function in functions:
                fExists = False
                k.seek(0)
                for line in k:
                    if function in line:
                        fExists = True
                        break
                
                if fExists == True:
                   continue 
                else:
                    appendList.append(function)
                    fExists = False
        
        if len(appendList) == 0:
            error_out(6, libData)
        else:
            with open("keywords.txt", 'a') as k:
                for function in appendList:
                    k.write("{}\tKEYWORD2\n".format(function))



    else:
        print("New keywords.txt file created.")
        with open("keywords.txt", 'w') as k:
            k.write("Class {} \n".format(STRING_FLAIR))
            k.write("{}\tKEYWORD1\n".format(cName))
            k.write("Functions {} \n".format(STRING_FLAIR))
            for function in functions: 
                k.write("{}\tKEYWORD2\n".format(function))
            


def create_keyword_file(lData):

    ardPath = get_path_to_arduino_dir()
    libData["Arduino Path"] = ardPath
    srcPath = get_path_to_src_dir(ardPath)
    libData["Source Path"] = srcPath 
    print("Arduino Library Path:\n{}\nPath to Source File:\
          \n{}\n{}".format(ardPath, srcPath, SEPERATOR))

    headerFilePath = get_path_to_header(srcPath)
    libData["Header Path"] = headerFilePath 
    headerFile     = get_header_file_name(srcPath)
    libData["Header File"] = headerFile 
    print("Header File Path:\n{}\nHeader File Name:\
          \n{}\n{}".format(headerFilePath, headerFile, SEPERATOR))

    className = get_class_name(headerFilePath)
    libData["Class Name"] = className 
    print("Class name:\n{}\n{}".format(className, SEPERATOR))

    print("Getting Functions....")
    functionList = list()
    get_functions(srcPath, headerFilePath, className, functionList)
    print("Functions gathered.\n{}".format(SEPERATOR))

    print("Creating Keyword File.")
    format_keyword_file(ardPath, className, functionList, headerFile)


print("\n{}\nArduino Keywords.txt File Creator\n{}\n".format(STRING_FLAIR,
                                                             STRING_FLAIR))
create_keyword_file(libData)
print("\n{}\n Keywords.txt Ready\n{}\n".format(SUCCESS_FLAIR, SUCCESS_FLAIR))
