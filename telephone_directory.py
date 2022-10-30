import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["Telephone_Directory"]

mycol = db["telephone_directory"]

#Inserting single record
mydict = { "name": "Peter", "phone number": 9876543210, "place":"chennai" }
add_one= mycol.insert_one(mydict)
print(add_one.inserted_id)

#Inserting Multiple records
mydictlist = [
    { "name": "Hannah", "phone number": 9876543210, "place":"chennai" },
    { "name": "Michael", "phone number": 9876512345, "place":"bangalore" },
    { "name": "Sandy", "phone number": 9123443210, "place":"kolkatta" },
    { "name": "Richard", "phone number": 9876778920, "place":"delhi" },
    { "name": "Vicky", "phone number": 9812343210, "place":"bombay" },
    { "name": "Ben", "phone number": 9832143210, "place":"bombay" }
]
add_many = mycol.insert_many(mydictlist)
print(add_many.inserted_ids)


#To find the records in the collection
result = []
for x in mycol.find():
    result.append(x)
    print(x)

#To modify one record in the collection
query = { "place": "delhi" }
update = { "$set": { "place": "new delhi" } }
mycol.update_one(query,update)

#To modify multiple records in the collection
query_mul = { "place": "bombay" }
update_mul = { "$set": { "place": "mumbai" } }
mycol.update_many(query_mul,update_mul)


#To delete a record from the collection
del_query = { "place": "bangalore" }
mycol.delete_one(del_query)

#To delete many records from the collection
del_query_multiple = { "place": "chennai" }
del_records = mycol.delete_many(del_query_multiple)
print(del_records.deleted_count, " documents deleted.")

#To delete all the records from the collection
# del_all = mycol.delete_many({})
# print(del_all.deleted_count, " documents deleted.")




