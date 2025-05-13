#Таблица
import pandas as pd
from tabulate import tabulate
#Латиница
from string import ascii_lowercase, ascii_uppercase
#Граф
import networkx as nx
import matplotlib.pyplot as plt
#Регулярки
import re

def generate_undetermined_grammar_sheet(nonterminals_count, terminals_count):
    #Первая строка - F, S, нетерминалы
    field_names = (
            ["f"] +
            ["S"] +
            [nonterminal for nonterminal in ascii_uppercase[:nonterminals_count] if nonterminal not in {"S"}]
    )
    table = pd.DataFrame(columns=field_names)

    #Первая колонка - терминалы, остальные ячейки - пустые строки
    for i in range(terminals_count):
        row = (
            [ascii_lowercase[i]] +
            ["" for _ in range(len(field_names) - 1)]
        )
        table.loc[i] = row

    #Вывод: незаполненная таблица
    print("Ваша незаполненная таблица:")
    print(format_table(table), end="\n\n")

    #Ручной ввод грамматики в таблицу
    for lin in range(terminals_count):
        for col in range(1, nonterminals_count + 2):
            table.iloc[lin, col] = "INPUT"
            print(format_table(table.iloc[[lin]]))

            user_input = input("Введите заместо 'INPUT': ")
            while not re.match(r"^[A-Z](,[A-Z])*$", user_input):
                print("Неверный ввод!")
                user_input = input("Введите заместо 'INPUT': ")
            table.iloc[lin, col] = user_input

    #Добавим столбец N после ввода грамматики
    table["N"] = "-"
    return table

def define_unavailability(table=pd.DataFrame()):
    # Ключ: состояния, значение: количество входов (по умолч. = 0)
    unavailability = {header: 0 for header in table.columns[2:]}
    for lin in range(table.shape[0]):
        for col in range(1, table.shape[1]):
            terminal = table.iloc[lin, col]
            if terminal in table.columns:
                unavailability[terminal] += 1
    return unavailability

def remove_unavailability(table=pd.DataFrame()):
    while True:
        unavailability = define_unavailability(table)
        print("Количество переходов в состояния:")
        for key, value in unavailability.items():
            print(f"{key}: {value}")

        cols_to_remove = []
        for col in table.columns[2:]:
            if unavailability.get(col, 0) == 0:
                cols_to_remove.append(col)

        if not cols_to_remove:
            print("Все 'нулевые' состояния удалены.")
            break
        else:
            print("\nУдаляю 'нулевые' состояния: ", cols_to_remove)

        table.drop(columns=cols_to_remove, inplace=True)

    return table

def define_equivalents(table=pd.DataFrame()):
    transitions = {}
    for lin in range(table.shape[0]):
        for col in range(1, table.shape[1]):
            non_terminal = table.iloc[lin, 0]
            transitions[non_terminal] = {}

    for lin in range(table.shape[0]):
        for col in range(1, table.shape[1]):
            non_terminal = table.iloc[lin, 0]
            terminal = table.columns[col]
            value = table.iloc[lin, col]
            if value != "-":
                transitions[non_terminal][terminal] = value
    print("Все состояния:")
    for key, value in transitions.items():
        print(f"{key}: {value}")

    equivalents = []
    for key, nested_dictionary in transitions.items():
        if len(nested_dictionary) <= 1:
            continue

        items = list(nested_dictionary.items())

        for i in range(len(items) - 1):
            trans_key, trans_value = items[i]

            for j in range(i + 1, len(items)):
                next_key, next_value = items[j]

                if trans_value == next_value:
                    equivalents.append((trans_key, next_key))
    return equivalents

def merge_equivalents(table=pd.DataFrame()):
    while True:
        equivalents = define_equivalents(table)

        if not equivalents:
            break

        print("Ваши эквивалентные состояния: ", equivalents)

        column_to_pop = equivalents[0][1]
        column_to_rename = equivalents[0][0]
        new_name = equivalents[0][0] + equivalents[0][1]

        for lin in range(table.shape[0]):
            for col in range(1, table.shape[1]):
                if table.iloc[lin, col] == column_to_pop or table.iloc[lin, col] == column_to_rename:
                    table.iloc[lin, col] = new_name

        table.drop(column_to_pop, axis=1, inplace=True)
        table.rename(columns={column_to_rename: new_name}, inplace=True)

    return table

def draw_graph(table=pd.DataFrame()):
    #Создаём граф и заполняем его вершинами названий колонок (кроме "F")
    column_names_list = table.columns.to_list()[1:]
    grammar_graph = nx.DiGraph()
    grammar_graph.add_nodes_from(column_names_list)

    for i in range(table.shape[0]):
        for j in range(1, table.shape[1]):
            source = table.iloc[i, j]
            if source == "-":
                continue
            else:
                grammar_graph.add_edge(table.columns[j], table.iloc[i, j], type=table.iloc[i, 0])

    #Рисуем граф без весов
    pos = nx.spring_layout(grammar_graph)
    nx.draw(grammar_graph,
            pos,
            with_labels=True,
            node_color='lightblue',
            node_size=1000,
            font_size=10)
    edge_labels = nx.get_edge_attributes(grammar_graph, 'type')

    #Рисуем веса
    nx.draw_networkx_edge_labels(grammar_graph, pos, edge_labels=edge_labels)

    plt.show()

def format_table(table):
    #Формирование любого вида таблицы (даже строки) с "шапкой"
    return tabulate(table, headers="keys", tablefmt="grid")

def format_dict(d):
    # Форматируем вывод
    formatted_output = []
    for key, values in d.items():
        formatted_output.append(f"{key} = ({', '.join(values)})")
    return "\n".join(formatted_output)
