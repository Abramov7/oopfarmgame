import dearpygui.dearpygui as dpg
import classes as cl

dpg.create_context()
dpg.create_viewport(title='Farming Simulator', width=1080, height=720)

years = []
global_food_price = 0
a = 0
money_curve = []


with dpg.theme() as green_button:
    with dpg.theme_component():
        dpg.add_theme_color(dpg.mvThemeCol_Button, (98, 210, 162))

with dpg.theme() as red_button:
    with dpg.theme_component():
        dpg.add_theme_color(dpg.mvThemeCol_Button, (232, 74, 95))

def tax_calc():
    return (years[player.current_year].animals_amount['young'] - years[player.current_year].already_sold['young']) + (years[player.current_year].animals_amount['adult'] - years[player.current_year].already_sold['adult']) + (
        (years[player.current_year].animals_amount['adult'] - years[player.current_year].already_sold['adult'])
    )

#Функция для отчистки окна
def clear(window):
    for item in dpg.get_item_children(window)[1]:
        dpg.delete_item(item)

def g(item):
    return dpg.get_value(item)

def get_str(s):
    match s:
        case 'young':
            return 'Молодые'
        case 'adult':
            return 'Взрослые'
        case 'old':
            return 'Старые'

#Функция обновление контракта в стартовом меню
def update_contract(n):
    clear('contract_years')

    for i in range(n):
        dpg.add_text(f'Год #{i+1}', parent='contract_years')
        #Поля ввода для каждого вида животных
        dpg.add_input_int(tag=f'young({i+1})', label='Продать молодых', parent='contract_years', min_value=0, min_clamped=True)
        dpg.add_input_int(tag=f'adult({i+1})', label='Продать взрослых', parent='contract_years', min_value=0, min_clamped=True)
        dpg.add_input_int(tag=f'old({i+1})', label='Продать старых', parent='contract_years', min_value=0, min_clamped=True)
        
        #Поля для ввода цены
        dpg.add_input_int(tag=f'youngc({i+1})', label='Цена молодых', parent='contract_years', min_value=0, min_clamped=True)
        dpg.add_input_int(tag=f'adultc({i+1})', label='Цена взрослых', parent='contract_years', min_value=0, min_clamped=True)
        dpg.add_input_int(tag=f'oldc({i+1})', label='Цена старых', parent='contract_years', min_value=0, min_clamped=True)
        
        dpg.add_input_int(tag=f'fine({i+1})', label='Штраф за неустойку', parent='contract_years', min_value=0, min_clamped=True)
        dpg.add_separator(parent='contract_years')

def profit_test():
    
    dpg.show_item('profit')

def info_contract():
    clear('cnt')
    n = 1
    for i in years:
        dpg.add_text(f'Год #{n}', parent='cnt')
        
        dpg.add_text('[ Нужно продать ]', parent='cnt')
        dpg.add_text(f'Молодые - {i.animals_amount["young"]} ({i.animals_prices["young"]}$)', parent='cnt')
        dpg.add_text(f'Взрослые - {i.animals_amount["adult"]} ({i.animals_prices["adult"]}$)', parent='cnt')
        dpg.add_text(f'Старые - {i.animals_amount["old"]} ({i.animals_prices["old"]}$)', parent='cnt')
        dpg.add_spacing(parent='cnt')
        dpg.add_separator(parent='cnt')
        n += 1
    dpg.show_item('cnt')
    dpg.hide_item('journal')


#Функция начала игры
def start_game():
    #Запуск игрока
    global player
    global producer
    global a

    for i in range(g('years')):
        print(f'Год {i+1} запущен')
        x = cl.Year({'young': g(f'young({i+1})'), 'adult': g(f'adult({i+1})'), 'old': g(f'old({i+1})')},
                    {'young': g(f'youngc({i+1})'), 'adult': g(f'adultc({i+1})'), 'old': g(f'oldc({i+1})')}, g(f'fine({i+1})'))
        years.append(x)
    
    player = cl.Farmer({'young': g('young'), 'adult': g('adult'), 'old': g('old')}, g('money'), years)
    producer = cl.Producer(player,years)
    a = player.money
    
    print('Игрок запущен')

    dpg.hide_item('start')
    dpg.hide_item('contract')

    buy_food()
    a = a - player.money
    dpg.add_text(f'Покупка корма - {round(a,2)}$', parent='journal')
    
    game()
    info()
    
    dpg.show_item('game')
    dpg.show_item('year_info')


#Окно с информацией о текущем годе
def info():
    clear('year_info')
    dpg.set_item_label('year_info', f'Информация о текущем годе ({player.current_year+1}/{len(years)})')

    dpg.add_text('[ Вам нужно продать ]', parent='year_info')
    dpg.add_text(f'Молодых - {years[player.current_year].already_sold["young"]}/{years[player.current_year].animals_amount["young"]} ({years[player.current_year].animals_prices["young"]}$)', parent='year_info')
    dpg.add_text(f'Взрослых - {years[player.current_year].already_sold["adult"]}/{years[player.current_year].animals_amount["adult"]} ({years[player.current_year].animals_prices["adult"]}$)', parent='year_info')
    dpg.add_text(f'Старых - {years[player.current_year].already_sold["old"]}/{years[player.current_year].animals_amount["old"]} ({years[player.current_year].animals_prices["old"]}$)', parent='year_info')
    dpg.add_spacer(parent='year_info')
    dpg.add_text(f"В случае невыполнения, неустойка составит: {producer.taxes}$", parent='year_info')

    dpg.add_spacer(parent='year_info')
    dpg.add_separator(parent='year_info')

    dpg.add_text('[ Цена за корм ]', parent='year_info')
    dpg.add_text(f'В этом году цена за корм составила: {round(a,2)}$', parent='year_info')
    
    dpg.add_separator(parent='year_info')
    dpg.add_spacer(parent='year_info')

    with dpg.group(tag='info_buttons', horizontal=True, parent='year_info'):
        dpg.add_button(label='Контракт', parent='info_buttons', width=250, height=40, callback=info_contract)
        dpg.add_button(label='Журнал собитый', parent='info_buttons', width=250, height=40, callback=lambda: dpg.show_item('journal'))
        # dpg.add_button(label='Рентабельность', parent='info_buttons', width=250, height=40, callback=profit_test)

    dpg.show_item('year_info')

def try_again():
    global years
    years = []
    clear('journal')
    dpg.hide_item('game_over')
    dpg.hide_item('game')
    dpg.hide_item('year_info')
    dpg.show_item('start')
    dpg.show_item('contract')

#Окно с игрой
def game():
    clear('game')

    dpg.add_text('[ Животные ]', parent='game')
    with dpg.group(tag='your_young', horizontal=False,parent='game'):
        dpg.add_input_int(tag='young_sell', max_value = player.animals["young"], max_clamped = True, min_value=0, min_clamped=True,label=f'Молодые - {player.animals["young"]}',parent='your_young', width=150)

    with dpg.group(tag='your_adult', horizontal=False,parent='game'):
        dpg.add_input_int(tag='adult_sell',max_value = player.animals["adult"], max_clamped = True, min_value=0, min_clamped=True,label=f'Взрослые - {player.animals["adult"]}',parent='your_adult', width=150)

    with dpg.group(tag='your_old', horizontal=False,parent='game'):
        dpg.add_input_int(tag='old_sell',max_value = player.animals["old"], max_clamped = True, min_value=0, min_clamped=True,label=f'Старые - {player.animals["old"]}',parent='your_old', width=150)
    
    dpg.add_spacer(parent='game')

    with dpg.group(tag='sell_clear', horizontal=True, parent='game'):
        dpg.add_button(label='Продать', callback=lambda: sell(), parent='sell_clear', width=250, height=40, tag='sell_button')
        dpg.add_button(label='Сбросить', callback=lambda: game(), parent='sell_clear', width=250, height=40, tag='clear_button')
    dpg.bind_item_theme('sell_button', green_button)
    dpg.bind_item_theme('clear_button', red_button)

    dpg.add_spacer(parent='game')
    dpg.add_separator(parent='game')
    
    dpg.add_text('[ Деньги ]', parent='game')
    dpg.add_text(f'Деньги наличными: {round(player.money,2)}$', parent='game')
    dpg.add_text(f'''Ваш общий капитал: {player.money + years[player.current_year].animals_prices["young"]*player.animals["young"] +
    years[player.current_year].animals_prices["adult"]*player.animals["adult"] +
    years[player.current_year].animals_prices["old"]*player.animals["old"]}$''', parent='game')
    dpg.add_text(f'Ваша еда: {player.food}', parent='game')

    dpg.add_separator(parent='game')

    dpg.add_button(label='Следующий год', callback=lambda: next_year(), parent='game', width=250, height=40)
    # dpg.add_button(label='Купить еды',callback=lambda: print(producer.game_over), parent='game', width=250, height=40)

#Переход на следующий год
def next_year():
    global a
    a = player.money
    temp_animals = [player.animals['young'], player.animals['adult'], player.animals['old']]
    n = 0
    if not producer.food_status:
        x = 100 - (player.food / sum(temp_animals))*100
        x = round(x / 3) / 100
        for item in player.animals:
            y = round(player.animals[item]*x)
            player.animals[item] = player.animals[item] - round(player.animals[item]*x)
            dpg.add_text(f'Падеж скота (Нехватки еды) {get_str(item)} - {y}', parent='journal')
    
    producer.next_year()
    for item in player.animals:
        if player.animals[item] - temp_animals[n] < 0:
            dpg.add_text(f'Падеж скота (Шторм) {get_str(item)} - {abs(player.animals[item] - temp_animals[n])}', parent='journal')
        else:
            dpg.add_text(f'Прирост скота {get_str(item)} - {abs(player.animals[item] - temp_animals[n])}', parent='journal')
    

    player.food = 0
    player.buy_food(player.animals['young']+player.animals['adult']+player.animals['old'],producer.food_price)
    a = a - player.money
    dpg.add_text(f'Покупка корма - {round(a,2)}$', parent='journal')
    game()
    info()

    if producer.game_over == True:
        dpg.show_item('game_over')
    
#Функция покупки еды (только в начале года)
def buy_food():
    player.buy_food(player.animals['young']+player.animals['adult']+player.animals['old'],producer.food_price)
    game()

#Функция для продажи животных
def sell():
    for item in player.animals:
        if (g(f'{item}_sell') > 0) and (years[player.current_year].already_sold[item]+g(f'{item}_sell') <= years[player.current_year].animals_amount[item]):
            player.sell(item,g(f'{item}_sell'))
            years[player.current_year].sold(item, g(f'{item}_sell'))
            dpg.add_text(f'Продажа {g(f"{item}_sell")} {get_str(item)} - {g(f"{item}_sell")*years[player.current_year].animals_prices[item]}$', parent='journal')
    
    game()
    info()

#Окно стартовых настроек
with dpg.window(label='Стартовые Настройки', width=750, height=795, tag='start', no_close=True, no_resize=True, no_collapse=True, pos=[0,0]):
    with dpg.group():
        dpg.add_text('Настройки игрока:')
        dpg.add_input_int(label='Стартовый Капитал', tag='money', min_value=0, min_clamped=True, default_value=80000)
        dpg.add_input_int(label='Молодые', tag='young', min_value=0, min_clamped=True, default_value=70)
        dpg.add_input_int(label='Взрослые', tag='adult', min_value=0, min_clamped=True, default_value=90)
        dpg.add_input_int(label='Старые', tag='old', min_value=0, min_clamped=True, default_value=85)
    
    dpg.add_button(label='Начать игру',width=500,height=100,pos=[50,500], callback=lambda: start_game(), tag='start_button')
    dpg.bind_item_theme('start_button', green_button)


#Окно настроек контркта
with dpg.window(label='Контракт', width=800, height=795, pos=[750,0], tag='contract'):
    dpg.add_slider_int(label='Кол-во лет', width=500, default_value=3, min_value=3, max_value=5, callback=lambda: update_contract(dpg.get_value('years')),tag='years')
    with dpg.group(tag='contract_years'):
        pass

#Окно с информацией о текущем годе
with dpg.window(label='Информация о текущем годе',no_move=True,tag='year_info',show=False, width=800, height=795,pos=[750,0], no_close=True, no_resize=True, no_collapse=True, no_bring_to_front_on_focus=True):
    pass

#Окно игры / игрока
with dpg.window(label='Игра',no_move=True,tag='game',show=False, width=750, height=795, no_close=True, no_resize=True, no_collapse=True):
    pass

with dpg.window(label='Журнал событый',no_move=True,show=False, width=800, height=795, no_close=True, no_resize=True, no_collapse=True, tag='journal', pos=[750,300], no_bring_to_front_on_focus=False):
    dpg.add_text('Здесь будут отображаться события, что происходят на ферме')

with dpg.window(label='Контракт',no_move=True,show=False, width=850, height=500, no_close=True, no_resize=True, no_collapse=True, tag='cnt', pos=[750,300]):
    pass

with dpg.window(label='Вы проиграли',no_move=True,tag='game_over',show=False, width=1550, height=795, no_close=True, no_resize=True, no_collapse=True):
    dpg.add_text('''  К сожалению, вы обонкротились. 
      Хотите попробовать ещё раз?''', tag='game_over_text', pos=[600,350])
    dpg.add_button(label='Попробовать ещё раз',width=500,height=100,pos=[500,500], callback=lambda: try_again(), tag='again_button')
    dpg.bind_item_theme('again_button', green_button)
    dpg.add_button(label='Выйти',width=500,height=100,pos=[500,650], callback=lambda: start_game(), tag='exit_button')
    dpg.bind_item_theme('exit_button', red_button)

# with dpg.window(label='Победа!',no_move=True,tag='victory',show=False, width=1550, height=795, no_close=True, no_resize=True, no_collapse=True):
#     dpg.add_text(f'''  Поздравляем! Вы закончили игру.
#       Хотите попробовать ещё раз?''', tag='game_over_text', pos=[600,350])
#     dpg.add_button(label='Попробовать ещё раз',width=500,height=100,pos=[500,500], callback=lambda: try_again(), tag='again_button')
#     dpg.bind_item_theme('again_button', green_button)
#     dpg.add_button(label='Выйти',width=500,height=100,pos=[500,650], callback=lambda: start_game(), tag='exit_button')
#     dpg.bind_item_theme('exit_button', red_button)
    

with dpg.window(label='Рентабельность',no_move=True,show=False, width=800, height=500, no_close=True, no_resize=True, no_collapse=True, tag='profit', pos=[750,300]):
    y = []
    for i in range(len(years)):
        y.append(i+1)

    with dpg.plot(tag='plot'):
        dpg.add_plot_axis(dpg.mvXAxis, label="Года", no_gridlines=True, tag="x_axis")
        dpg.add_plot_axis(dpg.mvYAxis, label="Деньги", no_gridlines=True, tag="y_axis")
        
update_contract(3)

with dpg.font_registry():
    with dpg.font(f'C:\\Windows\\Fonts\\arialbi.ttf', 18, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

with dpg.theme() as global_theme:

    with dpg.theme_component():
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 245, 249))
    
    with dpg.theme_component():
        dpg.add_theme_color(dpg.mvThemeCol_Text, (30, 32, 34))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (201, 214, 223))
    
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
    
    with dpg.theme_component():
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (201, 214, 223))

    with dpg.theme_component():
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (118, 159, 205))
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (118, 159, 205))
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (118, 159, 205))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (118, 159, 205))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (118, 159, 205))


dpg.bind_theme(global_theme)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()