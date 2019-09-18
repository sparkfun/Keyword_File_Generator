import os
import sys
import getpass
import CppHeaderParser

FILE_PATH_OPERATOR = ":\\"
PATH_TO_GITHUB = "C:\\Users\\{}\\Documents\\GitHub\\".format(getpass.getuser())
STRING_FLAIR = "=================================="
ERROR_FLAIR = "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
SUCCESS_FLAIR = "*********************"
SEPERATOR = "-----"
libData = dict.fromkeys(["Arduino Path", "Source Path", "Header File",
                         "Header Path", "Class Name"])

# This function prints out the errors messages defined for this script.
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

# This functions gets the path to the Arduino Library directory through the
# name given via command line. If no argument is provided then it checks to see
# if the script was run from within the folder. 
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
            error_out(0, libData)

    else:
        if verify_arduino_directory(os.getcwd()): 
            return os.getcwd() 
        else:
            error_out(0, libData)

# This function retrieves the directory path to the source ("src") file in the
# Arduino Library Directory.
def get_path_to_src_dir(pPath):
    
    for file in os.listdir(pPath):
        if "src" in file:
            return pPath + os.sep + file
    
    error_out(1, libData)

# This function checks that the Arduino Library is "valid" by checking that
# there is a "src" file in it. 
def verify_arduino_directory(arPath):
    for file in os.listdir(arPath):
        if "src" in file:
            return True
    
    error_out(2, libData)

# This function retrieves the directory path to the header file.
def get_path_to_header(sPath):

    for file in os.listdir(sPath):
        if file.endswith(".h"):
            if(confirm_header_file(sPath + os.sep + file)):
                return sPath + os.sep + file
            

# This function confirms that there is a header file in teh Arduino Library 
# folder.
def confirm_header_file(fPath):
    
    with open(fPath, 'r') as h:
        for line in h:
            if "class" in line:
                return True
    
    error_out(3, libData)
                               
# This function gets the name of the header file in the Arduino Library folder.
def get_header_file_name(sPath, hList):
    
    for file in os.listdir(sPath):
        if file.endswith(".h"):
            hList.append(file)

    return hList

# This function gets the class name from the header file.        
def get_class_name(headerPath):

    with open(headerPath, 'r') as h: 
        for line in h:
            if "class" in line:
                words = line.split(' ')
                className = words[1] 
                if "\n" in className:
                    className = className.rstrip('\n')
                return className
    
    error_out(4, libData)

# This function gets the function names from the header file.        
def get_functions(sPath, hName, cName, fList, hList):
   
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

# This function gets the constants from the header file.        
def get_constants_and_enums(sPath, hName, cList, eList):

    os.chdir(sPath)

    header = CppHeaderParser.CppHeader(hName)

    # Ignore the protection define at the top of the list. 
    for define in header.defines: 
        if define.startswith("_"):
            continue
        cList.append(define.split(" ")[0])

    # Gets each individual value within enum.
    for i in range(len(header.enums)):
        for x in range(len(header.enums[i]["values"])):
            cList.append(header.enums[i]["values"][x]["name"])
    
    # Gets the type name of the enum.
    for enum in header.enums:
        eList.append(enum["name"])

    if len(cList) == 0:
        print("Didn't find any constants......no problemo, continuing.")
    else:
        return cList

# This function checks if the keywords.txt file is already in the library file. 
def check_if_keywords_exists(arPath):

    for file in os.listdir(arPath):
        if file == "keywords.txt":
            print("Keywords.txt file found.")
            return True

    print("Existing Keywords.txt file not found, creating new one!")

# This creates the file after all of the class names, functions, and constants
# have been gathered.
def format_keyword_file(lPath, cName, functions, constants, enums):

    os.chdir(lPath)
    exists = False
    fExists = False
    cExists = False
    eExists = False
    funcAppendList = list()
    constAppendList = list()
    enumAppendList = list()
   
    # This "if" statement checks for a "keywords.txt" file. If the file exists 
    # then we take stock of what functions and constants are already there, and
    # only add the ones that are not. 
    print("Checking if keywords.txt already exists.")
    if check_if_keywords_exists(lPath):
        # Check for class name first -> that's KEYWORD1
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
            # Check for functions next -> KEYWORD2
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
                    funcAppendList.append(function)
                    fExists = False

            # Check for constants next -> LITERAL1
            for constant in constants:
                cExists = False
                k.seek(0)
                for line in k:
                    if constant in line:
                        cExists = True
                        break
                
                if cExists == True:
                   continue 
                else:
                    constAppendList.append(constant)
                    cExists = False

            # Check for enum last -> KEYWORD1
            for enum in enums:
                eExists = False
                k.seek(0)
                for line in k:
                    if enum in line:
                        eExists = True
                        break
                
                if eExists == True:
                   continue 
                else:
                    enumAppendList.append(enum)
                    eExists = False
       
        #The lists of missing items is ready, now they are appended to file. 
        if len(funcAppendList) == 0:
            error_out(6, libData)
        else:
            with open("keywords.txt", 'a') as k:
                for function in funcAppendList:
                    k.write("{}\tKEYWORD2\n".format(function))
                for constant in constAppendList:
                    k.write("{}\LITERAL1\n".format(constant))
                for enum in enumAppendList:
                    k.write("{}\tKEYWORD1\n".format(enum))


    
    #If the file does not exist (easy), just make a file with the goods. 
    else:
        print("New keywords.txt file created.")
        with open("keywords.txt", 'w') as k:
            k.write("{}\nCLASS\n{}\n".format(STRING_FLAIR, STRING_FLAIR))
            k.write("{}\tKEYWORD1\n".format(cName))
            k.write("\n{}\nFUNCTIONS\n{}\n".format(STRING_FLAIR, STRING_FLAIR))
            for function in functions: 
                k.write("{}\tKEYWORD2\n".format(function))
            k.write("\n{}\nCONSTANTS\n{}\n".format(STRING_FLAIR, STRING_FLAIR))
            for constant in constants: 
                k.write("{}\tLITERAL1\n".format(constant))
            k.write("\n{}\nDATA TYPES\n{}\n".format(STRING_FLAIR, STRING_FLAIR))
            for enum in enums: 
                k.write("{}\tKEYWORD1\n".format(enum))
            


# This creates a new keywords file from the given ,or not given, directory
# path. 
def create_keyword_file(lData):

    ardPath = get_path_to_arduino_dir()
    libData["Arduino Path"] = ardPath
    srcPath = get_path_to_src_dir(ardPath)
    libData["Source Path"] = srcPath 

    print("Arduino Library Path:\n{}\nPath to Source File:\
          \n{}\n{}\n".format(ardPath, srcPath, SEPERATOR))

    headerFilePath = get_path_to_header(srcPath)
    libData["Header Path"] = headerFilePath 
    headerList = list()
    headerList = get_header_file_name(srcPath, headerList)
    libData["Header File"] = headerList 

    print("Header File Path:\n{}\n".format(headerFilePath, SEPERATOR))
    print("Header Files: ")
    for file in headerList:
        print(file)
    print(SEPERATOR)

    className = get_class_name(headerFilePath)
    libData["Class Name"] = className 

    print("Class name:\n{}\n{}".format(className, SEPERATOR))

    print("Getting Functions....")
    functionList = list()
    get_functions(srcPath, headerFilePath, className, functionList, hList)
    print("Functions gathered.\n{}".format(SEPERATOR))

    print("Getting Literals....") 
    constantList = list();
    enumList = list()
    get_constants_and_enums(srcPath, headerFilePath, constantList, enumList)
    print("Constants gathered.\n{}".format(SEPERATOR))
    
    print("Creating Keyword File.")
    format_keyword_file(ardPath, className, functionList, constantList,
                        enumList)







#-----------------End of Functions----------------------------------------





print("\n{}\nArduino Keywords.txt File Creator\n{}\n".format(STRING_FLAIR,
                                                             STRING_FLAIR))
create_keyword_file(libData)
print("\n{}\n Keywords.txt Ready\n{}\n".format(SUCCESS_FLAIR, SUCCESS_FLAIR))
