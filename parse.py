import json

label = ['RECID', 'MSG_ID', 'COMPONENT', 'SUBCOMPONENT', 'ERRCODE', 'SEVERITY', 'EVENT_TIME', 'FLAGS', 'PROCESSOR', 'NODE', 'BLOCK', 'LOCATION', 'SERIALNUMBER', 'ECID', 'MESSAGE']

pattern = ['-----------', # RECID 11
		   '----------', # MSG_ID 10
		   '----------------', # COMPONENT 16
		   '--------------------', # SUBCOMPONENT 20
		   '----------------------------------------', # ERRCODE 40
		   '--------', # SEVERITY 8
		   '--------------------------', # EVENT_TIME 26
		   '----------', # FLAGS 10
		   '-----------', # PROCESSOR 11
		   '-----------', # NODE 11
		   '--------------------------------', # BLOCK 32
		   '----------------------------------------------------------------', # LOCATION 64
		   '-------------------', # SERIALNUMBER 19
		   '-------------------------------', # ECID 31
		   '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------']
		   # MESSAGE 1024


cnt = 0


def getMessage(line, f):
	msg_prefix_list = ['A DDR ', 'A DMA ', 'A kernel ', 'A Link ', 'A memory ', 'A message ', 'A processor ', 'A script ', 'An ', 
					   'ACCESS: ', 'ACCESS_SCOM_STAT: ', 
					   'Bootloader ', 'Broken ', 
					   'Can no ', 'Cannot ', 'Checksum ', 'CIO service ', 'Collective ', 'Correctable ', 'Could ', 
					   'DDR ', 'Detected ', 'DMA SRAM ', 'DMA unit ', 
					   'E10000 ', 'ECC-correctable ', 'ECID: ', 'Environment ', 'Error ', 
					   'Global ', 
					   'Had ', 'HBIST loopback ', 
					   'Initialization ', 'Insufficient ', 'Internal ', 'Invalid ', 'IOCard ', 
					   'Lbist ', 'Link ', 'L1 data ', 'L1 instruction ', 'L2 snoop ', 'L3 cache ', 'L3 Correctable ', 'L3 directory ', 'L3 machine ', 
					   'Machine ', 'Missing bulk ', 
					   'Node ', 
					   'Power ', 'Problem ', 
					   'SerDes ', 'Service ', 'Software ', 'Spurious ', 'Successfully ', 
					   'The ', 'There ', 'This ', 'TLB Entry ', 'TLB parity ', 'Torus ', 
					   'Unable ', 
					   '1.2 power ', '1.5 power ', '1.5V power ', '1.8 Power ', '1.8 power ', '1.8vV power ', '3.3 power ', '5.0 power ']
	# 'The' : 'The global ', 'The microloader ', 'The TNK '
	# 'An' : 'An attempt ', 'An error(s) ', 'An illegal ', 'An oops '
	global cnt
	idx = -1
	# print '-----loop-----'
	line_buf = [] # DEBUG
	while idx < 0:
		# print line
		idx_flag = 0
		idx_min = 2000
		for item in msg_prefix_list:
			idx_tmp = line.find(item)
			if idx_tmp >= 0 and idx_tmp < idx_min:
				idx_flag = 1
				idx_min = idx_tmp
		if idx_flag:
			idx = idx_min
		else:
			line_buf.append(line) # DEBUG
			line = f.readline()
			cnt += 1
			if line.strip() != '' and line.strip()[0] == '2':
				print line_buf # DEBUG
				print 'UNSEEN'
				print cnt
				exit()
		# print idx
		# raw_input()
	msg = line[idx:].strip()
	msg = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
	return msg


def parse(filename):
	f = open(filename, 'r')
	out_f = open(filename + '.json', 'w')
	unsolved_f = open(filename + '_unsolved', 'w')
	global cnt
	legal_cnt = 0
	start = 0
	while True:
		line = f.readline()
		cnt += 1
		if not line:
			break
		if cnt < start:
			continue
		if line.strip() == '':
			continue
		if legal_cnt % 10000 == 0:
			print legal_cnt
		# print cnt
		try:
			if cnt < 274525:
				log = {}
				log['RECID'] = line[0:11]
				log['MSG_ID'] = line[12:22]
				log['COMPONENT'] = line[23:39]
				log['SUBCOMPONENT'] = line[40:60]
				log['ERRCODE'] = line[61:101]
				log['SEVERITY'] = line[102:110]
				log['EVENT_TIME'] = line[111:137]
				# log['FLAGS'] = line[138:148]
				log['PROCESSOR'] = line[149:160]
				# log['NODE'] = line[161:172]
				log['BLOCK'] = line[173:205]
				log['LOCATION'] = line[206:270]
				# log['SERIALNUMBER'] = line[271:290]
				# log['ECID'] = line[291:322]
				log['MESSAGE'] = line[323:]
				json.dump(log, out_f)
				out_f.write('\n')
				out_f.flush()
				legal_cnt += 1
			else:
				log = {}
				log['RECID'] = line[0:11]
				log['MSG_ID'] = line[13:23]
				log['COMPONENT'] = line[26:42]
				log['SUBCOMPONENT'] = line[45:65]
				log['ERRCODE'] = line[68:108]
				log['SEVERITY'] = line[111:119]
				log['EVENT_TIME'] = line[122:148]
				if log['COMPONENT'][:4] == 'MMCS':
					if log['ERRCODE'][:14] == 'SERVER_STARTED' or log['ERRCODE'][:16] == 'SERVER_RESTARTED' or log['ERRCODE'][:18] == 'SERVER_TERMINATION' or log['ERRCODE'][:17] == 'BGPMASTER_STARTED' or log['ERRCODE'][:17] == 'BGPMASTER_STOPPED':
						log['PROCESSOR'] = ''.join([' ' for i in range(11)]) # empty
						log['BLOCK'] = ''.join([' ' for i in range(32)]) # empty
						log['LOCATION'] = ''.join([' ' for i in range(64)]) # empty
						msg = line[158:].strip()
						log['MESSAGE'] = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
					elif log['ERRCODE'][:16] == 'KILL_JOB_TIMEOUT':
						log['PROCESSOR'] = ''.join([' ' for i in range(11)]) # empty
						log['BLOCK'] = line[154:186]
						log['LOCATION'] = ''.join([' ' for i in range(64)]) # empty
						msg = line[258:].strip()
						log['MESSAGE'] = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
					else:
						log['PROCESSOR'] = ''.join([' ' for i in range(11)]) # empty
						log['BLOCK'] = ''.join([' ' for i in range(32)])
						log['LOCATION'] = line[155:219]
						msg = line[224:].strip()
						log['MESSAGE'] = msg + ''.join([' ' for i in range(1024 - len(msg))]) + '\n'
				elif log['COMPONENT'][:9] == 'BAREMETAL' or log['COMPONENT'][:4] == 'CARD' or log['COMPONENT'][:2] == 'MC' or (log['COMPONENT'][:5] == 'DIAGS' and line[151] == ' '):
					log['PROCESSOR'] = ''.join([' ' for i in range(11)]) # empty
					log['BLOCK'] = line[154:186]
					log['LOCATION'] = line[189:253]
					log['MESSAGE'] = getMessage(line, f)
				else:
					log['PROCESSOR'] = ''.join([' ' for i in range(10)]) + line[151]
					log['BLOCK'] = line[155:187]
					log['LOCATION'] = line[190:254]
					log['MESSAGE'] = getMessage(line, f)
				json.dump(log, out_f)
				out_f.write('\n')
				out_f.flush()
				legal_cnt += 1
		except Exception as e:
			print 'Exception:', cnt
			unsolved_f.write(line)
			unsolved_f.write('\n')
			# exit()
	f.close()
	out_f.close()
	unsolved_f.close()


if __name__ == '__main__':
	parse('Intrepid_RAS_0901_0908_scrubbed')
