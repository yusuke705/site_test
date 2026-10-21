import random

# サイゼリヤの代表的なメニューと価格のリスト（例）
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
    # パリア・ドリア
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
  """サイゼリヤ1000円ガチャを実行する関数

  budget: 目標金額 (デフォルト1000円) tolerance: 許容する誤差の範囲（例: 予算の上下150円以内におさめる）
  """
  best_combination = []
  best_diff = float("inf")

  # ランダムな組み合わせを何回か試して、もっとも予算に近いものを探す
  for _ in range(10000):
    # メニューをシャッフルして上から順に選んでみる
    shuffled_menu = menu.copy()
    random.shuffle(shuffled_menu)

    current_combination = []
    current_total = 0

    for item in shuffled_menu:
      # 予算を超えない、または許容範囲内であれば追加
      if current_total + item["price"] <= budget + tolerance:
        current_combination.append(item)
        current_total += item["price"]

        # 予算ぴったりになったら即終了
        if current_total == budget:
          break

    # 今回の組み合わせの予算との差分を計算
    diff = abs(budget - current_total)

    # より良い（予算に近い）組み合わせがあれば更新
    if diff < best_diff:
      best_diff = diff
      best_combination = current_combination

      # ぴったり予算通りならループを抜ける
      if diff == 0:
        break

  return best_combination


# ガチャを回す
if __name__ == "__main__":
  print("🎰 サイゼリヤ1000円ガチャを回しています...\n")
  result = saizeriya_gacha(budget=1000, tolerance=100)

  total_price = sum(item["price"] for item in result)

  print("【本日のご注文内容】")
  print("-" * 30)
  for item in result:
    print(f"- {item['name']} ({item['price']}円)")
  print("-" * 30)
  print(f"合計金額: **{total_price}円**")

  if total_price <= 1000:
    print(f"お釣りは {1000 - total_price}円 です！")
  else:
    print(f"予算より {total_price - 1000}円 オーバーしちゃいました！")