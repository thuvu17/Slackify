#!/bin/sh
# Script to backup production database to JSON files.

. ./common.sh

chmod 755 bkup.sh

for collection in ${slackify_collections[@]}; do
    echo "Backing up $collection"
    $EXP --collection=$collection --db=$DB --out=$BKUP_DIR/$collection.json $CONNECT_STR --username $USER --password $SLACKIFY_DB_PW
done

git add $BKUP_DIR/*.json
git add $BKUP_DIR/*.json
git commit $BKUP_DIR/*.json -m "Mongo DB backup"
git pull origin master
git push origin master