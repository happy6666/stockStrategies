#!/usr/bin/python
import sys
def readProfile(f):
	result=dict()
	data=file(f).readlines()
	for line in data:
		line=line.strip().decode('utf8')
		if line.startswith('Code'):
			code=line[-6:]
			state=False
		if line.startswith(u'\u8bc1\u76d1\u4f1a\u6838\u51c6\u516c\u544a\u65e5'):
			state=False
		if line.startswith(u'\u65b9\u6848\u8fdb\u5ea6') and line.endswith(u'\u5df2\u5b9e\u65bd'):
			state=True
		if line.startswith(u'\u53d1\u884c\u65b0\u80a1\u65e5'):
			time=line[line.rfind('>')+1:].strip()
		if state and line.startswith(u'\u5b9e\u9645\u53d1\u884c\u4ef7\u683c'):
			if result.has_key(code):
				try:
					result[code].append((float(line[line.find('>')+1:line.rfind(u'\u5143')].strip()),time))
				except:
					pass
			else:
				try:
					result[code]=[(float(line[line.find('>')+1:line.rfind(u'\u5143')].strip()),time)]
				except:
					pass
	return result
		
def readPrice(f):
	data=file(f).readlines()
	result=dict()
	for line in data:
		line=line.strip()
		ss=line.split('\t')
		try:
			result[ss[0][2:]]=float(ss[2])
		except:
			pass
	return result

if __name__=='__main__':
	addtition=sys.argv[1]
	price=sys.argv[2]
	priceDict=readPrice(price)
	additionDict=readProfile(addtition)
	for k,v in priceDict.items():
		if additionDict.has_key(k):
			for p in additionDict[k]:
				if p[0]>v:
					print k,v,p[0],p[1]
