#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains network functions."""

import sys
import traceback
import os
import urllib2
#import requests
import sdxml
from sdtypes import Response
from sdexception import SDException
from sdtime import SDTimer
import sdlog
import sdconfig
import sdpoodlefix
import httplib

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    """HTTP handler that transmits an X509 certificate as part of the request."""
    def __init__(self, key, cert):
            urllib2.HTTPSHandler.__init__(self)
            self.key = key
            self.cert = cert
    def https_open(self, req):
            return self.do_open(self.getConnection, req)
    def getConnection(self, host, timeout=300):
            return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)

def download_file(url, local_path):

    try:

        # setup HTTP handler

        opener = urllib2.build_opener(HTTPSClientAuthHandler(sdconfig.esgf_x509_proxy,sdconfig.esgf_x509_proxy))
        opener.add_handler(urllib2.HTTPCookieProcessor())


        # prepare local file

        destdir=os.path.dirname(local_path)
        if not os.path.exists(destdir):
            os.mkdirs(destdir)

        f=open(local_path, 'w')

        
        # download file

        socket=opener.open(url) # 'socket' name is arbitrary (maybe 'o', or 'object' is better)

        # TODO
        # JRA: modify below to add checksum & huge file support (i.e. file that doesn't fit in memory)
        #https://gist.github.com/brianewing/994303
        #http://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file

        f.write(socket.read())

        
        # cleanup

        f.close()
        socket.close()
        opener.close()

    except Exception,e:

        traceback.print_exc(file=sys.stderr)

        return 1

    return 0

def call_web_service(request,timeout):
    start_time=SDTimer.get_time()
    buf=HTTP_GET(request.get_url(),timeout)
    elapsed_time=SDTimer.get_elapsed_time(start_time)

    # HACK
    #
    # This is to prevent fatal error when document contain mixed encodings
    #
    # e.g. http://esgf-data.dkrz.de/esg-search/search?distrib=true&fields=*&type=File&limit=100&title=sftgif_fx_IPSL-CM5A-LR_abrupt4xCO2_r0i0p0.nc&format=application%2Fsolr%2Bxml&offset=0
    #
    if sdconfig.fix_encoding:
        import sdencoding
        buf=sdencoding.fix_mixed_encoding_ISO8859_UTF8(buf)

    try:
        result=sdxml.parse_metadata(buf)
    except Exception,e:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        sdlog.info('SDNETUTI-001','XML parsing error (exception=%s). Most of the time, this error is due to a network error.'%str(e))

        # debug
        #
        # TODO: maybe always enable this
        #
        #import sdconfig
        #traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))

        # debug
        #
        # (if the error is not due to a network error (e.g. internet connection
        # problem), raise the original exception below and set the debug mode
        # to see the stacktrace.
        #
        #raise

        raise SDException('SDNETUTI-008','Network error (see log for details)') # we raise a new exception 'network error' here, because most of the time, 'xml parsing error' is due to an 'network error'.

    return Response(call_duration=elapsed_time,**result)

def call_param_web_service(url,timeout):
    buf=HTTP_GET(url,timeout)

    try:
        params=sdxml.parse_parameters(buf)
    except:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        raise SDException('SDNETUTI-003','Network error')

    return params

def HTTP_GET(url,timeout=20):
    sock=None
    buf=None

    try:
        sdpoodlefix.start(url)

        # urllib2
        #
        sock=urllib2.urlopen(url, timeout=timeout)
        buf=sock.read()

        # requests
        #
        #response=requests.get(url, timeout=timeout)
        #buf=response.text

    except Exception, e:
        errmsg="HTTP query failed (url=%s,exception=%s,timeout=%d)"%(url,str(e),timeout)
        errcode="SDNETUTI-002"

        raise SDException(errcode,errmsg)

    finally:
        if sock!=None:
            sock.close()

        sdpoodlefix.stop()

    return buf

def test_access():
    urlfile = urllib2.urlopen("http://www.google.com")

    data_list = []
    chunk = 4096
    while 1:
        data = urlfile.read(chunk)
        if not data:
            break
        data_list.append(data)
        #print "Read %s bytes"%len(data)
