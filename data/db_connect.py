import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

SLACKIFY_DB = 'slackifyDB'

client = None

MONGO_ID = '_id'


def connect_db():
    global client
    if client is None:
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("SLACKIFY_DB_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://tnv2002:{password}'
                                    + '@cluster0.r9gin96.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


# Compatible with playlists, songs, and users collections
def insert_one(collection, doc, db=SLACKIFY_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


# Compatible with playlists, songs, and users collections
def fetch_one(collection, filt, db=SLACKIFY_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


# Compatible with playlists, songs, and users collections
def del_one(collection, filt, db=SLACKIFY_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


# Compatible with playlists, songs, and users collections
def update_doc(collection, filters, update_dict, db=SLACKIFY_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


# Compatible with playlists, songs, and users collections
# Used only for song collection by 12/15/2023
def fetch_all_songs_as_dict(collection, db=SLACKIFY_DB):
    """
    Fetch all documents in given collection into a dictionary.
    Each doc will has its MongoDB id as the key in the dict.
    Return the dict.
    """
    ret = {}
    for doc in client[db][collection].find():
        id = str(doc[MONGO_ID])
        del doc[MONGO_ID]
        ret[id] = doc
    return ret


# Compatible with playlists, songs, and users collections
# Used only for user collection by 12/15/2023
def fetch_all_as_dict(key, collection, db=SLACKIFY_DB):
    """
    Fetch all documents in given collection into a dictionary.
    Each doc will has given key as the key in the dict.
    Return the dict.
    """
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


# Compatible with playlists, songs, and users collections
# Used only for playlist collection by 12/15/2023
def fetch_all_as_list(collection, filt, key, db=SLACKIFY_DB):
    """
    Find with a filter,
    with every document found,
    fetch the value corresponding to the given key into a list
    Return the list of corresponding values.
    """
    ret = []
    for doc in client[db][collection].find(filt):
        if key in doc:
            ret.append(doc[key])
    return ret
