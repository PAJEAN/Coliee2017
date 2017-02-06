#!/bin/python
# -*- coding:utf-8 -*-
#import nltk,
import glob
import numpy as np
import boite_a_outils as bao

###### Description ###
###
# Détection des articles par apprentissage.
###

###### Inputs ###
###
path_file_civcode = "Data/civcode.xml"
path_folder_queries = "Data/Training"
result_articles_path = "terrier-core-4.2/var/results/BM25b0.75_articles.res"
index_article_path = "Data/Index/id_query-num_articles.tsv"
nb_results = 1
###

###### Ouputs ###
###
out = open("Data/features.txt", "w")
###

corpus = {}
queries = {}

"""
corpus = {"a":"Human machine interface for lab abc computer applications",
			"b":"A survey of user opinion of computer system response time",
			"c":"The EPS user interface management system",
			"d":"System and human system engineering testing of EPS",
			"e":"Relation of user perceived response time to error measurement",
			"f":"The generation of random binary unordered trees",
			"g":"The intersection graph of paths in trees",
			"h":"Graph minors IV Widths of trees and well quasi ordering",
			"i":"Graph minors A survey"}

queries = {"r_a":"Human machine",
			"r_b":"User interface",
			"r_c":"Generation of graph minors"}
"""

###### ######  Load Data. ######  ######
###### Civ. Code.
with bao.XML_parser_civil_code(path_file_civcode) as xml_parser:
	xml_parser.extraction_articles()
	for id_article in xml_parser.articles:
		corpus[id_article] = xml_parser.articles[id_article]
###### Queries
# Extraire les questions.
links = glob.glob(path_folder_queries+"/*.xml")
compteur = 0
for link in links:
	print "Lien: "+link
	xml_parser = bao.XML_parser_question_answering(link)
	xml_parser.extractions()
	for id_question in xml_parser.questions:
		queries[id_question] = xml_parser.questions[id_question]

id_query_num_art = {}
with bao.TSV_parser(index_article_path) as tsv_parser:
	tsv_parser.load_outs_sep(";")
	id_query_num_art = tsv_parser.outs

###### ######  Résultats fournis par Terrier. ######  ######
###### Articles.
with bao.TSV_parser(result_articles_path) as tsv_parser_articles:
	tsv_parser_articles.load_outs_terrier()

obj_tf_idf = bao.Tf_idf(corpus)
obj_tf_idf.corpus_processing()

for id_query in queries:
	print("Query: "+id_query)
	termes = set(obj_tf_idf.normalisation(queries[id_query]))
	# stat_corpus est récupéré sur les premiers résultats du BM25.
	for id_article in corpus:
	
		termes_art = set(obj_tf_idf.tf[id_article])
		# Features.
		feature = []
		label = "0"
		
		tf_art = []
		tf_idf_art = []
		t_cover = 0
		t_cover_ratio = 0.0
		
		bm25 = 0.0
		if id_query in tsv_parser_articles.outs:
			for bm_res in tsv_parser_articles.outs[id_query]:
				if bm_res[0] == id_article:
					bm25 = bm_res[1]
			
		
		# TF-IDF.
		t_intersection = termes.intersection(termes_art)
		if len(t_intersection) > 0:
			for t in t_intersection:
				tf_art.append(obj_tf_idf.tf[id_article][t])
				tf_idf_art.append(obj_tf_idf.tf_idf[id_article][t])
				
			t_cover = len(t_intersection)
			t_cover_ratio = t_cover / float(len(termes))
			
		else:
			tf_art.append(0)
			tf_idf_art.append(0)
		
		feature += [t_cover, t_cover_ratio, len(termes), sum(tf_art), min(tf_art), max(tf_art), np.mean(tf_art), np.var(tf_art), sum(tf_idf_art), min(tf_idf_art), max(tf_idf_art), np.mean(tf_idf_art), np.var(tf_idf_art), bm25]
		
		if id_article in id_query_num_art[id_query]:
			label = "1"
		
		out.write(label+" qid:"+id_query)
		cmpt = 0
		for f in feature:
			out.write(" "+str(cmpt)+":"+str(f))
			cmpt += 1
		out.write(" #docid = "+id_article+"\n")

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
