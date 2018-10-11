import requests
import base64
import sys
import uritools
import keyring

s = requests.Session()

# User Credentials
USER_NAME = "jls102"
PASSWORD = keyring.get_password('webprint', USER_NAME)

# Mostly useless constants
FILE_NAME = sys.argv[1]
FILE_PATH = sys.argv[2]
verify = True

print(FILE_NAME)
print(FILE_PATH)

# Form the string for the login request, by concatenating the username and
# password.
authcode = base64.b64encode(bytes(USER_NAME + ":" + PASSWORD, 'utf-8')).decode('ASCII')
authheaders = {'Authorization' : 'PHAROS-USER ' + authcode}

# Send a login request
s.get("https://webprint.bucknell.edu/PharosAPI/logon?KeepMeLoggedIn=no", headers=authheaders, verify=verify)

# Get the end of the URL for uploading the file.
useruri = uritools.uridecode(s.cookies['PharosAPI.X-PHAROS-USER-URI'])

# Establish the headers for the upload request
headers={'X-Requested-With':'XMLHttpRequest',
         'Accept':'*/*', 
         'Referer':'https://webprint.bucknell.edu/myprintcenter/', 
         'Origin':'https://webprint.bucknell.edu',
         'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) " +
          "Chrome/47.0.2526.111 Safari/537.36"}
url = "https://webprint.bucknell.edu/PharosAPI" + useruri + "/printjobs"
files = {'content': (FILE_NAME.replace("/", ":").replace("\\", ":"), open(FILE_PATH, 'rb'), "application/pdf")}

data = {'MetaData':'{"FinishingOptions":{"Mono":true,"Duplex":true,"PagesPerSide":"1","Copies":"1","DefaultPageSize":"Letter"}}'}

# Make the upload request
s.post(url, files=files, data=data, headers=headers)
