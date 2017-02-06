#!/bin/bash

rm terrier-core-4.2/var/index/*
bash terrier-core-4.2/bin/trec_setup.sh /media/pierre-antoine/Data/Code_civil/Data/Indexation/Articles/
#bash terrier-core-4.2/bin/trec_setup.sh /media/pierre-antoine/Data/Code_civil/Data/Indexation/Chapitres/
#bash terrier-core-4.2/bin/trec_setup.sh /media/pierre-antoine/Data/Code_civil/Data/Indexation/Sections/
#bash terrier-core-4.2/bin/trec_setup.sh /media/pierre-antoine/Data/Code_civil/Data/Indexation/Paragraphs/

bash terrier-core-4.2/bin/trec_terrier.sh -i
bash terrier-core-4.2/bin/trec_terrier.sh -r -Dtrec.topics=/media/pierre-antoine/Data/Code_civil/Data/requetes.xml -Dtrec.model=BM25
bash terrier-core-4.2/bin/trec_terrier.sh --printstats
