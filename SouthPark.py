#!/usr/bin/python

import sys
import pandas
from nltk.tokenize import RegexpTokenizer
import mincemeat

dataPath = "./data/All-seasons.csv"
if len(sys.argv) == 2:
    dataPath = sys.argv[1]

token = RegexpTokenizer(r'\w+')
pairs = []
for pair in pandas.read_csv(dataPath)[['Character', 'Line']].values:
    pairs.append([pair[0], token.tokenize(pair[1].lower())])

server = mincemeat.Server()
server.mapfn = lambda _, arr: (yield arr[0], set(arr[1]))
server.reducefn = lambda _, arr: len(set().union(*arr))
server.datasource = dict(enumerate(pairs))

results = server.run_server(password='changeme')
with open('SouthPark.csv', 'w') as csvFile:
    csvFile.write('Character, UniqueWords\n')
    for name, words in results.iteritems():
        csvFile.write(name + ',' + str(words) + '\n')
