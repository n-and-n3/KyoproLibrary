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

Codon版はMontgomery乗算、radix-4 NTT、8レーンSIMDを使います。PyPy版はradix-2 NTTです。両版とも短い入力の愚直積、長さが大きく異なる入力の分割積、定数配列、両端のゼロ、平方を処理します。動作確認はCodon 0.20.6、PyPy 3.9.18、x86-64 AVX2環境で行いました。

検証にはLibrary Checkerの `convolution_mod` 公式53ケースと追加乱数200ケースを使用しました。速度比較の基準は、[Qiitaの記事](https://qiita.com/navel_tos/items/9195de7041cf2c8b535b)の実装と、[Library CheckerのアセンブリなしC++提出](https://judge.yosupo.jp/submission/393435)です。

2026-11-06 のローカル計測（i7-1355U、1コア固定、Codonは `-release`、C++は `-O3 -std=gnu++20 -march=native`、9回の実行時間中央値、ms）:

| 入力 | C++ AVX2 | 記事のCodon | このCodon |
| --- | ---: | ---: | ---: |
| 最大乱数 `524288 × 524288` | 56 | 640 | 218 |
| 長短 `100 × 524288` | 53 | 536 | 131 |
| 定数 `524288 × 524288` | 93 | 835 | 179 |

記事の実装に対しては改善しましたが、指定された「アセンブリなしC++の2倍速」の目標は未達です。CPU負荷による変動が大きいため、数値はこの環境での参考値です。

PyPy版は別の5回計測で、同じ順の入力に対して中央値が約5.22秒、1.37秒、0.61秒でした。

1コアで実行する場合、Codonランタイムのスレッド競合を避けるため、実行前に `OMP_NUM_THREADS=1` を設定すると速くなる場合があります。同じ条件で記事のCodon実装にも設定した9回計測では、最大乱数入力がC++ 50 ms、記事のCodon 593 ms、このCodon 184 msでした。ランタイムが起動する前に指定する必要があります。
