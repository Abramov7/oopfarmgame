import random

#Класс фермера / игрока
class Farmer():
    def __init__(self, animals, money, contract):
        self.__animals = animals #Передаём словарь с видами животных
        self.__food = 0
        self.__money = money
        self.__contract = contract
        self.__year = contract[0]

    @property
    def animals(self):
        return self.__animals
    
    @property
    def food(self):
        return self.__food
    
    @food.setter
    def food(self, newFood):
        self.__food = newFood

    @property
    def money(self):
        return self.__money
    
    @property
    def all_money(self):
        c = 0
        for item in self.__animals:
            c += self.__animals[item]*self.__year.animals_prices[item]
        c += self.money
        return c
    
    @money.setter
    def money(self, newMoney):
        self.__money = newMoney
    
    @property
    def current_year(self):
        return self.__contract.index(self.__year)
    
    def sell(self,who, amount):
        if self.__animals[who] > 0:
            self.__animals[who] -= amount
            self.__money += self.__year.animals_prices[who]*amount
            print(self.__money)
    
    def buy_food(self, amount, price):
        x = self.__animals['young'] + self.__animals['adult'] + self.__animals['old']
        y = price / x

        while (self.__money - y >= 0) and (self.__food != x):
            self.__food = self.__food + 1
            self.__money = round(self.__money - y,2)
        print(self.__money)

    
    def next_year(self):
        self.__year = self.__contract[self.__contract.index(self.__year) + 1]

#Класс Года (Условия для контракта для данного года)
class Year():
    def __init__(self, animals_amount, animals_prices, tax):
        self.__animals_amount = animals_amount
        self.__animals_prices = animals_prices
        self.__tax = tax
        self.__already_sold = {'young': 0, 'adult':0, 'old': 0}
    
    @property
    def animals_amount(self):
        return self.__animals_amount
    
    @property
    def animals_prices(self):
        return self.__animals_prices
    
    @property
    def tax(self):
        return self.__tax
    
    @property
    def already_sold(self):
        return self.__already_sold
    
    def sold(self, who, amount):
        self.__already_sold[who] += amount

#Класс режиссёра
class Producer():
    def __init__(self,farmer: Farmer,contract):
        self.__farmer = farmer
        self.__contract = contract
        self.__idk = 200*(self.__farmer.animals['young']/2 + self.__farmer.animals['adult'] + self.__farmer.animals['old']/3)
    
    @property
    def food_status(self):
        if self.__farmer.food >= (self.__farmer.animals['young']+self.__farmer.animals['adult']+self.__farmer.animals['old']):
            return True
        else:
            return False
    
    @property
    def game_over(self):
        return self.__farmer.all_money <= 0
    
    @property
    def food_price(self):
        return self.__idk
    
    @property
    def taxes(self):
        c = 0
        for item in self.__contract[self.__farmer.current_year].animals_amount:
            x = self.__contract[self.__farmer.current_year].animals_amount[item] - self.__contract[self.__farmer.current_year].already_sold[item]
            c += x
        return c * self.__contract[self.__farmer.current_year].tax

    def animals_growth(self):
        a, b, g, p = 0.5, 0.4, 0.8, 0.65
        x = int(a*self.__farmer.animals['adult'] + b*self.__farmer.animals['old'])
        y = int(g*self.__farmer.animals['young'])
        z = int(self.__farmer.animals['adult'] + (1-p)*self.__farmer.animals['old'])
        self.__farmer.animals['young'], self.__farmer.animals['adult'], self.__farmer.animals['old'] = x, y, z
    
    def incident(self):
        x = random.randint(0,100)
        if x <= 20:
            self.__farmer.animals['young'] = self.__farmer.animals['young'] - int(self.__farmer.animals['young']*random.uniform(0.05,0.2)*random.randint(0,1))
            self.__farmer.animals['adult'] = self.__farmer.animals['adult'] - int(self.__farmer.animals['adult']*random.uniform(0.05,0.2)*random.randint(0,1))
            self.__farmer.animals['old'] = self.__farmer.animals['old'] - int(self.__farmer.animals['old']*random.uniform(0.05,0.2)*random.randint(0,1))
            print('Плохая погода')
        else:
            print('Всё хорошо')
    
    def next_year(self):
        self.__farmer.money = self.__farmer.money - self.taxes
        self.animals_growth()
        self.incident()
        self.__idk = 200*(self.__farmer.animals['young']/2 + self.__farmer.animals['adult'] + self.__farmer.animals['old']/3)
        self.__farmer.next_year()
