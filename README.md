# 16S_Tools
Tools to process files related to 16S amplicon sequencing data.
## custom categorize_by_function.py
This script is intended to categorize PICRUSt1 output KO abundance tab-separated values file by function. It can handle PICRUSt1 tab-separated values file rather than biom file, and also [PICRUSt2](https://github.com/picrust/picrust2) output tab-separated values file (pred_metagenome_unstrat.tsv), although run_minpath.py is available. Only KO categorizing are supported.

First you should make tab-separated mapping file from ko_13_5_precalculated.tab.gz in PICRUSt1, where column named “KO”, “KEGG_Description”, “KEGG_Pathways” each correspond to first line, second last line, last line of the file.

`usage: python cbf.py –d 1 –l 3 –m map.tab –i inputfile.tab –o outputfile.tab`

-d if PICRUSt1 tabular output file, then specify 1, and if PICRUSt2, 2. This is to drop “KEGG_Pathways” column contained in PICRUSt1 tabular output.  
-l level [1,2,3]  
-m mapping file with column names [“KO”,”KEGG_Description”,”KEGG_Pathways”]  
-i input tab-separated values file  
-o output tab-separated values file  

- NOTE1: Some of KO from PICRUSt2 output would be filtered as they are not listed in PICRUSt1 pre-calculated file.
- NOTE2: The result of categorizing to level 3 by categorize_by_function.py (input is PICRUSt1 predict_metagenomes.py BIOM) and categorizing to level 3 by this script (input is the tsv converted by biom-format from the same BIOM file) were compared, and pearson correlation coefficient was all 1.0 except all-zero pathways.
