## Elasticsearch Query Results

### Search Query Used

```bash
curl -X GET "http://localhost:9200/students/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "skills": "Python"
    }
  }
}'
```
```bash
curl -X GET "http://localhost:9200/students/_search?q=name:*Anderson&pretty"
```




{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.18232156,
    "hits" : [
      {
        "_index" : "students",
        "_type" : "_doc",
        "_id" : "8",
        "_score" : 0.18232156,
        "_source" : {
          "student_id" : 8,
          "name" : "David Anderson",
          "title" : "Machine Learning Engineer",
          "skills" : [
            "Python",
            "TensorFlow",
            "Keras"
          ]
        }
      },
      {
        "_index" : "students",
        "_type" : "_doc",
        "_id" : "9",
        "_score" : 0.18232156,
        "_source" : {
          "student_id" : 9,
          "name" : "David Anderson",
          "title" : "Machine Learning Engineer",
          "skills" : [
            "Python",
            "TensorFlow",
            "Keras"
          ]
        }
      }
    ]
  }
}

<!-- code -->
