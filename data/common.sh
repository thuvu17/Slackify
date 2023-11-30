#!/bin/sh
# Some common shell stuff.

echo "Importing from common.sh"

DB=slackifyDB
USER=Thu
CONNECT_STR="mongodb+srv://cluster0.r9gin96.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/Users/thuvu/Desktop/SE-F23/slackify/data
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/opt/homebrew/bin/mongoexport
IMP=/opt/homebrew/bin/mongoimport

if [ -z $SLACKIFY_DB_PW ]
then
    echo "You must set SLACKIFY_DB_PW in your env before running this script."
    exit 1
fi


declare -a slackify_collections=("songs" "users")
