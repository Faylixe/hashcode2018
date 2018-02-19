#!/bin/bash

# Configure virtualenv.
virtualenv venv

# Get google account credentials. 
echo 'Please enter your google account credentials :'
echo -n 'Email: '
read username
echo -n 'Password: '
read -s password
echo 'Please enter target HashCode round identifier :'
echo -n 'Round: '
read round

#read workspace

# Export required environment variable.
echo "export SLACK_WEBHOOK='https://hooks.slack.com/services/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'" >> venv/bin/activate
echo "export GOOGLE_USERNAME=$username" >> venv/bin/activate
echo "export GOOGLE_PASSWORD=$password" >> venv/bin/activate
echo "export ROUND=$round" >> venv/bin/activate
echo "export WORKSPACE=''" >> venv/bin/activate

echo >>venv/bin/activate <<EOL

get_solution_path() {
    local directory="solution/$dataset"
    mkdir -p $directory
    local signature="${script//./_}"
    local result="$directory/$WORKSPACE-$signature-$(ls $directory | wc -l).out"
    echo "$result"
}

run() {
    script=$1
    if [ ! -f $WORKSPACE/$script ]
    then
        echo "Unknown script $WORKSPACE/$script. Abort."
    else
        dataset=$2
        if [ ! -f $WORKSPACE/$script ]
        then
            echo "Unknown dataset $dataset. Abort."
        else
            git pull
            output=$(get_solution_path $dataset $script)
            cat dataset/$dataset | python workspace/$WORKSPACE/$script > $output
            if [ $? -eq 0 ]
            then
                python utils/eval_solution.py $dataset $output
                if [ $? -eq 0 ]
                then
                    git add -A
                    git commit -m "[RUN] $WORKSPACE/$script $dataset"
                    git push
                fi
            fi
        fi
    fi
}
EOL

source venv/bin/activate
pip install -r requirements.txt
