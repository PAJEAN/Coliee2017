#!/usr/bin/python

import boite_a_outils as tbx

bm25results = "terrier-core-4.2/var/results/BM25b0.75_articles.res"
colieeResults = "Data/Index/id_query-num_articles.tsv"

terrier_results = tbx.TSV_parser(bm25results)
terrier_results.load_outs_terrier()


coliee_results = tbx.TSV_parser(colieeResults)
coliee_results.load_outs_sep(";")

distrib = {}
count_articles = 0

distrib_best_article_query = {}

distrib_nb_articles_per_queries = {}


for entry in coliee_results.outs:
    print entry
    
    best_rank_article = None
    
    for article_id in coliee_results.outs[entry]:
        
        
        rank_terrier = "no_result"
        
        for i in range(0,len(terrier_results.outs[entry])):
            article_2_info=terrier_results.outs[entry][i]
            
            if article_2_info[0] == article_id:
                rank_terrier = i
                break
                
        if not rank_terrier in distrib:
            distrib[rank_terrier] = 1
        else : distrib[rank_terrier] +=1
        
        count_articles+=1
        
        if best_rank_article == None or (rank_terrier != "no_result" and best_rank_article > rank_terrier) :
            best_rank_article = rank_terrier
            
        
        print "\t",article_id, " (",str(rank_terrier),") "

    if not best_rank_article in distrib_best_article_query:
        distrib_best_article_query[best_rank_article] = 1
    else : distrib_best_article_query[best_rank_article] +=1
    
    if not len(coliee_results.outs[entry]) in distrib_nb_articles_per_queries:
        distrib_nb_articles_per_queries[len(coliee_results.outs[entry])] = 1
    else : distrib_nb_articles_per_queries[len(coliee_results.outs[entry])] +=1


print "distribution of ranks of expected articles"
per_cum = 0
for k in sorted(distrib):
    per = (distrib[k] * 100 / float(count_articles));
    per_cum += per
    print k, "\t", distrib[k], "\t", per, "%  -> ", per_cum, "%"


print "---------------------"
print "k  : percentage of queries having an expected article having a terrier best rank equal to k"

per_cum = 0
for k in sorted(distrib_best_article_query):
    per = (distrib_best_article_query[k] * 100 / float(len(coliee_results.outs)));
    per_cum += per
    print k, "\t", distrib_best_article_query[k], "\t", per, "%  -> ", per_cum, "%"
    
print "---------------------"
print "distribution of number of expected articles for each query"

per_cum = 0
for k in sorted(distrib_nb_articles_per_queries):
    
    per = (distrib_nb_articles_per_queries[k] * 100 / float(len(coliee_results.outs)));
    per_cum += per
    print k, "\t", distrib_nb_articles_per_queries[k], "\t", per, "%  -> ", per_cum, "%"
