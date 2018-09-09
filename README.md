# codeXaminer
This script extracts changed code or in-scope files from codebase and then run cloc utility to get Lines of Code (LOC). Then scan in-scope files with Checkmarx CxSAST and generate report.<br />

#### Dependency:<br />
* Selenium WebDriver & Python Client (https://www.seleniumhq.org/download/)<br />
* cloc (http://cloc.sourceforge.net/)<br />

#### Usage:<br />
_D:\Code\Python_programs>codeXaminer.py -h
_usage: codeXaminer.py [-h]
                      _sourcePath destinationPath changedFileList clocPath
                      _projectName

_positional arguments:
  _sourcePath       _Enter local path where codebase is located
  _destinationPath  _Enter local path where changed code or in-scope files will
                   _be saved
  _changedFileList  _Enter local path of the file containing list of changed
                   _code or in-scope files
  _clocPath         _Enter local path of the cloc utility
  _projectName      _Enter a unique project code or name_

_optional arguments:
  _-h, --help       show this help message and exit
  <br />

I developed it to help my colleagues who do code review. This helped us to channel our saved time and effort at code analysis on tight time constraint projects with huge codebase.<br />

If you understand DOM, then you can easily tweak the code to work with any Enterprise scanner of your choice. Also, I've added comments wherever possible for better understanding.<br />

I'd love to hear if this helped you in anyway.
