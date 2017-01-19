import pandas
import matplotlib.pyplot as plt
import os
import subprocess
import sys
import string
import random

def id_generator():
  return ''.join(random.choice(string.lowercase) for i in range(6))


chrom=sys.argv[1]
start=sys.argv[2]
end=sys.argv[3]

tmpfile=id_generator()

os.system('bigWigToBedGraph -chrom='+chrom+' -start='+start+' end='+end+' d1_pilon_sorted_filtered2.bw '+tmpfile)
data=pandas.read_table(tmpfile,header=None)
data[3].plot(kind='density')
plt.show(block=True)
os.remove(tmpfile)

