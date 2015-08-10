#!/usr/bin/env python

"""
sudo pip install psutil requests
"""

###############################################################################
# Based on                                                                    #
# pymetrics                                                                   #
# https://raw.githubusercontent.com/braindump/Dirty-little-helpers/master/pymetrics                                                                            #
# by Lars Herbach                                                             #
# lars@freistil.cz                                                            #
# http://freistil.cz                                                          #
#                                                                             #
#                                                                             #
# MIT License                                                                 #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files (the             #
# "Software"), to deal in the Software without restriction, including         #
# without limitation the rights to use, copy, modify, merge, publish,         #
# distribute, sublicense, and/or sell copies of the Software, and to          #
# permit persons to whom the Software is furnished to do so, subject to       #
# the following conditions:                                                   #
#                                                                             #
# The above copyright notice and this permission notice shall be              #
# included in all copies or substantial portions of the Software.             #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,             #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF          #
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                       #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE      #
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION      #
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION       #
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.             #
###############################################################################

import psutil
import requests
import time
import os
from socket import gethostname

try:
    user = os.environ['LIBRATO_USER']
    api  = os.environ['LIBRATO_API']
except:
    print "Please set LIBRATO_USER and LIBRATO_API environment variables!"
    print ""
    quit(-1)

url  = "https://metrics-api.librato.com/v1/metrics"

def main():
    hostname        = gethostname()
    processes       = len(psutil.get_pid_list())
    cpu_combined    = psutil.cpu_percent(interval = 0.3)
    # cpu_list        = psutil.cpu_percent(interval = 0.3, percpu = True)
    phymem          = psutil.virtual_memory()
    phymem_total    = phymem[0]
    phymem_used     = phymem[2]
    swapmem         = psutil.swap_memory()
    swapmem_total   = swapmem[0]
    swapmem_used    = swapmem[3]

    net_start    = psutil.network_io_counters()
    time.sleep(1)
    net_stop     = psutil.network_io_counters()

    disk_start    = psutil.disk_io_counters()
    time.sleep(1)
    disk_stop     = psutil.disk_io_counters()

    payload = {"source"           : hostname,
               "measure_time"     : int(time.time()),
               "gauges[0][name]"  : "Number_of_Processes",
               "gauges[0][value]" : processes,
               "gauges[1][name]"  : "CPU_Usage",
               "gauges[1][value]" : cpu_combined,
               "gauges[2][name]"  : "Physical_Memory",
               "gauges[2][value]" : phymem_used,
               "gauges[3][name]"  : "Swap_Memory",
               "gauges[3][value]" : swapmem_used,
               "gauges[4][name]"  : "Network_In",
               "gauges[4][value]" : net_stop[1] - net_start[1],
               "gauges[5][name]"  : "Network_out",
               "gauges[5][value]" : net_stop[0] - net_start[0],
               "gauges[6][name]"  : "Disk_Reads",
               "gauges[6][value]" : disk_stop[0] - disk_start[0],
               "gauges[7][name]"  : "Disk_Writes",
               "gauges[7][value]" : disk_stop[1] - disk_start[1],
               }

    gauge_count = (len(payload) - 2) / 2

    for disk in psutil.disk_partitions():
        key_source = "gauges[" + str(gauge_count) + "][source]"
        key_name   = "gauges[" + str(gauge_count) + "][name]"
        key_value  = "gauges[" + str(gauge_count) + "][value]"
        payload[key_source] = hostname + "_" + disk[0][disk[0].rfind("/") + 1:]
        payload[key_name]   = "Disk_Usage"
        payload[key_value]  = psutil.disk_usage(disk[1])[3]
        gauge_count += 1

    header = {"content-type": "application/x-www-form-urlencoded"}
    r = requests.post(url,
                      auth = requests.auth.HTTPBasicAuth(user, api),
                      headers = header,
                      data = payload)

    if r.status_code != 200:
        print "Error :("
        print r.text


if __name__ == '__main__':
    main()