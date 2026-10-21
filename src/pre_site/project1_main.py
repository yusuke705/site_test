import random
from project1_menu_list import Menu_list

class calc:
    class Menu:
        def __init__(self, name, price, cal, protein):
            self.name = name
            self.price = price
            self.cal = cal
            self.protein = protein

        def __str__(self):
            return f"{self.name}({self.price}円, {self.cal}kcal, {self.protein}g)"
    
    def __init__(self, menu):
        self.menus = [calc.Menu(*m) for m in menu]
        self.result_mode1 = []
        self.result_mode2 = []
        self.result_mode3 = []


    def calc_price(self, index, now, total, target):
        if target - 100 <= total <= target:
            self.result_mode1.append(now.copy())
            return
        if total > target or index == len(self.menus):
            return

        Menu = self.menus[index]

        now.append(Menu)
        self.calc_price(index + 1, now, total + self.menus[index].price, target)
        now.pop()

        self.calc_price(index + 1, now, total, target)

    def solve_price(self, target):
        self.result_mode1 = []
        self.calc_price(0, [], 0, target)

        if not self.result_mode1:
            return None

        result = random.choice(self.result_mode1)
        total_price = sum(m.price for m in result)
        total_cal = sum(m.cal for m in result)
        total_protein = sum(m.protein for m in result)

        return result, total_price, total_cal, total_protein
        


    def calc_cal(self, index, now, total, target):
        if target - 100 <= total <= target:
            self.result_mode2.append(now.copy())
            return
        if total > target or index == len(self.menus):
            return
        
        Menu = self.menus[index]
        
        now.append(Menu)
        self.calc_cal(index + 1, now, total + self.menus[index].cal, target)
        now.pop()
        
        self.calc_cal(index + 1, now, total, target)
        
    def solve_cal(self, target):
        self.result_mode2 = []
        self.calc_cal(0, [], 0, target)
        
        if not self.result_mode2:
            return None
        
        result = random.choice(self.result_mode2)
        total_price = sum(m.price for m in result)
        total_cal = sum(m.cal for m in result)
        total_protein = sum(m.protein for m in result)
        
        return result, total_price, total_cal, total_protein

    def calc_protein(self, index, now, total, target):
        if target - 5.0 <= total <= target:
            self.result_mode3.append(now.copy())
            return
        if total > target or index == len(self.menus):
            return
    
        Menu = self.menus[index]
    
        now.append(Menu)
        self.calc_protein(index + 1, now, total + self.menus[index].protein, target)
        now.pop()
    
        self.calc_protein(index + 1, now, total, target)
    
    def solve_protein(self, target):
        self.result_mode3 = []
        self.calc_protein(0, [], 0, target)
    
        if not self.result_mode3:
            return None
    
        result = random.choice(self.result_mode3)
        total_price = sum(m.price for m in result)
        total_cal = sum(m.cal for m in result)
        total_protein = sum(m.protein for m in result)
        
        return result, total_price, total_cal, total_protein


        

print("モード選択")
print("1：値段ガチャ, 2:カロリーガチャ, 3:トレーニーガチャ")
while True:
    try:
        mode = int(input())
        if mode == 1 or mode == 2 or mode == 3:
            break
        else:
            print("retry")
    except ValueError:
        print("retry")

if mode == 1:
    target_price = int(input("目標金額："))
    solver = calc(Menu_list)
    response = solver.solve_price(target_price)

    if response is None:
        print("もう一度")
    else:
        result, price, cal, protein = response
        print("メニュー")
        for m in result:
            print(m)
        print(f"合計：{price} 円")
        print(f"総カロリー： {cal} kcal")
        print(f"総タンパク質量：{protein} g")

if mode == 2:
    target_cal = int(input("目標カロリー："))
    solver = calc(Menu_list)
    response = solver.solve_cal(target_cal)

    if response is None:
        print("もう一度")
    else:
        result, price, cal, protein = response
        print("メニュー")
        for m in result:
            print(m)
        print(f"合計：{price} 円")
        print(f"総カロリー：{cal} kcal")
        print(f"総タンパク質量：{protein} g")   

if mode == 3:
    weight = float(input("体重の入力(kg)："))
    target_protein = weight * 0.475
    print(f"目標タンパク質量：{target_protein}")
    solver = calc(Menu_list)
    response = solver.solve_protein(target_protein)

    if response is None:
        print("もう一度")
    else:
        result, price, cal, protein = response
        print("メニュー")
        for m in result:
            print(m)
        print(f"合計：{price} 円")
        print(f"総カロリー：{cal} kcal")
        print(f"総タンパク質量：{protein} g") 
