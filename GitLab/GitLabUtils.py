import sys
import requests
import io
import json

class GitLabUtils():

  def __init__(self, ProjectID):
    self.gitlab_url = "http://gitlab.devops.local/api/v4"
    self.gitlab_token = "<GITLAB_TOKEN>"
    self.ProjectID = ProjectID

  def http_req(self, method, apiURL, headers, data):
    url = "{0}/{1}".format(self.gitlab_url, apiURL)
    response = requests.request(method, url, headers=headers, data=data)
    return response

  def get_repo_file(self, filePath, branch, targetFile):
    apiurl = "/projects/{0}/repository/files/{1}/raw?ref={2}".format(self.ProjectID, filePath, branch)
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
    apiurl = "/projects/{0}/repository/files/manifests%2f{1}".format(ProjectID, filePath)
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
    if msg.status_code == 400:
      raise Exception("A file with this name already exists.")
  
  def update_repo_file(self, filePath, branch, content, commit_message):
    apiurl = "/projects/{0}/repository/files/manifests%2f{1}".format(ProjectID, filePath)
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

if __name__ == "__main__":
  if sys.argv[1] == "getfile":
    ProjectID, filename, branch, targetFile = sys.argv[2:]
    GitLabUtils(ProjectID).get_repo_file(filename, branch, targetFile)

  if sys.argv[1] == "updatefile":
    ProjectID, filename, branch, targetFile = sys.argv[2:]
    with io.open(filename, 'r', encoding='utf-8') as f:
      content = f.read()
      f.close()
    try:
      GitLabUtils(ProjectID).create_repo_file(targetFile, branch, content, "created by ZCHENG.")
    except Exception as e:
      print(e)
      GitLabUtils(ProjectID).update_repo_file(targetFile, branch, content, "updated by ZCHENG.")
