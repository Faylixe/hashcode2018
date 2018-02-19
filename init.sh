#!/bin/bash

if [ $# -eq 0 ]
then
    echo 'Workspace name not provided'
    echo 'Usage : bash init.sh workspace_name'
    exit -1
fi

# Get google account credentials. 
echo 'Please enter your google account credentials :'
echo -n 'Email: '
read username
echo -n 'Password: '
read -s password

# TODO : Add round id here.
round=''
# echo 'Please enter target HashCode round identifier :'
# echo -n 'Round: '
# read round

# Configure workspace.
workspace=$1
mkdir -p workspace/$workspace
if [ ! -f workspace/$workspace/__init__.py ]
then
    touch workspace/$workspace/__init__.py
    cp utils/template.py workspace/$workspace/
fi

# Configure virtualenv.
# TODO : Remove old virtualenv if any ?
virtualenv venv
echo "export SLACK_WEBHOOK='https://hooks.slack.com/services/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'" >> venv/bin/activate
echo "export GOOGLE_USERNAME='$username'" >> venv/bin/activate
echo "export GOOGLE_PASSWORD='$password'" >> venv/bin/activate
echo "export ROUND='$round'" >> venv/bin/activate
echo "export WORKSPACE='$workspace'" >> venv/bin/activate
echo >>venv/bin/activate <<EOL
_get_solution_path() {
    local directory="solution/$2"
    mkdir -p $directory
    local script=$1
    local signature="${script//./_}"
    local result="$directory/$WORKSPACE-$signature-$(ls $directory | wc -l).out"
    echo "$result"
}

_commit() {
    git add -A
    git commit -m "[RUN] $WORKSPACE/$1 $2"
    git push
}

_exec() {
    git pull
    output=${3:-/dev/stdout}
    cat dataset/$2 | python workspace/$WORKSPACE/$1 > $output
    if [ $? -eq 0 ]
    then
        python utils/eval_solution.py $2 $output
        if [ $? -eq 0 ]
        then
            _commit $1 $2
        else
            python utils/slack.py < "Error error on evaluating score for output $output"
        fi
    else
        python utils/slack.py < "Execution error on dataset $2 with $WORKSPACE/$1"
    fi
}

_verify_args() {
    if [ $# -ne 2 ]
    then
        echo "Please provide script and dataset paramters"
        return 1
    script=$1
    if [ ! -f $WORKSPACE/$1 ]
    then
        echo "Unknown script $WORKSPACE/$1. Abort."
        return 1
    fi
    if [ ! -f dataset/$2 ]
    then
        echo "Unknown dataset dataset/$2. Abort."
        return 1
    fi
}

test() {
    _verify_args "$@"
    if [ $? -ne 0 ]
    then
        return 1
    fi
    _exec "$@"
}

run() {
    _verify_args "$@"
    if [ $? -ne 0 ]
    then
        return 1
    fi
    output=$(get_solution_path "$@")
    _exec "$@" $output
}
EOL
source venv/bin/activate
pip install -r requirements.txt
