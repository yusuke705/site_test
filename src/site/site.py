import random
import streamlit as st

# サイゼリヤのメニューリスト
menu = [
    # 前菜・サラダ
    {"name": "小エビのサラダ", "price": 350},
    {"name": "グリーンサラダ", "price": 350},
    {"name": "モッツァレラのカプレーゼ", "price": 430},
    {"name": "辛味チキン", "price": 300},
    {"name": "ポップコーンシュリンプ", "price": 300},
    {"name": "カリッとポテト", "price": 300},
    # スープ
    {"name": "ミネストローネ", "price": 300},
    {"name": "コーンクリームスープ", "price": 150},
    # ピザ・パン
    {"name": "マルゲリータピザ", "price": 400},
    {"name": "野菜ペーストのミラノ風ドリア", "price": 400},
    {"name": "ミニフィセル", "price": 170},
    {"name": "ガーリックトースト", "price": 220},
    # パスタ・ドリア
    {"name": "ミラノ風ドリア", "price": 300},
    {"name": "タラコソースシシリー風", "price": 400},
    {"name": "パルマ風スパゲッティ", "price": 400},
    {"name": "イカの墨つきスパゲッティ", "price": 500},
    # 肉料理
    {"name": "ハンバーグステーキ", "price": 400},
    {"name": "若鶏のディアボラ風", "price": 500},
    # デザート
    {"name": "イタリアンジェラート", "price": 280},
    {"name": "プリンとティラミスの盛り合わせ", "price": 500},
    {"name": "トリフアイスクリーム", "price": 380},
    # ドリンクバー
    {"name": "ドリンクバー", "price": 300},
]


def saizeriya_gacha(budget=1000, tolerance=150):
  best_combination = []
  best_diff = float("inf")

  for _ in range(10000):
    shuffled_menu = menu.copy()
    random.shuffle(shuffled_menu)

    current_combination = []
    current_total = 0

    for item in shuffled_menu:
      if current_total + item["price"] <= budget + tolerance:
        current_combination.append(item)
        current_total += item["price"]

        if current_total == budget:
          break

    diff = abs(budget - current_total)
    if diff < best_diff:
      best_diff = diff
      best_combination = current_combination

      if diff == 0:
        break

  return best_combination


# --- Webアプリの画面レイアウト ---
st.title("🎰 サイゼリヤ 1000円ガチャ")
st.write("ボタンを押すと、予算に合わせたおすすめのメニューをランダムで提案します！")

# サイドバーで設定を変更できるようにする
st.sidebar.header("ガチャの設定")
budget = st.sidebar.slider(
    "目標予算（円）", min_value=500, max_value=3000, value=1000, step=100
)
tolerance = st.sidebar.slider(
    "許容誤差（円）", min_value=0, max_value=300, value=100, step=50
)

# ガチャを回すボタン
if st.button("ガチャを回す！", type="primary"):
  with st.spinner("メニューを選定中..."):
    result = saizeriya_gacha(budget=budget, tolerance=tolerance)
    total_price = sum(item["price"] for item in result)

  st.subheader("【本日のご注文内容】")
  for item in result:
    st.write(f"- {item['name']}：**{item['price']}円**")

  st.markdown("---")

  # 金額の表示とメトリクス
  st.metric(
      label="合計金額",
      value=f"{total_price}円",
      delta=f"{budget - total_price}円 (差分)",
  )

  if total_price <= budget:
    st.success(f"予算内です！お釣りは {budget - total_price}円 です！🎉")
  else:
    st.warning(f"予算より {total_price - budget}円 オーバーしちゃいました！💦")