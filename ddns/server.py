# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Jacob Feisley
# http://feisley.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# $Id$

"""
Dynamic DNS Update Server
"""

from twisted.application import internet, service
from twisted.web import static, resource, server

from ddns.updater import DynamicDNSUpdater


class UrlHandler(resource.Resource):
    def render(self, request):
        args = request.args
        
        request.write("DDNS Proxy")
        request.write("<br /><br />")
        request.write("Arguments: %s" % request.args)
        
        def cb(r):
            request.write("<br /><br />")
            request.write('Success: %s' % r)
            print r
            request.finish()
        
        #Do requested operation here!
        try:
            DynamicDNSUpdater(
                tsig_key = {args['tsig_id'][0]: args['tsig_key'][0]},
                zone = args['zone'][0],
                record = args['record'][0],
                ttl = args['ttl'][0],
                dns_ip = args['dns_server'][0],
                type = args['type'][0]
            ).update(args['value'][0]).addCallback(cb)
        
        except Exception, e:
            request.write("<br /><br />")
            request.write('Exception: %s' % e)
            request.finish()
        
        return server.NOT_DONE_YET
    
    
root = UrlHandler()
root.putChild("update", UrlHandler())

site = server.Site(root)
