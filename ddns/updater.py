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
Dynamic DNS Updater
"""

from twisted.internet import threads

import dns.query
import dns.tsigkeyring
import dns.update

class DynamicDNSUpdater(object):

    def __init__(self, tsig_key, zone, record, ttl, dns_ip, type):
        
        self.tsig_key = tsig_key
        self.zone = zone
        self.record = record
        self.ttl = ttl
        self.dns_ip = dns_ip
        self.type = type

    def update(self, value):
        d = threads.deferToThread(self._submitDNS, value)
        return d

    def _submitDNS(self, value):

        update = dns.update.Update(
            self.zone,
            keyring=dns.tsigkeyring.from_text(self.tsig_key))

        update.delete(self.record, self.type)
        update.add(self.record, self.ttl, self.type, "%s" % value)
        #print update

        response = dns.query.tcp(update, self.dns_ip)
        #print response

        if response.rcode() != 0:
            raise ValueError("Unexpected Response Code")

        return str(response)
