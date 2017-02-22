#!/bin/python
# -*- coding:utf-8 -*-
from lxml import etree


###### Description ###
###
# Les classes pour manipuler les fichiers.
# La classe pour l'évaluation.
###


############################ Files parser.

class File_parser:
    def __init__(self, path):
        self.path = path

    # Pour formater les phrases.
    def queries(self, text):
        # maj = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" ")
        minuscules = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")
        num = "0 1 2 3 4 5 6 7 8 9".split(" ")
        phrase = ""
        for s in text.lower():
            if s in minuscules or s in num or s in [" ", "-", "."]:
                phrase += s
            elif s in ["\n"]:
                phrase += " "
        return phrase

    # Permet d'utiliser with (context managers) avec un objet.
    # Ceci a pour effet de fermer la ressource.
    def __enter__(self):
        return self

    def close(self):
        pass

    def __exit__(self, *err):
        self.close()


class TSV_parser(File_parser):
    def __init__(self, path):
        File_parser.__init__(self, path)
        self.lignes = []
        self.load()
        self.outs = {}

    def load(self):
        with open(self.path) as data_file:
            self.lignes = data_file.readlines()
        print("File " + self.path + " loaded.")

    def load_outs_sep(self, sep):
        for line in self.lignes:
            spl = line.strip().split("\t")
            if len(spl) == 2:
                articles = spl[1].split(sep)
                self.outs[spl[0]] = articles

    def load_outs(self):
        for line in self.lignes:
            spl = line.strip().split("\t")
            if len(spl) == 2:
                self.outs[spl[0]] = spl[1]

    def load_outs_terrier(self):
        for line in self.lignes:
            spl = line.strip().split(" ")
            if len(spl) == 6:
                # spl[0] est l'id de la ligne, spl[2] est le résultat et spl[4] est le score.
                if spl[0] in self.outs:
                    self.outs[spl[0]].append([spl[2], spl[4]])
                else:
                    self.outs[spl[0]] = []
                    self.outs[spl[0]].append([spl[2], spl[4]])


class XML_parser(File_parser):
    def __init__(self, path):
        File_parser.__init__(self, path)
        self.tree = etree.parse(self.path)
        self.root = self.tree.getroot()


class XML_parser_civil_code(XML_parser):
    def __init__(self, path):
        XML_parser.__init__(self, path)
        self.articles = {}
        self.sections = {}
        self.chapters = {}

    #  Extraire le contenu de tous les articles.
    def extraction_articles(self):
        for article in self.root.iter("article"):
            text = self.extraction_article(article)
            self.articles[article.get("id")] = self.queries(text)
        print("Articles extraction done.")

    #  Extraire les id des articles par chapitre.
    def extraction_chapters(self):
        romain_number = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6", "VII": "7", "VIII": "8",
                         "IX": "9", "X": "10"}
        for part in self.root.iter("part"):
            for chapter in part.findall("chapter"):
                # Get id of the chapter.
                if part.get("id") in romain_number:
                    part_number = romain_number[part.get("id")]
                else:
                    part_number = part.get("id")
                if chapter.get("id") in romain_number:
                    chapter_number = romain_number[chapter.get("id")]
                else:
                    chapter_number = chapter.get("id")
                id_chapter = part_number + "." + chapter_number

                # Articles by part/chapter.
                id_articles = []
                for article in chapter.iter("article"):
                    id_articles.append(article.get("id"))
                self.chapters[id_chapter] = id_articles
        print("Chapters extraction done.")

    #  Extraire les titres des sections pour chaque article.
    def extraction_sections(self):
        for article in self.root.iter("article"):
            id_article = article.get("id")
            # .. représente l'élément parent du noeud actuel.
            title = article.find("..").get("title")
            self.sections[id_article] = self.queries(title)

        print("Sections extraction done.")

    #  Extraire le contenu d'un article.
    def extraction_article(self, article):
        text = ""
        paragraphs = article.findall("paragraph")
        if len(paragraphs) > 0:
            for paragraph in paragraphs:
                text += paragraph.text + " "
        else:
            text = article.text
        return text


class XML_parser_question_answering(XML_parser):
    def __init__(self, path):
        XML_parser.__init__(self, path)
        self.questions = {}
        self.answers = {}

    def extractions(self):
        for dataset in self.tree.xpath("/dataset"):
            for pair in dataset.findall("pair"):
                id_pair = pair.get("id")
                answer = pair.find("t1")
                question = pair.find("t2")
                self.answers[id_pair] = []
                if answer is not None:
                    for answer in answer.findall("article"):
                        self.answers[id_pair].append(answer.get("id"))
                self.questions[id_pair] = self.queries(question.text)


############################ Évaluation.

class Evaluation:
    # data_eval et results --> id_query: [id_articles]
    def __init__(self, data_eval, results):
        self.data_eval = data_eval
        self.results = results
        self.recall = 0.0
        self.precision = 0.0
        self.fmesure = 0.0

    def scores(self):
        print("Evaluation.")
        len_queries = 0
        len_articles = 0
        articles_found = 0
        articles_retrieved = 0

        for id_query in self.data_eval:
            len_queries += 1
            len_articles += len(self.data_eval[id_query])
            ok = 0
            if id_query in self.results:
                articles_retrieved += len(self.results[id_query])
                for id_article in self.data_eval[id_query]:
                    if id_article in self.results[id_query]:
                        articles_found += 1

        self.precision = round((articles_found / float(articles_retrieved)) * 100, 1)
        self.recall = round((articles_found / float(len_articles)) * 100, 1)
        self.fmesure = round(((2 * self.precision * self.recall) / (self.precision + self.recall)), 1)

        print("Number of queries: " + str(len_queries))
        print("Number of articles: " + str(len_articles))
        print("\t### ### ###")
        self.__str__()

    def __str__(self):
        print("PRECISION: " + str(self.precision) + "%")
        print("RECALL: " + str(self.recall) + "%")
        print("F-MESURE: " + str(self.fmesure) + "%")
