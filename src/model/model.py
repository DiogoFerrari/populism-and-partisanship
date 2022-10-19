import sys
sys.path.append("..")
from __paths__ import *
from __constants__ import *
from __functions__ import *

SAVE = False
SAVE = True

# * Loading data

fn = PATH_DATA_FINAL / 'survey.csv'
df = ds.read_data(fn=fn)

# * Descriptive statistics
# ** Figure 1: Support for Populist Rherotic by treatment and party id

tab=(
    df
    .freq(vars='y', condition_on=['ptyid', f'cue', f'cueg'])
    .mutate_rowwise({'nlabel': lambda x: f"n={x['n']}"})
    .select_rows(query=f"ptyid!='Independent'")
    .select_rows(query=f"y==1")
    .mutate_categorical(var=f'cueg', cats=['Control', 'Biden', 'Trump'],
                        ordered=True)
)
tab.print()


# Plot 
# ----
x=f'cueg'
y='freq'
color='ptyid'
xlab='Message Supporter (Partisan Treatment Cue)'
ylab='Proportion of Voters in Favor of\nPopulist or Anti-populist Messages'
title='Proportion of Voters in Favor of Populist and Anti-populist Positions'
subtitle="(Bars represent the proportion standard errors)"
dodge=1
facet=f'cue'
legtitle="Voter's Party Identification"
alpha=.7
alpha=.6
g = (
    gg.ggplot(tab)
    + gg.geom_bar(gg.aes_string(x = x, y=y, fill=color),
                  position = 'dodge', stat="identity", colour='white', alpha=alpha)
    + gg.geom_text(gg.aes_string(x=x, y=y, label="nlabel", group=color),
                   vjust=-.5, position=gg.position_dodge(dodge), size=3 )
    + gg.geom_errorbar(gg.aes_string(x=x, ymin='lo', ymax='hi', color=color),
                       width=.3, position=gg.position_dodge(dodge))
    + gg.scale_y_continuous(expand = FloatVector([0, 0]),
                            limits=FloatVector([0, 110]))
    + gg.theme_bw()
    + ggtheme()
    + ggguides(ncol=3)
    + gg.facet_wrap(f"~ {facet}" , ncol=2,
                    scales=robj.NULL, labeller="label_value",
                    dir="h", as_table=True) 
    + gg.labs(
        x        = xlab,
        y        = ylab,
        color    = legtitle, 
        fill     = legtitle,
    	linetype = robj.NULL,
    	shape    = robj.NULL,
        )
    # 
    # 
    + gg.scale_colour_manual(values = ru.dict2namedvector({"Democrat" : 'blue',
                                                           'Republican':'red'})) 
    + gg.scale_fill_manual(values = ru.dict2namedvector({"Democrat" : 'blue',
                                                         'Republican':'red'})) 
    # + gg.scale_fill_grey(start = 0.1, end = .75,  na_value="red") 
    # + gg.scale_color_grey(start = 0.1, end = .75,  na_value="red") 
)
g.plot()
if SAVE:
    # fns = [PATH_MANUSCRIPT_FIGURES  / f'fig-proportions.png',
    #        PATH_MANUSCRIPT_FIGURES  / f'fig-proportions.pdf']
    fns = [PATH_MANUSCRIPT_FIGURES  / f'figure-1.png',
           PATH_MANUSCRIPT_FIGURES  / f'figure-1.pdf']
    [g.save(filename=str(fn), width=7, height=4) for fn in fns]

# * Models
# ** Figure 2: Causal Effect on Msg Support

# Estimation 
# ----------
cues   = ["Populist Message", 'Anti-populist Message']
ptyids = ['Democrat', 'Republican']
mod    = dm.regression()
for cue, ptyid, controls in it.product(cues, ptyids, [False, True]):
    label, vars, tab = get_data(df, cue, ptyid, controls)
    mod.add_models(models={label: (vars, 'binomial', tab)})
# 
# Summary 
# -------
mod.summary()
# Effect (odds ratio)
mod.get_odds(models='Pop-Dem').print()
mod.get_odds(models='APop-Dem').print()
mod.get_odds(models='Pop-Rep').print()
mod.get_odds(models='APop-Rep').print()
# predicted probability
mod.predict('APop-Dem', predictor='cueg').print()
mod.predict('APop-Rep', predictor='cueg').print()
# 
# Plot 
# ----
g=mod.plot_coef(
    regex="^(?!.*with controls).*",
    text={'vjust':.5, 'hjust':-.25, 'size':3.5},
    facet={'Anti-populist Message': ['APop-Dem', 'APop-Rep'],
           'Populist Message'     : ['Pop-Dem' , 'Pop-Rep']},
    color={'Democrat'   : ['APop-Dem', 'Pop-Dem'],
           'Republican' : ['APop-Rep', 'Pop-Rep']},
    color_manual={"Democrat" : 'blue',
                  'Republican':'red'},
    # color_grey=True,
    switch_axes=True,
    leg_title="Voter's Party Identification",
    leg_ncol=2, 
    # title=title, subtitle=subtitle,
    # facet_scales='free',
    ylab=("Average Causal Effect of Partisan Cue<br> "+\
          "on Voter's Support for the Message"),
    xlab='Message Supporter (Partisan Treatment Cue)'
)
g.plot()
# 
# Saving 
# ------
if SAVE:
    # Plot 
    # ----
    fns = [PATH_MANUSCRIPT_FIGURES  / f'figure-2.png',
           PATH_MANUSCRIPT_FIGURES  / f'figure-2.pdf']
    [g.save(filename=str(fn), width=6.5, height=4) for fn in fns]
    # ----------------
    # Regression table (sup material)
    # ----------------
    for pty in ['Dem', 'Rep']:
        mods=[f'Pop-{pty}' , f'Pop-{pty} (with controls)',
              f'APop-{pty}', f'APop-{pty} (with controls)']
        # 
        ptylabel='Democrat' if pty=='Dem' else 'Republican'
        label=f'tab-reg-{pty.lower()}.tex'
        fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / label
        mod.summary(
            models=mods,
            fn=fn,
            align='lC{2.7cm}C{2.7cm}C{2.7cm}C{2.7cm}',
            replace={'term': {"`":'', 'cueg':'Cue: '}},
            caption=('Logistic regression of support for the populist (Pop) and '+\
                     f'anti-populist (APop) messages on partisan cue '+\
                     f'among {ptylabel} ({pty}) voters. '
                     'Numbers in parentheses are 95\% confidence intervals.'
                     ),
            label=label)



# ** Figure 3: Causal Effect on Msg Support (strong partisans)

# Estimation 
# ----------
cues = ["Populist Message", 'Anti-populist Message']
mod  = dm.regression()
for cue,  controls in it.product(cues, [False, True]):
    label, vars, tab = get_data_pred(df, cue,  controls)
    mod.add_models(models={label: (vars, 'binomial', tab)})
mod.summary()


# Plot 
# ----
g=mod.plot_predict(predictor=COVARS_PRED['ptyid7'],
                   predictor_values=list(np.linspace(-3.5, 3.5, 8)),
                   covars_at={'cueg':['Trump', 'Biden', ' Control']},
                   regex='^(?!.*controls).*',
                   facet='model_id',
                   color='cueg',
                   # color_grey=True,
                   color_manual={' Control': 'black',
                                 "Biden"  : 'blue',
                                 'Trump'  : 'red',},
                   linetype='cueg',
                   xlab="Voters' Party Identification",
                   ylab='Predicted Probability of<br>Supporting the Message',
                   leg_title='Treatment Group (Partisan Cue)',
                   leg_title_linetype='Treatment Group (Partisan Cue)',
                   leg_ncol=3,
                   facet_scales='free'
                   )
g = axis_relabel(g)
g.plot()

# Saving 
# ------
if SAVE:
    # Plot 
    # ----
    fns = [PATH_MANUSCRIPT_FIGURES  / f'figure-3.png',
           PATH_MANUSCRIPT_FIGURES  / f'figure-3.pdf']
    [g.save(filename=str(fn), width=8, height=4) for fn in fns]
    # Regression table 
    # ----------------
    fn = 'tab-estimation-strong-partisans.tex'
    mod.summary(fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / fn,
                caption=('Logistic regression of support for populist and '+\
                         'anti-populist messages on partisan cue. '+\
                         'Number in parentheses are 95\% '+\
                         'confidence intervals. Party identification (Pty Id.) range ' +\
                         "from -3 (strong Democrat) to 3 (Strong Republican)."),
                label=fn,
                align='lC{3cm}C{3cm}C{3cm}C{3cm}',
                replace={'term':{'`':'', 'cueg':'',
                                 'Party identification \(with leaners\)': 'Pty Id.'}})

# ** Figure 4: Causal Effect on Populist Attitudes


# Estimation 
# ----------
cues   = ["Populist Message", 'Anti-populist Message']
ptyids = ['Democrat', 'Republican']
mod    = dm.regression()
y = 'popmin'
for cue, ptyid, controls in it.product(cues, ptyids, [False, True]):
    label, vars, tab = get_data(df, cue, ptyid, controls, y)
    mod.add_models(models={label: (vars, 'gaussian', tab)})
mod.summary()
# 
# Plot 
# ----
g=mod.plot_coef(regex='^(?!.*controls).*',
                text={'vjust':.5, 'hjust':-.25},
                # text_leg=None,
                digits=3,
                # coefs=coefs,
                facet={'Anti-populist Message': ['APop-Dem', 'APop-Rep'],
                       'Populist Message'     : ['Pop-Dem' , 'Pop-Rep']},
                color={'Democrat'   : ['APop-Dem', 'Pop-Dem'],
                       'Republican' : ['APop-Rep', 'Pop-Rep']},
                # color_grey=True,
                color_manual={"Democrat" : 'blue',
                              'Republican':'red'},
                switch_axes=True,
                # labels
                leg_title="Voter's Party Identification",
                leg_ncol=2, 
                ylab=("Average Causal Effect of Partisan Cue<br> "+\
                      "on Voter's Populist Attitudes"),
                xlab='Message Supporter (Partisan Treatment Cue)')
g.plot()
# 
# 
# Saving results 
# --------------
if SAVE:
    # Plot 
    # ----
    fns = [PATH_MANUSCRIPT_FIGURES  / f'figure-4.png',
           PATH_MANUSCRIPT_FIGURES  / f'figure-4.pdf']
    [g.save(filename=str(fn), width=8, height=4) for fn in fns]
    #
    # Regression table 
    # ----------------
    for pty in ['Dem', 'Rep']:
        mods=[f'Pop-{pty}' , f'Pop-{pty} (with controls)',
              f'APop-{pty}', f'APop-{pty} (with controls)']
        # 
        ptylabel='Democrat' if pty=='Dem' else 'Republican'
        label=f'tab-reg-{pty.lower()}-popmin.tex'
        mod.summary(
            models=mods,
            fn=PATH_MANUSCRIPT_SUP_MAT_TABLES / label,
            caption=('Linear regression of populist attitudes (minimal index) on '+\
                     'partisan cue for populist (Pop) and anti-populist (APop) '+\
                     f'messages among {ptylabel} ({pty}) voters. '
                     'Number in parentheses are 95\% '+\
                     'confidence intervals.'),
            label=label,
            align='lC{3cm}C{3cm}C{3cm}C{3cm}',
            replace={'term':{'`':'', 'cueg':'Cue: ',}})

print('Done!')

