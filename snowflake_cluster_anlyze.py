import pandas as pd
from datetime import datetime, timedelta

# 入力データのCSVファイルパス
input_file = "input.csv"

# 出力データのCSVファイルパス
output_file = "output.csv"

# 入力データを読み込む
df = pd.read_csv(input_file)

# 列名を設定
df.columns = ['開始時刻', '終了時刻', 'クラスタ数']

# 開始時刻と終了時刻をdatetime形式に変換
df['開始時刻'] = pd.to_datetime(df['開始時刻'], format='%Y%m%d %H:%M:%S')
df['終了時刻'] = pd.to_datetime(df['終了時刻'], format='%Y%m%d %H:%M:%S')

# 入力データ範囲を特定
min_date = df['開始時刻'].dt.date.min()
max_date = df['終了時刻'].dt.date.max()

# 出力データを保存するリスト
result = []

# 指定範囲内の日付を順に処理
current_date = min_date
while current_date <= max_date:
    # 当日の日付範囲の開始と終了を設定
    day_start = datetime.combine(current_date, datetime.min.time())

    # 24時間を1時間単位で処理
    for hour in range(24):
        hour_start = day_start + timedelta(hours=hour)
        hour_end = hour_start + timedelta(hours=1)

        # 該当時間帯のデータをフィルタリング
        filtered_df = df[(df['開始時刻'] < hour_end) & (df['終了時刻'] > hour_start)]

        # 該当時間帯の秒あたりのクラスタ数を計算
        total_sum = 0
        if not filtered_df.empty:
            for _, row in filtered_df.iterrows():
                # データの適用範囲を調整
                start = max(hour_start, row['開始時刻'])
                end = min(hour_end, row['終了時刻'])

                # 秒数を計算してクラスタ数を加算
                duration_seconds = (end - start).total_seconds()
                total_sum += duration_seconds * row['クラスタ数']

        # 出力データとして結果を保存（ゼロも含む）
        result.append([current_date.strftime('%Y%m%d'), f"{hour:02d}", total_sum])

    # 次の日に進む
    current_date += timedelta(days=1)

# 結果をDataFrame化
result_df = pd.DataFrame(result, columns=['日付', '時間', '秒あたりのクラスタ数の総和'])

# CSVファイルとして保存
result_df.to_csv(output_file, index=False)
print(f"結果を保存しました: {output_file}")

