```bash
#!/usr/bin/env bash

# ASSIGN REPO NAME AS VARIABLE 
REPO_NAME="AngularDemo"
SINCE='1 month ago'

# CLONE THE REPO WITHOUT CHECKOUT
git clone -n git@github.com:FourTimes/AngularDemo.git

# SWITCH THE REPO DIRECTORY
cd $REPO_NAME

for branch in $(git branch -r  | grep -v HEAD | egrep -v "(^\*|master|dev|main)" | sed /\*/d); do
        if [ -z "$(git log -1 --since=${SINCE} -s ${branch})" ]; then
                echo -e `git show --format="%ci %cr %an" ${branch} | head -n 1` \\t$branch
                remote_branch=$(echo ${branch} | sed 's#origin/##' )
                # To delete the branches uncomment the bellow git delete command
                git push origin --delete ${remote_branch}
        fi
done

# REMOVE THE REPO DIRECTORY
rm -rf ../$REPO_NAME

# NOTE => $(git branch -r  | grep -v HEAD | grep -v develop | grep -v master | grep -v main |  grep -v release | sed /\*/d)

```
