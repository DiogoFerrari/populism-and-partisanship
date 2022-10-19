# Replication files 

This repository contains replication files for the article:

	- Ferrari, D. (2022). The Effect of Party Identification and Party Cues on Populist Attitudes. Research and Politics (provisionally accepted).

# Citation

```latex
@article{ferrari2022effect,
    author = {Ferrari, Diogo},
    title = {The Effect of Party Identification and Party Cues on Populist Attitudes},
    year={2022},
    journal = {Research and Politics (provisionally accepted)},
    url = {},
}
```

# This repository contains

1. Tables and figures in separate .tex and .pdf files
2. The scripts used to generate the analysis, tables, and figures
3. Data set(s) used in the analyses

# Pre-analysis plan

Available [here](https://osf.io/79w5k/?view_only=25f37005f7d7418c9c9695e25c53a6c6)

# Instructions for replication

For replication, make sure you have the following folder structure in place
```ascii
.
├── data
│   └── final                        <- folder with data used in the analysis
├── man                              <- folder with the manuscript (limited if copyright applies)
│   ├── figures-and-tables           <- tables and figures (in .pdf, .png. etc) used in the manuscript
│   └── supplementary-material       <- supplementatry material (SM)
│       └── figures-and-tables       <- tables and figures (in .pdf, .png. etc) used in the SM
├── src                              <- scripts for replication
│   └── model                        <- folder with the scripts that contain the analyses
└── README.md                        <- the file you are reading now
```


## Replication

- Note the steps below were tested on Linux.

### Cloning from github

1. Clone the repository:
``` shell
$ git close https://github.com/DiogoFerrari/populism-and-partisanship.git
```
2. Run the scripts in the folder `model`

### Downloading from other repositories (e.g., Dataverse)

1. Create the folder structure above, if needed
2. Put the scripts in the folder `model`, 
   - For scripts following this pattern in their name `__<filname>__`, leave them at the `src` folder
3. Run the scripts in the folder `model`


## Note

- The raw data (simulated or not) was recoded using the file `./src/data-organizing/recodings.py` (not provided)

