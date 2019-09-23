import os
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from api import getUnique, beginWith, findDigit, outputFile, getHexNum
from drawFig import drawCDF, drawPlot


def analyze0():
    f = open('RAS_0901_0908.json', 'r')
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
    print('Totally', cnt, 'logs.')


def analyze1():
    """
    Get all the unique contents in specific fields, and get their counts.
    """
    f = open('RAS_0901_0908.json', 'r')
    log = []
    while True:
        line = f.readline()
        if not line:
            break
        log.append(json.loads(line))
    n_log = len(log)
    # print('A total of', n_log, 'logs.')
    
    log_dic = getUnique(log, n_log, ['SEVERITY'])
    print('Totally', len(log_dic), 'classes.')
    value_sorted_list = sorted(log_dic.items(), key=lambda x: x[1], reverse=True)
    for item in value_sorted_list:
        print(item)
    f.close()


def analyze2():
    """
    Get the original MESSAGE
    """
    f = open('RAS_0901_0908.json', 'r')
    cnt = 0
    goal = 100
    while True:
        line = f.readline()
        if not line:
            break
        log = json.loads(line)
        msg = str(log['MESSAGE']).strip()
        if beginWith(msg, 'MESSAGE') or beginWith(msg, '-------'):
            continue
        if beginWith(msg, 'Correctable errors'):
            print(msg)
            cnt += 1
            if cnt == goal:
                f.close()
                exit()
    f.close()
    exit()


def analyze3():
    """
    Analyze the MESSAGE.
    Split the title of MESSAGE using ':', '.', '(', digits.
    """
    f = open('RAS_0901_0908.json', 'r')
    msg_dic = {}
    unsolved_msg = {}
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 200000 == 0:
            print(cnt)
        log = json.loads(line)
        msg = str(log['MESSAGE']).strip()
        if beginWith(msg, 'MESSAGE') or beginWith(msg, '-------'):
            continue
        idx_array = []
        idx_array.append(msg.find(':'))
        idx_array.append(msg.find('.'))
        idx_array.append(msg.find('('))
        idx_array.append(findDigit(msg))
        idx_array.sort()
        idx = -1
        for i in range(len(idx_array)):
            if idx_array[i] > 0:
                idx = idx_array[i]
                break
        msg_title = ''
        if idx > 0:
            msg_title = msg[:idx].strip()
        else:
            msg_title = msg.strip()
        if msg_title in msg_dic:
            msg_dic[msg_title] += 1
        else:
            msg_dic[msg_title] = 1
    f.close()
    # json
    msg_dic_json_file = open('msg_dic.json', 'w')
    json.dump(msg_dic, msg_dic_json_file)
    msg_dic_json_file.close()
    # txt
    msg_dic_txt_file = open('msg_dic.txt', 'w')
    outputFile(msg_dic, msg_dic_txt_file, 0)
    msg_dic_txt_file.close()
    # unsolved_msg_file = open('unsolved_msg.json', 'w')
    # json.dump(unsolved_msg, unsolved_msg_file)
    # unsolved_msg_file.close()


def analyze4():
    """
    Extract MESSAGE related to DRAM
    """
    f = open('RAS_0901_0908.json', 'r')
    fo = open('DRAM_0901_0908.json', "w")
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 200000 == 0:
            print(cnt)
        log = json.loads(line)
        msg = str(log['MESSAGE']).strip()
        if beginWith(msg, 'MESSAGE') or beginWith(msg, '-------'):
            continue
        if beginWith(msg, 'Correctable errors') \
        or beginWith(msg, 'DDR Controller') \
        or beginWith(msg, 'DDR correctable') \
        or beginWith(msg, 'ECC-correctable'):

            # Correctable errors

            # DDR Controller

            # DDR correctable single symbol error
            # DDR correctable double symbol error
            # DDR correctable chipkill error

            # ECC-correctable single symbol error
            # ECC-correctable double symbol error
            # ECC-correctable chipkill error

            """ no address """
            # DDR controller single symbol error count
            # DDR controller double symbol error count
            # DDR controller chipkill error count
            # DDR controller machine check

            """ abandon """
            # or beginWith(msg, 'A DDR controller raised a machine check')
            # or beginWith(msg, 'An ECC uncorrectable error occurred in DRAM')
            # or beginWith(msg, 'DDR Redundant Bit Steering activated on bit')
            # or beginWith(msg, 'DDR redundant bit steering activated')

            json.dump(log, fo)
            fo.write('\n')
            fo.flush()
    f.close()
    fo.close()


def analyze5():
    """
    Decode 32-bit memory bus
    """
    f = open('DRAM_0901_0908.json', 'r')
    fo = open('DRAM_decoded_0901_0908.json', 'w')
    # f = open('RAS_0901_0908.json', 'r')
    # fo = open('RAS_decoded_0901_0908.json', 'w')
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 20000 == 0:
            print(cnt)
        log = json.loads(line)
        msg = str(log['MESSAGE']).strip()
        # msg_max_length = 347
        # log['MESSAGE'] = '%-350s' % msg
        log['ADDR'] = ''
        log['BANK'] = -1
        log['ROW'] = -1
        log['COLUMN'] = -1
        addr_idx = msg.find('address')
        if (addr_idx >= 0):
            hex_idx = msg[addr_idx:].find('0x')
            if (hex_idx >= 0):
                addr = getHexNum(msg[addr_idx:], hex_idx)
                log['ADDR'] = hex(addr)
                log['BANK'] = ((1 << 3) - 1) & (addr >> 14)
                log['ROW'] = ((1 << 14) - 1) & (addr >> 17)
                log['COLUMN'] = ((1 << 11) - 1) & (addr >> 3)
        json.dump(log, fo)
        fo.write('\n')
        fo.flush()
    f.close()
    fo.close()


def analyze6():
    """
    error cnt per node
    """
    f = open('DRAM_0901_0908.json', 'r')
    node_log_cnt = {}
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 20000 == 0:
            print(cnt)
        log = json.loads(line)
        location = str(log['LOCATION']).strip()
        if location in node_log_cnt:
            node_log_cnt[location] += 1
        else:
            node_log_cnt[location] = 1
    f.close()
    total_log_cnt = 0
    for v in node_log_cnt.values():
        total_log_cnt += v
    print('Total number of logs:', total_log_cnt)
    """ json """
    node_log_cnt_json_file = open('node_log_cnt.json', 'w')
    json.dump(node_log_cnt, node_log_cnt_json_file)
    node_log_cnt_json_file.close()
    """ draw CDF """
    drawCDF(node_log_cnt, 'node_log_cnt.png', 'Log distribution among nodes', 'Number of nodes', 'Number of logged errors')
    """ txt """
    # log_cnt_txt_file = open('node_log_cnt.txt', 'w')
    # outputFile(node_log_cnt, log_cnt_txt_file, 1)
    # log_cnt_txt_file.close()


def analyze61():
    """
    error cnt per node in the top 1% nodes
    """
    f = open('DRAM_0901_0908.json', 'r')
    node_log_cnt = {}
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 20000 == 0:
            print(cnt)
        log = json.loads(line)
        location = str(log['LOCATION']).strip()
        if location in node_log_cnt:
            node_log_cnt[location] += 1
        else:
            node_log_cnt[location] = 1
    f.close()
    node_log_cnt_sorted_list = sorted(node_log_cnt.items(), key=lambda x: x[1], reverse=True)
    node_num = len(node_log_cnt_sorted_list)
    node_log_cnt_top1percent = {}
    for i in range(node_num):
        if (i < int(0.01 * node_num)):
            node_log_cnt_top1percent[node_log_cnt_sorted_list[i][0]] = node_log_cnt_sorted_list[i][1]
    """ json """
    node_log_cnt_top1percent_json_file = open('node_log_cnt_top1percent.json', 'w')
    json.dump(node_log_cnt_top1percent, node_log_cnt_top1percent_json_file)
    node_log_cnt_top1percent_json_file.close()
    """ draw CDF """
    drawCDF(node_log_cnt_top1percent, 'node_log_cnt_top1percent.png', 'Log distribution among nodes in the top 1% nodes', 'Number of nodes', 'Number of logged errors')


def analyze7():
    """
    Error distribution among pages per node
    """
    f = open('DRAM_0901_0908.json', 'r')
    node_pfns = {}
    node_log_cnt = {}
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 20000 == 0:
            print(cnt)
        log = json.loads(line)
        node = str(log['LOCATION']).strip()
        msg = str(log['MESSAGE']).strip()
        addr_idx = msg.find('address')
        if addr_idx >= 0:
            hex_idx = msg[addr_idx:].find('0x')
            if hex_idx >= 0:
                addr = getHexNum(msg[addr_idx:], hex_idx)
                pfn = addr >> 12
                if node in node_pfns:
                    node_pfns[node].append(pfn)
                    node_log_cnt[node] += 1
                else:
                    node_pfns[node] = [pfn]
                    node_log_cnt[node] = 1
    node_log_cnt_sorted_list = sorted(node_log_cnt.items(), key=lambda x: x[1], reverse=True)
    node_num = len(node_log_cnt_sorted_list)
    hist_num = 50
    page_log_hist_top5percent_list = []
    page_log_hist_mid5percent_list = []
    for i in range(node_num):
        if (i < int(0.05 * node_num) or (i >= int(0.5 * node_num) and i < int(0.55 * node_num))):
            node = node_log_cnt_sorted_list[i][0]
            pfns_cnt_sorted_list = pd.Series(node_pfns[node]).value_counts(normalize=True, ascending=True).tolist()
            page_log_hist_tmp = [0 for j in range(hist_num)]
            pfn_num = len(pfns_cnt_sorted_list)
            p = 0
            for hist in range(hist_num):
                if (hist > 0):
                    page_log_hist_tmp[hist] += page_log_hist_tmp[hist - 1]
                while (p < pfn_num and (p / pfn_num >= hist / hist_num) and (p / pfn_num < (hist + 1) / hist_num)):
                    page_log_hist_tmp[hist] += pfns_cnt_sorted_list[p]
                    p += 1
            if (i < int(0.05 * node_num)):
                page_log_hist_top5percent_list.append(page_log_hist_tmp)
            else:
                page_log_hist_mid5percent_list.append(page_log_hist_tmp)
    page_log_hist_top5percent = np.asarray(page_log_hist_top5percent_list).mean(axis=0)
    print(page_log_hist_top5percent)
    drawPlot(page_log_hist_top5percent, 'page_log_hist_top5percent.png', 'Error distribution among pages in the top 5% nodes', 'Number of nodes', 'Normalized number of logged errors', 0, 1.1)
    page_log_hist_mid5percent = np.asarray(page_log_hist_mid5percent_list).mean(axis=0)
    print(page_log_hist_mid5percent)
    drawPlot(page_log_hist_mid5percent, 'page_log_hist_mid5percent.png', 'Error distribution among pages in the mid 5% nodes', 'Number of nodes', 'Normalized number of logged errors', 0, 1.1)


def analyze8():
    """
    error cnt per cell
    """
    f = open('DRAM_decoded_0901_0908.json', 'r')
    # f = open('RAS_decoded_0901_0908.json', 'r')
    cell_log_cnt = {}
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 20000 == 0:
            print(cnt)
        log = json.loads(line)
        cell = str(log['ADDR']).strip()
        if cell in cell_log_cnt:
            cell_log_cnt[cell] += 1
        else:
            cell_log_cnt[cell] = 1
    f.close()
    """ statistics """
    num_of_distinct_cells = len(cell_log_cnt)
    num_of_cells_with_repeated_errors = 0
    num_of_cells_with_nlt100_errors = 0
    log_cnt_on_cells_with_repeated_errors = 0
    for v in cell_log_cnt.values():
        if v > 1:
            num_of_cells_with_repeated_errors += 1
            log_cnt_on_cells_with_repeated_errors += v
            if v >= 100:
                num_of_cells_with_nlt100_errors += 1
    print('Number of distinct cells:', num_of_distinct_cells)
    print('Number of cells with repeated errors:', num_of_cells_with_repeated_errors)
    print('Number of logs on the cells with repeated errors:', log_cnt_on_cells_with_repeated_errors)
    print('Number of cells with no less than 100 errors:', num_of_cells_with_nlt100_errors)
    """ json """
    cell_log_cnt_json_file = open('cell_log_cnt.json', 'w')
    json.dump(cell_log_cnt, cell_log_cnt_json_file)
    cell_log_cnt_json_file.close()
    """ draw CDF """
    drawCDF(cell_log_cnt, 'cell_log_cnt.png', 'Log distribution among cells', 'Number of cells', 'Number of logged errors')


def analyze81():
    """
    error cnt per cell
    """
    f = open('DRAM_decoded_0901_0908.json', 'r')
    cell_log_cnt = {}
    cnt = 0
    while True:
        line = f.readline()
        if not line:
            break
        cnt += 1
        if cnt % 20000 == 0:
            print(cnt)
        log = json.loads(line)
        cell = str(log['ADDR']).strip()
        if cell in cell_log_cnt:
            cell_log_cnt[cell] += 1
        else:
            cell_log_cnt[cell] = 1
    f.close()
    cell_log_cnt_sorted_list = sorted(cell_log_cnt.items(), key=lambda x: x[1], reverse=True)
    cell_num = len(cell_log_cnt_sorted_list)
    cell_log_cnt_top1percent = {}
    for i in range(cell_num):
        if (i < int(0.01 * cell_num)):
            cell_log_cnt_top1percent[cell_log_cnt_sorted_list[i][0]] = cell_log_cnt_sorted_list[i][1]
    """ json """
    cell_log_cnt_top1percent_json_file = open('cell_log_cnt_top1percent.json', 'w')
    json.dump(cell_log_cnt_top1percent, cell_log_cnt_top1percent_json_file)
    cell_log_cnt_top1percent_json_file.close()
    """ draw CDF """
    drawCDF(cell_log_cnt_top1percent, 'cell_log_cnt_top1percent.png', 'Log distribution among cells in the top 1% cells', 'Number of cells', 'Number of logged errors')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", default=0)
    args = parser.parse_args()
    version = float(args.version)
    if version == 0:
        analyze0()
    elif version == 1:
        analyze1()
    elif version == 2:
        analyze2()
    elif version == 3:
        analyze3()
    elif version == 4:
        analyze4()
    elif version == 5:
        analyze5()
    elif version == 6:
        analyze6()
    elif version == 6.1:
        analyze61()
    elif version == 7:
        analyze7()
    elif version == 8:
        analyze8()
    elif version == 8.1:
        analyze81()
    else:
        print('Error: no such analysis function.')
