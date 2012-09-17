# -*- coding: utf-8 -*-

import sys, os
import cPickle
import matplotlib.pyplot as plt
import networkx as nx

fileName = sys.argv[1]
site, event_id = fileName.split('.')[0].split('_')[:2]

nodes = cPickle.load(open('%s_%s_nodes.pkl' % (site, event_id)))
edges = cPickle.load(open('%s_%s_edges.pkl' % (site, event_id)))

g = nx.DiGraph()
sources = set(edges.keys())
for source, dests in edges.iteritems():
    inDests = set(dests) & sources
    for dest in inDests:
        g.add_edge(nodes[source], nodes[dest])

# ノードの大きさを入次数に比例させる
node_size = {}
for node in g:
    node_size[node] = float(g.in_degree(node)) * 5 + 2

# 描画の際にはUndirected Graphに変換
g = nx.Graph(g)
nx.draw(g, nx.spring_layout(g), with_labels=True,
        node_size=[node_size[node] for node in g],
        node_color='red', width=0.1, alpha=0.7)
plt.show()
