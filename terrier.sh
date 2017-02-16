#!/bin/bash

rm terrier-core-4.2/var/index/*
rm terrier-core-4.2/var/results/*

bash terrier-core-4.2/bin/trec_setup.sh tmp/index/

bash terrier-core-4.2/bin/trec_terrier.sh -i -Dindexer.meta.forward.keylens=50
bash terrier-core-4.2/bin/trec_terrier.sh -r -Dtrec.topics=Data/requetes.xml -Dtrec.model=BM25 -c 1
bash terrier-core-4.2/bin/trec_terrier.sh --printstats

cp -r terrier-core-4.2/var/results/ tmp/terrier_results

