#!/bin/python
# -*- coding:utf-8 -*-
from sklearn import svm
import re, math, glob
from collections import Counter
import boite_a_outils as bao

###### Description ###
###
# Détection des articles par apprentissage.
###

###### Inputs ###
###
path_folder = "Data/Index/id_query-num_articles.tsv"
path_folder1 = "terrier-core-4.2/var/results/BM25b0.75_articles.res"
path_folder2 = "terrier-core-4.2/var/results/BM25b0.75_sections.res"
path_folder3 = "terrier-core-4.2/var/results/BM25b0.75_chapters.res"

index_chapter_path = "Data/Index/num_articles-id_chapitre.tsv"
###

###### Ouputs ###
###
#out = open("Data/", "w")
###

WORD = re.compile(r'\w+')
def get_cosine(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])
	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)
	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

def text_to_vector(text):
	words = WORD.findall(text)
	return Counter(words)

def lim_dictionnaire(dictionnaire, lim):
	for id_query in dictionnaire:
		dictionnaire[id_query] = dictionnaire[id_query][:lim]
		tmp = []
		for cmpt in dictionnaire[id_query]:
			tmp.append(cmpt)
		dictionnaire[id_query] = tmp
	return dictionnaire

def lim_dictionnaire_sep(dictionnaire, lim):
	dico = dictionnaire
	for id_query in dictionnaire:
		dico[id_query] = dictionnaire[id_query][:lim]
		tmp = []
		for cmpt in dico[id_query]:
			tmp.append(cmpt[0])
		dico[id_query] = tmp
	return dictionnaire

"""	
text1 = 'This is a foo bar sentence .'
text2 = 'This sentence is similar to a foo bar sentence .'
vector1 = text_to_vector(text1)
vector2 = text_to_vector(text2)
cosine = get_cosine(vector1, vector2)
#print 'Cosine:', cosine
"""

# Jeu training/eval.

conf_results = {}
id_queries_training = []
id_queries_eval = []
id_query_num_art = {}
with bao.TSV_parser(path_folder) as tsv_parser:
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

# score_Terrier_articles > 40.0 --> 82 ok et 6 bad.

# Res. articles.
tsv_parser = bao.TSV_parser(path_folder1)
tsv_parser.load_outs_terrier()
nb_results = 3
query_article = tsv_parser.outs
query_article1 = dict(tsv_parser.outs)
query_article_sep = lim_dictionnaire_sep(query_article1, 1)
query_article = lim_dictionnaire(query_article, nb_results)

# Res. Sections.
with bao.TSV_parser(path_folder2) as tsv_parser:
	tsv_parser.load_outs_terrier()
	sections = tsv_parser.outs
	sections1 = dict(tsv_parser.outs)
	query_section_sep = lim_dictionnaire_sep(sections1, 3)
	sections = lim_dictionnaire(sections, nb_results)

# Res. Chapitres.
with bao.TSV_parser(index_chapter_path) as tsv_parser:
	tsv_parser.load_outs()
	article_chapter = tsv_parser.outs

with bao.TSV_parser(path_folder3) as tsv_parser:
	tsv_parser.load_outs_terrier()
	chapters = tsv_parser.outs
	chapters1 = dict(tsv_parser.outs)
	query_chapter_sep = lim_dictionnaire_sep(chapters1, 3)
	chapters = lim_dictionnaire(chapters, nb_results)
	
	

"""
with bao.TSV_parser(path_folder1) as tsv_parser:
	tsv_parser.load_outs_terrier()
	articles = tsv_parser.outs
"""
# Le texte des articles.
path_file = "Data/civcode.xml"
xml_parser = bao.XML_parser_civil_code(path_file)
xml_parser.extraction_articles()
articles = xml_parser.articles

# Extraire le texte des questions.
requetes = {}
path_folder = "Data/Training"
links = glob.glob(path_folder+"/*.xml")
compteur = 0
for link in links:
	print "Lien: "+link
	xml_parser = bao.XML_parser_question_answering(link)
	xml_parser.extractions()
	for quest in xml_parser.questions:
		if not quest in requetes:
			requetes[quest] = xml_parser.questions[quest]

features = []
features_p = {}
labels_training = []
labels_eval = {}
for id_query in query_article:
	features_p[id_query] = []
	labels_eval[id_query] = []
	if len(query_article[id_query]) == nb_results:
		for id_article in range(len(query_article[id_query])):
			feature = []
			label = "n"

			# Chapitres.
			num_chap = -1
			sc_chap = 0.0
			for chap in range(len(chapters[id_query])):
				if article_chapter[query_article[id_query][id_article][0]] == chapters[id_query][chap][0]:
					num_chap = chap
					sc_chap = chapters[id_query][chap][1]
			feature.append(num_chap)
			feature.append(sc_chap)
			
			# Sections.
			num_sect = -1
			sc_chap = 0.0
			for section in range(len(sections[id_query])):
				if query_article[id_query][id_article][0] == sections[id_query][section][0]:
					num_sect = section
					sc_sect = sections[id_query][section][1]
			feature.append(num_sect)
			#feature.append(sc_sect)
			
			# Emplacement.
			feature.append(id_article)
			# Score.
			#feature.append(query_article[id_query][id_article][1])
			"""
			# Distance.
			vector1 = text_to_vector(requetes[id_query])
			vector2 = text_to_vector(articles[query_article[id_query][id_article][0]])
			cosine = get_cosine(vector1, vector2)
			feature.append(cosine)
			"""
			if query_article[id_query][id_article][0] in id_query_num_art[id_query]:
				label = "y"
			
			if id_query in id_queries_training:
				features.append(feature)
				labels_training.append(label)
			elif id_query in id_queries_eval:
				features_p[id_query].append(feature)
				labels_eval[id_query].append(label)

			
# SVM 3 labels.
# Learning.
clf = svm.SVC(C=1, kernel = 'rbf')
clf.fit(features, labels_training)
# PREDICTION.
results_terrier = {}
won = 0; fail = 0; fail_y = 0; won_y = 0; nb_y = 0
for id_query in id_queries_eval: #.append(feature)
	predictions = clf.predict(features_p[id_query])
	yes_found = []
	for i in range(len(labels_eval[id_query])):
		if labels_eval[id_query][i] == "y":
			nb_y += 1
		if predictions[i] == labels_eval[id_query][i]:
			won += 1
		if predictions[i] == labels_eval[id_query][i] == labels_eval[id_query][i] == "y":
			won_y += 1
		if predictions[i] != labels_eval[id_query][i]:
			fail += 1
		if predictions[i] != labels_eval[id_query][i] and labels_eval[id_query][i] == "y":
			fail_y += 1
		if predictions[i] == "y":
			yes_found.append(query_article[id_query][i][0])
		
	"""
	#for id_query in query_article:
	ok = 0
	for id_article in query_article_sep[id_query]:
		if ok == 0:
			if id_article in query_section_sep[id_query]:
				if not id_article in yes_found:
					yes_found.append(id_article)
					ok = 1

			else:
				if article_chapter[id_article] in query_chapter_sep[id_query]:
					if not id_article in yes_found:
						yes_found.append(id_article)
						ok = 1
	"""
	if len(yes_found) > 1:
		print yes_found,"/"," ".join(conf_results[id_query])
	#if len(yes_found) == 0:
	#	yes_found.append(query_article[id_query][0][0])
			
	results_terrier[id_query] = yes_found
		
print won_y, "/", nb_y
print "WON:", won, "/ FAIL:", fail
print fail_y

# EVALUATION.
res_eval = bao.Evaluation(conf_results, results_terrier)
res_eval.scores()

"""
elif modele == 3:
	from sklearn import svm
	
	query_article = tsv_parser_articles.outs
	query_section = tsv_parser_sections.outs
	query_chapter = tsv_parser_chapters.outs
	
	# Le nombre de features doit être identique pour chaque requête.
	# On exploite la valeur minimale des résultats de Terrier.
	min_lim = []
	for id_query in query_article:
		min_lim.append(len(query_article[id_query]))
	#val_min = min(min_lim)
	val_min = 20
	
	
	# Construction du jeu training/eval.
	id_queries_training = []
	id_queries_eval = []
	id_query_num_art = {}
	with bao.TSV_parser(index_article_path) as tsv_parser:
		tsv_parser.load_outs_sep(";")
		id_query_num_art = tsv_parser.outs
		compt = 0
		for id_q in tsv_parser.outs:
			if compt%3 == 0:
				id_queries_eval.append(id_q)
			else:
				id_queries_training.append(id_q)
			compt += 1
	
	# Construction des caractéristiques.
	features = []
	features_p = {}
	labels_training = []
	labels_eval = {}
	for id_query in query_article:
		features_p[id_query] = []
		labels_eval[id_query] = []
		cmpt = 0
		for id_article in range(len(query_article[id_query])):
			if cmpt < val_min:
				cmpt += 1
			
				feature = []
				label = "n"

				# Emplacement & score.
				feature.append(id_article)
				#feature.append(query_article[id_query][id_article][1])

				# Chapitres.
				num_chap = -1
				#sc_chap = 0.0
				for chap in range(len(query_chapter[id_query])):
					if article_chapter[query_article[id_query][id_article][0]] == query_chapter[id_query][chap][0]:
						num_chap = chap
						#sc_chap = query_chapter[id_query][chap][1]
				feature.append(num_chap)
				#feature.append(sc_chap)

				# Sections.
				num_sect = -1
				#sc_sect = 0.0
				for section in range(len(query_section[id_query])):
					if query_article[id_query][id_article][0] == query_section[id_query][section][0]:
						num_sect = section
						#sc_sect = query_section[id_query][section][1]
				feature.append(num_sect)
				#feature.append(sc_sect)
				
				
				if query_article[id_query][id_article][0] in id_query_num_art[id_query]:
					label = "y"
				
				if id_query in id_queries_training:
					features.append(feature)
					labels_training.append(label)
				elif id_query in id_queries_eval:
					features_p[id_query].append(feature)
					labels_eval[id_query].append(label)
	
	query_article = dict(tsv_parser_articles.outs)
	query_article_sep = lim_dictionnaire(tsv_parser_articles.outs, nb_results)
	query_section = lim_dictionnaire(query_section, nb_results_section)
	query_chapter = lim_dictionnaire(query_chapter, nb_results_chapter)
	
	# SVM 3 labels.
	# Learning.
	clf = svm.SVC(C=1, kernel = 'rbf')
	clf.fit(features, labels_training)
	# PREDICTION.
	won = 0; fail = 0; fail_y = 0; won_y = 0; nb_y = 0
	for id_query in id_queries_eval: #.append(feature)
		predictions = clf.predict(features_p[id_query])
		yes_found = []
		for i in range(len(labels_eval[id_query])):
			if labels_eval[id_query][i] == "y":
				nb_y += 1
			if predictions[i] == labels_eval[id_query][i]:
				won += 1
			if predictions[i] == labels_eval[id_query][i] and labels_eval[id_query][i] == "y":
				won_y += 1
			if predictions[i] != labels_eval[id_query][i]:
				fail += 1
			if predictions[i] != labels_eval[id_query][i] and labels_eval[id_query][i] == "y":
				fail_y += 1
			if predictions[i] == "y":
				yes_found.append(query_article[id_query][i][0])
		
		results_terrier[id_query] = yes_found
		#if len(yes_found) > 1:
		#	print yes_found,"/"," ".join(conf_results[id_query])
	
		
	
			
	print won_y, "/", nb_y
	#print "WON:", won, "/ FAIL:", fail
	#print fail_y
"""














