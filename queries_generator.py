#!/bin/python
# -*- coding:utf-8 -*-
import glob
import boite_a_outils as bao

import kb_generator as kbg

###### Description ###
###
# Permet d'extraire les questions et les réponses associées.
# Permet de générer le fichier de requête pour le soumettre à Terrier.
# Permet de générer le fichier tsv avec l'id de la question et les articles associés.
###

###### Inputs ###
###
path_folder = "Data/Training"
###

###### Ouputs ###
###
out = open("Data/requetes.xml", "w")
out2 = open("tmp/id_query-num_articles.tsv", "w")
out3 = open("tmp/requetes_lem.tsv", "w")
out4 = open("tmp/requetes.tsv", "w")
###

# Extraire les questions/réponses.
links = glob.glob(path_folder+"/*.xml")
compteur = 0
for link in links:
	print "Lien: "+link

	xml_parser = bao.XML_parser_question_answering(link)
	xml_parser.extractions()
	
	for id_question in xml_parser.answers:
		out2.write(id_question+"\t"+";".join(xml_parser.answers[id_question])+"\n")
	
	# Création du fichier de requêtes.
	for id_question in xml_parser.questions:
		out.write("<top>\n")
		out.write("<num>"+id_question+"</num><title>\n")

		question_text = xml_parser.questions[id_question]
		question_text_lem = kbg.lemmatize(question_text)

		out.write(question_text_lem+"\n")
		out.write("</title>\n")
		out.write("</top>\n")

		out3.write(id_question+"\t"+question_text_lem+"\n")
		out4.write(id_question+"\t"+question_text+"\n")
			
out.close()
out2.close()
out3.close()
out4.close()


			
			
			
