#!/usr/bin/python
# -*- coding:utf-8 -*-
# from sklearn import svm
# Syntax: python score.py [repertoire des fichiers xml de requetes][True/False sont -ils annotés?]

import boite_a_outils as bao
import os
import sys

'''
 Class used to store the K best results. We define a capacity (max size) then for each result
 we ask the result set to evaluate it; the result will be stored only if it has be (e.g. has it improves existing ones)
'''


class ResultSet():
    def __init__(self, max_size):
        self.max_size = max_size
        self.items = []
        self.itemScores = []

    def eval(self, item, score):

        #print "____\nEVAL", item, score
        #print self.items
        #print self.itemScores

        if (len(self.items) < self.max_size) or (self.itemScores[-1] < score):

            #print "ADDING"

            # detect location of insertion
            newItemId = len(self.items)
            for i in range(0, len(self.items)):
                if score > self.itemScores[i]:
                    newItemId = i


            #print "loc: ",newItemId
            # Add element
            self.items.insert(newItemId, item)
            self.itemScores.insert(newItemId, score)

            if len(self.items) > self.max_size:
                del self.items[-1]
                del self.itemScores[-1]
            # print r.items, r.itemScores


def loadBestKTerrierResults(path_terrier_results, k_limit):
    print "Loading Terrier results from: ", path_terrier_results
    print "Filtering : top ", k_limit

    terrier_results_full = {}

    for f_name in os.listdir(path_terrier_results):

        if f_name.endswith(".res"):
            f_path = path_terrier_results + "/" + f_name
            print "loading ", f_path

            with open(f_path) as terrier_result_file:
                for line in terrier_result_file:
                    spl = line.strip().split(" ")

                    if len(spl) == 6:
                        id_query = spl[0]
                        id_doc = spl[2]
                        score_doc = spl[4]

                        data_doc = [id_doc, float(score_doc)]

                        if id_query not in terrier_results_full: terrier_results_full[id_query] = []
                        terrier_results_full[id_query].append(data_doc)
                    else:
                        print "[WARNING] excluding ill formatted result: ", line

    terrier_results_bestk = {}

    # filtering the k_limit results
    for id_query in terrier_results_full:

        r = ResultSet(k_limit)

        for data_doc in terrier_results_full[id_query]:
            r.eval(data_doc[0], data_doc[1])

        terrier_results_bestk[id_query] = r
    # print terrier_results_bestk[id_query].items, terrier_results_bestk[id_query].itemScores

    print "Terrier results loaded"
    return terrier_results_bestk

def printPredictions(predictedResults, resultsFile, teamName):
    '''predictedResults is a queryId:[articleId] dictionnary'''
    f = open(resultsFile, 'w')
    for qId in predictedResults:
        for aId in predictedResults[qId]:
            f.write(qId+' '+aId+' '+teamName+'\n')
    f.close()

'''
#############################
PARAMETERS
#############################
'''
# path to terrier results
#path_terrier_results = "tmp/terrier_results/results"
path_terrier_results = "tmp/terrier_results_parts"
# tsv of the matching part of each articles
articleToPartPath = "tmp/articleToPart.tsv"
# path to the index storing expected results for each query
index_expected_query_results = "tmp/id_query-num_articles.tsv"
#index_expected_query_results = "tmp/id_query-num_articles.tsv"
# path to the index storing the articles associated to each doc
docArticle_path = "tmp/docToArticles.tsv"

# number of results that will be considered for a deep analysis
# the k best ranked terrier results will be analysed.
# This parameter thus define k
NB_RESULTS_DEEP_ANALYSIS = 5
# number of final document(s) that will be considered at the end
# note that a document can be linked to several articles
# set to 1 for final run
NB_RESULTS_FINAL = 1
# minimal terrier score a document have to have
# in order to be considered as a result: -1 no threshold
THRESHOLD_TERRIER_SCORE = -1
THRESHOLD_DELTA_TERRIER_SCORE = -1

# retrieve command line parameters
# usage python script_name.py NB_RESULTS_FINAL THRESHOLD_TERRIER
if len(sys.argv) > 1:
    NB_RESULTS_FINAL = int(sys.argv[1])
if len(sys.argv) > 2:
    THRESHOLD_TERRIER_SCORE = int(sys.argv[2])

# Index providing a doc to article mapping
# dict : id_doc -> list of article ids
docToArticle = {}

# Index providing an article to a part mapping
articleToPart = {}

# Expected results
# dict : id_query -> list of article ids
expected_results = {}

# Best NB_RESULTS_DEEP_ANALYSIS for each query
# dict : id_query -> list of ResultSet instances
terrier_results_bestk = {}

# Loading correspondences between indexed documents and articles
with open(docArticle_path) as doc2ArticleFile:
    for l in doc2ArticleFile:
        data = l.strip().split("\t")
        #print data
        if len(data) == 2:
            article_ids = map(str.strip, data[1].split(","))
            docToArticle[data[0]] = article_ids
### Part intead of article
# Loading correspondences between indexed articles and parts
parts = set([])
with open(articleToPartPath) as articleToPartFile:
    for l in articleToPartFile:
        data = l.strip().split("\t")
        #print data
        if len(data) == 2:            
            articleToPart[data[0]] = data[1]
            parts |= {data[1]}
docToArticle = {}
for partId in parts:
    docToArticle[partId] = partId
###


# Loading expected results
with bao.TSV_parser(index_expected_query_results) as tsv_parser:
    tsv_parser.load_outs_sep(";")
    expected_results = tsv_parser.outs
    '''
    print "Expected results"
    for r in expected_results: print "'" + r + "'", expected_results[r]
    '''
    
# convert expected results to parts instead of articles
for queryId in expected_results:
    #queryExpectedParts = []
    for i in range(len(expected_results[queryId])):
        articleId = expected_results[queryId][i]
        expected_results[queryId][i] = articleToPart[articleId]
    expected_results[queryId] = list(set(expected_results[queryId]))

for r in expected_results: print "'" + r + "'", expected_results[r]


# Loading best NB_RESULTS_DEEP_ANALYSIS terrier results for each query
terrier_results_bestk = loadBestKTerrierResults(path_terrier_results, NB_RESULTS_DEEP_ANALYSIS)
print "terrier_results_bestk", terrier_results_bestk
# Filtering results
# based on delta threshold

terrier_results_final_articles = {}

for query_id in terrier_results_bestk:

    print "-----------------------------------------"
    print "Filtering results of query: ", query_id
    print "-----------------------------------------"

    terrier_results_final_articles[query_id] = []

    resultset_query = terrier_results_bestk[query_id]
    print resultset_query.items
    print resultset_query.itemScores

    articles_first_result_doc = None
    articles_saved = None

    first_result_doc_score = None
    delta_best_FirstCompletlyDifferent = None
    delta_best_FirstPartiallyDifferent = None

    for i in range(0, len(resultset_query.items)):

        doc_id = resultset_query.items[i]
        doc_score = resultset_query.itemScores[i]
        doc_articles = docToArticle[doc_id]

        print "result", i, "\t", "doc_id: ", doc_id, "\tscore: ", doc_score, "\t", doc_articles

        if i == 0:
            articles_first_result_doc = docToArticle[doc_id]
            first_result_doc_score = doc_score
            articles_saved = articles_first_result_doc
        else:
            # check if results are different
            intersec = set(articles_first_result_doc) & set(doc_articles)
            equalResults = len(articles_first_result_doc) == len(doc_articles) and len(intersec) == len(articles_first_result_doc)

            if not equalResults:
                print "Different result at pos: ",i, "\t best ", articles_first_result_doc, "\t ", doc_articles
                print "intersection: ", intersec

                if len(intersec) != 0:
                    articles_saved = intersec
                    print "Reconsidering result to ", intersec

                    if delta_best_FirstPartiallyDifferent is None:
                        delta_best_FirstPartiallyDifferent = first_result_doc_score - doc_score


                elif delta_best_FirstCompletlyDifferent is None:
                    delta_best_FirstCompletlyDifferent = first_result_doc_score - doc_score
            else:
                print "similar results"

        print "Article first doc: ",articles_first_result_doc
        print "Article saved: ", articles_saved
        print "Delta: ", delta_best_FirstCompletlyDifferent


    if THRESHOLD_TERRIER_SCORE == -1 or doc_score > THRESHOLD_TERRIER_SCORE:

        if THRESHOLD_DELTA_TERRIER_SCORE == -1:
            terrier_results_final_articles[query_id].extend(list(articles_first_result_doc))
        elif delta_best_FirstPartiallyDifferent >= THRESHOLD_DELTA_TERRIER_SCORE:
            terrier_results_final_articles[query_id].extend(list(articles_first_result_doc))
        elif delta_best_FirstCompletlyDifferent >= THRESHOLD_DELTA_TERRIER_SCORE:
            terrier_results_final_articles[query_id].extend(list(articles_saved))
        else:
            print "excluding result " + doc_id + " because of THRESHOLD_DELTA_TERRIER_SCORE"

    else:
        print "excluding result " + doc_id + " because of TERRIER THRESHOLD"

## enregistre les résultats dans un fichier resultats au format de COLIEE
printPredictions(terrier_results_final_articles, 'tmp/Testdata.task1.KID17', 'KID17')


'''
if len(articles_first_result_doc) != 1:
    quit()
'''

# print k, terrier_results_bestk[k], terrier_results_final_articles[k]



'''
print "Expected results"

for r in expected_results:
	print r, expected_results[r], terrier_results_final_articles[r]
#'''

index_file_path_tsv = "tmp/index.tsv"

query_lem_path = "tmp/requetes_lem.tsv"
query_path = "tmp/requetes.tsv"

# Loading index

index_doc = {}
query = {}
query_lem = {}

for l in open(index_file_path_tsv):
    data = l.strip().split("\t")
    index_doc[data[0]] = " ".join(data[1:])

for l in open(query_path):
    data = l.strip().split("\t")
    query[data[0]] = " ".join(data[1:])

for l in open(query_lem_path):
    data = l.strip().split("\t")
    query_lem[data[0]] = " ".join(data[1:])

log_path = "tmp/results.log"
log_file = open(log_path, 'w')

for query_id in expected_results:

    query_expected_articles_ids = expected_results[query_id]
    query_provided_articles_ids = terrier_results_final_articles[query_id]

    # count the number of expected result in the result set provided
    log_string_header = ""
    count_found = 0
    for expected_article_id in query_expected_articles_ids:

        log_string_header += " " + expected_article_id
        # get id of expected article in resultset
        id_expected_result_in_retrieved = query_provided_articles_ids.index(
            expected_article_id) if expected_article_id in query_provided_articles_ids else -1
        if id_expected_result_in_retrieved != -1:
            count_found += 1
            log_string_header += " rank: " + str(id_expected_result_in_retrieved + 1) + "/" + str(NB_RESULTS_FINAL)
        else:
            log_string_header += " not returned "

    print query_id, query_expected_articles_ids, query_provided_articles_ids, count_found, "/", len(
        query_expected_articles_ids)

    log_file.write("---------------------------------------------------\n")
    log_file.write("---------------------------------------------------\n")
    log_file.write(query_id + " | found: " + str(count_found) + "/" + str(
        len(query_expected_articles_ids)) + "\ndetails: " + log_string_header + "\n")
    log_file.write("---------------------------------------------------\n")
    log_file.write("---------------------------------------------------\n")
    log_file.write("QUERY              : " + query[query_id] + "\n\n")
    log_file.write("QUERY: INDEXED FORM: " + query_lem[query_id] + "\n")
    log_file.write("---------------------------------------------------\n")

    for a_id in query_expected_articles_ids:
        log_file.write("EXPECTED RESULT: " + str(a_id) + "\n")
        log_file.write("EXPECTED RESULT: INDEXED FORM: " + #index_doc["ARTICLE_" + str(a_id)] + 
                       "\n")
        log_file.write("---------------------------------------------------\n")

    for i in range(0, len(terrier_results_bestk[query_id].items)):
        log_file.write(
            "DOC PROVIDED RESULT " + str(i + 1) + " ID : " + terrier_results_bestk[query_id].items[i] + " score " + str(
                terrier_results_bestk[query_id].itemScores[i]) + "\n")
        log_file.write("INDEXED FORM: " + #index_doc[terrier_results_bestk[query_id].items[i]] + 
                       "\n")
        log_file.write("---------------------------------------------------\n")

log_file.close()

#  EVALUATION.
print "NB_RESULTS_FINAL", NB_RESULTS_FINAL
print "THRESHOLD_TERRIER_SCORE ", THRESHOLD_TERRIER_SCORE
print "THRESHOLD_DELTA_TERRIER_SCORE ", THRESHOLD_DELTA_TERRIER_SCORE
res_eval = bao.Evaluation(expected_results, terrier_results_final_articles)
res_eval.scores()
