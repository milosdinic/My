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
        substituted_phrase = last_element.replace("endmodule", "" )
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
        substituted_phrase = substituted_phrase.replace("reg", "wire" )
        newfile.write(substituted_phrase.lstrip())

with open('wire_list_new.txt', 'r') as f:
    data = f.read()
    with open('wire_list.txt', 'w') as w:
        w.write(data[:-1])

right_words = ['wire']
with open('wire_list.txt') as oldfile, open('wire_lists.txt', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in right_words):
            line = 'wire      ' + line
            newfile.write(line)
        if any(bad_word in line for bad_word in right_words):
            newfile.write(line)

file = open('wire_lists.txt', 'a')
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


############## PARAMS START ######################################
with open(filename, 'r') as f, open ('params.txt', 'w') as nf:
    for line in f:
        if '#(' in line:
            for line in f:
                nf.write(line)
                if ')' in line:
                  break

with open('params.txt','r') as oldfile , open('params1.txt', 'w') as newfile:
    while True:
        line = oldfile.readline()
        if not line:
           break
        last_element = line
        substituted_phrase = last_element.replace("#(", "" )
        substituted_phrase = substituted_phrase.replace(")", "" )
        substituted_phrase = substituted_phrase.replace("parameter", "" )
        newfile.write(substituted_phrase)

with open('params1.txt','r') as f , open('params2.txt', 'w') as newf:
    while True:
        line = f.readline()
        if not line:
           break
        x = line.partition('=')
        line = x[0]
        new_line = line.replace(" ", "" )
        newf.write(new_line)
        newf.write('\n')

with open('params2.txt','r+') as f , open('params3.txt', 'w') as newf:
    for line in f:
        if line.rstrip() or not line.isspace():
            newf.write(line)
par=1
if os.stat("params2.txt").st_size == 0:
    par=0


data5 = ""
with open ('params3.txt') as f:
    data5 = f.read()

maxparamLen = len(max(open('params3.txt').readlines(), key=len))
minparamLen = len(min(open('params3.txt').readlines(), key=len))
data5 = ""

with open('params3.txt') as f:
    port_lines = f.read().splitlines()
with open('params4.txt', 'w') as newf:
    for line in port_lines:
        Len = len(line)
        print('     .' + line + " "*(maxparamLen+2-Len) + '( ' + line + " "*(3*maxparamLen-minparamLen-Len) + '),', file=newf)


with open('params4.txt', 'r') as f:
    for count, line in enumerate(f):
        pass

with open('params4.txt', 'r') as f: 
    data = f.readlines() 
data[count] = data[count].replace("),", ") )" )
  
with open('params5.txt', 'w') as f: 
    f.writelines(data)

paramdata1 = "( \n"
paramdata2 = ""

with open ('params5.txt') as f:
    paramdata2 = f.read()

paramdata1 += paramdata2
 
with open ('parameters.txt', 'w') as f:
    f.write(paramdata1)
    
paramdata1 = ""
paramdata2 = ""

############## PARAMS END   ######################################


############## COMBINE ALL START #################################
data5 = ""
data4 = ""
data3 = ""
data2 = ""
data1 = ""
with open('parameters.txt') as file:
    data5 = file.read()

with open('module_name.txt') as file:
    data3 = file.read()

with open('module_name_instance.txt') as file:
    data4 = file.read()

with open('wire_lists.txt') as file:
    data1 = file.read()
 
with open('instance.txt') as f2:
    data2 = f2.read()
 
data1 += "\n"
data1 += "\n"
data1 += data3
if par:
    data1 += data5
data1 += data4
data1 += "("
data1 += "\n"
data1 += data2
 
with open ('module_instance.txt', 'w') as f:
    f.write(data1)

data5 = ""
data4 = ""
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
if os.path.exists('wire_list1.txt'):
    os.remove('wire_list1.txt')
if os.path.exists('wire_list.txt'):
    os.remove('wire_list.txt')
if os.path.exists('wire_lists.txt'):
    os.remove('wire_lists.txt')
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
if os.path.exists('params.txt'):
    os.remove('params.txt')
if os.path.exists('params1.txt'):
    os.remove('params1.txt')
if os.path.exists('params2.txt'):
    os.remove('params2.txt')
if os.path.exists('params3.txt'):
    os.remove('params3.txt')
if os.path.exists('params4.txt'):
    os.remove('params4.txt')
if os.path.exists('params5.txt'):
    os.remove('params5.txt')
