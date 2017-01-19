import pandas
import matplotlib.pyplot as plt
import os
import subprocess
import sys
import string
import random

def id_generator():
  return ''.join(random.choice(string.lowercase) for i in range(6))

tmpfile=id_generator()

def find_peak(chrom,start,end):
  os.system('bigWigToBedGraph -chrom='+chrom+' -start='+start+' end='+end+' d1_pilon_sorted_filtered5.bw '+tmpfile)
  data=pandas.read_table(tmpfile,header=None)
  os.remove(tmpfile)
  return data[3].median()

hist1_data=pandas.read_table(sys.argv[1],header=None)
hist1=hist1_data.apply(lambda x: find_peak(x[0],str(x[1]),str(x[2])), axis=1)

hist2_data=pandas.read_table(sys.argv[2],header=None)
hist2=hist2_data.apply(lambda x: find_peak(x[0],str(x[1]),str(x[2])), axis=1)

result=hist2.apply(lambda x: float(sum(hist1>float(x)))/float(len(hist1)))

#print type(hist2)
#print type(result)
result2=pandas.concat([hist2,result],axis=1)
result2.to_csv('results.txt',sep='\t',index=False,header=False)

print result2
print sum(result<0.05)
print sum(result>0.95)

#testval=sys.argv[2]
#print float(sum(hist1>float(testval)))/float(len(hist1))

