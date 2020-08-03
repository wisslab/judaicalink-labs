from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from elasticsearch import Elasticsearch
import json


# Create your views here.

@api_view(["GET"])
def persons(request):
    es = Elasticsearch()
    
    query = request.GET.get('lookfor')

    # body = {
    #     "from" : 0, "size" : 1000,
    #     "query" : {
            
    #         "match" : {
    #             "deathLocation": "Stuttgart"
    #         }
    #     },
    # }
    if query == None: 
           body = {
                "from" : 0, "size" : 10000,
                "query" : {
                    "match_all" : {}
                },
            }
    else: 
        body = {
            "from" : 0, "size" : 10000,
            "query" : {
                "query_string": {
                    "query": query,
                    "fields": ["name^4", "Alternatives^3", "birthDate", "birthLocation^2", "deathDate", "deathLocation^2", "Abstract", "Publication"]
                }
            },
        }

    result = es.search(index="judaicalink", body = body)
   # dataset = []
    #for d in result ["hits"] ["hits"]:
      #  data = {
       #     "id" : d ["_id"],
            #name
       # }
       # dataset.append (data)

    context = {
        "result":json.dumps(result)
    }

    return JsonResponse(result)