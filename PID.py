import os, json, time, IFTTT

def checkPID(pid):
	try: os.kill(pid,0)
	except OSError: return False
	else: return True

def openFile(): f = open(os.path.expanduser("~") + "/pid.txt"); g = f.read(); f.close(); return json.loads(g)

def updtFile(v): u = open(os.path.expanduser("~") + "/pid.txt", "w"); u.write(v); u.close()

def remCurrent(fname):
	cList = openFile()
	try: cList.pop(fname)
	except KeyError: pass
	else: updtFile(json.dumps(cList))

def addCurrent(fname, fnum): remCurrent(fname); updtFile(json.dumps(dict(openFile().items() + {fname: fnum}.items())))

def checkAll():
	cList = openFile(); keyList, valueList = list(), list()
	if not len(cList): exit()
	for key, value in cList.items():
		keyList.append(key); valueList.append(value)
	for k in range(0, len(keyList)):
		cKey = keyList[k]; cValue = valueList[k]
		if not checkPID(cValue):
			print "PID " + str(cValue) + " [" + cKey + "] exit."
			IFTTT.pushbots(
				"Detected PID " + str(cValue) + ", refrenced to " + cKey + " exit.",
				"Python Runtime Error", "", "raw", IFTTT.getkey()[0].split(), 0)
			remCurrent(cKey)

if __name__ == "__main__":
	while True: checkAll(); print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()); time.sleep(600)