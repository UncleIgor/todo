#!/usr/bin/env python3

import re
#import sys
from datetime import datetime

def parsing_task(task_str):
    dsc_task=dict()

    if not task_str:
        return 1;

    if task_str.isspace():
        return dsc_task
    
    #Вычисляем отступ
    indent=re.match('^\s+', task_str)
    if indent:
        dsc_task['indent']=round(indent.end()/4)
    
    #Статус задачи
    if re.search('\[x\]', task_str):
        dsc_task['chekbox']=1        
    
    #Дата_начала 
    start_date=re.findall('\[(\d{1,2}\.\d{1,2}\.\d{2,4}).*\]', task_str)
    if start_date:
        dsc_task['start_date']=''.join(start_date)
        task_str=task_str.replace(dsc_task['start_date'], "", 1)
    
    #Дата_завершения
    close_date=re.findall('\[.*-.(\d{1,2}\.\d{1,2}\.\d{2,4}).*\]', task_str)
    if close_date:
        dsc_task['close_date']=''.join(close_date)
        task_str=re.sub('\[.-.\d{1,2}\.\d{1,2}\.\d{2,4}\]', '', task_str)
    
    #Теги
    dsc_task['tags']=re.findall(r'[@,+,#]\S+', task_str)
    if dsc_task['tags']:
        for tag in dsc_task['tags']:
            task_str=task_str.replace(tag, "")
            if "#pr:" in tag:
                dsc_task['prio']=int(tag.replace("#pr:", ""))

    #Содержание
    task_str=re.sub('\[\]', '', task_str)
    task_str=re.match('^\s*(.+)\s+', task_str)
    if task_str:
        dsc_task['content']=re.sub(r'\s\s+', '', task_str.group(1))

    return dsc_task

def processing_task(task):
    indent=task.get("indent", 0)
    tags=task.get("tags", None)
    content=task.get("content", None)

    #Пустые строки
    if not task:
        return task

    #Добавление даты начала
    if not task.get("start_date", None):
        # now = datetime.datetime.now()
        now = datetime.now()
        task["start_date"]=now.strftime("%d.%m.%Y")
    
    #Добавление даты завершения
    if task.get("chekbox", None) and not task.get("close_date", None) :
        # now = datetime.datetime.now()
        now = datetime.now()
        task["close_date"]=now.strftime("%d.%m.%Y")

    #Обработка тегов


    return task

def print_todo_2_file(todo_list):

    if not todo_list:
        print ("Пустое TODO")
        return 1

    try:
        tmp_f = open('./tmp/tmp_todo', 'w')
    except:
        print ("Не смог создать временный файл")
        return 2

    for task in todo_list:
        if not task:
            tmp_f.write('\n')
            continue

        content=task.get("content", None)
        indent=task.get("indent", 0)
        start_date=task.get("start_date", "")
        chekbox=task.get("chekbox", None)
        close_date=task.get("close_date", None)
        tags=' '.join(task.get("tags", ""))
        indent=''.rjust(indent*4, " ")

        if close_date and chekbox:
            date='[{0} - {1}]'.format(start_date, close_date)
        else:
            date='[{0}]'.format(start_date)

        tmp_f.write(''.join("%s%-80s %s %s\n" % (indent, content, date, tags)))
        
    tmp_f.close()

def sort_by_prio(todo_list):
    if not todo_list:
        print ("Пустое TODO")
        return 1

    sort_todo=[]
    
    for task in todo_list:
        if not task:
            continue
        
        indent=task.get("indent", 0)
        prio=task.get("prio", -1)
        print(prio)

def cmp_date(date):
    date2 = datetime.now()
    date1 = datetime.strptime(date, "%d.%m.%Y") 
    delta = date2 - date1
    return delta.days

def print_2_chlog(task):
    try:
        chlog_f = open('./tmp/new_chlog', 'a')
    except:
        print ("Нет файла для дозаписи")
        return 2

    if not task:
        chlog_f.write('\n')
        chlog_f.close()
        return 0

    content=task.get("content", None)
    indent=task.get("indent", 0)
    start_date=task.get("start_date", "")
    close_date=task.get("close_date", None)
    tags=' '.join(task.get("tags", ""))
    
    if close_date:
        date='[{0} - {1}]'.format(start_date, close_date)
    else:
        date='[{0}]'.format(start_date)
    indent=''.rjust(indent*4, " ")

    chlog_f.write(''.join("%-80s %s %s\n" % (content, date, tags)))
        
    chlog_f.close()

def main(file_name):
    idx_deph=list()
    idx_deph.append(-1)
    todo_list=list()

    try:
        file_handler = open(file_name, 'r', encoding="utf-8")
    except IOError:
        print("Файла не существует")
        exit(1)
    
    for line in file_handler:
        task=parsing_task(line)
        task=processing_task(task)        
        close_date=task.get("close_date", None)
        if close_date and (cmp_date(close_date) > 2):
            print_2_chlog(task)
            continue
        todo_list.append(task)      
    file_handler.close()
    print_todo_2_file(todo_list)

#if __name__ == "__main__" and (len (sys.argv) != 2):
#    print ("Ошибка входных параметров параметров.")
#    sys.exit (1)    
# param_value = sys.argv[1]
# print(param_value)
# main(sys.argv[1])   
main("test_todo.txt")

exit(0)

