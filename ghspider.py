import requests
import json
import os
import datetime
import sys
from git import Repo
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

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

def get_repos(params, out):
    response = requests.get("https://api.github.com/users/%s/repos" % params['user'])
    repolist = json.loads(response.text)
    for repo in repolist:
        reponame = repo["name"]
        repourl = repo["git_url"]
        print("Cloning repo " + reponame + " from " + repourl)
        out.text += "Cloning repo " + reponame + " from " + repourl + '\n'
        Clock.schedule_once(Repo.clone_from(repourl, params['path'] + reponame), 1)

class GHSpiderWidget(Widget):
    def gather_and_backup(self, args):
        user = args['ghuser_ti'].text
        path = args['targetpath_ti'].text
        out = args['output_ti']
        out.text = "Cloning repos of /u/%s into %s..." % (user, path)
        repo_params = {
            'user': user,
            'path': path
        }
        get_repos(repo_params, out)

class GHSpiderApp(App):
    def build(self):
        return GHSpiderWidget()


if __name__ == '__main__':
    GHSpiderApp().run()
