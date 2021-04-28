#!/usr/bin/env python3

import re

DEF_TASK_PARAMS=(("dates", 0), ("content", 0), ("tags", 0), ("indent", 0), ("chekbox", 0))

def reset_dict():
    dsc_task.clear()
    dsc_task['chekbox']=0 #bool
    dsc_task['content']=None
    dsc_task['dates']=None
    dsc_task['tags']=None
    dsc_task['indent']=0 #int
    dsc_task['prio']=0 #int

def parsing_task(in_str):
    dsc_task=dict()

    if not in_str:
        return 1;

    if in_str.isspace():
        return dsc_task
    
    #Вычисляем отступ
    indent=re.match('^\s+', in_str)
    if indent:
        dsc_task['indent']=(indent.end()//4)*4
    
    #Статус задачи
    if re.search('\[x\]', in_str):
        dsc_task['chekbox']=1        

    #Дата 
    date=re.findall('\[(\d{1,2}\.\d{1,2}\.\d{2,4}.*)\]', in_str)
    if date:
        dsc_task['dates']=''.join(date)
    
    #Теги
    dsc_task['tags']="NO_ЕФПЫ"
    tags = re.findall(r'[@,+,#]\S+', in_str)
    
    return dsc_task
    

    dsc_task['content'] = re.sub(r"\[x\]|\s+", ' ', in_str)
    
    if dsc_task['dates']:
       print(1)
       dsc_task['content'] = re.findall(r'^\s*(.+)\s+\[', dsc_task['content'])
    else:
       print(2)
       dsc_task['content'] = re.findall(r'^\s*(.+)\s*', dsc_task['content'])

    #print (dsc_task['content'])
    tags = re.findall(r'[@,+,#]\S+', in_str)
    if tags:
        dsc_task['tags']=tags
        myString = ''.join(dsc_task['content'])
        for list_pattern in dsc_task['tags']:
            myString = myString.replace(list_pattern, '')
            #print (myString)
        dsc_task['content'] = myString
    #print ("Стока:", num_in_str, "Состояние", dsc_task['chekbox'], dsc_task['dates'], dsc_task['content'], "Отступ", dsc_task['indent'], dsc_task['tags'])
    return 0

def add_def_params_2_task(task):
    if not task:
        return dict()

    for parameters in DEF_TASK_PARAMS:
        parameter, value = parameters
        if not parameter in task:
            task[parameter]=value
    
    return task

def processing_task(task):
    if not task or task[content] == 0:
        return "EMPTY_STR"
    return "blablabla"


def print_task(task):
    if not task:
        print ("Пустая строка")
        return 0

    print(task, len(task) )
    return 0
    for item in task:
        if not task['dates']:
            task['dates']=""

    print("Отступ:", task['indent'], "Статус:", task['chekbox'], "Дата:", task['dates'])
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

def main(file_name):
    todo_list = list();

    try:
        file_handler = open(file_name, 'r')
    except IOError:
        print("Файла не существует")
        exit(0)
        
    for line in file_handler:
        task=parsing_task(line)
        task=add_def_params_2_task(task)
        task=processing_task(task)
        print_task(task)
    file_handler.close()

main("TODO")


