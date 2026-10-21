import random
import streamlit as st
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


# --- Streamlit UI のレイアウト ---
st.title("🎰 ガチャアプリ (値段・カロリー・トレーニー)")
st.write(
    "サイドバーからモードを選んで、目標値を設定してガチャを回してください！"
)

# サイドバーでモード選択
st.sidebar.header("ガチャの設定")
mode_option = st.sidebar.selectbox(
    "モード選択",
    ("1：値段ガチャ", "2：カロリーガチャ", "3：トレーニーガチャ"),
)

solver = calc(Menu_list)

if mode_option == "1：値段ガチャ":
  st.header("💰 値段ガチャ")
  target_price = st.number_input(
      "目標金額（円）", min_value=100, max_value=5000, value=1000, step=100
  )

  if st.button("ガチャを回す！", type="primary"):
    with st.spinner("メニューを選定中..."):
      response = solver.solve_price(target_price)

    if response is None:
      st.warning(
          "条件に合う組み合わせが見つかりませんでした。もう一度試してください。"
      )
    else:
      result, price, cal, protein = response
      st.subheader("【選ばれたメニュー】")
      for m in result:
        st.write(
            f"- **{m.name}** （{m.price}円 / {m.cal}kcal / {m.protein}g）"
        )

      st.markdown("---")
      col1, col2, col3 = st.columns(3)
      col1.metric("合計金額", f"{price} 円")
      col2.metric("総カロリー", f"{cal} kcal")
      col3.metric("総タンパク質", f"{protein} g")

elif mode_option == "2：カロリーガチャ":
  st.header("🔥 カロリーガチャ")
  target_cal = st.number_input(
      "目標カロリー（kcal）", min_value=100, max_value=3000, value=600, step=50
  )

  if st.button("ガチャを回す！", type="primary"):
    with st.spinner("メニューを選定中..."):
      response = solver.solve_cal(target_cal)

    if response is None:
      st.warning(
          "条件に合う組み合わせが見つかりませんでした。もう一度試してください。"
      )
    else:
      result, price, cal, protein = response
      st.subheader("【選ばれたメニュー】")
      for m in result:
        st.write(
            f"- **{m.name}** （{m.price}円 / {m.cal}kcal / {m.protein}g）"
        )

      st.markdown("---")
      col1, col2, col3 = st.columns(3)
      col1.metric("合計金額", f"{price} 円")
      col2.metric("総カロリー", f"{cal} kcal")
      col3.metric("総タンパク質", f"{protein} g")

elif mode_option == "3：トレーニーガチャ":
  st.header("💪 トレーニーガチャ")
  weight = st.number_input(
      "体重の入力 (kg)", min_value=30.0, max_value=150.0, value=60.0, step=1.0
  )
  target_protein = weight * 0.475
  st.info(f"計算された目標タンパク質量：**{target_protein:.1f} g**")

  if st.button("ガチャを回す！", type="primary"):
    with st.spinner("メニューを選定中..."):
      response = solver.solve_protein(target_protein)

    if response is None:
      st.warning(
          "条件に合う組み合わせが見つかりませんでした。もう一度試してください。"
      )
    else:
      result, price, cal, protein = response
      st.subheader("【選ばれたメニュー】")
      for m in result:
        st.write(
            f"- **{m.name}** （{m.price}円 / {m.cal}kcal / {m.protein}g）"
        )

      st.markdown("---")
      col1, col2, col3 = st.columns(3)
      col1.metric("合計金額", f"{price} 円")
      col2.metric("総カロリー", f"{cal} kcal")
      col3.metric("総タンパク質", f"{protein} g")