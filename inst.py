import copy
import os
import re
import sys
import fnmatch
import argparse

if os.path.exists('clean.txt'):
    os.remove('clean.txt')
if os.path.exists('port_list_filter.txt'):
    os.remove('port_list_filter.txt')
if os.path.exists('port_list_new2.txt'):
    os.remove('port_list_new2.txt')
if os.path.exists('port_list_new3.txt'):
    os.remove('port_list_new3.txt')

delimiter = " "

#######  filter all non input or output lines ########
right_words = ['input', 'output']
with open('port_list.txt') as oldfile, open('port_list_filter.txt', 'w') as newfile:
    for line in oldfile:
        if any(bad_word in line for bad_word in right_words):
            newfile.write(line)

######################   CLEAN   ######################
# clean.txt all wire names
with open('port_list_filter.txt','r') as oldfile , open('clean.txt', 'w') as newfile:
    while True:
        line = oldfile.readline()
        if not line:
           break
        last_element = line.rsplit(delimiter, 1)[-1]
        substituted_phrase = last_element.replace(",", "" )
        substituted_phrase = substituted_phrase.replace("_i", "_s" )
        substituted_phrase = substituted_phrase.replace("_o", "_s" )
        newfile.write(substituted_phrase)

#################    WIREs    #########################
with open('port_list_filter.txt','r') as oldfile , open('wire_list_new.txt', 'w') as newfile:
    while True:
        line = oldfile.readline()
        if not line:
           break
        substituted_phrase = line.replace("input", "" )
        substituted_phrase = substituted_phrase.replace("output", "" )
        substituted_phrase = substituted_phrase.replace(",", ";" )
        substituted_phrase = substituted_phrase.replace("_i", "_s" )
        substituted_phrase = substituted_phrase.replace("_o", "_s" )
        newfile.write(substituted_phrase.lstrip())

with open('wire_list_new.txt', 'r') as f:
    data = f.read()
    with open('wire_list.txt', 'w') as w:
        w.write(data[:-1])

file = open('wire_list.txt', 'a')
file.write(';')

if os.path.exists('wire_list_new.txt'):
    os.remove('wire_list_new.txt')
#######################################################

with open('port_list_filter.txt','r') as f , open('port_list_clean.txt', 'w') as newf:
    while True:
        line = f.readline()
        if not line:
           break
        last_element = line.rsplit(delimiter, 1)[-1]
        last_element = '        .' + last_element
        substituted_phrase = last_element.replace(",", "" )
        newf.write(substituted_phrase)


with open("clean.txt") as xh:
  with open('port_list_clean.txt') as yh:
    with open("port_list_prep.txt","w") as zh:
      xlines = xh.readlines()
      ylines = yh.readlines()
      add    = '),'
      for i in range(len(xlines)):
        line = ylines[i].strip() + '(' + xlines[i]
        zh.write(line)

if os.path.exists('port_list_filter.txt'):
    os.remove('port_list_filter.txt')

with open('port_list_prep.txt') as f:
    lines = f.read().splitlines()
with open('port_list_ready.txt', "w") as f:
    for line in lines:
        print(line + "),", file=f)

with open('port_list_ready.txt', 'r') as f:
    for count, line in enumerate(f):
        pass

with open('port_list_ready.txt', 'r') as f: 
    data = f.readlines() 
data[count] = data[count].replace("),", ") );" )
  
with open('instance.txt', 'w') as f: 
    f.writelines(data)

if os.path.exists('port_list_prep.txt'):
    os.remove('port_list_prep.txt')
if os.path.exists('port_list_ready.txt'):
    os.remove('port_list_ready.txt')
if os.path.exists('clean.txt'):
    os.remove('clean.txt')
if os.path.exists('port_list_clean.txt'):
    os.remove('port_list_clean.txt')


data = data2 = "";

with open('wire_list.txt') as f1:
    data = f1.read()

with open('instance.txt') as f2:
    data2 = f2.read()
 
data += "\n"
data += "\n"
data += "\n"
data += "\n"
data += "("
data += "\n"
data += data2

print(data)
 
with open ('module_instance.txt', 'w') as f:
    f.write(data)

