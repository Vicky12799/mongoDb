 # 1.Find the student name who scored maximum scores in all (exam, quiz and homework)?
 ```Javascript
db.student.aggregate([{"$project": {_id: "$name","x":  {"$sum": "$scores.score"}}},{ $sort : { x : -1 } },{ $limit : 1 } ])
```

# 2. Find students who scored below average in the exam and pass mark is 40%?
```Javascript
var examAvg = db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',0]}}}}]).toArray()[0]["avg_val"];
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

# 5.Create a new collection which consists of students who scored below average and above 40% in all the categories
```JavaScript
var examAvg =  db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',0]}}}}]).toArray()[0]["avg_val"];
var quizAvg =  db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',1]}}}}]).toArray()[0]["avg_val"];
var hwAvg =  db.student.aggregate([{$group: {_id:null, avg_val:{$avg:{$arrayElemAt: ['$scores.score',2]}}}}]).toArray()[0]["avg_val"];

var avgInExam = db.student.find({$and: [{"scores.0.score":{$lte:examAvg}},{"scores.0.score":{$gte:40}}]}).toArray()
var avgInQuiz = db.student.find({$and: [{"scores.1.score":{$lte:quizAvg}},{"scores.1.score":{$gte:40}}]}).toArray()
var avgInHw = db.student.find({$and: [{"scores.2.score":{$lte:hwAvg}},{"scores.2.score":{$gte:40}}]}).toArray()

var average_students = db.student.aggregate(
  [
     { $project: { AllValues:{ $setIntersection: [ avgInExam, avgInQuiz,avgInHw ] }} }
   ]
).toArray()[0]["AllValues"]

db.createCollection("average_students")

db.average_students.insertMany(average_students)
db.average_students.find()
```

# 6. Create a new collection which consists of students who scored below the fail mark in all the categories.
```Javascript
var failInExam = db.student.find({"scores.0.score":{$lt:40}}).toArray()
var failInQuiz = db.student.find({"scores.1.score":{$lt:40}}).toArray()
var failInHw = db.student.find({"scores.2.score":{$lt:40}}).toArray()

var failed_students = db.student.aggregate(
  [
     { $project: { AllValues:{ $setIntersection: [ failInExam, failInQuiz,failInHw ] }} }
   ]
).toArray()[0]["AllValues"]

db.createCollection("failed_students")
db.failed_students.insertMany(failed_students)
db.failed_students.find()
```

# 7. Create a new collection which consists of students who scored above pass mark in all the categories
```Javascript
var passInExam = db.student.find({"scores.0.score":{$gte:40}}).toArray()
var passInQuiz = db.student.find({"scores.1.score":{$gte:40}}).toArray()
var passInHw = db.student.find({"scores.2.score":{$gte:40}}).toArray()

var passed_stud=db.student.aggregate(
  [
     { $project: { AllValues:{ $setIntersection: [ passInExam, passInQuiz,passInHw ] }} }
   ]
).toArray()[0]["AllValues"]

db.createCollection("passed_students")
db.passed_students.insertMany(passed_stud)
db.passed_students.find()
```