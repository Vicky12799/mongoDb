 # 1.Find the student name who scored maximum scores in all (exam, quiz and homework)?
 ```Javascript
db.student.aggregate([{"$project": {_id: "$name","x":  {"$sum": "$scores.score"}}},{ $sort : { x : -1 } },{ $limit : 1 } ])
```
# 2. Find students who scored below average in the exam and pass mark is 40%?
```Javascript
var average = db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',0]}}}}]).toArray()[0]["avg_val"];
db.student.find({$and: [{"scores.0.score":{$lte:examAvg}},{"scores.0.score":{$gte:40}}]})
```
# 3. Find students who scored below pass mark and assigned them as fail, and above pass mark as pass in all the categories?
```Javascript
db.student.updateMany({"scores.0.score":{$gte:40}},{ $set: { "status": "pass" } })
db.student.updateMany({"scores.0.score":{$lt:40}},{ $set: { "status": "fail" } })
db.student.find()
   ```
# 4. Find the total and average of the exam, quiz and homework and store them in a separate collection?
```Javascript
var examAvg =  db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',0]}}}}]).toArray()[0]["avg_val"];
var quizAvg =  db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',1]}}}}]).toArray()[0]["avg_val"];
var hwAvg =  db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',2]}}}}]).toArray()[0]["avg_val"];

var examTotal =  db.student.aggregate([{$group: {_id:null, total_val:{$sum:{$arrayElemAt: ['$scores.score',0]}}}}]).toArray()[0]["total_val"];
var quizTotal =  db.student.aggregate([{$group: {_id:null, total_val:{$sum:{$arrayElemAt: ['$scores.score',1]}}}}]).toArray()[0]["total_val"];
var hwTotal =  db.student.aggregate([{$group: {_id:null, total_val:{$sum:{$arrayElemAt: ['$scores.score',2]}}}}]).toArray()[0]["total_val"];

db.createCollection("statistics")
var a = [{"_id":1,"type":"exam","total":examTotal,"average":examAvg},
{"_id":2,"type":"quiz","total":quizTotal,"average":quizAvg},
{"_id":3,"type":"homework","total":hwTotal,"average":hwAvg}
]
db.statistics.insertMany(a)

db.statistics.find()
```