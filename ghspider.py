import requests
import json
import os
import datetime
import sys
from git import Repo
from kivy.app import App
from kivy.uix.widget import Widget
import threading

now = datetime.datetime.now()
scriptdir = "/ghspider-%d-%d-%d/" % (now.year, now.month, now.day)

ghuser = ""
if len(sys.argv) > 1:
    ghuser = sys.argv[1]

targetpath = ""
if len(sys.argv) < 3:
    targetpath = os.getcwd()
else:
    targetpath = sys.argv[2]

targetpath += scriptdir
print("Saving repos from /u/%s to %s" % (ghuser, targetpath))

class GHSpiderWidget(Widget):
    stop = threading.Event()

    def gather_and_backup(self, args):
        user = args['ghuser_ti'].text
        path = args['targetpath_ti'].text
        out = args['output_ti']
        out.text = "Cloning repos of /u/%s into %s...\n" % (user, path)
        repo_params = {
            'user': user,
            'path': path
        }
        threading.Thread(target=self.get_repos, args=(repo_params, out)).start()

    def get_repos(self, params, out):
        response = requests.get("https://api.github.com/users/%s/repos" % params['user'])
        repolist = json.loads(response.text)
        for repo in repolist:
            if self.stop.is_set():
                return
            reponame = repo["name"]
            repourl = repo["git_url"]
            print("Cloning repo " + reponame + " from " + repourl)
            out.text += "Cloning repo " + reponame + " from " + repourl + '...'
            Repo.clone_from(repourl, params['path'] + reponame)
            out.text += 'Done\n'

class GHSpiderApp(App):
    def build(self):
        return GHSpiderWidget()


if __name__ == '__main__':
    GHSpiderApp().run()
