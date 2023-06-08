#!/bin/bash
URL="<https://domain_name>"
OLD_IP="<OLD_REPO_ADDR>"
NEW_IP="<NEW_REPO_ADDR>"
USER="<USERNAME>"
PASS="<PASSWORD>"
PROJ_NAME=$2
PROJ_ID=$2

function search(){
    curl -s -X GET "${URL}/api/projects" -H "accept: application/json" -u ${USER}:${PASS} | grep -B 3 ${PROJ_NAME}
}

function pull(){
    REPOS=$( curl -s -X GET --header 'Accept: application/json' "${URL}/api/repositories?project_id=${PROJ_ID}" -u ${USER}:${PASS} |grep "name" | awk -F '"' '{print $4}' )
    for repo in ${REPOS}
    do
      TAGS=$( curl -s -X GET --header 'Accept: application/json' "${URL}/api/repositories/${repo}/tags" -u ${USER}:${PASS} |grep \"name\"|awk -F '"' '{print $4}'|sort -r )
      a=$(echo ${repo}|awk -F "/" '{print $2}')
        for tag in ${TAGS}
        do
          docker pull ${OLD_IP}"/"${repo}:${tag}
          echo ${NEW_IP}"/"${repo}:${tag} >> /opt/docker.tag
          docker tag ${OLD_IP}"/"${repo}:${tag} ${NEW_IP}"/"${repo}:${tag}
        done
    done
    echo -e "\033[32mexport successful!\033[0m"
}

function push(){
    for i in `cat /opt/docker.tag`; do docker push $i; done
}

case $1 in
    search)
        search
        ;;
    pull)
        pull
        ;;
    push)
        push
        ;;
    *)
        echo -e "\033[32mUsage：\n- ./harbor.sh search PROJECT_NAME\n- ./harbor.sh pull PROJECT_ID\n- ./harbor.sh push\033[0m"
esac
