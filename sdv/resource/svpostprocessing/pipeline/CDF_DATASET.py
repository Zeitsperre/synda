#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS. All Rights Reserved��
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains CDF 'dataset' pipeline definition."""

import sppipelineutils
from sppostprocessingutils import PostProcessingPipeline, State, Transition


def get_pipeline():
    return ppp


def set_dataset_path_type(kw):
    assert kw.variable == ''
    kw.path_type = 'dataset'


def f1(kw):
    set_dataset_path_type(kw)
    path = sppipelineutils.build_user_path('interpolated', kw)
    return {'project': kw.project, 'dataset_path': path}


def f2(kw):
    set_dataset_path_type(kw)
    path = sppipelineutils.build_user_path('bias-adjusted', kw)
    return {'project': kw.project, 'dataset_path': path}


name = 'CDF_DATASET'
ppp = PostProcessingPipeline(name)

t1 = Transition(name='latest', destination='S3200', get_args=f1)
t2 = Transition(name='latest', destination='S3300', get_args=f2)

s1 = State(name='S3100', transition=t1, initial=True)
s2 = State(name='S3200', transition=t2)
s3 = State(name='S3300', transition=None)

ppp.add(s1, s2, s3)
