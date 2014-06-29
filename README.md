check_f5_virtual_conns.py
=========================

Nagios plugin for monitoring connection counts on F5 BigIP virtual servers.

This was originally created to satisfy the monitoring needs of tracking open connections to virtual servers that have a defined connection limit.  However, this plugin can be used with any virtual server.

# Usage:

The nagios command for this plugin should be defined something like this:

```
define command{
        command_name    check_f5_virtual_conns
        command_line    /usr/lib/nagios/plugins/check_f5_virtual_conns.py -H $HOSTADDRESS$ -C $USER7$ -v $ARG1$ -w $ARG2$ -c $ARG3$
}
```

And so the service definition would be something like this:

```
define service {
  host_name                     f5_viprion.example.com
  service_description           A Very Importand VIP
  check_command                 check_f5_virtual_conns!very.important.vip.example.com!80!90
  use                           vip_general
  servicegroups                 prod
}
```

This setup you pull data for the virtual server named 'very.important.vip.example.com'.  This check would throw a warning if the polled connection count is above eighty percent of the limit and would throw a critical if the count was above ninety percent of the limit. If no limit is set, the plugin will always return OK with the current connection count.

# Details:

This script was build for use on a RHEL6 box using python 2.6.  It was developed and tested against an F5 Viprion running BigIP 10.X.

This script is pulling its data using SNMP via the snimpy module.  It can be found here: https://github.com/vincentbernat/snimpy

Because SNMP is in use, you will need to provide the location of the F5 MIBs.  This location is hard-coded at the beginning of the script within the F5_MIB_DIR variable.  You'll need to set this variable to the location of the directory that holds your F5-BIGIP-COMMON-MIB and F5-BIGIP-LOCAL-MIB files.
