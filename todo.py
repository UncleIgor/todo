#!/usr/bin/env python3

import re

STR_COUNT=0
FULL_LINE=""
DOC_LIST = list();

def reset_dict():
    DSC_TASK.clear()
    DSC_TASK['chekbox']=0 #bool
    DSC_TASK['content']=None
    DSC_TASK['dates']=None
    DSC_TASK['tags']=None
    DSC_TASK['indent']=0 #int
    DSC_TASK['prio']=0 #int

def parsing_task(line, num_line):
    
    line = re.sub("\n|\r", '', line)
    if not line:
        DSC_TASK['content']=None
        return 2
    
    reset_dict()
    
    DSC_TASK['indent']=re.match('^\s+', line)

    if re.search(r'\[x\]', line):
        DSC_TASK['chekbox'] = 1        
    
    DSC_TASK['dates'] = re.findall(r'\[(\d{1,2}\.\d{1,2}\.\d{2,4}.*)\]', line)

    DSC_TASK['content'] = re.sub(r"\[x\]|\s+", ' ', line)
    
    if DSC_TASK['dates']:
       print(1)
       DSC_TASK['content'] = re.findall(r'^\s*(.+)\s+\[', DSC_TASK['content'])
    else:
       print(2)
       DSC_TASK['content'] = re.findall(r'^\s*(.+)\s*', DSC_TASK['content'])

    #print (DSC_TASK['content'])
    tags = re.findall(r'[@,+,#]\S+', line)
    if tags:
        DSC_TASK['tags']=tags
        myString = ''.join(DSC_TASK['content'])
        for list_pattern in DSC_TASK['tags']:
            myString = myString.replace(list_pattern, '')
            #print (myString)
        DSC_TASK['content'] = myString
    #print ("Стока:", num_line, "Состояние", DSC_TASK['chekbox'], DSC_TASK['dates'], DSC_TASK['content'], "Отступ", DSC_TASK['indent'], DSC_TASK['tags'])
    return 0

def print_format_task():
    chekbox=""
    indent=""
    tags=""
    
    tmp_f = open('tmp', 'w')
    for task in DOC_LIST:
        print(task['content'])
        if task['tags'] != None:
            tags=''.join(task['tags'])
        
        if task['chekbox'] == 1:
            chekbox="[x]"
            
        if task['dates'] == None:
            dates="[11.22.3333]"
        else:
            dates=''.join("%s" % task['dates'])
        
        if task['content'] != None:
            myString=''.join("%s%3s %-80s %-27s %s\n" % (indent, chekbox, task['content'], dates, tags))
        else:
            myString='\n'
        
        tmp_f.write(myString)
    
    tmp_f.close()

try:
    with open("TODO", encoding="utf-8") as file_handler:
        for line in file_handler:
            
            STR_COUNT+=1
            #print(STR_COUNT)
            result=re.search(r'/$', line)
            if result != None:
                FULL_LINE+=line 
                continue
            if FULL_LINE:
                line=FULL_LINE+line
                FULL_LINE=""    

            #if parsing_task(line, STR_COUNT) == 2:
                #tmp_todo.write("\n")
             #   continue
            parsing_task(line, STR_COUNT)
            DOC_LIST.append(DSC_TASK.copy())

except IOError:
    print("Файла не существует")
    exit(0)

print_format_task()

