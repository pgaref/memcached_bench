import requests
import time
from datetime import datetime
import json, io, os


def writefileheaders(filename, json_data):
    with io.open(filename, 'w', encoding='utf-8') as f:
        for bolt in range(len(data["bolts"])):
            f.write(unicode("boltId, emitted, executeLatency(s), processLatency(s), "))
        for spout in range(len(data["spouts"])):
            f.write(unicode("spoutId, completeLatency(s), "))
        f.write(unicode("tasksTotal, completeLatency(s), uptime"))
        f.write(unicode("\n"))


def dump2file(filename, json_data):
    if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
        writefileheaders(filename, json_data)

    with io.open(filename, 'a', encoding='utf-8') as f:
        print data["topologyStats"]
        # f.write(unicode(json.dumps(json_data, ensure_ascii=False)))
        for bolt in range(len(data["bolts"])):
            f.write(unicode(data["bolts"][bolt]["boltId"])+", ")
            f.write(unicode(data["bolts"][bolt]["emitted"])+", ")
            f.write(unicode(data["bolts"][bolt]["executeLatency"])+", ")
            f.write(unicode(data["bolts"][bolt]["processLatency"])+", ")

        for spout in range(len(data["spouts"])):
            f.write(unicode(data["spouts"][spout]["spoutId"])+", ")
            f.write(unicode(data["spouts"][spout]["completeLatency"])+", ")

        f.write(unicode(data["tasksTotal"])+", ")
        f.write(unicode(data["topologyStats"][0]["completeLatency"])+", ")
        f.write(unicode(data["uptime"]))
        f.write(unicode("\n"))


if __name__ == '__main__':
    storm_topology_url = 'http://example.com:49467/api/v1/topology/trendingHashTags-15-1476271470'
    experiment_name = "YARN-Default_1Node"
    experiment_outfile = "./Storm_"+experiment_name+\
                         "-"+str(datetime.now())+".dat"


    while True:
        response = requests.get(storm_topology_url)
        data = response.json()
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        dump2file(experiment_outfile, data)
        time.sleep(10)
