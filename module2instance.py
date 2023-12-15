import os
import re
import sys
import argparse

delimiter = " "

if len(sys.argv)==1: sys.exit("Error: ther is no input file added as argument!")
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

data4 = ""
with open ('port_list_clean.txt') as f:
    data4 = f.read()

maxLen = len(max(re.findall(r"^\S+", data4, re.M), key=len))
minLen = len(min(re.findall(r"^\S+", data4, re.M), key=len))
data4 = ""

with open('port_list_clean.txt') as f:
    port_lines = f.read().splitlines()
with open('port_list_clean1.txt', 'w') as newf:
    for line in port_lines:
        Len = len(line)
        print('     .' + line + " "*(maxLen+2-Len) + '( ', file=newf)

with open("clean.txt") as xh:
  with open('port_list_clean1.txt') as yh:
    with open("port_list_clean2.txt","w") as zh:
      xlines = xh.readlines()
      ylines = yh.readlines()
      for i in range(len(xlines)):
        line = ylines[i].strip() + ' ' + xlines[i]
        zh.write(line)

with open('port_list_clean2.txt') as f:
    port_lines = f.read().splitlines()
with open('port_list_clean3.txt', 'w') as newf:
    for line in port_lines:
        Len = len(line)
        print(line + " "*(3*maxLen-minLen-Len) + '),', file=newf)

with open('port_list_clean3.txt','r') as f , open('port_list_clean4.txt', 'w') as newf:
    while True:
        line = f.readline()
        if not line:
           break
        line = '        ' + line
        newf.write(line)

with open('port_list_clean4.txt', 'r') as f:
    for count, line in enumerate(f):
        pass

with open('port_list_clean4.txt', 'r') as f: 
    data = f.readlines() 
data[count] = data[count].replace("),", ") );" )
  
with open('instance.txt', 'w') as f: 
    f.writelines(data)


data3 = ""
data2 = ""
data1 = ""
with open('module_name_n.txt') as file:
    data3 = file.read()

with open('wire_list.txt') as file:
    data1 = file.read()
 
with open('instance.txt') as f2:
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
 
with open ('module_instance.txt', 'w') as f:
    f.write(data1)

data3 = ""
data2 = ""
data1 = ""
########## REMOVE ALL THE MESS ###########
if os.path.exists('port_list_filter.txt'):
    os.remove('port_list_filter.txt')
if os.path.exists('port_list_clean.txt'):
    os.remove('port_list_clean.txt')
if os.path.exists('port_list_clean1.txt'):
    os.remove('port_list_clean1.txt')
if os.path.exists('port_list_clean2.txt'):
    os.remove('port_list_clean2.txt')
if os.path.exists('port_list_clean3.txt'):
    os.remove('port_list_clean3.txt')
if os.path.exists('port_list_clean4.txt'):
    os.remove('port_list_clean4.txt')
if os.path.exists('wire_list.txt'):
    os.remove('wire_list.txt')
if os.path.exists('wire_list_new.txt'):
    os.remove('wire_list_new.txt')
if os.path.exists('instance.txt'):
    os.remove('instance.txt')
if os.path.exists('clean.txt'):
    os.remove('clean.txt')
if os.path.exists('module.txt'):
    os.remove('module.txt')
if os.path.exists('module_name_instance.txt'):
    os.remove('module_name_instance.txt')
if os.path.exists('module_name.txt'):
    os.remove('module_name.txt')
if os.path.exists('module_name_n.txt'):
    os.remove('module_name_n.txt')



