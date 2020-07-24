from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from elasticsearch import Elasticsearch
import json
from backend.models import Dataset

def test(request):
    list_dataslugs = []
    list_amount_data = []

    dataset_objects = Dataset.objects.all()
    dataslugs = []
    for i in dataset_objects:
        if i.dataslug:
            dataslugs.append (i.dataslug)

    for dataslug in dataslugs:
        es = Elasticsearch()
        body = {
            "query" : {
                "match" : {
                    "dataslug": dataslug
                }
            },
        }
        result = es.count(index="judaicalink", body = body)
        amount = result ["count"]
        list_dataslugs.append (dataslug)
        list_amount_data.append (amount)

    context = {
        "result": json.dumps(result),
        "list_dataslugs": list_dataslugs,
        "list_amount_data": list_amount_data,
    }

    return render(request, "dashboard/dashboard_main.html", context)

