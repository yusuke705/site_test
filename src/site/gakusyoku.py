import random
import json
import os
import tkinter as tk
from tkinter import messagebox
import streamlit as st


# JSON読み込み
def load_menu():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "menu.json")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

menu = load_menu()


# -----------------------------
# トレーニーモード
# 身長・体重から推定必要カロリーを計算し、
# その範囲内でランダムにメニューを選ぶ
# -----------------------------
def choose_trainer_mode(height, weight):
    # 簡易的な推定式（基礎代謝 + 活動量）
    bmr = 13.397 * weight + 4.799 * height - 5.677  # 男性向け式
    target_cal = int(bmr * 1.2)  # 軽い活動量

    selected = []
    total_cal = 0
    total_price = 0

    affordable = menu[:]  # 全メニューから選ぶ

    while True:
        choice = random.choice(affordable)
        if total_cal + choice["cal"] > target_cal:
            break
        selected.append(choice)
        total_cal += choice["cal"]
        total_price += choice["price"]

    return selected, total_cal, total_price, target_cal


# -----------------------------
# ダイエットモード
# 入力したカロリー以内でメニューを選ぶ
# -----------------------------
def choose_diet_mode(limit_cal):
    sorted_menu = sorted(menu, key=lambda m: m["cal"])

    selected = []
    total_cal = 0
    total_price = 0

    for item in sorted_menu:
        if total_cal + item["cal"] <= limit_cal:
            selected.append(item)
            total_cal += item["cal"]
            total_price += item["price"]
        else:
            break

    return selected, total_cal, total_price


# -----------------------------
# ノーマルモード
# 予算以内でランダムに選ぶ
# -----------------------------
def choose_normal_mode(budget):
    selected = []
    total_price = 0
    total_cal = 0

    affordable = [m for m in menu if m["price"] <= budget]

    if not affordable:
        return [], 0, 0

    while True:
        choice = random.choice(affordable)
        if total_price + choice["price"] > budget:
            break
        selected.append(choice)
        total_price += choice["price"]
        total_cal += choice["cal"]

    return selected, total_cal, total_price


# # -----------------------------
# # GUI処理
# # -----------------------------
# def on_click():
#     mode = mode_var.get()

#     if mode == "trainer":
#         try:
#             height = int(entry_height.get())
#             weight = int(entry_weight.get())
#         except ValueError:
#             messagebox.showerror("エラー", "身長・体重は整数で入力してください")
#             return

#         selected, total_cal, total_price, target_cal = choose_trainer_mode(height, weight)

#         if not selected:
#             messagebox.showinfo("結果", "条件に合うメニューがありません")
#             return

#         text = f"トレーニーモード（目標カロリー：{target_cal} kcal）\n\n"
#         for item in selected:
#             text += f"- {item['name']} ({item['price']}円, {item['cal']} kcal)\n"
#         text += f"\n合計カロリー：{total_cal} kcal\n合計金額：{total_price} 円"

#         messagebox.showinfo("おすすめメニュー", text)

#     elif mode == "diet":
#         try:
#             limit_cal = int(entry_cal.get())
#         except ValueError:
#             messagebox.showerror("エラー", "カロリーは整数で入力してください")
#             return

#         selected, total_cal, total_price = choose_diet_mode(limit_cal)

#         if not selected:
#             messagebox.showinfo("結果", "そのカロリーでは選べるメニューがありません")
#             return

#         text = "ダイエットモード\n\n"
#         for item in selected:
#             text += f"- {item['name']} ({item['price']}円, {item['cal']} kcal)\n"
#         text += f"\n合計カロリー：{total_cal} kcal\n合計金額：{total_price} 円"

#         messagebox.showinfo("おすすめメニュー", text)

#     elif mode == "normal":
#         try:
#             budget = int(entry_budget.get())
#         except ValueError:
#             messagebox.showerror("エラー", "予算は整数で入力してください")
#             return

#         selected, total_cal, total_price = choose_normal_mode(budget)

#         if not selected:
#             messagebox.showinfo("結果", "その予算では買えるメニューがありません")
#             return

#         text = "ノーマルモード\n\n"
#         for item in selected:
#             text += f"- {item['name']} ({item['price']}円, {item['cal']} kcal)\n"
#         text += f"\n合計カロリー：{total_cal} kcal\n合計金額：{total_price} 円"

#         messagebox.showinfo("おすすめメニュー", text)


# # -----------------------------
# # GUIレイアウト
# # -----------------------------
# root = tk.Tk()
# root.title("学食メニューおすすめアプリ（3モード対応）")

# mode_var = tk.StringVar(value="normal")

# tk.Label(root, text="モードを選択:").pack()

# tk.Radiobutton(root, text="ノーマルモード（予算）", variable=mode_var, value="normal").pack()
# tk.Radiobutton(root, text="ダイエットモード（カロリー）", variable=mode_var, value="diet").pack()
# tk.Radiobutton(root, text="トレーニーモード（身長・体重）", variable=mode_var, value="trainer").pack()

# # ノーマルモード入力
# tk.Label(root, text="予算（円）:").pack()
# entry_budget = tk.Entry(root)
# entry_budget.pack()

# # ダイエットモード入力
# tk.Label(root, text="カロリー上限（kcal）:").pack()
# entry_cal = tk.Entry(root)
# entry_cal.pack()

# # トレーニーモード入力
# tk.Label(root, text="身長（cm）:").pack()
# entry_height = tk.Entry(root)
# entry_height.pack()

# tk.Label(root, text="体重（kg）:").pack()
# entry_weight = tk.Entry(root)
# entry_weight.pack()

# button = tk.Button(root, text="おすすめを表示", command=on_click)
# button.pack()

# root.mainloop()

# -----------------------------
# Streamlit UI 
# -----------------------------
st.title("🍽️ 学食メニューおすすめアプリ")

# モード選択ラジオボタン
mode = st.radio(
    "モードを選択してください",
    ["ノーマルモード（予算）", "ダイエットモード（カロリー）", "トレーニーモード（身長・体重）"],
)

st.markdown("---")

# 選択されたモードに応じて入力欄と処理を切り替え
if mode == "ノーマルモード（予算）":
  budget = st.number_input("予算（円）", min_value=0, value=500, step=50)

  if st.button("おすすめを表示"):
    selected, total_cal, total_price = choose_normal_mode(budget)
    if not selected:
      st.warning("その予算では買えるメニューがありません。")
    else:
      st.subheader("おすすめメニュー")
      for item in selected:
        st.write(f"- {item['name']} （{item['price']}円 / {item['cal']} kcal）")
      st.metric("合計金額", f"{total_price} 円")
      st.metric("合計カロリー", f"{total_cal} kcal")

elif mode == "ダイエットモード（カロリー）":
  limit_cal = st.number_input(
      "カロリー上限（kcal）", min_value=0, value=700, step=50
  )

  if st.button("おすすめを表示"):
    selected, total_cal, total_price = choose_diet_mode(limit_cal)
    if not selected:
      st.warning("そのカロリーでは選べるメニューがありません。")
    else:
      st.subheader("おすすめメニュー")
      for item in selected:
        st.write(f"- {item['name']} （{item['price']}円 / {item['cal']} kcal）")
      st.metric("合計金額", f"{total_price} 円")
      st.metric("合計カロリー", f"{total_cal} kcal")

elif mode == "トレーニーモード（身長・体重）":
  height = st.number_input("身長（cm）", min_value=100, value=170, step=1)
  weight = st.number_input("体重（kg）", min_value=30, value=60, step=1)

  if st.button("おすすめを表示"):
    selected, total_cal, total_price, target_cal = choose_trainer_mode(
        height, weight
    )
    if not selected:
      st.warning("条件に合うメニューがありません。")
    else:
      st.subheader(f"おすすめメニュー（目標カロリー：{target_cal} kcal）")
      for item in selected:
        st.write(f"- {item['name']} （{item['price']}円 / {item['cal']} kcal）")
      st.metric("合計金額", f"{total_price} 円")
      st.metric("合計カロリー", f"{total_cal} kcal")
