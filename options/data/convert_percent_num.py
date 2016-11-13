#!/usr/bin/python
import sys

output=file(sys.argv[2],'w')
with file(sys.argv[1]) as input:
	while True:
		line=input.readline()
		if len(line)==0:
			break
		towrite=[]
		for v in line.strip().split('\001'):
			if not v.endswith('%'):
				towrite.append(str(v))
			else:
				try:
					towrite.append(str(float(v[:-1])/100))
				except ValueError:
					towrite.append(str(v))
		output.write('%s\n'%'\001'.join(towrite))
output.close()
