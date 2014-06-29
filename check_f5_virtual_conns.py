#!/usr/bin/python

import sys
from optparse import OptionParser

import snimpy.snmp, snimpy.mib
from snimpy.manager import Manager as M
from snimpy.manager import load

F5_MIB_DIR = "/usr/local/f5_mibs"

parser = OptionParser()
parser.add_option( "-H", "--host", dest = "host", help = "SNMP agent host name or IP" )
parser.add_option( "-C", "--community", dest = "community", help = "SNMP community string" )
parser.add_option( "-v", "--virtual", dest = "virtual", help = "F5 virtual server" )
parser.add_option( "-w", "--warning", dest = "warning", help = "Warning threshold", type = "int", default = 80 )
parser.add_option( "-c", "--critical", dest = "critical", help = "Critical threshold", type = "int", default = 90 )
( options, args ) = parser.parse_args()

if not options.host:
    print 'UNKNOWN|Host name is not valid.'
    sys.exit(3)

if not options.community:
    print 'UNKNOWN|Community string is not valid.'
    sys.exit(3)

if not options.virtual:
    print 'UNKNOWN|F5 virtual server is not valid.'
    sys.exit(3)

try:
    load("%s/F5-BIGIP-COMMON-MIB.txt" % F5_MIB_DIR)
    load("%s/F5-BIGIP-LOCAL-MIB.txt" % F5_MIB_DIR)
except snimpy.mib.SMIException:
    print 'UNKNOWN|Error while loading required mibs.'
    sys.exit(3)

manager = M( host = options.host, community = options.community, version = 2 )

try:
    client_conns = int( manager.ltmVirtualServStatClientCurConns[ options.virtual ] )
    client_limit = int( manager.ltmVirtualServConnLimit[ options.virtual ] )
except ( snimpy.snmp.SNMPNoSuchObject, snimpy.snmp.SNMPException ), e:
    print 'UNKNOWN|%s' % str(e)
    sys.exit(3)

if client_limit > 0:
    used_pct = int( round( ( float( client_conns ) / client_limit ) * 100 ) )

    warn_amount = int( round( client_limit * ( float( options.warning ) / 100 ) ) )
    crit_amount = int( round( client_limit * ( float( options.critical ) / 100 ) ) )

    perf_data = "conn_limit=%d;;;; conn_count=%d;%d;%d;; percent_used=%d;%d;%d;;" % ( client_limit, client_conns, warn_amount, crit_amount, used_pct, options.warning, options.critical )

    if used_pct >= options.critical:
        print "CRITICAL ( used_pct:%d ) | %s" % ( used_pct, perf_data )
        sys.exit(2)
    elif used_pct >= options.warning:
        print "WARN ( used_pct:%d ) | %s" % ( used_pct, perf_data )
        sys.exit(1)

    print "OK ( used_pct:%d ) | %s" % ( used_pct, perf_data )
    sys.exit(0)
else:
    print "OK ( client_conns:%d ) | conn_count=%d;;;;" % ( client_conns, client_conns )
    sys.exit(0)
