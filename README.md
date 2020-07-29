Keyword File Generator
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

The ```keywords_populator.py``` script is used as follows:

```./keywords_populator.py [-p PATHSPEC] [-r] [--recursive] [-d DEST] [-v] [--verbose]```

* **PATHSPEC**: a pattern that matches files or directories to search for keywords
  * *default*: ```'./*/*'```
  * ```PATHSPEC``` is expanded using the ```braceexpansion``` module 
  * all results from expansion are fed to the ```glob``` module to determine pattern matches ```glob.glob(PATHSPEC)``` - see Python ```glob``` module
  * all pattern matches are concatenated then only header (```'*.h'``` or ```'.H'```) files are processed
* **--recursive**: if specified the matches will be obtained using ```glob.glob(PATHSPEC, recursive=True)```
  * *default*: ```False```
* **DEST**: the desired output path to the ```keywords.txt``` file (```DEST/keywords.txt```)
  * *default*: ```None```
  * is not brace expanded or pattern matched - this should be a single relative or absolute path
* **--verbose**: enable verbose output
  * *default*: ```False```


## Tips

### Simple Case

To generate the ```keyword.txt``` file for a standard Arduino library you may place the script in the library directory as so:

```
- myLibrary
|- keywords_populator.py
|- src
 |- myHeader.h
 |- mySource.cpp
```

Now running:

```
cd myLibrary
./keywords_populator.py
```

will add the ```keywords.txt``` file in the ```myLibrary``` directory next to the script. This is the proper location for a typical Arduino library.

What happened:
* the default ```PATHSPEC``` is ```'./*/*'``` which allows the generator to find ```'./src/myHeader.h'```
* the default ```DEST``` is ```None``` so the common path between all the matched files is: ```'./src'``` and the output path uses the 'dirname' of the common path, or: ```'.'```. Lastly the otuput filename is constructed as ```output_path + '/keywords.txt'```
