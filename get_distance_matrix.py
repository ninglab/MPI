import networkx as nx
import argparse
import numpy as np
import pandas as pd
import sys
from scipy.special import softmax
import pdb
from collections import OrderedDict
import scipy.stats as stats
from random import randint
from utils import utils

def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--embedding_file", required=True, help="Embedding file")
    #parser.add_argument("--out_prefix", required=True, help="Out prefix")
    
    
    #args = parser.parse_args()
    uti  = utils()

    print("run function.....\n")
    inputfile = "/fs/ess/PCON0041/shunian/AD_drugRep_project_202209/Data/Intermediate_data/Graphs_and_embeddings/Embed_JackList/Final_network_with386drugs_10_128.embeddings"
    outPrefix = "/fs/ess/PCON0041/shunian/AD_drugRep_project_202209/Data/Intermediate_data/Graphs_and_embeddings/Embed_JackList/Final_network_with386drugs_10_128"
    uti.get_dotProd_L1_L2_matrix(inputfile, outPrefix)

if __name__ == '__main__':
    main()
