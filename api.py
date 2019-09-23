def getUnique(log, n_log, field_list):
    result = {}
    for i in range(n_log):
        tmp_list = []
        for j in field_list:
            tmp_list.append(log[i][j])
        tmp = str(' : '.join(tmp_list))
        if tmp in result:
            result[tmp] += 1
        else:
            result[tmp] = 1
    return result


def beginWith(string, substring):
    length = len(substring)
    if string[:length] == substring:
        return True
    else:
        return False


def findDigit(msg):
    idx = [-1 for i in range(10)]
    for i in range(10):
        idx[i] = msg.find(str(i))
    idx.sort()
    res = -1
    for i in range(10):
        if idx[i] > 0:
            res = idx[i]
            break
    return res


def outputFile(dic, fo, sortCount):
    msg_sorted_list = {}
    if (sortCount):
        msg_sorted_list = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    else:
        msg_sorted_list = sorted(dic.items(), key=lambda x: x[0])
    for item in msg_sorted_list:
        fo.write('%-100s' % item[0])
        fo.write('%d\r\n' % item[1])
    fo.close()


def getHexNum(msg, start_idx):
    i = start_idx;
    if (msg[start_idx : start_idx + 2] == '0x' or msg[start_idx : start_idx + 2] == '0X'):
        i += 2
    while ((msg[i]>='0' and msg[i]<='9') or (msg[i]>='a' and msg[i]<='f') or (msg[i]>='A' and msg[i]<='F')):
        i += 1
    return int(msg[start_idx : i], 16)
