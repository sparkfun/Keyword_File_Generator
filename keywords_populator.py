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

        
def get_path_to_src_dir(pPath):
    
    for file in os.listdir(pPath):
        if "src" in file:
            return pPath + os.sep + file

def verify_parent_directory(parPath):
    for file in os.listdir(parPath):
        if "src" in file:
            return True

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

    return fList

        

def check_if_keywords_exists(parPath):

    for file in os.listdir(parPath):
        if file == "keywords.txt":
            print("Keywords.txt file found.")
            return True

    print("Existing Keywords.txt file not found, creating new one!")

def format_keyword_file(lPath, cName, functions):

    os.chdir(lPath)
    exists = False
    z = 0
    
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
                k.write("Functions {} \n".format(STRING_FLAIR))
          
            for line in k:
                for i in range(len(functions)):
                    if functions[i] in line:
                        break
                    elif i == len(functions) - 1:
                        k.write("{}\tKEYWORD2\n".format(functions[z]))
                        z += 1
                        print(z)
                        k.seek(0)
                        break


    else:
        print("New keywords.txt file created.")
        with open("keywords.txt", 'w') as k:
            k.write("Class {} \n".format(STRING_FLAIR))
            k.write("{}\tKEYWORD1\n".format(cName))
            k.write("Functions {} \n".format(STRING_FLAIR))
            for function in functions: 
                k.write("{}\tKEYWORD2\n".format(function))
            


def create_keyword_file():

    parPath = get_path_to_src_par_dir()
    srcPath = get_path_to_src_dir(parPath)
    print("Arduino Library Path:\n{}\nPath to Source File:\
          \n{}\n".format(parPath, srcPath))

    headerFilePath = get_path_to_header(srcPath)
    headerFile     = get_header_file_name(srcPath)
    print("Header File Path:\n{}\nHeader File Name:\
          \n{}\n".format(headerFilePath, headerFile))

    className = get_class_name(headerFilePath)
    print("Class name:\n{}".format(className))

    print("Getting Functions....")
    functionList = list()
    get_functions(srcPath, headerFilePath, className, functionList)
    print("Functions gathered.")

    print("Creating Keyword File.")
    format_keyword_file(parPath, className, functionList)
    print("Keywords.txt populted with class name and its' functions.")


print("\n{}\nArduino Keywords.txt File Creator\n{}\n".format(STRING_FLAIR,
                                                             STRING_FLAIR))
create_keyword_file()
