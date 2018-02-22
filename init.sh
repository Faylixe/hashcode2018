#!/bin/bash

if [ $# -eq 0 ]
then
    echo 'Workspace name not provided'
    echo 'Usage : bash init.sh workspace_name'
    exit -1
fi

# Get google account credentials. 
echo 'Please enter your google account credentials'
echo -n 'Email: '
read username
echo -n 'Password: '
read -s password

round='5736842779426816'

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
echo "export DATASET_PATH='dataset'" >> venv/bin/activate
echo "export SOLUTION_PATH='solution'" >> venv/bin/activate
echo "export WORKSPACE='$workspace'" >> venv/bin/activate
cat >>venv/bin/activate <<'EOL'
_get_solution_path() {
    local directory="$SOLUTION_PATH/$2"
    mkdir -p $directory
    local script=$1
    local signature=${script/./_}
    local count="$(ls $directory | wc -l)"
    local result="$directory/$WORKSPACE-$signature-$(($n)).out"
    echo "$result"
}

_commit() {
    git pull
    git add -A
    git commit -m "[RUN] workspace/$WORKSPACE/$1 $2"
    git push
}

_exec() {
    git pull
    cat dataset/$2 | python -m workspace.$WORKSPACE.$1 > ${4:-/dev/stdout} 2> $3
}

_report() {
    report=$(mktemp /tmp/hashcode_report.XXXXXX)
    echo $1 > $report
    cat $2 >> $report
    cat $report | python -m utils.slack
    rm $report
    rm $2
}

_push_result() {
    error_file=$(mktemp /tmp/hashcode_error.XXXXXX)
    python -m utils.eval_solution $2 $3 2> $error_file
    if [ $? -eq 0 ]
    then
         _commit $1 $2
    else
        _report "Error error on evaluating score for output $output (see stack trace below)" $error_file
    fi
}

_verify_args() {
    if [ $# -ne 2 ]
    then
        echo "Please provide script and dataset paramters"
        return 1
    fi
    script=$1
    if [ ! -f workspace/$WORKSPACE/$1.py ]
    then
        echo "Unknown script workspace/$WORKSPACE/$1.py. Abort."
        return 1
    fi
    if [ ! -f dataset/$2 ]
    then
        echo "Unknown dataset dataset/$2. Abort."
        return 1
    fi
}

_run() {
    _verify_args $1 $2
    if [ $? -ne 0 ]
    then
        return 1
    fi
    git pull
    cat dataset/$2 | python -m workspace.$WORKSPACE.$1 > $3 2> $4
}

testrun() {
    _run $1 $2 /dev/stdout /dev/stderr
}

run() {
    output=$(_get_solution_path $1 $2)
    error_file=$(mktemp /tmp/hashcode_error.XXXXXX)
    _run $1 $2 $output $error_file
    if [ $? -ne 0 ]
    then
        _report "Execution error on workspace/$WORKSPACE/$1 using dataset '$2' (see stack trace below)" $error_file
    else
        _push_result $1 $2 $output
    fi
}

runall() {
    if [ ! -f workspace/$WORKSPACE/$1.py ]
    then
        echo "Unknown script workspace/$WORKSPACE/$1.py. Abort."
        return 1
    fi
    for dataset in `ls dataset/`
    do
        run $1 $dataset
    done
}
EOL
source venv/bin/activate
pip install -r requirements.txt