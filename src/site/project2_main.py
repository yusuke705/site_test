import html
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


# =====================================================================
#  ここから下が見た目（Streamlit UI）
# =====================================================================

st.set_page_config(
    page_title="ガチャアプリ",
    page_icon="🎰",
    layout="centered",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=swap');

:root {
  --ink: #3b2a20;
  --muted: #8a7466;
  --accent: #ff6b35;
  --card: #ffffff;
  --line: #f3e3d3;
}

/* ---------- 全体 ---------- */
.stApp {
  background:
    radial-gradient(circle at 8% 0%, #ffe4cc 0, transparent 38%),
    radial-gradient(circle at 100% 15%, #ffd6e0 0, transparent 34%),
    #fff8f0;
  color: var(--ink);
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 760px; padding-top: 2rem; padding-bottom: 4rem; }

.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp li,
.stMarkdown, .stButton button, .stTabs [data-baseweb="tab"], input {
  font-family: 'Zen Maru Gothic', 'Hiragino Maru Gothic ProN', 'Meiryo', sans-serif;
}
.stApp p, .stApp label, .stApp li { color: var(--ink); }

/* ---------- ヒーロー ---------- */
.hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #ff6b35 0%, #ff9a3c 55%, #ffc15e 100%);
  border-radius: 28px;
  padding: 34px 28px;
  margin-bottom: 26px;
  box-shadow: 0 18px 40px -18px rgba(255, 107, 53, .65);
}
.hero::after {
  content: ""; position: absolute; right: -40px; top: -40px;
  width: 180px; height: 180px; border-radius: 50%;
  background: rgba(255, 255, 255, .18);
}
.hero::before {
  content: ""; position: absolute; right: 70px; bottom: -64px;
  width: 120px; height: 120px; border-radius: 50%;
  background: rgba(255, 255, 255, .12);
}
.hero-badge {
  display: inline-block;
  background: rgba(255, 255, 255, .25);
  color: #fff;
  font-size: .72rem; font-weight: 700; letter-spacing: .14em;
  padding: 4px 12px; border-radius: 999px;
}
.stApp .hero h1 {
  color: #fff; font-weight: 900; font-size: 2.2rem;
  margin: 8px 0 6px; padding: 0; letter-spacing: .02em;
}
.stApp .hero p { color: rgba(255, 255, 255, .92); margin: 0; font-size: .98rem; }

/* ---------- タブ（モード切り替え） ---------- */
.stTabs [data-baseweb="tab-list"] {
  gap: 8px; background: transparent; border-bottom: none; flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  height: auto; padding: 10px 18px; border-radius: 999px;
  background: #fff; border: 1px solid var(--line); color: var(--muted);
}
.stTabs [data-baseweb="tab"] p { color: inherit; font-weight: 700; margin: 0; }
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #ff6b35, #ff9a3c);
  border-color: transparent; color: #fff;
  box-shadow: 0 8px 18px -8px rgba(255, 107, 53, .7);
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px; }

/* ---------- 各モードの説明カード ---------- */
.intro {
  display: flex; align-items: center; gap: 14px;
  background: var(--card); border: 1px solid var(--line);
  border-radius: 18px; padding: 14px 18px; margin-bottom: 14px;
}
.intro .emoji { font-size: 1.9rem; }
.intro .ttl { font-weight: 900; font-size: 1.05rem; color: var(--ink); }
.intro .sub { color: var(--muted); font-size: .85rem; }

/* ---------- 入力欄 ---------- */
[data-testid="stNumberInput"] [data-baseweb="input"] {
  background: #fff; border: 1px solid var(--line); border-radius: 14px;
}
[data-testid="stNumberInput"] input { color: var(--ink); background: #fff; font-weight: 700; }

.target-chip {
  display: inline-block; background: #fff; border: 1px solid var(--line);
  border-radius: 999px; padding: 8px 18px; margin: 2px 0 14px;
  font-weight: 700; color: var(--ink);
}
.target-chip b { color: var(--accent); font-size: 1.15rem; }

/* ---------- ガチャボタン ---------- */
.stButton { margin-top: 6px; }
.stButton > button {
  width: 100%; border: none; border-radius: 999px;
  padding: .85rem 1.2rem;
  background: linear-gradient(135deg, #ff6b35, #ff9a3c);
  box-shadow: 0 14px 26px -14px rgba(255, 107, 53, .9);
  transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button p {
  color: #fff; font-weight: 900; font-size: 1.1rem; letter-spacing: .06em;
}
.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 30px -14px rgba(255, 107, 53, 1);
  border: none;
}
.stButton > button:active { transform: translateY(1px) scale(.99); }

/* ---------- 結果カード ---------- */
.result-card {
  background: var(--card); border: 1px solid var(--line);
  border-radius: 22px; padding: 20px 22px 10px; margin-top: 22px;
  box-shadow: 0 20px 40px -26px rgba(120, 70, 30, .45);
  animation: pop .45s cubic-bezier(.2, 1.3, .4, 1);
}
.result-head { font-weight: 900; font-size: 1.15rem; margin-bottom: 8px; color: var(--ink); }
.item {
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 8px;
  padding: 12px 0; border-top: 1px dashed var(--line);
}
.item-name { font-weight: 700; font-size: 1rem; color: var(--ink); }
.tags { display: flex; gap: 6px; flex-wrap: wrap; }
.tag { font-size: .78rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.tag-price { background: #fff1d6; color: #a86400; }
.tag-cal   { background: #ffe3dc; color: #c2411f; }
.tag-pro   { background: #dff5e6; color: #1f7a45; }

.stats {
  display: grid; gap: 12px; margin-top: 16px;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  animation: pop .55s cubic-bezier(.2, 1.3, .4, 1);
}
.stat { border-radius: 20px; padding: 16px 18px; color: #fff; }
.stat .label { font-size: .78rem; font-weight: 700; letter-spacing: .08em; opacity: .92; }
.stat .value { font-size: 1.7rem; font-weight: 900; line-height: 1.25; }
.stat .unit  { font-size: .9rem; font-weight: 700; margin-left: 4px; }
.stat-price { background: linear-gradient(135deg, #ffb347, #ff8c42); }
.stat-cal   { background: linear-gradient(135deg, #ff7a59, #ee4b6a); }
.stat-pro   { background: linear-gradient(135deg, #3ecf8e, #1fa971); }

@keyframes pop {
  0%   { transform: scale(.9) translateY(10px); opacity: 0; }
  100% { transform: none; opacity: 1; }
}

/* ---------- サイドバー・フッター ---------- */
section[data-testid="stSidebar"] { background: #fffdf9; border-right: 1px solid var(--line); }
.foot { text-align: center; color: var(--muted); font-size: .8rem; margin-top: 44px; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def intro(emoji, title, sub):
  """各モードの説明カード"""
  st.markdown(
      f'<div class="intro"><div class="emoji">{emoji}</div>'
      f'<div><div class="ttl">{title}</div><div class="sub">{sub}</div></div></div>',
      unsafe_allow_html=True,
  )


def render_result(response, use_fx):
  """ガチャ結果の表示（3つのモードで共通）"""
  if response is None:
    st.warning("条件に合う組み合わせが見つかりませんでした。もう一度試してください。")
    return

  result, price, cal, protein = response

  items = "".join(
      '<div class="item">'
      f'<div class="item-name">{html.escape(str(m.name))}</div>'
      '<div class="tags">'
      f'<span class="tag tag-price">💴 {m.price}円</span>'
      f'<span class="tag tag-cal">🔥 {m.cal}kcal</span>'
      f'<span class="tag tag-pro">💪 {m.protein:g}g</span>'
      '</div></div>'
      for m in result
  )
  st.markdown(
      '<div class="result-card">'
      '<div class="result-head">🎉 選ばれたメニュー</div>'
      f'{items}</div>',
      unsafe_allow_html=True,
  )

  st.markdown(
      '<div class="stats">'
      '<div class="stat stat-price"><div class="label">合計金額</div>'
      f'<div class="value">{price:,.0f}<span class="unit">円</span></div></div>'
      '<div class="stat stat-cal"><div class="label">総カロリー</div>'
      f'<div class="value">{cal:,.0f}<span class="unit">kcal</span></div></div>'
      '<div class="stat stat-pro"><div class="label">総タンパク質</div>'
      f'<div class="value">{protein:.1f}<span class="unit">g</span></div></div>'
      '</div>',
      unsafe_allow_html=True,
  )

  if use_fx:
    st.balloons()


# ---------- サイドバー ----------
with st.sidebar:
  st.markdown("### ⚙️ 設定")
  use_fx = st.toggle("当たり演出（風船）", value=True)
  st.markdown("---")
  st.markdown("### 📖 遊び方")
  st.markdown(
      "1. 上のタブでモードを選ぶ\n"
      "2. 目標値を入力する\n"
      "3. **ガチャを回す！** を押す\n\n"
      "気に入らなければ、何度でも回し直せます。"
  )
  st.markdown("---")
  st.markdown("### 🎯 当たりの範囲")
  st.markdown(
      "- 値段：目標金額の **−100円〜** 目標金額\n"
      "- カロリー：目標の **−100kcal〜** 目標\n"
      "- タンパク質：目標の **−5g〜** 目標"
  )

# ---------- ヒーロー ----------
st.markdown(
    '<div class="hero">'
    '<div class="hero-badge">MENU GACHA</div>'
    '<h1>🎰 ガチャアプリ</h1>'
    '<p>値段・カロリー・タンパク質から、今日のメニューを引き当てよう！</p>'
    '</div>',
    unsafe_allow_html=True,
)

solver = calc(Menu_list)

tab_price, tab_cal, tab_protein = st.tabs(
    ["💰 値段ガチャ", "🔥 カロリーガチャ", "💪 トレーニーガチャ"]
)

# ---------- 1: 値段ガチャ ----------
with tab_price:
  intro("💰", "値段ガチャ", "予算にぴったりのメニューの組み合わせを引きます")
  target_price = st.number_input(
      "目標金額（円）", min_value=100, max_value=5000, value=1000, step=100
  )

  if st.button("🎰 ガチャを回す！", type="primary", key="spin_price"):
    with st.spinner("メニューを選定中..."):
      response = solver.solve_price(target_price)
    render_result(response, use_fx)

# ---------- 2: カロリーガチャ ----------
with tab_cal:
  intro("🔥", "カロリーガチャ", "目標カロリーに合わせてメニューを引きます")
  target_cal = st.number_input(
      "目標カロリー（kcal）", min_value=100, max_value=3000, value=600, step=50
  )

  if st.button("🎰 ガチャを回す！", type="primary", key="spin_cal"):
    with st.spinner("メニューを選定中..."):
      response = solver.solve_cal(target_cal)
    render_result(response, use_fx)

# ---------- 3: トレーニーガチャ ----------
with tab_protein:
  intro("💪", "トレーニーガチャ", "体重から目標タンパク質量を計算して、メニューを引きます")
  weight = st.number_input(
      "体重の入力 (kg)", min_value=30.0, max_value=150.0, value=60.0, step=1.0
  )
  target_protein = weight * 0.475
  st.markdown(
      f'<div class="target-chip">🎯 目標タンパク質量　<b>{target_protein:.1f} g</b></div>',
      unsafe_allow_html=True,
  )

  if st.button("🎰 ガチャを回す！", type="primary", key="spin_protein"):
    with st.spinner("メニューを選定中..."):
      response = solver.solve_protein(target_protein)
    render_result(response, use_fx)

st.markdown('<div class="foot">Made with Streamlit 🍙</div>', unsafe_allow_html=True)