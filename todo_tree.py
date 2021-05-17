#!/usr/bin/env python3

from operator import add
import re
from datetime import datetime
from anytree import Node, RenderTree, Walker,  Resolver 

#Количество дней до переноса задачи в Chenge_log (PS После даты закрытия)
CHECK_DAYS=2
#Приоритет задачи по умолчанию
DEFAULT_TASK_PRIO=100

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
    # indent=task.get("indent", 0)
    # tags=task.get("tags", None)
    # content=task.get("content", None)

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

def cmp_date(date):
    date2 = datetime.now()
    date1 = datetime.strptime(date, "%d.%m.%Y") 
    delta = date2 - date1
    return delta.days

def print_task(Node):
    f_open="./tmp/todo"
    
    try:
        task=Node.task
    except:
        return 0

    content=task.get("content", None)
    indent=task.get("indent", 0)
    start_date=task.get("start_date", "")
    close_date=task.get("close_date", None)
    tags=' '.join(task.get("tags", ""))
    
    if close_date:
        date='[{0} - {1}]'.format(start_date, close_date)
        if cmp_date(close_date) > CHECK_DAYS:   
            f_open="./tmp/chlog"
    else:
        date='[{0}]'.format(start_date)
    
    try:
        file_dest = open(f_open, 'a', encoding="utf-8")
    except:
        print ("Не смог открыть", f_open)
        return 2

    if indent == 0 and file_dest.tell() != 0:
        file_dest.write("\n")
    indent=''.rjust(indent*4, " ")
    
    file_dest.write(''.join("%s%-80s %s %s\n" % (indent, content, date, tags)))
    file_dest.close()
    
    return 0

def print_tree(todo_tree):
    print_task(todo_tree)
    if len(todo_tree.children) == 0:
        return 0
    for child in sorted(todo_tree.children, key=lambda x: x.task.get("prio", DEFAULT_TASK_PRIO)):
        print_tree(child)
    return 0 

def main(file_name):
    puth_task=list(range(1))
    prev_indent=0

    idx_deph=list()
    root=Node("root")
    
    try:
        file_handler = open(file_name, 'r', encoding="utf-8")
    except IOError:
        print("Файла не существует")
        exit(1)
    
    for line in file_handler:
        task=parsing_task(line)
        task=processing_task(task)

        indent=task.get("indent", 0)
        idx_deph.insert(indent, None)
        content=task.get("content", "\n")
        
        #Пропуск пустых строк
        if (indent == 0) and (content == "\n"):
            continue
        
        #Вычисление имени узла
        if indent == prev_indent:
            puth_task[prev_indent]+=1
        elif indent > prev_indent:
            prev_indent=indent
            puth_task.insert(prev_indent, 0)
        elif indent < prev_indent:
            for number in range(prev_indent-indent):
                puth_task.pop(-1)
            prev_indent=indent
        puth_task[prev_indent]+=1
        name_task=puth_task[-1]
        
        #Добавление к дереву
        if indent == 0:
            idx_deph[indent]=Node(name_task, parent=root, task=task)
            continue
        idx_deph[indent]=Node(name_task, parent=idx_deph[indent-1], task=task)    

    file_handler.close()
    
    file_dest = open("./tmp/todo", 'w')
    file_dest.close()   
    file_dest = open("./tmp/chlog", 'w')
    file_dest.close()   
    
    print_tree(root)

main("test_todo.txt")

exit(0)
