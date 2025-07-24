#!/bin/bash
source /projects/mailparser/venv/bin/activate
echo "main.py triggered at $(date)" >> /projects/mailparser/logs/procmail.log
cat - | python /projects/mailparser/main.py
status=$?
echo "main.py exited with code $status at $(date)" >> /projects/mailparser/logs/procmail.log
exit $status