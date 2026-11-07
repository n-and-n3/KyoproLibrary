# Codon 版 KyoproLibrary

AtCoder の Codon 0.19.3 を対象に、`Python/` の 23 ファイルと `cpp/` の 43 ファイルに対応するコードを置いています。`convolution.py` はこのディレクトリの直下にあり、`convolution(a, b)` で 998244353 を法とする畳み込みを返します。`simd` は使用しません。64-bit 素数判定と素因数分解は `factorize.py`、多数の素数判定向け高速版は `is_prime_fast.py`、短い Baillie–PSW 版は `is_prime_bpsw.py` にあります。詳細は [../README.md](../README.md) を参照してください。

```
AI-slop/Codon/
├── convolution.py       # 単体で提出可能
├── factorize.py         # is_prime / factorize、10**18 まで
├── is_prime_fast.py     # 多数の判定向けの FJ32_256 / FJ64_16k 版
├── is_prime_bpsw.py     # 短い Baillie–PSW 版
├── verify_factorize.py # 数論ライブラリの自己検証
├── Python/              # 元の Python ファイルごとに対応
├── cpp/                 # 元の cpp ファイルごとに対応
└── README.md
```

`Python/` と `cpp/` の同名ファイルは独立した移植です。競技提出では必要なファイルを貼り付けて使えます。`cpp/Prime.py` は別の `cpp/` ファイルを import する集約入口で、`cpp/Prod_of_Sum_of_Log.py` は `cpp/PSL.py` を import します。この 2 ファイルを使う場合は依存先も同じディレクトリに置いてください。

## 元のインターフェースからの差

- C++ のテンプレート引数で指定していた定数は、`BinaryTreeSet(universe)`、`static_modint(value, MOD)` のようにコンストラクタ引数へ移しました。`static_modint` の MOD 省略時は 998244353 です。
- `Prime.cpp` 内の `n3::...` の名前空間は Codon では `from Prime import BIT, UnionFind, ...` のような直接 import にしました。遅延セグ木用の状態型は `PrimePresets.py` から `RSQ_RUQ_S`、`RSQ_RUQ_F` などとして import します。
- 演算を受け取る一部の汎用クラスでは、Codon 0.19.3 の型推論のためラムダより名前付き関数を渡してください。`UnionFindwithMonoid` では名前付き関数による呼び出しを確認しています。
- `PersistentSegmentTree.cpp` は元の `array` が構築されないまま参照されるため、Codon 版では共有ノードを使う永続セグ木として修正し、`clone()` と `copy()` を追加しました。
- `DoubleEndedPriorityQueue.cpp` の `pop_min` / `pop_max`、`PersistentQueue.cpp` のキュー本体、`UnionFindwithPotential.cpp` の本体、`Montgomery.cpp` の演算本体は元ファイルでは未実装でした。Codon 版には使用可能な実装を置きました。
- `Prod_of_Sum_of_Log.cpp` の本関数は元ファイルで未完成です。Codon 版の 1 引数関数は `PSL.py` の一般化関数を素数 3 で呼びます。

## 性能と前提

- `RangeParallelUnionFind.query` は階層ごとの UnionFind で対応区間を統合します。ハッシュ衝突がなく、償却計算量はおおむね `O((N+Q) log N α(N))` です。
- `PSL.py` の `Prod_of_Sum_of_Log` は完全冪の境界ごとに素数の指数を数えます。計算量はおおむね `O(√N log N)` で、元の `PSL.cpp` が狙う巨大な `N` では遅くなります。
- `WaveletMatrix` と `WaveletMatrixSegmentTree` のキーは非負整数を想定します。`Sum_of_Prod_of_Root` の MOD と `Prod_of_Sum_of_Log` の P は素数を想定します。
- Codon の `int` は符号付き 64 ビットです。素数判定には積で `u128` を使い、64 ビット付近のオーバーフローを避けています。

## 確認内容

Codon 0.19.3 で各公開 API の代表的な呼び出しをコンパイル・実行しました。追加で遅延セグ木、Wavelet Matrix、値付き Wavelet Matrix、PriorityQue、DeletablePriorityQue、MexMultiSet、区間並列 UnionFind、履歴付き二辺連結性を乱数ケースの愚直解と照合しました。`Sum_of_Prod_of_Root` と `Prod_of_Sum_of_Log` は小さい入力で元の愚直関数と照合しました。保存した回帰確認は `codon run selfcheck.py` で実行できます。
