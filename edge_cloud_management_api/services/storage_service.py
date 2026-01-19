from edge_cloud_management_api.configs.env_config import config
import pymongo

storage_url = mongo_host = config.MONGO_URI
mydb_mongo = 'oeg_storage'

def insert_zones(zone_list: list):
        collection = "zones"
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient[mydb_mongo]
        col = mydbmongo[collection]
        col.insert_many(zone_list)

def get_zone(zone_id: str):
        collection = "zones"
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient[mydb_mongo]
        col = mydbmongo[collection]
        zone = col.find_one({'_id': zone_id})
        return zone

def delete_partner_zones():
        collection = "zones"
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient[mydb_mongo]
        col = mydbmongo[collection]
        col.delete_many({'isLocal': 'false'})

def insert_federation(fed: dict):
        collection = 'federations'
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient[mydb_mongo]
        col = mydbmongo[collection]
        col.insert_one(fed)

def get_fed(fed_context_id: str):
        collection = 'federations'
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient[mydb_mongo]
        col = mydbmongo[collection]
        fed = col.find_one({'_id': fed_context_id})
        return fed

def get_all_feds():
        collection = 'federations'
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient[mydb_mongo]
        col = mydbmongo[collection]
        feds = col.find()
        return feds.to_list()

def delete_fed(fed_context_id: str):
        collection = 'federations'
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient[mydb_mongo]
        col = mydbmongo[collection]
        col.delete_one({'_id': fed_context_id})

