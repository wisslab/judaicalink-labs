from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from elasticsearch import Elasticsearch
import json
from backend.models import Dataset

def test(request):
    es = Elasticsearch()
    body = {
        "from" : 0, "size" : 10000,
        "query" : {
            "match_all" : {}
        },
        }
    result = es.search(index="judaicalink", body = body)

    total_hits = result ["hits"] ["total"] ["value"]

    dataset_objects = Dataset.objects.all()
    dataslug_to_dataset = {}
    for i in dataset_objects:
        dataslug_to_dataset [i.dataslug] = i.title

    dataslugs_amaount = {}

    for data in result ["hits"] ["hits"]:
        dataslug = data ["_source"] ["dataslug"]
        if dataslug in dataslugs_amaount:
            dataslugs_amaount [dataslug] += 1
        else:
            if dataslug in dataslug_to_dataset:
                dataslugs_amaount [dataslug] = 1

    list_dataslugs = []
    list_amount_data = []

    for d in dataslugs_amaount:
        list_dataslugs.append (d)
        list_amount_data.append (dataslugs_amaount [d])

    print (dataslugs_amaount)
    print (list_dataslugs)
    print (list_amount_data)
    print (total_hits)

    context = {
        "result": json.dumps(result),
        "list_dataslugs": list_dataslugs,
        "list_amount_data": list_amount_data,
    }

    return render(request, "dashboard/dashboard_main.html", context)

