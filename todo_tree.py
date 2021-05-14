#!/usr/bin/env python3

from operator import add
import re
import datetime
from anytree import Node, RenderTree, Walker,  Resolver 

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
        task_str=task_str.replace(dsc_task['start_date'], "")
    
    #Дата_завершения
    close_date=re.findall('\[.-.(\d{1,2}\.\d{1,2}\.\d{2,4})\]', task_str)
    if close_date:
        dsc_task['close_date']=''.join(close_date)
        task_str=re.sub('\[.-.(\d{1,2}\.\d{1,2}\.\d{2,4})\]', '', task_str)
        
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
        tags=' '.join(task.get("tags", ""))
        
        if close_date:
            date='[{0} - {1}]'.format(start_date, close_date)
        else:
            date='[{0}]'.format(start_date)

        indent=''.rjust(indent*4, " ")

        tmp_f.write(''.join("%s%-80s %s %s\n" % (indent, content, date, tags)))
        
    tmp_f.close()

def print_tree_old(todo_tree):
    todo_list=list()
    # получить кол детей 
    # если 0:
    #     отправить на печать
    #     выход
    # если >1 отсортировать по приоритету
    # рекурсия ин

    size_ch=len(todo_tree.children)
    if size_ch == 0:
        print(todo_tree.task.get("content", None))
        return 0
    
    for child in todo_tree.children:
        prio=child.task.get("prio", 100)
        print
        todo_list.insert(prio, child)
    
    for child in todo_list:
        print(child.task.get("content", None))
        #if len(child.children) > 0 :
        #    print_tree(child)
        #task=child.task
        #print(task.get("content", None))
    return 0

def print_tree1(todo_tree):
    todo_list=Node("root1")
    # получить кол детей 
    # если 0:
    #     отправить на печать
    #     выход
    # если >1 отсортировать по приоритету
    # рекурсия ин

    size_ch=len(todo_tree.children)
    if size_ch == 0:
        print(todo_tree.task.get("content", None))
        return 0
    
    for child in todo_tree.children:
        prio=child.task.get("prio", None)
        if prio == 1:
            todo_list.insert()
    
    for child in todo_list:
        if len(child.children) > 0 :
            print_tree(child)
        task=child.task
        print(task.get("prio", None))
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

    print_tree(root)

    #w = Walker()
    #res=w.walk(root, root)
    #print(res)
    

main("test_todo.txt")

exit(0)

# #Вычисление имени узла2
#         size_path=len(ddd)
#         if size_path < indent:
#             ddd.insert(indent,0)
#         elif size_path > indent:
#             ddd[-1]+=1
#         elif size_path == indent:
#             print(size_path,  indent)
#             ddd[indent-1]+=1
#             for num in range(size_path-indent):
#                 ddd[size_path-num]=0


puth_task=list()
puth_task.insert(0,0)
prev_indent=0
indent_mas=(0, 0, 1, 2, 2, 1, 2, 2, 3, 3, 0, 1, 0)

for cur_indent in indent_mas:    
    if cur_indent == prev_indent:
        puth_task[prev_indent]+=1
    elif cur_indent > prev_indent:
        prev_indent=cur_indent
        puth_task.insert(prev_indent, 0)
    elif cur_indent < prev_indent:
        for number in range(prev_indent-cur_indent):
            puth_task.pop(-1)
        prev_indent=cur_indent
        puth_task[prev_indent]+=1
    str='.'.join("{0}".format(n) for n in puth_task)

    print("Путь строки", str)



# depth - переключатель глубины
# last_depth_idx - последний индекс на текущей глубине
# cur_depth - текщая глубина
# prev_depth - глубина предыдущей задачи
# idx_deph_mas - массив индексов на каждой глубине [0, 0, 0]


# def save_task(puth, task):
#     db_list=TODO_DB
#     interator=0
#     print(puth)
#     size_puth=len(puth)
#     for node in puth:
#         interator+=1
#         print(interator, size_puth)
#         if interator > size_puth:
#             db_list=list()
#             db_list.append(task)
#             return 0
#         # try:
        
#         if node == 0:
#             print(node, len(db_list))
#             db_list=db_list[node]
#         else:
#             db_list=db_list[node-1]
#         # except:
#         #     db_list.insert(node, task)
#         #     return 0
#     #print("----------------------")

# TODO_DB=list()
# idx_deph=list()
# idx_deph.append(-1)
# depth=0
# indent=(0, 0, 1, 2, 2, 1, 2, 2, 3, 3, 0, 1, 0)

# for cur_depth in indent:    
#     if cur_depth == depth:
#         idx_deph[depth]+=1
#     elif cur_depth > depth:
#         depth=cur_depth
#         idx_deph.insert(depth, 0)
#     elif cur_depth < depth:
#         up_depth=depth-cur_depth
#         for number in range(up_depth):
#             idx_deph.pop(-1)
#             depth=cur_depth
#             idx_deph[depth]+=1
#     #print("Путь строки", idx_deph)
#     
# save_task(idx_deph, list(range(5)))
#     #print(TODO_DB)
#         #TODO_DB.append(list(range(1)))
# print(TODO_DB)

    # if cur_depth == depth:
    #     idx_deph[depth]+=1
    # elif cur_depth > depth:
    #     depth=cur_depth
    #     idx_deph.insert(depth, 0)
    # elif cur_depth < depth:
    #     up_depth=depth-cur_depth
    #     for number in range(up_depth):
    #         idx_deph.pop(-1)
    #     depth=cur_depth
    #     idx_deph[depth]+=1
    # save_task(idx_deph)        
#    print("Путь строки", idx_deph)



        # if cur_depth == depth:
        #     #Узел добавления остается прежний
        #     idx_deph[depth]+=1
        # elif cur_depth > depth:
        #     #Узел добавления меняется на предыдущего
        #     depth=cur_depth
        #     idx_deph.insert(depth, 0)
        # elif cur_depth < depth:
        #     #Узел добавления переключается вверх на одного
        #     up_depth=depth-cur_depth
        #     for number in range(up_depth):
        #         idx_deph.pop(-1)
        #     depth=cur_depth
        #     idx_deph[depth]+=1
        # print("Путь строки", idx_deph)
