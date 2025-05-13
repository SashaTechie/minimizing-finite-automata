#Библиотека функций грамматики
import GrammarRework as gr
#Таблица
import Example
#Регулярки
import re

def handle_option_1():
    print("1. РАСЧЁТ ВАРИАНТА ЗАДАНИЯ\n")
    grammar = Example.example_table()


    print("Ваша грамматика:")
    print(gr.format_table(grammar))
    gr.draw_graph(grammar)

    print("\nОбработка недостижимых состояний:")
    gr.remove_unavailability(grammar)

    print("\nОбработаем эквивалентные состояния:")
    gr.merge_equivalents(grammar)
    print(gr.format_table(grammar))

    gr.draw_graph(grammar)

    print()

def handle_option_2():
    print("2. ВВОД СОБСТВЕННОЙ ГРАММАТИКИ\n")

    user_input_non_t = input("Введите количество нетерминалов (1-26): ")
    while not re.match(r'^[1-9]|1[0-9]|2[0-9]$', user_input_non_t):
        user_input_non_t = input("Введите количество нетерминалов (1-26): ")
    user_input_non_t = int(user_input_non_t)

    user_input_t = input("Введите количество терминалов (1-26): ")
    while not re.match(r'^[1-9]|1[0-9]|2[0-9]$', user_input_t):
        user_input_t = input("Введите количество терминалов (1-26): ")
    user_input_t = int(user_input_t)

    grammar = gr.generate_undetermined_grammar_sheet(user_input_non_t, user_input_t)

    print("Ваша грамматика:\n" + gr.format_table(grammar), end="\n\n")

    print()

flag = True
while flag:
    print("Меню:\n"
          "1. Произвести расчёт варианта задания.\n"
          "2. Ввести собственную грамматику.\n"
          "3. Выход.\n")

    menu_selector = input("Введите пункт меню: ")
    if menu_selector == "1":
        handle_option_1()
    elif menu_selector == "2":
        handle_option_2()
    elif menu_selector == "3":
        flag = False
    else:
        print("\nВведите верный пункт меню!\n")
