import sdconst

# not used yet

# this dict contains the default
default={
    sdconst.EVENT_FILE_COMPLETE:False,
    sdconst.EVENT_VARIABLE_COMPLETE:True,
    sdconst.EVENT_DATASET_COMPLETE:False,
    sdconst.EVENT_DATASET_LATEST:False,
    sdconst.EVENT_LATEST_DATASET_COMPLETE:False,
    sdconst.EVENT_NON_LATEST_DATASET_COMPLETE:False,

    sdconst.EVENT_OUTPUT12_VARIABLE_COMPLETE:False,
    sdconst.EVENT_OUTPUT12_DATASET_COMPLETE:False,
    sdconst.EVENT_OUTPUT12_LATEST_DATASET_COMPLETE:False,
    sdconst.EVENT_OUTPUT12_NON_LATEST_DATASET_COMPLETE:False,
    sdconst.EVENT_OUTPUT12_DATASET_LATEST:False,
}

# this dict override the default on a per-project basis
project_override={
    sdconst.EVENT_FILE_COMPLETE:{
        'CMIP8':True
    },
    sdconst.EVENT_VARIABLE_COMPLETE:{
        'CMIP5':False
    },
    sdconst.EVENT_DATASET_COMPLETE:{
        'CMIP2':True
    }
}
