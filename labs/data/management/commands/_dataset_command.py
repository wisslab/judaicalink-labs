from django.core.management.base import BaseCommand
from django.utils import timezone
import gzip
import rdflib
from bs4 import BeautifulSoup
from pathlib import Path
import scrapy
import scrapy.crawler
import re
import gzip as gziplib
import shutil
import os
import json

namespaces = {
        "jlo": rdflib.Namespace("http://data.judaicalink.org/ontology/"),
        "jld": rdflib.Namespace("http://data.judaicalink.org/data/"),
        "skos": rdflib.Namespace("http://www.w3.org/2004/02/skos/core#"),
        "dcterms": rdflib.Namespace("http://purl.org/dc/terms/"),
        "rdf": rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        "rdfs": rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#"),
        "owl": rdflib.Namespace("http://www.w3.org/2002/07/owl#"),
        "xsd": rdflib.Namespace("http://www.w3.org/2001/XMLSchema#"),
        "geo": rdflib.Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
        "void": rdflib.Namespace("http://rdfs.org/ns/void#"),
        "foaf": rdflib.Namespace("http://xmlns.com/foaf/0.1/"),
}

for ns in namespaces:
    exec(f"{ns} = namespaces['{ns}']")


def gzip_file(filename):
    with open(filename, 'rb') as f_in:
        with gziplib.open(f'{filename}.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(filename)


class DatasetCommand(BaseCommand):
    help = 'Base Command for a scraper'

    def add_arguments(self, parser):
        parser.add_argument("--clear-cache", action="store_true", help="Clear cache before scraping.")
        parser.add_argument("--skip-scraping", action="store_true", help="Create RDF from JSON.")
        parser.add_argument("--no-rdf", action="store_true", help="Create only json")
        parser.add_argument("--gzip", action="store_true", help="Zip output files.")




    def set_metadata(self, metadata):
        self.metadata = metadata
    

    def start_scraper(self, scraper_class, filename=None, gzip=False, settings={}, args_list=[], kwargs_dict={}):
        if not filename:
            filename = f"{scraper_class.name}.jsonl"
        os.remove(filename)
        default_settings = {
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'FEED_FORMAT': 'jsonlines',
                'FEED_URI': filename,
                'HTTPCACHE_ENABLED': True,
                'HTTPCACHE_DIR': f'{scraper_class.name}-cache',
        }
        default_settings.update(settings)
        process = scrapy.crawler.CrawlerProcess(default_settings)
        process.crawl(scraper_class, *args_list, **kwargs_dict)
        process.start()

        if gzip:
            gzip_file(f"{scraper_class.name}.jsonl")


    def jsonlines_to_rdf(self, dict_to_graph_function, jsonl_filename=None, rdf_filename=None, gzip=False):
        if not jsonl_filename:
            jsonl_filename = f"{self.metadata['name']}.jsonl"
        if not rdf_filename:
            rdf_filename = f"{self.metadata['name']}.ttl"
        if gzip and not jsonl_filename.endswith(".gz"):
            jsonl_filename += ".gz" 
        graph = rdflib.Graph()
        for ns in namespaces:
            graph.bind(ns, namespaces[ns])
        openfunc = open
        if jsonl_filename.endswith(".gz"):
            openfunc = gziplib.open
        with openfunc(jsonl_filename, "rt", encoding="utf-8") as jsonlines:
            for line in jsonlines:
                line_dict = json.loads(line)
                dict_to_graph_function(graph, line_dict)
        with open(rdf_filename, "wb") as f:
            f.write(graph.serialize(format="turtle"))
        if gzip:
            gzip_file(rdf_filename)




    def handle(self, *args, **kwargs):
        print("This command is not meant to be executed directly, use a subclass.")



