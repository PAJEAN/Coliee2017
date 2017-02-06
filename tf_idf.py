#!/bin/python
# -*- coding:utf-8 -*-
#import nltk,
import glob
import numpy as np
from sklearn import svm
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
#out = open("Data/", "w")
###

# Pour limiter les résultats de Terrier.
def lim_dictionnaire(dictionnaire, lim, option = 1):
	for id_query in dictionnaire:
		dictionnaire[id_query] = dictionnaire[id_query][:lim]
		tmp = []
		for cmpt in dictionnaire[id_query]:
			if option == 1:
				tmp.append(cmpt[0])
			else:
				tmp.append(cmpt)
		dictionnaire[id_query] = tmp
	return dictionnaire

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

###### ######  Data Éval. . ######  ######
# On récolte les données issues de la conférence.
# Ces données sont les id des requêtes et les numéros des articles associées.
# Construction du jeu training/eval.
conf_results = {}
id_queries_training = []; id_queries_eval = []
id_query_num_art = {}
with bao.TSV_parser(index_article_path) as tsv_parser:
	tsv_parser.load_outs_sep(";")
	id_query_num_art = tsv_parser.outs
	compt = 0
	for id_q in tsv_parser.outs:
		if compt%3 == 0:
			id_queries_eval.append(id_q)
			conf_results[id_q] = tsv_parser.outs[id_q]
		else:
			id_queries_training.append(id_q)
		compt += 1
	print("Training data: "+str(len(id_queries_training))+" / Eval data: "+str(len(id_queries_eval)))


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
	

###### ######  Résultats fournis par Terrier. ######  ######
###### Articles.
with bao.TSV_parser(result_articles_path) as tsv_parser_articles:
	tsv_parser_articles.load_outs_terrier()

query_article = lim_dictionnaire(tsv_parser_articles.outs, nb_results, 0)


obj_tf_idf = bao.Tf_idf(corpus)
obj_tf_idf.corpus_processing()


features = []; labels_training = []
features_p = {}; labels_eval = {}
id_eval = {}
for id_query in queries:
	termes = set(obj_tf_idf.normalisation(queries[id_query]))
	# stat_corpus est récupéré sur les premiers résultats du BM25.
	features_p[id_query] = []
	labels_eval[id_query] = []
	id_eval[id_query] = []
	for id_article in query_article[id_query]:
	
		termes_art = set(obj_tf_idf.tf[id_article[0]])
		# Features.
		feature = []
		label = "n"
		
		tf_art = []
		tf_idf_art = []
		t_cover = 0
		t_cover_ratio = 0.0
		bm25 = id_article[1]
		
		# TF-IDF.
		t_intersection = termes.intersection(termes_art)
		if len(t_intersection) > 0:
			for t in t_intersection:
				tf_art.append(obj_tf_idf.tf[id_article[0]][t])
				tf_idf_art.append(obj_tf_idf.tf_idf[id_article[0]][t])
				print obj_tf_idf.tf_idf[id_article[0]][t]
			t_cover = len(t_intersection)
			t_cover_ratio = t_cover / float(len(termes))
			
		else:
			tf_art.append(0)
			tf_idf_art.append(0)
		
		feature += [t_cover, t_cover_ratio, len(termes), sum(tf_art), min(tf_art), max(tf_art), np.mean(tf_art), np.var(tf_art), sum(tf_idf_art), min(tf_idf_art), max(tf_idf_art), np.mean(tf_idf_art), np.var(tf_idf_art), bm25]
		
		if id_article[0] in id_query_num_art[id_query]:
			label = "y"
		
		if id_query in id_queries_training:
			features.append(feature)
			labels_training.append(label)
		elif id_query in id_queries_eval:
			id_eval[id_query].append(id_article[0])
			features_p[id_query].append(feature)
			labels_eval[id_query].append(label)

# SVM 2 labels y/n.
results_terrier = {}
# Learning.
clf = svm.SVC(C=1, kernel = 'rbf')
clf.fit(features, labels_training)
# Prediction.
for id_query in id_queries_eval:
	predictions = clf.predict(features_p[id_query])
	yes_found = []
	cmpt = 1
	for label in range(len(predictions)):
		if predictions[label] == "y":
			yes_found.append(id_eval[id_query][label])
			if cmpt > 1:
				print "Prediction: ", predictions, "/ Evaluation: ", labels_eval[id_query]
		cmpt += 1
	
	results_terrier[id_query] = yes_found


res_eval = bao.Evaluation(conf_results, results_terrier)
res_eval.scores()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
