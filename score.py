#!/bin/python
# -*- coding:utf-8 -*-
#from sklearn import svm
import boite_a_outils as bao

###### Description ###
###
# Pour évaluer les résultats de Terrier.
# On évalue tout d'abord les 3 premiers résultats (avec le score le plus élevé).
# L'option chapter (!= 0) permet d'évaluer selon un pré-filtrage des chapitres.
###

###### Inputs ###
###

# Articles.
#result_articles_path = "terrier-core-4.2/var/results/BM25b0.75_12.res"
result_articles_path = "terrier-core-4.2/var/results/BM25b0.75_articles.res"
index_article_path = "Data/Index/id_query-num_articles.tsv"
nb_results = 1

# Chapitres.
index_chapter_path = "Data/Index/num_articles-id_chapitre.tsv"
result_chapter_path = "terrier-core-4.2/var/results/BM25b0.75_chapters.res"
nb_results_chapter = 5
	
# Sections.
result_section_path = "terrier-core-4.2/var/results/BM25b0.75_sections.res"
nb_results_section = 3

# Paragraphs.
result_paragraph_path = "terrier-core-4.2/var/results/BM25b0.75_13.res"
nb_results_paragraph = 1

links = 0
if links == 1:
	adjacences_articles_path = "Data/Index/adjacences_articles.tsv"


###

###### Ouputs ###
###
out = open("Data/details_evaluation.tsv", "w")
out.write("nb_Query\tTraining\tEval\n")
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

###### ######  Data Éval. . ######  ######
# On récolte les données issues de la conférence.
# Ces données sont les id des requêtes et les numéros des articles associées.
with bao.TSV_parser(index_article_path) as tsv_parser:
	tsv_parser.load_outs_sep(";")
	conf_results = tsv_parser.outs

###### ######  Résultats fournis par Terrier. ######  ######
###### Chapitres.
# Pour considérer les chapitres des articles.
# On stock pour chaque article du code civil leur chapitre.
with bao.TSV_parser(index_chapter_path) as tsv_parser:
	tsv_parser.load_outs()
	article_chapter = tsv_parser.outs

# On stock pour chaque requête, les chapitres retrouvés par Terrier.
with bao.TSV_parser(result_chapter_path) as tsv_parser_chapters:
	# load_outs_terrier --> [id_result, score].
	tsv_parser_chapters.load_outs_terrier()

###### Sections.
# Pour considérer les sections des articles.		
# id_query -- articles.
with bao.TSV_parser(result_section_path) as tsv_parser_sections:
	tsv_parser_sections.load_outs_terrier()

###### Articles.
with bao.TSV_parser(result_articles_path) as tsv_parser_articles:
	tsv_parser_articles.load_outs_terrier()

###### Paragraphes.
with bao.TSV_parser(result_paragraph_path) as tsv_parser_paragraphs:
	tsv_parser_paragraphs.load_outs_terrier()
	
# Pour considérer les chapitres des articles.
if links != 0:
	tsv_parser = bao.TSV_parser(adjacences_articles_path)
	tsv_parser.load_outs()
	links_articles = tsv_parser.outs

###### ######  Modélisation de l'évaluation ######  ######
modele = 0
results_terrier = {}
# Sections & Chapitres.
if modele in [0,1,2,3]:
	query_paragraph = lim_dictionnaire(tsv_parser_paragraphs.outs, nb_results_paragraph)
	query_article = lim_dictionnaire(tsv_parser_articles.outs, nb_results)
	query_section = lim_dictionnaire(tsv_parser_sections.outs, nb_results_section)
	query_chapter = lim_dictionnaire(tsv_parser_chapters.outs, nb_results_chapter)
elif modele in [4,5]:
	query_article = lim_dictionnaire(tsv_parser_articles.outs, nb_results, 0)
	query_section = lim_dictionnaire(tsv_parser_sections.outs, nb_results_section, 0)
	query_chapter = lim_dictionnaire(tsv_parser_chapters.outs, nb_results_chapter, 0)

if modele == 0:
	for id_query in query_paragraph:
		for id_article in query_paragraph[id_query]:
			spl = id_article.split("_")
			if len(spl) > 1:
				id_article = spl[0]
			if id_query in results_terrier:
				results_terrier[id_query].append(id_article)
			else:
				results_terrier[id_query] = []
				results_terrier[id_query].append(id_article)
elif modele == 1:
	for id_query in query_article:
		for id_article in query_article[id_query]:
			if article_chapter[id_article] in query_chapter[id_query] and id_article in query_section[id_query]:
				if id_query in results_terrier:
					results_terrier[id_query].append(id_article)
				else:
					results_terrier[id_query] = []
					results_terrier[id_query].append(id_article)
# Sections & Chapitres.
elif modele == 2:
	for id_query in query_article:
		for id_article in query_article[id_query]:
			if id_article in query_section[id_query]:
				if id_query in results_terrier:
					results_terrier[id_query].append(id_article)
				else:
					results_terrier[id_query] = []
					results_terrier[id_query].append(id_article)
			else:
				if article_chapter[id_article] in query_chapter[id_query]:
					if id_query in results_terrier:
						results_terrier[id_query].append(id_article)
					else:
						results_terrier[id_query] = []
						results_terrier[id_query].append(id_article)
# Articles.
elif modele == 3:
	for id_query in query_article:
		for id_article in query_article[id_query]:
			if id_query in results_terrier:
				results_terrier[id_query].append(id_article)
				print len(results_terrier[id_query])
			else:
				results_terrier[id_query] = []
				results_terrier[id_query].append(id_article)

# Apprentissage.
elif modele == 4:
	# Package.
	from sklearn import svm
	
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
	
	# Construction du vecteur des caractéristiques.
	features = []; labels_training = []
	features_p = {}; labels_eval = {}
	id_eval = {}
	for id_query in query_article:
		features_p[id_query] = []
		labels_eval[id_query] = []
		id_eval[id_query] = []
		for id_article in range(len(query_article[id_query])):
			
				feature = []
				label = "n"

				# Emplacement & score.
				feature.append(id_article)
				feature.append(query_article[id_query][id_article][1])

				# Chapitres.
				num_chap = -1
				#sc_chap = 0.0
				for chap in range(len(query_chapter[id_query])):
					if article_chapter[query_article[id_query][id_article][0]] == query_chapter[id_query][chap][0]:
						num_chap = chap
						sc_chap = query_chapter[id_query][chap][1]
				#feature.append(num_chap)
				feature.append(sc_chap)

				# Sections.
				num_sect = -1
				#sc_sect = 0.0
				for section in range(len(query_section[id_query])):
					if query_article[id_query][id_article][0] == query_section[id_query][section][0]:
						num_sect = section
						#sc_sect = query_section[id_query][section][1]
				#feature.append(num_sect)
				#feature.append(sc_sect)
				
				
				if query_article[id_query][id_article][0] in id_query_num_art[id_query]:
					label = "y"
				
				if id_query in id_queries_training:
					features.append(feature)
					labels_training.append(label)
				elif id_query in id_queries_eval:
					id_eval[id_query].append(query_article[id_query][id_article][0])
					features_p[id_query].append(feature)
					labels_eval[id_query].append(label)
	
	# SVM 2 labels y/n.
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

elif modele == 5:
	None
	
	
	
	
	
# EVALUATION.
res_eval = bao.Evaluation(conf_results, results_terrier)
res_eval.scores()
	
	
	
	
	
	
	
	
