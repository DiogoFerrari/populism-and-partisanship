import sys
sys.path.append("..")
from __paths__ import *
from __constants__ import *
from __functions__ import *

SAVE = False
SAVE = True

# * Loading data

fn = PATH_DATA_FINAL / 'survey-sm.csv'
df = ds.read_data(fn=fn)
# fn = PATH_DATA_INTERIM / 'survey-lucid-wide.csv'
# dfr = ds.read_data(fn=fn)

# * Demographics
# *** Gender

tab=(
    df
    .freq(vars='gender', groups=None, include_na=True)
    .select_cols(names=COVARS_RAW | {'n':'Sample Size', 'freq':'Freq (Survey)'})
)
tab.print()
# 
if SAVE:
    fn="tab-01-gender.tex"
    tab.tolatex(fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / fn,
                caption='Gender Groups in the Survey',
                label=fn)

# *** Age

var, sheet ='age', 'age-census'
tab=census_compare(df, var, sheet, PATH_DATA_FINAL)
tab.print()
# 
if SAVE:
    fn="tab-02-census-age.tex"
    tab.tolatex(fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / fn,
                caption='Age Groups in the Survey vs. the US Census',
                label=fn)


# *** Education 


var, sheet ='educ_cat', 'educ-census'
tab=census_compare(df, var, sheet, PATH_DATA_FINAL)
tab.print()
# 
if SAVE:
    fn="tab-03-census-educ.tex"
    tab.tolatex(fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / fn,
                caption='Education Groups in the Survey vs. the US Census',
                label=fn,
                align='p{7cm}ccc')



# *** Race

var, sheet ='race', 'race-census'
tab=census_compare(df, var, sheet, PATH_DATA_FINAL)
# 
tab.print()
if SAVE:
    fn="tab-04-census-race.tex"
    tab.tolatex(fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / fn,
                caption='Race Groups in the Survey vs. the US Census',
                label=fn,
                align='lccc')

# *** Income

var, sheet ='inc', 'inc-census'
tab=census_compare(df.replace({'inc':{' - ': ' to '}} , regex=True, inplace=False),
                   var, sheet, PATH_DATA_FINAL)
tab.print()
# 
if SAVE:
    fn="tab-05-census-inc.tex"
    tab.tolatex(fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / fn,
                caption='Income Groups in the Survey vs. the US Census',
                label=fn,
                align='lccc')

# * Pre-treatment Covariates 

tab=df.summary(COVARS_PRED)
tab.print()
if SAVE:
    fn='tab-covar-summary.tex'
    tab.tolatex(fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / fn,
                escape=True, align='p{3cm}cccccccc',
                caption='Summary statistics for the pre-treatment variables',
                label=fn
                )


# * Balance on Observables

COVARS
covars = COVARS.copy()
del covars['ptyid7']
# 
tab=ds.eDataFrame()
for cue in df.cue.unique():
    for cueg in ['Biden', 'Trump']:
        print(f"Checking balance for {cue} for {cueg}...")
        try:
            tabt=(
                df
                .select_rows(query=f"cue=='{cue}'")
                .select_rows(regex={'cueg':f"Control|{cueg}"})
                .mutate_case({
                    'Partisan Cue': {
                        f"(cueg=='Control') ": 0,
                        True:1
     	            }
                })
                # Balance
                .balance(covars, 'Partisan Cue')
                .mutate({'Message': cue,
                         'Cue'    : cueg})
            )
        except (OSError, IOError, BaseException, RuntimeError) as e:
            print("Balance not computed...")
        tab=tab.bind_row(tabt)
# 
# 
# 
x = "Std_Mean_Diff"
y = "variable"
color='Cue'
shape='Message'
title='Balance of Pre-Treatment Variables for Each Treatment Group'
subtitle=(f"Reference group: Control (no partisan cue) for each respective message")
tabt=(
    tab
    .rename_cols(regex={"\ ": '_'}, tolower=False)
    .select_cols(names=[x, y, color, shape])
    .mutate({x: lambda col: col[x].abs()})
    .drop_rows(dropna=True)
)
# 
g = (
    gg.ggplot(tabt, gg.aes_string(x=x, y=y, colour=color, shape=shape))
    + gg.geom_point(size=3, alpha=.4, position="identity") 
    + gg.geom_vline(gg.aes_string(xintercept=.1), linetype="dashed", col="red")
    + gg.scale_colour_grey(start=0, end=.6, na_value="red") 
    + gg.labs(x        = 'Absolute Standardized Mean Difference',
              y        = robj.NULL,
              title    = title,
              subtitle = subtitle)
    + gg.xlim(0, .5)
    + gg.theme_bw()
    + ggtheme()
    + ggguides()
    + gg. theme(legend_box = "horizontal",)
    + gg.guides(
        colour = gg.guide_legend(title_position = "top", ncol=2, size=8, title_hjust=0),
        fill   = gg.guide_legend(title_position = "top", ncol=2, size=8, title_hjust=0),
        shape  = gg.guide_legend(title_position = "top", ncol=2, size=8, title_hjust=0))
)
g.plot()
if SAVE:
    fns = [PATH_MANUSCRIPT_SUP_MAT_FIGURES  / f'fig-balance.png',
           PATH_MANUSCRIPT_SUP_MAT_FIGURES  / f'fig-balance.pdf']
    [g.save(filename=str(fn), width=8, height=4) for fn in fns]
    # for grid_arrange
    # [robj.lib.ggplot2.ggplot2.ggsave(filename=str(fn), width=8, height=4,
    #                                  plot=g) for fn in fns]





# * Populist Attitudes

# Note: PCA plots were created during the recoding

tab=(
    df
    .select_cols(names={'popmin':'Minimal Scale',
                        'popmul':'Multiplicative scale',
                        'popadd':'Additive scale',
                        })
    .drop_cols(regex='_sc')
    .select_cols(type='numeric')
)
tab
g=ggp.ggpairs(tab)
print(g)
if SAVE:
    fns = [PATH_MANUSCRIPT_SUP_MAT_FIGURES  / f'fig-pop-att-scales.png',
           PATH_MANUSCRIPT_SUP_MAT_FIGURES  / f'fig-pop-att-scales.pdf']
    # [g.save(filename=str(fn), width=8, height=4) for fn in fns]
    # for grid_arrange
    [robj.lib.ggplot2.ggplot2.ggsave(filename=str(fn), width=8, height=4,
                                     plot=g) for fn in fns]


# * Robustness


# Estimation 
# ----------
cues   = ["Populist Message", 'Anti-populist Message']
ptyids = ['Democrat', 'Republican']
mod    = dm.regression()
for y in ['popadd', 'popmul']:
    print(f"Dep. var: {y}")
    for cue, ptyid, controls in it.product(cues, ptyids, [False, True]):
        label, vars, tab = get_data(df, cue, ptyid, controls, y)
        mod.add_models(models={label: (vars, 'gaussian', tab)})
    # 
    if SAVE:
        # Regression table 
        # ----------------
        for pty in ['Dem', 'Rep']:
            mods=['term',
                  f'Pop-{pty}' ,
                  f'Pop-{pty} (with controls)',
                  f'APop-{pty}',
                  f'APop-{pty} (with controls)']
            # 
            ptylabel='Democrat' if pty=='Dem' else 'Republican'
            index='multiplicative' if y=='popmul' else 'additive'
            caption=(f'Linear regression of populist attitudes ({index} index) on '+\
                     'partisan cue for populist (Pop) and anti-populist (APop) '+\
                     f'messages among {ptylabel} ({pty}) voters. '
                     'Number in parentheses are 95\% '+\
                     'confidence intervals.')
            # 
            label=f'tab-reg-{pty.lower()}-{y}.tex'
            mod.summary(
                models=mods,
                fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / label,
                caption=caption,
                label=label,
                align='lC{3cm}C{3cm}C{3cm}C{3cm}',
                replace={'term':{'`':'', 'cueg':'Cue: ',}})


print("Done!")
