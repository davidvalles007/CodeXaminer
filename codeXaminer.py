import os,string,shutil,argparse,subprocess,sys,ctypes,time, winsound
from Tkinter import Label, Tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


parser=argparse.ArgumentParser()
parser.add_argument("sourcePath",help="Enter local path where codebase is located")
parser.add_argument("destinationPath",help="Enter local path where changed code or in-scope files will be saved")
parser.add_argument("changedFileList",help="Enter local path of the file containing list of changed code or in-scope files")
parser.add_argument("clocPath",help="Enter local path of the cloc utility")
parser.add_argument("projectName",help="Enter a unique project code or name")


args=parser.parse_args()
sourcePath=args.sourcePath
destinationPath=args.destinationPath
changedFileList=args.changedFileList
clocPath=args.clocPath
projectName=args.projectName

if len(sys.argv[1:])==0:
    parser.print_usage()
    raw_input()
    sys.exit(1)
    
if (os.path.isdir(sourcePath) and os.path.isdir(destinationPath) and os.path.isfile(changedFileList) and os.path.isfile(clocPath)):
    pass

else:
    print >> sys.stderr, "[!] Error. Please check whether the provided input paths exists."
    raw_input("Press any key to exit")
    os._exit()


banner = '''                 
               _     __  __               _                 
  ___ ___   __| | ___\ \/ /__ _ _ __ ___ (_)_ __   ___ _ __ 
 / __/ _ \ / _` |/ _ \\  // _` | '_ ` _ \| | '_ \ / _ \ '__|
| (_| (_) | (_| |  __//  \ (_| | | | | | | | | | |  __/ |   
 \___\___/ \__,_|\___/_/\_\__,_|_| |_| |_|_|_| |_|\___|_|   
                                                            
                By David Valles (@davidvalles007)
                
'''

print >> sys.stdout, banner

# Notification popup
msg='Extracting file(s)...'
def prompt(msg):
    root = Tk()
    prompt = msg
    label1 = Label(root, text='\n'+prompt+'\n', width=len(prompt), bg="black", fg="green", font="Time 16 bold")
    label1.pack()
    #makes the popup the center of the screen
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    
    def close_after_3s():
        root.destroy()

    if 'scanning complete' not in msg:
        root.after(3000, close_after_3s)

    root.mainloop()


prompt(msg)

print >> sys.stdout, '\n[+] Starting file(s) extraction...\n'
with open(changedFileList,'r') as fi:
    changedFiles=fi.readlines()

try:
    outfile=open('ScopeFiles.txt','w')
    outfile.write('In-Scope file(s): \n\n')
except:
    print >> sys.stderr, "[!] ERROR: Unable to create In-Scope Output file"

for changedFile in changedFiles:
    changedFile=changedFile.encode('string-escape')
    
    if '\\n' in changedFile:
        changedFile=changedFile[:-2]

    if os.path.exists(changedFile):
        if not os.path.isdir(string.replace(changedFile,sourcePath,destinationPath)):
                       
            #Creates New Directory Structure
            if not os.path.isdir(string.replace('\\'.join(changedFile.split('\\\\')[:-1]),sourcePath,destinationPath)):
                os.makedirs(string.replace('\\'.join(changedFile.split('\\\\')[:-1]),sourcePath,destinationPath))

            try:    
                #Moves File              
                shutil.copy2(changedFile,(string.replace('\\'.join(changedFile.split('\\\\')[:-1]),sourcePath,destinationPath)))
                print >> sys.stdout, '[-] '+'\\'.join(changedFile.split('\\\\'))
                outfile.write('\\'.join(changedFile.split('\\\\'))+"\n")
            except:
                print >> sys.stderr, "[!] ERROR: Unable to move files to %s" % destinationPath

    else:
        outfile.write('[!] Error in copying '+'\\'.join(changedFile.split('\\\\'))+"***\n")

outfile.close()

#ZIP-IT
try:
    shutil.make_archive(destinationPath+'\\'+projectName, 'zip', destinationPath)
    zipFile=destinationPath+'\\'+projectName+'.zip'
except:
    print >> sys.stderr, "[!] ERROR: Unable to create zip file"
    os._exit()

print >> sys.stdout, '\n[+] Done! You can also check the transfer log file - ScopeFiles.txt\n'
print >> sys.stdout, '\n[+] Running Cloc Utility now...\n'


# CLOC
msg='Starting Cloc...'
prompt(msg)

CREATE_NO_WINDOW = 0x08000000   #Hides cloc gui window

args = clocPath+" "+destinationPath
try:
    popen = subprocess.Popen(args, stdout=subprocess.PIPE,creationflags=CREATE_NO_WINDOW)
    popen.wait()
    output = popen.stdout.read()
    print >> sys.stdout, output
except:
    print >> sys.stderr, "ERROR: Cloc path not found"
    os._exit(1)

try:
    cloc_output=file("ClocOutput.txt","w")
    cloc_output.write(output)
    cloc_output.close()
except:
    print >> sys.stderr, "ERROR: Unable to create Cloc Output file"

msg = 'Cloc run complete.'
print >> sys.stdout, '\n[+] Cloc run complete..\n'
prompt(msg)

time.sleep(2)

# CHECKMARX
print >> sys.stdout, '\n[+] Starting Checkmarx CxSAST ...\n'
msg='Starting Checkmarx CxSAST'
prompt(msg)

url='REPLACE THIS STRING WITH CHECKMARX CxSAST LOGIN URL HERE'     # For e.g. https://scanmachine/CxWebClient/Login.aspx
browser = webdriver.Ie('C:\Selenium\IEDriver\IEDriverServer.exe')  # Local path of Selenium Web Driver. I used IE here.

#Login page
browser.get(url)
browser.maximize_window()
assert 'Checkmarx' in browser.title

elem = browser.find_element_by_name('txtUserName')  # Find the username box
elem.send_keys('REPLACE THIS STRING WITH USERNAME') # This is for educational purpose only. It is not recommended to leave plaintext username & password in the script.
elem = browser.find_element_by_name('txtPassword')  # Find the password box
elem.send_keys('REPLACE THIS STRING WITH PASSWORD' + Keys.RETURN)
time.sleep(2)

# NewProject Page
browser.get('REPLACE THIS STRING WITH THE URL OF THE NEW PROJECT PAGE') # For e.g. https://scanmachine/CxWebClient/NewProject.aspx

#General Page
elem = browser.find_element_by_name('ctl00$cpmain$ProjectNameTextBox')  # Find the ProjectName box
elem.send_keys('%s'%projectName)

elem = browser.find_element_by_name('ctl00$cpmain$PresetDropDownList')  # Find the Preset Option
elem.clear();
elem.send_keys('All'+ Keys.RETURN)
time.sleep(2)

elem = browser.find_element_by_name('ctl00$cpmain$NextButton')  # Click Next Button
elem.click()
time.sleep(2)

#Location Page
elem = browser.find_element_by_name('ctl00$cpmain$LocalButton_input')  # Click Select Button
elem.click()
time.sleep(2)

browser.switch_to_frame(browser.find_element_by_tag_name('iframe')) #Find the iframe loading the upload popup
elem = browser.find_element_by_name('FileAsyncUploadfile0')  # Click Select button
elem.send_keys('%s'%zipFile)

elem=browser.find_element_by_name('btnUpload') # Click Upload button
elem.click()

browser.switch_to_default_content() #Move back to original window

elem=browser.find_element_by_name('ctl00$cpmain$FinishButton') # Click Finish button
elem.click()

time.sleep(30)
tds=None
def check():    #Check if the scan is complete
    browser.get('REPLACE THIS STRING WITH URL OF SCAN PAGE')                 # https://scanmachine/CxWebClient/Scans.aspx
    browser.maximize_window()
    browser.execute_script("window.scrollTo(0,document.body.scrollWidth);")  #Horizontal Scroll to complete right so that "Action" column becomes visible to the script
    elem = browser.find_element_by_id('ctl00_cpmain_ScansGrid_ctl00__0')     #Iterate table row
    tds=elem.find_elements(By.TAG_NAME,'td')                                 #Iterate table data for a single selected row
    return tds

while True:
    tds=check()
    if tds[4].text!=projectName:    # Indicator that projectName is populated in dashboard once complete
        time.sleep(30)
    else:
        break
    
magnifyingGlass=tds[13].find_elements(By.TAG_NAME,'img')[0]
magnifyingGlass.click()

tds=check()
ReportGen=tds[13].find_elements(By.TAG_NAME,'img')[1]
ReportGen.click()

time.sleep(2)
browser.switch_to_frame(browser.find_element_by_tag_name('iframe'))
elem = browser.find_element_by_id('rblTypes_2')
elem.click()

elem = browser.find_element_by_id('btnGenerate_input')
elem.click()
browser.switch_to_default_content() #Move back to original window

#Make a beep sound to alert at the end of the scan completion
freq=2500
dur=300
winsound.Beep(freq,dur)
print >> sys.stdout, '\n[+] Checkmarx scanning complete.\n\n'
msg = 'Checkmarx scanning complete.\n\n'
prompt(msg)
time.sleep(2)
raw_input("Press any key to exit")
