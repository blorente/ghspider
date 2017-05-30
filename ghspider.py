import requests
import json
import os
import datetime
import sys
from git import Repo

now = datetime.datetime.now()
scriptdir = "/ghspider-%d-%d-%d/" % (now.year, now.month, now.day)

if len(sys.argv) == 1:
    print("No GitHub user specified")
    quit()

ghuser = sys.argv[1]

targetpath = ""
if len(sys.argv) < 3:
    targetpath = os.getcwd()
else:
    targetpath = sys.argv[2]

targetpath += scriptdir
print("Saving repos from /u/%s to %s" % (ghuser, targetpath))

response = requests.get("https://api.github.com/users/%s/repos" % ghuser)
repolist = json.loads(response.text)
for repo in repolist:
    reponame = repo["name"]
    repourl = repo["git_url"]
    print("Cloning repo " + reponame + " from " + repourl)
    Repo.clone_from(repourl, targetpath + reponame)
