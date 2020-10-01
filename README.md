# parse_kraken2_report
Taxonomically informed parsing of kraken2 report output.

## Motivation

I find simple parsing of kraken2 output report can be a bit annoying. If you 
parse only using the percentage/number of reads assigned, then you end up
not only with `Salmonella enterica` but also everything between `Salmonella enterica`
and `root`. If you filter to only include species or genus, then you could end up 
missing something significant at a higher level.

This script will read in a kraken2 report, establish the taxonomic relationships 
between the results, and then print out as many or as few taxonomic levels as 
you like, starting from the "tips". 

## Note

2020-10-01 This software is fresh out of the box. Please sanity check results and report
any bugs. 

## Arguments

```
required named arguments:
  -i INHANDLE           Path to kraken report file (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -n SAMPLE_NAME        Sample name to be included in output. If not give,
                        will take everything before the first period of the
                        file name. (default: None)
  -l NUMBER_OF_LEVELS   How far up from each tip do you want to check? If not
                        working as expected, you may ned to alter -r as well.
                        (default: 2)
  -p PERCENT_READS_ASSIGNED_THRESHOLD
                        Minimum threshold of percent_reads_assigned for
                        reporting (default: 0.05)
  -r TAXONOMIC_RANKS    Taxonomic ranks which you want to report given in
                        comma-separated, upper-case format, no spaces. Rank
                        codes should reflect Kraken2 output documented here ht
                        tps://github.com/DerrickWood/kraken2/wiki/Manual#sampl
                        e-report-output-format. Don't include number
                        indicating sub-ranks. If not working as expected, you
                        may need to alter -l as well. (default: S,G)
  -t                    Include this option if you want to print the tree
                        (default: False)
```

## Usage examples

Defaults:

`python kraken2_scripts/parse_kraken2_report.py -i example.kraken_report.txt -n sample1`

Report species, genus and family (note the -l is set to 3 as well).

`python kraken2_scripts/parse_kraken2_report.py -i example.kraken_report.txt -l 3 -r S,G,F`

This is quite a good option (considering switching the default), print all the "tips" which meet the
percentage of reads mapped criteria.

`parse_kraken2_report.py -l 1 -r S,G,F,O,C,P,K,D -i example.kraken_report.txt`

## Dependencies

Uses the python package `anytree` which can be installed from pip. Developed using anytree v2.8.0.
