#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains next url routine."""

import sdlog

def run(tr):
    TODO => select which protocol to use in the line below
    result=sdquicksearch.run(parameter=['limit=1','fields=%s'%timestamp_fields,'type=File','dataset_id=%s'%d['instance_id']],post_pipeline_mode=None)
    li=result.get_files()
    if len(li)>0:
        file_=li[0]
        url=file_['timestamp']

        sdlog.info("SDTIMEST-001","Dataset timestamp set from one dataset's file's timestamp (dataset_functional_id=%s,file_functional_id=%s)"%(d['instance_id'],file['instance_id']))
    else:
        sdlog.info("SDTIMEST-001","Dataset timestamp set from one dataset's file's timestamp (dataset_functional_id=%s,file_functional_id=%s)"%(d['instance_id'],file['instance_id']))
