Keyword File Genertor
=====================
This Python 3 script will generate an Arduino Keyword File from a header
file. First [install the required Python packages](#installing-requirements), then [run the
script from the command line](#usage). Voila, you now have a
keywords file like the one pictured. 


![Keyword Success!](https://github.com/sparkfun/Keyword_File_Generator/blob/master/Readme%20Images/Keywords%20created!.JPG)

Installing Requirements
====================
You can install required Python packages by running this command from the repo root:

```pip install -r requirements.txt```

Usage
====================

To generate your "keywords.txt" file, give the path of 
the Arduino Library after the call to the keywords python script.
There are three methods to do this: 

* **Method One**

This method requires that the Arduino Library is in the default Github 
repo installation location: "C:\Users\YourUsername\Documents\Github\Arduino
Library". Give the name of the Arduino Library Folder after the call to the
script as shown below. 
![Method 1](https://github.com/sparkfun/Keyword_File_Generator/blob/master/Readme%20Images/method%201%20Run%20Script.JPG)

* **Method Two** 

The next method is to pull the script into Arduino Library itself (_not_ source
("src") file) and call it without any arguments. 
![Method 2](https://github.com/sparkfun/Keyword_File_Generator/blob/master/Readme%20Images/method%202%20Run%20Script.JPG)

* **Method Three**

Give the entire path to the Arduino Library:
![Method 3](https://github.com/sparkfun/Keyword_File_Generator/blob/master/Readme%20Images/Method3%20Run%20Script.JPG)

After running the script you'll get a readout that looks like the following:
![Script Succes](https://github.com/sparkfun/Keyword_File_Generator/blob/master/Readme%20Images/Success_readout_in_shell.JPG)
