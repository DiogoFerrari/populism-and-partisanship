
print(f"Loading constants...", flush=True)

COVARS_RAW = {
    'educ_cat' : "Education",
    'gender'   : "Gender",
    'age'      : 'Age',
    'inc'      : 'Income',
    'race'     : 'Race'
}
COVARS_ATE = {
    'inchhpc_std' : "Income (std)",
    'age_std'     : "Age (std)",
    'educ_std'    : "Education (std)",
    'white'       : "Race (white)",
    'male'        : "Gender (male)",
    'ideo_std'    : "Ideology (std)",
}
COVARS_PRED = {
    'inchhpc_std' : "Income (std)",
    'age_std'     : "Age (std)",
    'educ_std'    : "Education (std)",
    'white'       : "Race (white)",
    'male'        : "Gender (male)",
    'ideo_std'    : "Ideology (std)",
    'ptyid7'      : "Party identification (with leaners)"
}
PTYID = {
    'ptyid'       : "Party identification",
#     'ptyid5'      : "Party identification (excluding leaners)",
}
COVARS  = COVARS_ATE | COVARS_PRED | PTYID
# COVARSExt  = {
#     'age4c'    :"Age",
#     'educ_std' :"Education (std)",
#     'educ3c'   :"Education (Categories)",
#     'educ'     :"Education",
# }
TREAT={
    'treat' : "Treatment",
    'cue'   : "Cue",
    'cueg'  : "Cue giver",
}
OUTCOME={
    'y'      :'Outcome',
    'popmin':"Populist Attitudes",
    'popmul':"Populist Attitudes (Multiplicative Index)",
    'popadd':"Populist Attitudes (Additive Index)",
}
CATs={
    'cueg':['Control', 'Biden', 'Trump']
}
