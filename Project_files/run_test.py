#!/usr/bin/python

import sys
import datetime
from Topology import *
from Node import *
from helpers import *

# if len(sys.argv) != 3:
#     print "Syntax:"
#     print "    python run_topo.py <topology_file> <log_file>"
#     exit()

topos = [
    'ComplexTopo',
    'LargeRandom',
    'new_ComplexTopoHalfed',
    'new_LongLoop',
    'new_NegCycleWithBiNegLink',
    'new_NoNegTopo',
    'new_TailNegativeCycle',
    'new_TailNegCycleWithBiNegLink',
    'new_v2_SingleNode',
    'new_v2_TwoNodesNeg',
    'new_v2_TwoNodes',
    'new_v2_TwoNodesUni',
    'new_v2_VeryComplex2',
    'new_v2_VeryComplex',
    'new_YoutubeTopo',
    'n_longAlternatingSeries',
    'n_longNegSeries2',
    'n_longNegSeries',
    'n_longSeries',
    'NodeDetectEarly',
    'NodeDetectWithCycle',
    'NoInOrOutLinks',
    'SimpleNegativeCycleTopo',
    'SimpleNegativeCycle',
    'SimpleOddLengthNegativeCycle',
    'SimpleTopo',
    'SingleLoopTopo',
    'TwoNegCycles',
    'QuadLoopTopo',
    'QuadLoopDiagnalTopo'
]

start_time = datetime.datetime.now()
test_results = []
total_full_topo_time = 0
tot_pass = 0
tot_fail = 0
topos.sort()
for t in topos:
    # print('Testing - ' + t)
    # Start up the logfile
    start_topo_time = datetime.datetime.now()
    open_log(t + ".log")
    # Populate the topology
    topo = Topology(t + ".txt")
    # Run the topology.
    topo.run_topo()
    # Close the logfile
    finish_log()
    end_topo_time = datetime.datetime.now()

    start_topo_test_time = datetime.datetime.now()
    res_lines_temp = []
    res_lines = []
    with open('full_logs/' + t + '.txt.log') as res:
        for line in res:
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            res_lines_temp.append(line)
    if res_lines_temp[len(res_lines_temp)-1] == '-----':
        _ = res_lines_temp.pop()

    try:
        idx = len(res_lines_temp) - res_lines_temp[::-1].index('-----')
        res_lines = res_lines_temp[idx:]
    except ValueError:
        res_lines = res_lines_temp

    out_lines_temp = []
    out_lines = []
    with open(t + '.log') as out:
        for line in out:
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            out_lines_temp.append(line)

    if out_lines_temp[len(out_lines_temp)-1] == '-----':
        _ = out_lines_temp.pop()

    try:
        idx = len(out_lines_temp) - out_lines_temp[::-1].index('-----')
        out_lines = out_lines_temp[idx:]
    except ValueError:
        out_lines = out_lines_temp

    # print(res_lines)
    # print(out_lines_temp)
    # print(out_lines)
    test_passed = False
    failed_line = 0
    if res_lines == out_lines:
        # print('full match')
        test_passed = True
    else:
        for res, out in zip(res_lines, out_lines):
            res = res.replace(':', ',')
            out = out.replace(':', ',')
            if res == out:
                # print('ACTUAL >>>> ' + res)
                # print('PASSED >>>> ' + out)
                pass
            else:
                res_ln_split = res.split(',')
                out_ln_split = out.split(',')
                res_ln_split.sort()
                out_ln_split.sort()
                if res_ln_split == out_ln_split:
                    # print('ACTUAL >>>> ' + res)
                    # print('PASSED >>>> ' + out)
                    pass
                else:
                    # print('ACTUAL >>>> ' + res)
                    # print('FAILED >>>> ' + out)
                    failed_line += 1
            # print('--')
        if failed_line == 0:
            test_passed = True
    end_topo_test_time = datetime.datetime.now()
    total_topo_time = (end_topo_time - start_topo_time).total_seconds()
    total_test_time = (end_topo_test_time -
                       start_topo_test_time).total_seconds()
    total_full_topo_time = total_full_topo_time + total_topo_time
    if test_passed:
        test_results.append(
            ' - PASS :)  >> ' + t +
            '[ran in ' + str(total_topo_time) +
            'sec, compare time=' + str(total_test_time) + ' sec]'
        )
        tot_pass += 1
    else:
        test_results.append(' - FAIL :(  >> ' + t)
        tot_fail += 1
        # print(res_lines)
        # print(out_lines)

end_time = datetime.datetime.now()
tot_time_to_test = (end_time - start_time).total_seconds()
for test_res in test_results:
    print(test_res)
print('>> COMPARED ' + str(len(topos)) + ' FILES')
print('>> TOTAL PASSED -> ' + str(tot_pass))
print('>> TOTAL FAILED -> ' + str(tot_fail))
print('>> TOTAL TIME TO RUN ALL TOPOS -> ' + str(total_full_topo_time) + 'sec')
print('>> TOTAL TIME -> ' + str(tot_time_to_test) + 'sec')
print('*** *** ***')
