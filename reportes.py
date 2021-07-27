#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas
import time
import os
import glob
import csv
import xlwt  # from http://www.python-excel.org/


class Incio:
    def __init__(self, objects):
        # start time of script
        self.start_time = time.time()
        self.ip = objects['ip']
        self.port = int(objects['port'])
        self.user = objects['user']
        self.password = objects['password']
        self.db = objects['db']
        self.collection = objects['collection']
        self.report = objects['report']
        self.query = objects['query']

    def conect(self):
        # build a new client instance of MongoClient
        # mongo_client = MongoClient('192.168.44.72', 27017, username="admin", password="password")
        try:
            mongo_client = MongoClient(self.ip, self.port, username=self.user, password=self.password)
            db = mongo_client[self.db]
            self.col = db[self.collection]
            self.proceso_principal()
        except NameError:
            print(NameError)
            # print("No se pudo conectar al mongo")

    def proceso_principal(self):
        try:
            # make an API call to the MongoDB server
            cursor = self.col.find(self.query)

            # extract the list of documents from cursor obj
            mongo_docs = list(cursor)

            # restrict the number of docs to export
            mongo_docs = mongo_docs[:]  # slice the list

            # create an empty DataFrame for storing documents
            self.docs = pandas.DataFrame(columns=[])
            # print("docs_vacio", docs)
            # iterate over the list of MongoDB dict documents
            for num, doc in enumerate(mongo_docs):
                # convert ObjectId() to str
                doc["_id"] = str(doc["_id"])

                # get document _id from dict
                doc_id = doc["_id"]

                # create a Series obj from the MongoDB dict
                series_obj = pandas.Series(doc, name=doc_id)

                # append the MongoDB Series obj to the DataFrame obj
                # print("series_obj", series_obj)
                self.docs = self.docs.append(series_obj)
                # print("docdocdoc", docs)
                # only print every 10th document
                if num % 10 == 0:
                    # print(type(doc))
                    # print(type(doc["_id"]))
                    print(num, "--", doc, "\n")

            # print("self.docs", docs)
            self.generando_archivos()
            # db = mongo_client.testmongoNew
            # col = db.repro2
        except NameError:
            print(NameError)

    def generando_archivos(self):
        try:
            """
            EXPORTAR LOS DOCUMENTOS DEL MONGODB
            EN DIFERENTES FORMATOS
            """
            # print("\nexporting Pandas objects to different file types.")
            print("\nCantidad de DataFrame (len):", len(self.docs))

            # export the MongoDB documents as a JSON file
            self.docs.to_json("{}.json".format(self.report))

            # have Pandas return a JSON string of the documents
            json_export = self.docs.to_json()  # return JSON data
            # print("\nJSON data:", json_export)

            # export MongoDB documents to a CSV file
            self.docs.to_csv("{}.csv".format(self.report), ",")  # CSV delimited by commas

            # export MongoDB documents to CSV
            csv_export = self.docs.to_csv(sep=",")  # CSV delimited by commas
            # print("\nCSV data:", csv_export)

            # create IO HTML string
            import io

            html_str = io.StringIO()

            # export as HTML
            self.docs.to_html(
                buf=html_str,
                classes='table table-striped'
            )

            # print out the HTML table
            print(html_str.getvalue())

            # save the MongoDB documents as an HTML table
            self.docs.to_html("{}.html".format(self.report))

            print("\n\ntime elapsed:", time.time() - self.start_time)
            self.ConvertirEnviar()
        except NameError:
            print(NameError)

    def ConvertirEnviar(self):
        try:
            print('{}.csv'.format(self.report))
            for csvfile in glob.glob(os.path.join('.', '{}.csv'.format(self.report))):
                print("csvfile", csvfile)
                wb = xlwt.Workbook()
                ws = wb.add_sheet('data')
                with open(csvfile, 'rt', encoding="utf8") as f:
                    reader = csv.reader(f)
                    for r, row in enumerate(reader):
                        # print(row)
                        for c, val in enumerate(row):
                            ws.write(r, c, val)
                wb.save(csvfile + '.xls')
                os.remove(csvfile)
        except NameError:
            print(NameError)


Condif = {
    "ip": "127.0.0.1",
    "port": "27017",
    "user": "",
    "password": "",
    "db": "mydb",
    "collection": "customers",
    "report": "reporte1",
    "query": "{}"
}

reporte = Incio(Condif)
reporte.conect()
