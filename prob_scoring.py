import networkx as nx
import argparse
import numpy as np
import pandas as pd
import sys
from scipy.special import softmax
import pdb
from utils import utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph_file", required=True, help="Graph edge list file")
    parser.add_argument("--emb", required=True, help='Embeddings file')
    parser.add_argument("--all_drug_id_name_file", required=True, help='Drugbank ID and drug name of the drug node id')
    parser.add_argument("--target_drug_id_name_file", required=True, help='Drugbank ID and drug name of the drug node id')
    parser.add_argument("--outprefix", required=True, help="Out file prefix")
    parser.add_argument("--cal_type", required=True, help="calculation type: dotProd_neighbor_softmax dotProd_direct dotProd_softmax l1Dist_direct l1Dist_softmax l2Dist_direct l2Dist_softmax")

    args = parser.parse_args()
    uti  = utils()

    # 1.read disease id for AD
    disease_id = '114483835'
    print("step 1 read disease id finished---------------------------------\n")
    
    # 2.read drug id
    drug_ids = []
    drug_id_name = {} 
    target_drug_ids = []

    with open(args.all_drug_id_name_file, 'r') as fh:
        for line in fh.readlines():
            line = line.rstrip("\n")
            fields = line.split("\t")
            drug_id_name[str(fields[1])] = fields[0]
            drug_ids.append(str(fields[1]))

    with open(args.target_drug_id_name_file, 'r') as fh:
        for line in fh.readlines():
            line = line.rstrip("\n")
            fields = line.split("\t")
            target_drug_ids.append(str(fields[1]))

    print("step 2 read drug id finished------------------------------------\n")
    
    # 3.read embedding file to get embeddings
    embedding_prefix = args.emb.rsplit(".",1)[0] 
    embeddings = {}
    embs  = np.loadtxt(args.emb, delimiter=' ', skiprows=1)
    idx, embedding_value = embs[:,0], embs[:,1:]
    idx = idx.astype(int).astype(str)
    for i in range(len(idx)):
        embeddings[idx[i]]=embedding_value[i]
    print("step 3 read embeddings finished---------------------------------\n")

    # 4.get all sum_path_probability for drug_ids
    path_info_file = args.outprefix + "_" + args.cal_type + "_path_info.txt"
    if args.cal_type == "single_dotProd":
        drug_scores = uti.get_all_path_prob(args.graph_file, disease_id, drug_ids, target_drug_ids, embeddings, embedding_prefix, path_info_file, args.cal_type)
        norm_drug_scores = uti.get_normalized_score([i[0] for i in drug_scores])
        score_file_dotProd = args.outprefix + "_" + args.cal_type + ".txt"
        out_score_dotProd = open(score_file_dotProd,'w')
        i=0
        for element in drug_scores:
            i = i+1
            out_score_dotProd.write(str(i)+"\t"+str(element[1])+"\t"+str(drug_id_name[str(element[1])])+"\t"+str(element[0])+"\t"+str(norm_drug_scores[i-1])+"\n")
        return 0

    ranked_scores_sum, ranked_scores_mean, ranked_scores_max,ranked_scores_top10mean, ranked_scores_top20mean = uti.get_all_path_prob(args.graph_file, disease_id, drug_ids, target_drug_ids, embeddings, embedding_prefix, path_info_file, args.cal_type)
    
    score_value_sum = [i[0] for i in ranked_scores_sum]
    score_value_mean = [i[0] for i in ranked_scores_mean]
    score_value_max = [i[0] for i in ranked_scores_max]
    score_value_top10mean = [i[0] for i in ranked_scores_top10mean]
    score_value_top20mean = [i[0] for i in ranked_scores_top20mean]
    norm_score_value_sum = uti.get_normalized_score(score_value_sum)
    norm_score_value_mean = uti.get_normalized_score(score_value_mean)
    norm_score_value_max = uti.get_normalized_score(score_value_max)
    norm_score_value_top10mean = uti.get_normalized_score(score_value_top10mean)
    norm_score_value_top20mean = uti.get_normalized_score(score_value_top20mean)
    print("step 4 get ranked score finished--------------------------------\n")
    
    # 5.output score results
    score_file_sum = args.outprefix + "_" + args.cal_type + "_score_file_sum.txt"
    score_file_mean = args.outprefix + "_" + args.cal_type + "_score_file_mean.txt"
    score_file_max = args.outprefix + "_" + args.cal_type + "_score_file_max.txt"
    score_file_top10mean = args.outprefix + "_" + args.cal_type +"_score_file_top10mean.txt"
    score_file_top20mean = args.outprefix + "_" + args.cal_type + "_score_file_top20mean.txt"
    out_score_sum = open(score_file_sum,'w')
    out_score_mean = open(score_file_mean, 'w')
    out_score_max = open(score_file_max, 'w')
    out_score_top10mean = open(score_file_top10mean, 'w')
    out_score_top20mean = open(score_file_top20mean, 'w')

    i=0
    for element in ranked_scores_sum:
        i = i+1
        out_score_sum.write(str(i)+"\t"+str(element[1])+"\t"+str(drug_id_name[str(element[1])])+"\t"+str(element[0])+"\t"+str(norm_score_value_sum[i-1])+"\n")
    
    i=0
    for element in ranked_scores_mean:
        i = i+1
        out_score_mean.write(str(i)+"\t"+str(element[1])+"\t"+str(drug_id_name[str(element[1])])+"\t"+str(element[0])+"\t"+str(norm_score_value_mean[i-1])+"\n")
  
    i=0
    for element in ranked_scores_max:
        i = i+1
        out_score_max.write(str(i)+"\t"+str(element[1])+"\t"+str(drug_id_name[str(element[1])])+"\t"+str(element[0])+"\t"+str(norm_score_value_max[i-1])+"\n")
    i=0
    for element in ranked_scores_top10mean:
        i = i+1
        out_score_top10mean.write(str(i)+"\t"+str(element[1])+"\t"+str(drug_id_name[str(element[1])])+"\t"+str(element[0])+"\t"+str(norm_score_value_top10mean[i-1])+"\n")
    i=0
    for element in ranked_scores_top20mean:
        i = i+1
        out_score_top20mean.write(str(i)+"\t"+str(element[1])+"\t"+str(drug_id_name[str(element[1])])+"\t"+str(element[0])+"\t"+str(norm_score_value_top20mean[i-1])+"\n")
    print("step 5 output finished-----------------------------------------\n")

    # 6. output single path prob
    single_prob_file = args.outprefix +  "_" + args.cal_type + "_single_path_prob_file.txt"
    out_singlePath_prob = open(single_prob_file,'w')
    for i in uti.ALL_SINGLE_PATH_PRO:
        out_singlePath_prob.write(str(i)+"\t"+str(uti.ALL_SINGLE_PATH_PRO[i])+"\n")
    print("step 6 output finished-----------------------------------------\n")

    #7. output single edge prob
    single_prob_file = args.outprefix +  "_" + args.cal_type + "_single_path_prob_file.txt"
    out_singlePath_prob = open(single_prob_file,'w')
    for i in uti.ALL_SINGLE_PATH_PRO:
        out_singlePath_prob.write(str(i)+"\t"+str(uti.ALL_SINGLE_PATH_PRO[i])+"\n")
    print("step 6 output finished-----------------------------------------\n")

if __name__ == '__main__':
    main()
