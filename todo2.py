#!/usr/bin/env python3

import re
import json




todo = [
    [
        ident=0 
        content:"Задача 1"
        tags:[@tag1, @tag2, tag3]
        prio:1
    ],
    [
        ident:4; 
        content:" подзадача 1"; 
        tags:[@tag1, @tag2, tag3];
        prio:0;
    ],
    [
        ident:8; 
        content:" под-под-задача 1"; 
        tags:[@tag1, @tag2, tag3];
        prio:0;
    ],
    [
        ident:0; 
        content:"Задача 2"; 
        tags:[@tag1, @tag2, tag3];
        prio:0;
    ]
]


[
    {'chekbox': 0, 'content': 'Обучение Xilinx   ', 'dates': ['04.03.2021'], 'tags': ['@DVSDVSDCDS', '#sdfsdf', '+sdfd'], 'indent': 0}, 
    {'chekbox': 1, 'content': 'Найти куры по xilinx в СПБ вечернее время', 'dates': ['04.03.2021 - 05.03.2021'], 'tags': ['@VSDVDV'], 'indent': 4}, 
    {'chekbox': 1, 'content': 'Разработка Xilinx / Создать qemu-машину используя xsa-файл / Взять проект arbitor_puf и запустить его в qemu-машине', 'dates': ['04.03.2021'], 'tags': ['#id:123'], 'indent': 0}, 
    {'chekbox': 0, 'content': 'Посмотреть архитектуру doc_center', 'dates': ['04.03.2021'], 'tags': None, 'indent': 0}, 
    {'chekbox': 0, 'content': 'Нарисовать картинку "Первый взгляд на арх док центр"', 'dates': ['04.03.2021'], 'tags': None, 'indent': 4}, 
    {'chekbox': 0, 'content': 'Изменить обработку комментариев', 'dates': ['12.04.2021'], 'tags': None, 'indent': 4}, 
    {'chekbox': 1, 'content': 'Внести правки в документацию Doc center', 'dates': ['12.04.2021'], 'tags': None, 'indent': 4}, 
    {'chekbox': 0, 'content': 'Обсудить систему версий проектов - Долго не делается merge develop ветки в master', 'dates': None, 'tags': None, 'indent': 0}, 
    {'chekbox': 0, 'content': 'Задача 1', 'dates': None, 'tags': None, 'indent': 4}
] 