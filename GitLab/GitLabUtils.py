import requests
import json
import base64
import sys
import io

class GitLabUtils():

    def __init__(self, projectID):
        self.gitlab_url = "http://gitlab.devops.local/api/v4"
        self.gitlab_token = '<GITLAB_ACCESS_TOKEN>'
        self.projectID = projectID
        self.encoding = "base64"

    def http_req(self, method, apiURL, headers, data):
        url = "{0}/{1}".format(self.gitlab_url, apiURL)
        response = requests.request(method, url, headers=headers, data=data)
        return response

    def write_file(self, content, filePath):
        with io.open(filePath, 'w', encoding = 'utf-8') as f:
            f.write(content)

    def get_repo_file(self, filePath, branch, targetFile):
        apiurl = "projects/{0}/repository/files/{1}/raw?ref={2}".format(self.projectID, filePath, branch)
        headers = {
          'PRIVATE-TOKEN': self.gitlab_token,
          'Content-Type': 'application/json'
        }
        response = self.http_req("GET", apiurl, headers, {})
        self.write_file(response.text, targetFile)

    def create_repo_file(self, filePath, branch, content, commit_message):
        apiurl = "projects/{0}/repository/files/{1}".format(self.projectID, filePath)
        data = json.dumps({
          "branch": branch,
          "content": content,
          "commit_message": commit_message
        })
        headers = {
          'PRIVATE-TOKEN': self.gitlab_token,
          'Content-Type': 'application/json'
        }
        msg = self.http_req("POST", apiurl, headers=headers, data=data)
        if json.loads(msg)["message"] == "A file with this name already exists":
            raise Exception("A file with this name already exists.")

    def update_repo_file(self, filePath, branch, content, commit_message):
        apiurl = "projects/{0}/repository/files/{1}".format(self.projectID, filePath)
        data = json.dumps({
          "branch": branch,
          "content": content,
          "commit_message": commit_message
        })
        headers = {
          'PRIVATE-TOKEN': self.gitlab_token,
          'Content-Type': 'application/json'
        }
        self.http_req("PUT", apiurl, headers=headers, data=data)


if __name__ == '__main__':
    if sys.argv[1] == "getfile":
        # python GitLabUtils.py getfile "19" "default.yaml" "master" "deployments.yaml"
        projectID, filename, branch, targetFile = sys.argv[2:]
        GitLabUtils(projectID).get_repo_file(filename, branch, targetFile)

    if sys.argv[1] == "updatefile":
        # python GitLabUtils.py updatefile "19" "default.yaml" "master" "deployments.yaml"
        projectID, filename, branch, targetFile = sys.argv[2:]
        f = io.open(filename, 'r', encoding = 'utf-8')
        content = f.read()
        f.close()
        try:
            GitLabUtils(projectID).create_repo_file(targetFile, branch, content, "commited by zcheng.")
        except Exception as e:
            print(e)
            GitLabUtils(projectID).update_repo_file(targetFile, branch, content, "commited by zcheng.")
