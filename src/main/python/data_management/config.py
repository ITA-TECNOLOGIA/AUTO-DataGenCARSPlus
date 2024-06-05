host = [{'host': 'analyticsopensearch.imascono.com', 'port': 443}]
auth = ('ita', 'kwv-fhb3PTJ7xtv5wdr')
index_tasks = "analytics*"
# index_tasks = "test_exclusiverse"
verify_certs = True
compress = True
use_ssl = True

scroll_time ='2s'

match_id={
  "query": {
    "ids": {
      "values": [
        "QPWLJX8B4583WKv6ffJc"
      ]
    }
  }
}

match_eva={
  "size":"1000",
  "query":
    {"match":
      {"object_id":"Eva"}
  }
}

match_all = {
    "size": 10000,
    "query": {
        "match_all": {}
    }
}

foodbot_match={
  "size":"10000",
  "query":
    {"match":
      {"virtual_space_id":"Foodbots"}
  }
}

spaceship_match={
  "size":"10000",
  "query":
    {"match":
      {"virtual_space_id":"Spaceship"}
  }
}

hospital_match={
  "size":"10000",
  "query":
    {"match":
      {"virtual_space_id":"San Juan de Dios IVS Fase 2"}
  }
}

target_user_spaceship_match={
  "size":"10000",
  "query": {
    "bool": {
        "must":  {"match": {"virtual_space_id":"Spaceship"} } ,
        "filter":{"range": {"@timestamp":{"gte": "now-5d" }}}
    }
  }
}