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

if len(sys.argv)==1: sys.exit("Error: ther is no input file added as argument!")

import sys
filename = sys.argv[1]


#######  filter for module name ######################
right_words = ['module']
with open(filename) as oldfile, open('module.txt', 'w') as newfile:
    for line in oldfile:
        if any(bad_word in line for bad_word in right_words):
            newfile.write(line)

with open('module.txt','r') as oldfile , open('module_name.txt', 'w') as newfile:
    while True:
        line = oldfile.readline()
        if not line:
           break
        last_element = line.rsplit(delimiter, 1)[-1]
        substituted_phrase = last_element.replace("module", "" )
        substituted_phrase = substituted_phrase.replace("(", "" )
        substituted_phrase = substituted_phrase.replace("#(", "" )
        newfile.write(substituted_phrase)

with open('module_name.txt','r') as f , open('module_name_instance.txt', 'w') as newf:
    while True:
        line = f.readline()
        if not line:
           break
        line = '  i_' + line
        newf.write(line)

data4 = ''
with open('module_name.txt', 'r') as f:
    data = f.read()
    with open('module_name_n.txt', 'w') as w:
        w.write(data[:-1])

with open('module_name_instance.txt') as file:
    data4 = file.read()

file = open('module_name_n.txt', 'a')
file.write(data4)

data4 = ''


if os.path.exists('module_name.txt'):
    os.remove('module_name.txt')
if os.path.exists('module_name_instance.txt'):
    os.remove('module_name_instance.txt')
if os.path.exists('module.txt'):
    os.remove('module.txt')

#######  filter all non input or output lines #########
right_words = ['input', 'output']
with open(filename) as oldfile, open('port_list_filter.txt', 'w') as newfile:
    for line in oldfile:
        if any(bad_word in line for bad_word in right_words):
            newfile.write(line)


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
        x = line.partition('//')
        line = x[0]
        line = line.replace(", ", "\n" )
        line = line.replace(",", "" )
       # last_element = line.rsplit(delimiter, 1)[-1]
       # last_element = '.' + last_element
       # newf.write(last_element)
        last_element = line.rsplit()
        last = last_element[-1]
        newf.write(last)
        newf.write('\n')
######################   CLEAN   ######################
# clean.txt all in/out names
with open('port_list_clean.txt','r') as oldfile , open('clean.txt', 'w') as newfile:
    while True:
        line = oldfile.readline()
        if not line:
           break
        substituted_phrase = line.replace(",", "" )
        substituted_phrase = substituted_phrase.replace("_i", "_s" )
        substituted_phrase = substituted_phrase.replace("_o", "_s" )
        newfile.write(substituted_phrase)
#######################################################

with open("clean.txt") as xh:
  with open('port_list_clean.txt') as yh:
    with open("port_list_prep.txt","w") as zh:
      xlines = xh.readlines()
      ylines = yh.readlines()
      add    =  '),'
      for i in range(len(xlines)):
        line = ylines[i].strip() + '\t\t\t( ' + xlines[i]
        zh.write(line)

if os.path.exists('port_list_filter.txt'):
    os.remove('port_list_filter.txt')

with open('port_list_prep.txt') as f:
    lines = f.read().splitlines()
with open('port_list_ready.txt', "w") as f:
    for line in lines:
        print(line + "\t\t\t ),", file=f)

with open('port_list_ready.txt', 'r') as f:
    for count, line in enumerate(f):
        pass

with open('port_list_ready.txt', 'r') as f: 
    data = f.readlines() 
data[count] = data[count].replace("),", " ) );" )
  
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

with open('instance.txt','r') as f , open('instance_space.txt', 'w') as newf:
    while True:
        line = f.readline()
        if not line:
           break
        line = '        .' + line
        newf.write(line)

data3 = ""
data2 = ""
data1 = ""


with open('module_name_n.txt') as file:
    data3 = file.read()

with open('wire_list.txt') as file:
    data1 = file.read()
 
with open('instance_space.txt') as f2:
    data2 = f2.read()
 
data1 += "\n"
data1 += "\n"
data1 += data3
data1 += "\n"
data1 += "// #(  ) //CHECK FOR PARAMETERS!"
data1 += "\n"
data1 += "\n"
data1 += "("
data1 += "\n"
data1 += data2

# print(data)
 
with open ('module_instance.txt', 'w') as f:
    f.write(data1)

data3 = ""
data2 = ""
data1 = ""

if os.path.exists('module_name_n.txt'):
    os.remove('module_name_n.txt')
if os.path.exists('wire_list.txt'):
    os.remove('wire_list.txt')
if os.path.exists('instance_space.txt'):
    os.remove('instance_space.txt')
if os.path.exists('instance.txt'):
    os.remove('instance.txt')
