#!/usr/bin/env python

import os
import sys
import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

Config = ConfigParser.ConfigParser()
#print sys.argv[1]
Config.read(sys.argv[1])
#print Config.sections()
#print ConfigSectionMap("bwa")

if os.path.isfile("bwa.done"):
  print "bwa already done. proceeding..."
else:
  print "starting bwa..."
  bwa_param = ConfigSectionMap("bwa")
  bwa_cmd = "bwa mem -t 12 "+bwa_param["index"]+" "+bwa_param["read1"]+" "+bwa_param["read2"]+" | samtools -bS - > alignment.bam"
  print bwa_cmd
  #os.system(bwa_cmd)
  sort_cmd = "samtools sort alignment.bam -o alignment_sorted.bam"
  print sort_cmd
  #os.system(sort_cmd)
  index_cmd = "samtools index alignment_sorted.bam"
  print index_cmd
  #os.system(index_cmd)
  filter_cmd = "samtools view -q 30 alignment_sorted.bam > alignment_sorted_filtered.bam"
  print filter_cmd
  #os.system(filter_cmd)

  #finally touch bwa.done
  os.system("touch bwa.done")

if os.path.isfile("bamCoverage.done"):
  print "bamCoverage already done. proceeding..."
else:
  print "starting bamCoverage..."
  #bamCoverage -b d1_pilon_sorted_filtered.bam -o d1_pilon_sorted_filtered2.bw --normalizeTo1x 825526369 --binSize 10
  bamcov_param = ConfigSectionMap("bamCoverage")
  bamcov_cmd = "bamCoverage -b alignment_sorted_filtered.bam -o alignment_sorted_filtered.bw --normalizeTo1x "+bamcov_param["genomesize"]+" --binSize "+bamcov_param["binsize"]
  print bamcov_cmd
  #os.system(bamcov_cmd)
