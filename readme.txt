

format du corpus indexé par terrier

<DOC>
<DOCNO>III-4-performance_of_obligations_of_others-707-2</DOCNO>
the provisions of the preceding paragraph shall not preclude the person who performed an obligation from exercising hisher right of subrogation against the obligor.
</DOC>


script d'execution de terrier terrier.sh cf root
    traitements réalisés par le script terrier.sh 
        rm -r terrier-core-4.2/var/index/* (suppression de l'index existant) 
        + execution de l'ensemble des requetes
        
dossier résultat par défaut terrier-core-4.2/var/results/


score.py

conf_results tableau associatif clé: id query, value set expected article id
results_terrier tableau associatif clé: id query, value set returned article id

# EVALUATION.
res_eval = bao.Evaluation(conf_results, results_terrier)
res_eval.scores()
