"""
This file contains some common MongoDB code.
"""
import os
import json
import pymongo as pm
import bson.json_util as bsutil

# all of these will eventually be put in the env:
user_nm = "meishinlee"
cloud_db = "email-filter.6vns1.mongodb.net"
# cloud_db = "cluster0.lh6bk.mongodb.net"
# cloud_db = "serverlessinstance0.irvgp.mongodb.net"
passwd = os.environ.get("MONGO_PASSWD", 'emailfilter')
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"
db_nm = "emailfilterDB"

client = pymongo.MongoClient("mongodb://meishinlee:emailfilter@email-filter-shard-00-00.6vns1.mongodb.net:27017,email-filter-shard-00-01.6vns1.mongodb.net:27017,email-filter-shard-00-02.6vns1.mongodb.net:27017/emailfilterDB?ssl=true&replicaSet=atlas-wpc2zu-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test


def get_client():
    """
    This provides a uniform way to get the client across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    """
    global client
    if os.environ.get("LOCAL_MONGO", False):
        client = pm.MongoClient()
    else:
        client = pm.MongoClient(f"mongodb+srv://{user_nm}:{passwd}.@{cloud_db}"
                                + f"/{db_nm}?{db_params}",
                                server_api=pm.ServerApi('1'))
    return client


def fetch_all(collect_nm, key_nm):
    all_docs = {}
    for doc in client[db_nm][collect_nm].find():
        print(doc)
        all_docs[doc[key_nm]] = json.loads(bsutil.dumps(doc))
    return all_docs


def insert_doc(collect_nm, doc):
    client[db_nm][collect_nm].insert_one(doc)
