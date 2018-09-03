# codeXaminer
This script extracts changed code or in-scope files from codebase and then run cloc utility to get Lines of Code (LOC). Then scan in-scope files with Checkmarx CxSAST and generate report.<br /><br />

#### Dependency:<br />
* Selenium WebDriver & Python Client (https://www.seleniumhq.org/download/)<br />
* cloc (http://cloc.sourceforge.net/)<br />

I developed it to help my colleagues who do code review. This helped us to channel our saved time and effort at code analysis on tight time constraint projects with huge codebase.<br />

If you understand DOM, then you can easily tweak the code to work with any Enterprise scanner of your choice. Also, I've added comments wherever possible for better understanding.<br />

I'd love to hear if this helped you in anyway.
