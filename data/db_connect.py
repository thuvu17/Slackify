import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

SLACKIFY_DB = 'slackifyDB'

client = None

MONGO_ID = '_id'


def connect_db():
    global client
    password = os.environ.get("SLACKIFY_DB_PW")
    print("Connecting to Mongo in the cloud.")
    client = pm.MongoClient(f'mongodb+srv://tnv2002:{password}'
                            + '@cluster0.r9gin96.mongodb.net/'
                            + '?retryWrites=true&w=majority')


def insert_one(collection, doc, db=SLACKIFY_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=SLACKIFY_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def del_one(collection, filt, db=SLACKIFY_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def fetch_all(collection, db=SLACKIFY_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=SLACKIFY_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret
