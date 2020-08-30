from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from elasticsearch import Elasticsearch
import json
from backend.models import Dataset

def test(request):

    es = Elasticsearch()
    body = {
        'size': '0',
        'aggs': {
            'uniq_year': {
                'terms': {
                    'field': 'birthYear', 'size': 1000000
                }
            }
        }
    }
    result = es.search(index="judaicalink", body = body)

    aggregation = result ["aggregations"] ["uniq_year"] ["buckets"]
    aggregation.sort(key=lambda r: r['key'])
    aggregation = json.dumps (aggregation)

    birthyears = []
    amount_of_people = []

    for i in result ["aggregations"] ["uniq_year"] ["buckets"]:
        birthyears.append (i ["key"])
        amount_of_people.append (i ["doc_count"])

    # list_dataslugs = []
    # list_amount_data = []
    #
    # dataset_objects = Dataset.objects.all()
    # dataslugs = []
    # for i in dataset_objects:
    #     if i.dataslug:
    #         dataslugs.append (i.dataslug)
    #
    # for dataslug in dataslugs:
    #     es = Elasticsearch()
    #     body = {
    #         "query" : {
    #             "match" : {
    #                 "dataslug": dataslug
    #             }
    #         },
    #     }
    #     result = es.count(index="judaicalink", body = body)
    #     amount = result ["count"]
    #     list_dataslugs.append (dataslug)
    #     list_amount_data.append (amount)

    context = {
        #"result": json.dumps(result),
        #"list_dataslugs": list_dataslugs,
        #"list_amount_data": list_amount_data,
        #'birthyears': birthyears,
        #'amount_of_people': amount_of_people,
        'aggregation': aggregation,
    }

    return render(request, "dashboard/dashboard_main.html", context)

