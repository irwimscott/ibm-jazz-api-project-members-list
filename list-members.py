import requests
import sys
import csv, itertools
from itertools import izip
from xml.dom import minidom
requests.packages.urllib3.disable_warnings()

reload(sys)
## Force UTF-8 - xml default encoding
sys.setdefaultencoding('utf-8')

## Start session
s = requests.Session()

## Insert csv filename thats the script will generate
csvfilename="jazz-projects-members.csv"

## Jazz URL
jazz_url = "myjazzserver.domain.com"

## Load username and password
username='USERNAMEHERE'
passwd='MYPASSWORDHERE'

## URL Parameters
url_auth = "https://%s/jazz/authenticated/j_security_check?j_username=%s&j_password=%s" % (jazz_url, username, passwd)
url_projects = "https://%s/jazz/process/project-areas" % (jazz_url)

## Make authentication - ALways ignoring certificate
auth = s.post(url_auth, verify=False)

## Obtain Token from cookies
ltpatoken = s.cookies['LtpaToken2']

## Add Token to header
headers = {'LtpaToken2': ltpatoken}

## Make a request to obtain all project names
projects_get = s.get(url_projects, headers=headers, verify=False)

## Parse the XML from projects
project_area_result = minidom.parseString(projects_get.text)
projects = project_area_result.getElementsByTagName("jp06:project-area")

## Start the loop creating a new CSV file and create the correct table with Prject name and current members
with open(csvfilename, 'wb') as csvfile:
  writer = csv.writer(csvfile, delimiter=";")
## Read the entire XML page to obtain project-names
  for project in projects:
     pid = project.getAttribute("jp06:name")
     members_url = project.getElementsByTagName("jp06:members-url")[0]
     urldosmembros=members_url.firstChild.data
     users_get = s.get(urldosmembros, headers=headers, verify=False)
     users_result = minidom.parseString(users_get.text)
     uget = users_result.getElementsByTagName("jp06:member")
     users_array=[]
     for staff in uget:
      u = staff.getElementsByTagName("jp06:user-url")[0]
      username = u.firstChild.data.split('/')[-1]
      users_array.append(username)
     total=users_array
     ## print(pid,[total])
     writer.writerows(izip([pid],[total]))
