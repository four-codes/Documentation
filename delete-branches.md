```bash
#!/usr/bin/env bash

GROUP_REPO_COMBINATION=$1
SINCE=$2
REPO_USERNAME=$3
REPO_TOKEN=$4 
REPO_NAME=`echo "${GROUP_REPO_COMBINATION}" | awk -F / '{print $2}'`

# REMOVE THE BASE REPO META INFORMATION
rm -rf .git

# SSH CLONE REPO WITHOUT CHECKOUT
# git clone -n "git@github.com:${GROUP_REPO_COMBINATION}.git"

# HTTPS CLONE REPO WITHOUT CHECKOUT
git clone "https://${REPO_USERNAME}:${REPO_TOKEN}@github.com/${GROUP_REPO_COMBINATION}.git"

# SWITCH THE REPO DIRECTORY
cd $REPO_NAME

for branch in $(git branch -r  | grep -v HEAD | egrep -v "(^\*|master|dev|main)" | sed /\*/d); do
        if [ -z '$(git log -1 --since="${SINCE}" -s ${branch})' ]; then
                echo -e `git show --format="%ci %cr %an" ${branch} | head -n 1` \\t$branch
                remote_branch=$(echo ${branch} | sed 's#origin/##' )
                # To delete the branches uncomment the bellow git delete command
                git push origin --delete ${remote_branch}
        fi
done

# REMOVE THE REPO DIRECTORY
rm -rf "../${REPO_NAME}"

# NOTE => $(git branch -r  | grep -v HEAD | grep -v develop | grep -v master | grep -v main |  grep -v release | sed /\*/d)
# run command => bash filename.sh REPO_NAME
```
