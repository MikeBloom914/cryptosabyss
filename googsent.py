#!/usr/bin/env python3

import requests
import datetime
import json


# def generate_graph():
#print ("[+] generating graph")
########################Numbers represent search interest relative to the highest point on the chart for the given region and time. A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular. A score of 0 means there was not enough data for this term.#########################

def get_volume_keyword_year(keyword):
    # use google trends to get volume search for keyword
   #print ("[+] getting volume for keyword " + keyword + " for last year")
    url = 'https://trends.google.com/trends/api/explore?hl=fr&tz=-60&req={"comparisonItem":[{"keyword":"' + keyword + '","geo":"","time":"today+12-m",}],"category":0,"property":""}&tz=-60'
    r = requests.get(url)
    widget = json.loads(r.text.split("'")[1])['widgets'][0]
    token = widget['token']
    time = widget['request']['time']
    url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv?req={"time":"' + time + '","resolution":"WEEK","locale":"fr","comparisonItem":[{"geo":{},"complexKeywordsRestriction":{"keyword":[{"type":"BROAD","value":"' + keyword + '"}]}}],"requestOptions":{"property":"","backend":"IZG","category":0}}&token=' + token + '&tz=-60'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.text.split("\n")[3:-1]
        for d in data:
            try:
                date = d.split(",")[0]
                count = d.split(",")[1]
                #print (date + " ==> " + str(count))
                print (date)
                print (count)
            except:
                pass
    else:
        print ("[+] error with token")


def get_volume_keyword_month(keyword):
    # use google trends to get volume search for keyword
    #print ("[+] getting volume for keyword " + keyword + " for last month")
    url = 'https://trends.google.com/trends/api/explore?hl=fr&tz=-60&req={"comparisonItem":[{"keyword":"' + keyword + '","geo":"","time":"today+1-m",}],"category":0,"property":""}&tz=-60'
    r = requests.get(url)
    widget = json.loads(r.text.split("'")[1])['widgets'][0]
    token = widget['token']
    time = widget['request']['time']
    url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv?req={"time":"' + time + '","resolution":"DAY","locale":"fr","comparisonItem":[{"geo":{},"complexKeywordsRestriction":{"keyword":[{"type":"BROAD","value":"' + keyword + '"}]}}],"requestOptions":{"property":"","backend":"IZG","category":0}}&token=' + token + '&tz=-60'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.text.split("\n")[3:-1]
        for d in data:
            try:
                date = d.split(",")[0]
                count = d.split(",")[1]
                #print(date + " = " + str(count))
                #print(date)
                #print(count)
            except:
                pass
    else:
        print ("[+] error with token")


def main():
    get_volume_keyword_year("bitcoin")
    get_volume_keyword_month("bitcoin")


if __name__ == '__main__':
    main()
