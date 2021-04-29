#!/usr/bin/env python3

import re
import datetime

def parsing_task(task_str):
    dsc_task=dict()

    if not task_str:
        return 1;

    if task_str.isspace():
        return dsc_task
    
    #Вычисляем отступ
    indent=re.match('^\s+', task_str)
    if indent:
        dsc_task['indent']=round(indent.end()/4)*4
    
    #Статус задачи
    if re.search('\[x\]', task_str):
        dsc_task['chekbox']=1        

    #Дата_начала 
    start_date=re.findall('\[(\d{1,2}\.\d{1,2}\.\d{2,4}).*\]', task_str)
    if start_date:
        dsc_task['start_date']=''.join(start_date)
        task_str=task_str.replace(dsc_task['start_date'], "")
    
    #Дата_завершения
    close_date=re.findall('\[.-.(\d{1,2}\.\d{1,2}\.\d{2,4})\]', task_str)
    if close_date:
        dsc_task['close_date']=''.join(close_date)
        task_str=re.sub('\[.-.(\d{1,2}\.\d{1,2}\.\d{2,4})\]', '', task_str)
        
    #Теги
    tags = re.findall(r'[@,+,#]\S+', task_str)
    if tags:
        dsc_task['tags']=' '.join(tags)
        for tag in tags:
            task_str=task_str.replace(tag, "")

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
        now = datetime.datetime.now()
        task["start_date"]=now.strftime("%d.%m.%Y")
    
    #Добавление даты завершения
    if task.get("chekbox", None):
        now = datetime.datetime.now()
        task["close_date"]=now.strftime("%d.%m.%Y")

    #Обработка тегов

    return task

def print_todo_2_file(todo_list):

    if not todo_list:
        print ("Пустое TODO")
        return 1

    try:
        tmp_f = open('tmp', 'w')
    except:
        print ("Не смог создать временный файл")
        return 2

    for task in todo_list:
        if not task:
            tmp_f.write('\n')
            continue

        content=task.get("content", None)
        indent=task.get("indent", 0)
        chekbox=task.get("chekbox", "")
        start_date=task.get("start_date", "")
        close_date=task.get("close_date", None)
        tags=task.get("tags", "")
                
        if close_date:
            date='[{0} - {1}]'.format(start_date, close_date)
        else:
            date='[{0}]'.format(start_date)

        indent=''.rjust(indent, " ")

        tmp_f.write(''.join("%s%-80s %-27s %s\n" % (indent, content, date, tags)))
        
    tmp_f.close()

def main(file_name):
    todo_list = list();

    try:
        file_handler = open(file_name, 'r', encoding="utf-8")
    except IOError:
        print("Файла не существует")
        exit(1)
    
    for line in file_handler:
        task=parsing_task(line)
        task=processing_task(task)
        todo_list.append(task)
    file_handler.close()

    #Сортировка
    print_todo_2_file(todo_list)

main("TODO")


