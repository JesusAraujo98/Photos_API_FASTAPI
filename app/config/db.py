from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('araujo')
password = urllib.parse.quote_plus('password')

# conn = MongoClient("monguito", 27017 ,username= username, password=password)

conn = MongoClient()