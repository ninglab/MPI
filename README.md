# Modeling Path Importance for Effective Alzheimer’s Disease Drug Repurposing

This is the implementation of our model MPI will be published in Pacific Symposium on Biocomputing (PSB) 2024.

## Dependency

- [DeepWalk](https://github.com/phanein/deepwalk)

Please install DeepWalk following their instruction.

## Dataset

We are not permitted to release the processed data. Please request access and download the datasets presented in Section Materials and Methods of our manuscript.
After downloading datasets, please use our notebook network_construction.ipynb to reproduce the network used in our study.

## Embedding Generation

Please run the following command to generate embeddings for all the nodes in the network.

`python get_distance_matrix.py`

## Drug Scoring

After generating node embeddings, please refer to the following example to score drugs.

`python prob_scoring.py --graph_file Network_forDeepwalk.txt --emb Network.embeddings --all_drug_id_name_file all_drugName_nodeID.txt --target_drug_id_name_file all_drugName_nodeID.txt --cal_type dotProd_softmax --outprefix ./score_ourMethod`

<code>graph\_file</code> specifies the network file.

<code>emb</code> specifies the file containing node embeddings.

<code>all\_drug\_id\_name\_file</code> specifies the file containing the mapping between drug name and node id in the network.

<code>cal\_type</code> specifies the method to calculate scores on edges.

## Acknowledgements

We leveraged [DeepWalk](https://github.com/phanein/deepwalk) to implement our framework. Thanks for the great work!
