import pymongo
import config


def create_conection(con_str) -> pymongo.MongoClient:
    return pymongo.MongoClient(con_str)
