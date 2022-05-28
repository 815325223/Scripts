import requests
import io
import sys
import json

class GitLabUtils():

  def __init__(self, projectID):
    self.gitlab_url = "https://gitlab.brooks.com/api/v4"
    self.gitlab_token = "<GITLAB_TOKEN>"
    self.projectID = projectID
  
  def http_req(self, method, apiURL, headers, data):
    url = "{0}/{1}".format(self.gitlab_url, apiURL)
    response = requests.request(method, url, headers=headers, data=data)
    return response

  def get_repo_file(self, filePath, branch, targetFile):
    apiurl = "/projects/{0}/repository/files/{1}/raw?ref={2}".format(self.projectID, filePath, branch)
    headers = {
      'PRIVATE-TOKEN': self.gitlab_token,
      'Content-Type': 'application/json'
    }
    response = self.http_req("GET", apiurl, headers, {})
    self.write_file(response.text, targetFile)

  def write_file(self, content, filePath):
    with io.open(filePath, 'w', encoding='utf-8') as f:
      f.write(content)
      f.close()

  def create_repo_file(self, filePath, branch, content, commit_message):
    apiurl = "/projects/{0}/repository/files/manifests%2F{1}".format(self.projectID, filePath)
    data = json.dumps(
      {
        "branch": branch,
        "content": content,
        "commit_message": commit_message
      }
    )
    headers = {
      'PRIVATE-TOKEN': self.gitlab_token,
      'Content-Type': 'application/json'
    }
    msg = self.http_req("POST", apiurl, headers, data)
    if msg.json()["message"] == "A file with this name already exists":
      raise Exception("A file with this name already exists.")

  def update_repo_file(self, filePath, branch, content, commit_message):
    apiurl = "/projects/{0}/repository/files/manifests%2F{1}".format(self.projectID, filePath)
    data = json.dumps(
      {
        "branch": branch,
        "content": content,
        "commit_message": commit_message
      }
    )
    headers = {
      'PRIVATE-TOKEN': self.gitlab_token,
      'Content-Type': 'application/json'
    }
    self.http_req("PUT", apiurl, headers, data)

if __name__ == '__main__':
  # python GitLabUtils.py getfile 19 default.yaml master template.yaml
  if sys.argv[1] == "getfile":
    projectID, filename, branch, targetFile = sys.argv[2:]
    GitLabUtils(projectID).get_repo_file(filename, branch, targetFile)
  
  # python GitLabUtils.py updatefile 19 template.yaml master release-2.0.3.yaml
  if sys.argv[1] == "updatefile":
    projectID, filename, branch, targetFile = sys.argv[2:]
    with io.open(filename, 'r', encoding='utf-8') as f:
      content = f.read()
      f.close()
    try:
      GitLabUtils(projectID).create_repo_file(targetFile, branch, content, "created by ZCHENG.")
    except Exception as e:
      print(e)
      GitLabUtils(projectID).update_repo_file(targetFile, branch, content, "updated by ZCHENG.")
