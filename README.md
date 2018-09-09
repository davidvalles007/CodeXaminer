# codeXaminer
This script extracts changed code or in-scope files from codebase and then run cloc utility to get Lines of Code (LOC). Then scan in-scope files with Checkmarx CxSAST and generate report.<br />

#### Dependency:<br />
* Selenium WebDriver & Python Client (https://www.seleniumhq.org/download/)<br />
* cloc (http://cloc.sourceforge.net/)<br />

#### Usage:<br />
_D:\Code\Python_programs>codeXaminer.py_ _-h_<br />
_usage:_ _codeXaminer.py_ _[-h]_<br />
                      _sourcePath_<br />
                      _destinationPath_<br />
                      _changedFileList_<br />
                      _clocPath_<br />
                      _projectName_<br />
<br />
_positional arguments:_<br />
  _sourcePath_      ->   _Enter local path where codebase is located_<br />
  _destinationPath_ ->   _Enter local path where changed code or in-scope files will be saved_<br />
  _changedFileList_  ->  _Enter local path of the file containing list of changed code or in-scope files_<br />
  _clocPath_      ->     _Enter local path of the cloc utility_<br />
  _projectName_   ->     _Enter a unique project code or name_<br />
<br />
_optional arguments:_<br />
  _-h, --help_       _show this help message and exit_<br />
  <br />

I developed it to help my colleagues who do code review. This helped us to channel our saved time and effort at code analysis on tight time constraint projects with huge codebase.<br />

If you understand DOM, then you can easily tweak the code to work with any Enterprise scanner of your choice. Also, I've added comments wherever possible for better understanding.<br />

I'd love to hear if this helped you in anyway.
