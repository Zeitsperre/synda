#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains shrink preprocessing routines."""

def is_nearestpost_enabled(metadata):

    if sdconfig.nearest_schedule=='post' and nearest_flag_set_on_all_files(metadata):
        return True
    else:
        return False

def nearest_flag_set_on_all_files(metadata):
    """This func checks that all files have the 'nearest' flag (as sdnearestpost processing type is 'interfile', we need ALL files to be flagged)."""

    # create light list with needed columns only not to overload system memory
    light_metadata=sdlmattrfilter.run(metadata,['attached_parameters']) # we keep 'attached_parameters' because it contains 'nearest' flag we are interested in

    for f in light_metadata.get_files(): # load complete list in memory
        nearest=sdpostpipelineutils.get_attached_parameter(f,'nearest','false')
        if nearest=='false':
            return False
    return True
