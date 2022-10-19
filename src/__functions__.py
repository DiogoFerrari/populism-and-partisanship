
print(f"Loading function...", flush=True)

# * Modules
# ** Modules

from __constants__ import *
import pandas as pd 
from pandasci import ds
from pandasci import models as dm
from pandasci import rutils
import itertools as it
import numpy as np
ru = rutils.rutils()

# ** R packages

import rpy2.robjects as robj
import rpy2.rlike.container as rlc
import rpy2.robjects.lib.ggplot2 as gg
from rpy2.robjects import r, FloatVector, pandas2ri, StrVector
from rpy2.robjects.packages import importr
from rpy2.robjects.packages import data as datar
from rpy2.interactive import process_revents # to refresh graphical device
try:
    process_revents.start()                      # to refresh graphical device
except (OSError, IOError, BaseException) as e:
    pass
# 
ggtxt = importr("ggtext")
ggp=importr("GGally")

# * Functions
# ** Ancillary

def census_compare(df, var, sheet, path_census):
    fn = path_census / 'census.xlsx'
    census = ds.read_data(fn=fn, sheet_name=sheet)
    tab=(
        df
        .freq(vars=var)
        .rename_cols(columns={'freq':'Freq (Survey)',
                              'n':'Sample Size'
                              }, tolower=False)
        .join(census
              .mutate({'freq': lambda col: col['freq']*100})
              .select_cols(names=['label', 'freq'])
              .rename_cols(columns={'freq':'Freq (Census)',
                                    'label':var}, tolower=False)
              , how='left', on=[var])
        .drop_cols(names=['stdev', 'lo', 'hi'])
        .rename_cols(columns=COVARS_RAW, tolower=False)
        .rename_cols(columns={var:var.title()}, tolower=False)
    )
    return tab

def get_data(df, cue, ptyid, controls, y='y'):
    # label  = f"{ptyid} receiving the {cue.lower()}"
    label_cue='Pop' if cue=="Populist Message" else "APop"
    label_pty='Dem' if ptyid=="Democrat" else "Rep"
    label  = f"{label_cue}-{label_pty}"
    if controls:
        label  += f" (with controls)"
        

    # formula 
    # ---------
    vars_dict={y:y, 'cueg':'cueg'}
    vars = {
        'output' : y,
        'inputs' : ["cueg"]
    }
    if controls:
        vars["inputs"]+=[*COVARS_ATE.values()]
        vars_dict|=COVARS_ATE

    # data 
    # ----
    tab=(
        df
        .select_rows(query=f"ptyid!='Independent'")
        .select_rows(query=f"ptyid=='{ptyid}'")
        .select_rows(query=f"cue=='{cue}'")
        .select_cols(names=vars_dict)
        .drop_rows(dropna=True)
        # .mutate_categorical(var='cueg', cats=['Control', 'Biden', 'Trump'],
        #                     ordered=False, wrap=False)
        .replace({'Control':" Control"} , regex=False, inplace=False)
        .fill_na(value=np.nan , vars=None)
    )
    return label, vars, tab

def get_data_pred(df, cue, controls):
    # label  = f"{ptyid} receiving the {cue.lower()}"
    label  = f"{cue}"
    if controls:
        label  += f" (with controls)"
        

    # formula 
    # ---------
    vars_dict={'y':'y', 'cueg':'cueg', "ptyid7":COVARS_PRED['ptyid7']}
    vars = {
        'output' : 'y',
        'inputs' : ["cueg", COVARS_PRED['ptyid7']],
        'interactions' : [(COVARS_PRED['ptyid7'], 'cueg')]
    }
    if controls:
        vars["inputs"]+=[*COVARS_PRED.values()]
        vars_dict|=COVARS_PRED

    # data 
    # ----
    tab=(
        df
        .select_rows(query=f"cue=='{cue}'")
        .select_cols(names=vars_dict)
        .drop_rows(dropna=True)
        # .mutate_categorical(var='cueg', cats=['Control', 'Biden', 'Trump'],
        #                     ordered=True, wrap=False)
        .replace({'Control':" Control"} , regex=False, inplace=False)
        .fill_na(value=np.nan , vars=None)
    )
    return label,  vars, tab


# ** Plots

def axis_relabel(g, size=7):
    g=(
        g
        + gg.scale_x_continuous(
            breaks=FloatVector([-3, -2, -1, 0, 1, 2, 3]),
            labels=ru.dict2namedvector({
                -3 : f"<span style = 'font-size:{size}pt;text-align:left'>"+\
                "Strong Dem.",
                -2 : "",
                -1 : "",
                0  : f"<span style = 'font-size:{size}pt;text-align:right'>"+\
                "Independent", # 
                2 : "",
                1 : "",
                3 : f"<span style = 'font-size:{size}pt;text-align:right'>"+\
                "Strong Rep.",
            }),
            expand = FloatVector([0, 0])
        )
    )
    return g

def ggtheme():
    g =gg.theme(
             ## ------
             ## legend
             ## ------ 
             legend_position = "top",
             # legend_position = [0.12, .96],
             legend_justification = FloatVector([0, .9]),
             legend_direction='horizontal',
             # legend_direction='horizontal',
             legend_title = gg.element_text( size=11),
             # legend_text  = gg.element_text( size=10),
             # legend_text_legend=element_text(size=10),
             # legend_text_colorbar=None,
             # legend_box=None,
             # legend_box_margin=None,
             # legend_box_just=None,
             # legend_key_width=None,
             # legend_key_height=None,
             # legend_key_size=None,
             # legend_margin=None,
             # legend_box_spacing=None,
             # legend_spacing=None,
             # legend_title_align=None,
             # legend_entry_spacing_x=None,
             # legend_entry_spacing_y=None,
             # legend_entry_spacing=None,
             # legend_key=None,
             # legend_background=None,
             # legend_box_background=None,
             strip_background = gg.element_rect(colour="transparent",
                                                fill='transparent'),
             # strip_placement = "outside",
             strip_text_x        = gg.element_text(size=10, face='bold', hjust=0),
             strip_text_y        = gg.element_text(size=9, face="bold", vjust=0,
                                                   angle=-90),
             ##panel_grid_major  = element_blank(),
             # panel_grid_minor_x  = gg.element_blank(),
             # panel_grid_major_x  = gg.element_blank(),
             # panel_grid_minor_y  = gg.element_blank(),
             # panel_grid_major_y  = gg.element_blank(),
             panel_grid_minor_y  = gg.element_line(colour="grey", size=.3, linetype=3),
             panel_grid_major_y  = gg.element_line(colour="grey", size=.3, linetype=3),
             panel_grid_minor_x  = gg.element_line(colour="grey", size=.3, linetype=3),
             panel_grid_major_x  = gg.element_line(colour="grey", size=.3, linetype=3),
             # border 
             # ------
             panel_border      = gg.element_blank(),
             axis_line_x       = gg.element_line(colour="black", size=.2, linetype=1),
             axis_line_y       = gg.element_line(colour="black", size=.2, linetype=1),
             # axis_line_y       = gg.element_line(colour="black"),
             legend_background  = gg.element_rect(fill='transparent'),
             # legend_key_height = grid::unit(.1, "cm"),
             # legend_key_width  = grid::unit(.8, "cm")
             axis_ticks_x        = gg.element_blank(),
             axis_ticks_y        = gg.element_blank(),
             axis_text_y         = ggtxt.element_markdown(),
             plot_title	         = gg.element_text(hjust=0, size = 11,
                                                   colour='grey40', face='bold'),
             plot_subtitle	 = gg.element_text(hjust=0, size = 9,
                                                   colour='grey30'),
             axis_title_y        = gg.element_text(size=10, angle=90),
        )
    return g
def ggguides(ncol=1):
    keywidth=2
    keyheight=.9
    leg_title_pos="top"
    g= gg.guides(colour = gg.guide_legend(title_position = leg_title_pos,
                                          ncol=ncol,
                                          size=8,
                                          keywidth=keywidth,
                                          keyheight=keyheight,
                                          title_hjust=0),
                 fill = gg.guide_legend(title_position = leg_title_pos,
                                        ncol=ncol,
                                        size=8,
                                        keywidth=keywidth,
                                        keyheight=keyheight,
                                        title_hjust=0),
                 shape = gg.guide_legend(title_position = leg_title_pos,
                                         ncol=ncol,
                                         size=8,
                                         keywidth=keywidth,
                                         keyheight=keyheight,
                                         title_hjust=0),
                 linetype = gg.guide_legend(title_position = leg_title_pos,
                                            ncol=ncol,
                                            size=8,
                                            keywidth=keywidth,
                                            keyheight=keyheight,
                                            title_hjust=0),
                 )
    return g        


