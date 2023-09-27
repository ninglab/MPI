import numpy as np 
import pandas as pd 
import networkx as nx 
import argparse
from utils import utils
from collections import OrderedDict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph_file", required=True, help="Graph edge list file")
    parser.add_argument("--all_drug_id_name_file", required=True, help='all Drugbank ID and drug name of the drug node id')
    parser.add_argument("--current_drug_id_name_file", required=True, help='current Drugbank ID and drug name of the drug node id')
    parser.add_argument("--outprefix", required=True, help="Out file prefix")
    
    args = parser.parse_args()
    uti  = utils()

    # 1, read graph
    G = nx.read_weighted_edgelist(args.graph_file)
    print("step 1 read graph finished-----------------------------------------\n")

    # 2, disease module 
    disease_id = '114483835'
    disease_module = [n for n in G.neighbors(disease_id)]
    print("step 2 get diseae module finished-----------------------------------------\n")

    # 3, drug nodes
    drug_node_ids = []
    drug_id_name = {} 
    current_drug_ids = []

    with open(args.all_drug_id_name_file, 'r') as fh:
        for line in fh.readlines():
            line = line.rstrip("\n")
            fields = line.split("\t")
            if fields[1]=="NodeID":
                continue
            drug_id_name[str(fields[1])] = fields[0]
            drug_node_ids.append(str(fields[1]))

    with open(args.current_drug_id_name_file, 'r') as fh:
        for line in fh.readlines():
            line = line.rstrip("\n")
            fields = line.split("\t")
            if fields[1]=="NodeID":
                continue
            current_drug_ids.append(str(fields[1]))

    print("step 3 read drug nodes finished-----------------------------------------\n")

    # 4, calculate z score of each drug node
    zscores = {}
    for node in current_drug_ids:
        if node in G:
            drug_module = [n for n in G.neighbors(node)]
            G_backup = G.copy()
            other_drug_nodes = drug_node_ids.copy()
            other_drug_nodes.remove(node)
            G_backup.remove_nodes_from(other_drug_nodes)
            each_zscore = uti.calculate_z_score(G_backup, disease_module, drug_module)
            #print("{} zscore {}".format(node, each_zscore))
            zscores[node] = each_zscore
        else:
            print("{} is not in the graph\n".format(node))
    print("step 4 calculate z score finished-----------------------------------------\n")

    # 5, rank the drugs by z score
    ranked_zscore = OrderedDict(sorted(zscores.items(), key=lambda x: x[1]))
    print("step 5 rank the drug by z score finished-----------------------------------------\n")

    # 6. output ranked drugs
    out_file = args.outprefix + "_drug_zscores.txt"
    out_f = open(out_file,'w')
    i=1
    for element in ranked_zscore:
        out_f.write(str(i)+"\t"+str(element)+"\t"+str(drug_id_name[str(element)])+"\t"+str(ranked_zscore[element])+"\n")
        i=i+1
    print("step 6 output finished-----------------------------------------\n")
