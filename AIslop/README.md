# 998244353 convolution

Yosupo `convolution_mod` 向けの、単独で使える実装です。入力係数は `0 <= x < 998244353`、NTT 長は最大 `2^23` を想定します。

| 実行環境 | ファイル | 関数 |
| --- | --- | --- |
| Codon | `convolution_codon.py` | `convolution(a: list[int], b: list[int]) -> list[int]` |
| PyPy 3 | `convolution_pypy.py` | `convolution(a, b)` |

両方とも空配列を渡すと空配列を返し、入力配列を変更しません。ファイルをそのまま提出すれば、Yosupo形式の標準入力・標準出力でも動きます。

Codon のビルド例:

```sh
codon build -release -o convolution_codon convolution_codon.py
```

Codon版はMontgomery乗算、radix-4 NTT、8レーンSIMDを使います。入力のMontgomery変換もSIMD化し、ゼロ埋めされた先頭段を簡略化します。PyPy版はradix-2 NTTで、長さ2の段と逆変換末尾の正規化を最適化しています。両版とも短い入力の愚直積、長さが大きく異なる入力の分割積、定数配列、両端のゼロ、平方を処理します。分割積ではNTT長を入力長に応じて選びます。動作確認はCodon 0.20.6、PyPy 3.9.18、x86-64 AVX2環境で行いました。

検証にはLibrary Checkerの `convolution_mod` 公式53ケース、切り替え境界70ケース、追加乱数200ケースを使用しました。速度比較の基準は、[Qiitaの記事](https://qiita.com/navel_tos/items/9195de7041cf2c8b535b)の実装と、[Library CheckerのアセンブリなしC++提出](https://judge.yosupo.jp/submission/393435)です。

2026-11-06 のローカル再計測（i7-1355U、1コア固定、`OMP_NUM_THREADS=1`、Codonは `-release`、C++は `-O3 -std=gnu++20 -march=native`、起動・入出力を含む15回の実行時間中央値、ms）:

| 入力 | C++ AVX2 | 記事のCodon | 旧Codon版 | 現Codon版 |
| --- | ---: | ---: | ---: | ---: |
| 最大乱数 `524288 × 524288` | 29.6 | 309.6 | 125.5 | 96.4 |
| 長短 `100 × 524288` | 22.0 | 276.0 | 55.4 | 47.4 |
| 定数 `524288 × 524288` | 21.7 | 223.8 | 39.8 | 40.6 |

同条件で再計測したCodon版は、最大乱数が旧版 `94.6 ms`・現行版 `93.2 ms`、長短が `52.5 → 44.7 ms`、定数が `39.3 → 43.4 ms` でした。最大乱数と定数の改善は安定していません。

PyPy版は別の11回計測で最大乱数が `975.4 → 907.7 ms`、長短が `368.9 → 213.4 ms` でした。定数ケースは25回の追加計測で旧版 `180.8 ms`、現行版 `182.7 ms` とほぼ同等でした。

記事のCodon実装に対しては改善しましたが、指定された「アセンブリなしC++の2倍速」の目標は未達です。CPU負荷による変動が大きいため、数値はこの環境での参考値です。

1コアで実行する場合、Codonランタイムのスレッド競合を避けるため、実行前に `OMP_NUM_THREADS=1` を設定すると速くなる場合があります。ランタイムが起動する前に指定してください。
