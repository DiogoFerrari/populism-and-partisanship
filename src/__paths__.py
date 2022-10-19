from pathlib import Path
import os

print(f"Loading paths...", flush=True)

ROOT                            = Path(os.path.abspath(os.curdir))
ROOT                            = ROOT.parent.parent

# data
PATH_DATA_FINAL                 = ROOT / "data" / "final"
PATH_DATA_RAW                   = ROOT / "data" / "raw"
PATH_DATA_INTERIM               = ROOT / "data" / "interim"
# scripts
PATH_SRC                        = ROOT / "src"
PATH_SRC_DATA_ORGANIZING        = PATH_SRC / "data-organizing"
PATH_SRC_DATA_COLLECTING        = PATH_SRC / "data-collecting"
PATH_SRC_DATA_MODEL             = PATH_SRC / "model"
PATH_SRC_DATA_EDA               = PATH_SRC / "eda"
# manuscript
PATH_MANUSCRIPT                 = ROOT / "man"
PATH_MANUSCRIPT_FIGURES         = PATH_MANUSCRIPT / 'tables-and-figures'
PATH_MANUSCRIPT_TABLES          = PATH_MANUSCRIPT / 'tables-and-figures'
# supplementary material
PATH_MANUSCRIPT_SUP_MAT         = PATH_MANUSCRIPT / 'supp-material'
PATH_MANUSCRIPT_SUP_MAT_FIGURES = PATH_MANUSCRIPT_SUP_MAT / 'tables-and-figures'
PATH_MANUSCRIPT_SUP_MAT_TABLES  = PATH_MANUSCRIPT_SUP_MAT / 'tables-and-figures'
# output
PATH_OUTPUTS                    = ROOT / 'out'
# reports and docs
PATH_REPORTS                    = ROOT / 'rep'
PATH_DOCS                       = ROOT / 'docs'
# PRR
PATH_PRR                        = PATH_DOCS / "prr"
PATH_PRR_FIGURES                = PATH_DOCS / "prr" / "tables-and-figures"
PATH_PRR_TABLES                 = PATH_DOCS / "prr" / "tables-and-figures"
# PAP 
PATH_PAP                        = PATH_DOCS / "pap"
PATH_PAP_FIGURES                = PATH_DOCS / "pap" / "tables-and-figures"
PATH_PAP_TABLES                 = PATH_DOCS / "pap" / "tables-and-figures"
