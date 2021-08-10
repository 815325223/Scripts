#!/bin/bash
URL="https://harbor.example.com"
IP="harbor.example.com"
USER="{USER}"
PASS="{PASSWORD}"
PROJ_NAME=$2
PROJ_ID=$2
NEW_ADDRESS=$2
SAVE=""
DATE=$(date "+%Y%m%d")

function search(){
    curl -s -X GET "${URL}/api/projects" -H "accept: application/json" -u ${USER}:${PASS} | grep -B 3 ${PROJ_NAME}
}

function export(){
    REPOS=$( curl -s -X GET --header 'Accept: application/json' "${URL}/api/repositories?project_id=${PROJ_ID}" -u ${USER}:${PASS} |grep "name" | awk -F '"' '{print $4}' )
    for repo in ${REPOS}
    do
      TAGS=$( curl -s -X GET --header 'Accept: application/json' "${URL}/api/repositories/${repo}/tags" -u ${USER}:${PASS} |grep \"name\"|awk -F '"' '{print $4}'|sort -r )
      a=$(echo ${repo}|awk -F "/" '{print $2}')
        for tag in ${TAGS}
        do
          docker pull ${IP}"/"${repo}:${tag}
          echo ${IP}"/"${repo}:${tag} >> /opt/docker.tag
          docker save ${IP}"/"${repo}:${tag} > /opt/docker/${IP}-${a}-${tag}.tar.gz
        done
    done
    echo -e "\033[32mexport successful!\033[0m"
}

function convert(){
    sed -i.bak "s/harbor.example.com/${NEW_ADDRESS}/g" /opt/docker.tag
}

function import(){
    for i in `cat /opt/docker.tag`; do docker push $i; done
}

case $1 in
    search)
        search
        ;;
    export)
        export
        ;;
    convert)
        convert
        ;;
    import)
        import
        ;;
    *)
        echo -e "\033[32mUsage：\n- ./harbor.sh search PROJECT_NAME\n- ./harbor.sh export PROJECT_ID\n- ./harbor.sh convert NEW_HARBOR_ADDRESS\n- ./harbor.sh import\033[0m"
esac
