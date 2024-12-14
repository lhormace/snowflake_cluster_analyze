# snowflake_cluster_analyze

## プログラムの目的
* これはsnowflakeのウェアハウスが特定の時間帯にどれくらいの、クラスタ多重度で稼働したかについて、計算をするためのプログラムです
* 出力データを用いて、ヒートマップを作成します。ヒートマップはEXCELで作成をします

## 入力データ
* 形式：csv
  * 条件：
    * クラスタ数は０である場合があります
    * 開始時間と終了時間の範囲は、各レコードで重複することはありません
    * 前のレコードと次のレコードの間で空白の時間帯は存在しません。よって、必ずある特定のレコードの終了時刻は、次のレコードの開始時刻となり、数珠繋ぎのようにレコードが作成されていく形となります
    * 開始時刻と終了時刻は秒単位で発生します
  * レコード形式：
    * [列1]開始時刻(yyyymmdd hh:mi:ss)
    * [列2]終了時刻(yyyymmdd hh:mi:ss)
    * [列3]クラスタ数(0〜9) 
## 変換仕様
* pythonのプログラムを書いてほしい
* １時間あたりは3600秒であるが、1秒から3600秒の1秒単位でクラスタ数がいくつかであったかをcsvから判断し、1時間単位で総和を求める。
* 複数の日付が存在するので、csvに含まれる開始時刻の日付の一番古い日付から、終了時刻の日付の一番新しい日付を範囲としたい
* 日付が存在する日については24時間分について、それぞれ１時間単位で総和を求めるが、総和が０の時間であっても０を計算する
## 出力データ
* 形式：csv
  * 条件：
    * クラスタ数が０の時間帯であってもレコードはクラスタ数０で作成する
  * レコード形式：
    * [列1]日付(YYYYMMDD)
    * [列2]時間(HH)
    * [列3]秒あたりのクラスタ数の総和
