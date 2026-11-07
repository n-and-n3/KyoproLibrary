# 64-bit 素数判定・素因数分解

Codon 0.19.3 用は [Codon/factorize.py](Codon/factorize.py)、PyPy 3.11 用は [PyPy/factorize.py](PyPy/factorize.py)。両方とも `is_prime(n) -> bool` と `factorize(n) -> list[int]` を公開する。`factorize` の結果は重複を含む昇順の素因数列で、`factorize(1) == []`。Codon 版は `1 <= n <= 10**18`、PyPy 版は `1 <= n < 2**64` を扱う。素数判定は 0 と負数に対して `False` を返す。

多数の素数判定だけを行う場合は、別の [Codon/is_prime_fast.py](Codon/is_prime_fast.py) と [PyPy/is_prime_fast.py](PyPy/is_prime_fast.py) にある同名の `is_prime` が速い。Forišek–Jančina の FJ32_256 と FJ64_16k ハッシュ表を使い、素数に対する Miller–Rabin を 32-bit 範囲では 1 回、64-bit 範囲では 3 回に減らす。約 145–200 KB のソースが増えるので、分解ライブラリには組み込んでいない。Codon 高速版は単一ファイルで完結している。

## 採用した方法

- 小さい素数で先に割り、残りを [決定的 64-bit Miller–Rabin](https://miller-rabin.appspot.com/) で判定する。小さい範囲では `{2,7,61}`、それ以外では 7 基底を使う。
- 判定中に `x² ≡ 1 (mod n)` かつ `x ≠ ±1 (mod n)` となったら `gcd(x−1,n)` で因数を取り出す。因数が出ない合成数は、近い因数向けの短い Fermat 法を試し、残りを [Brent 版 Pollard rho](https://maths-people.anu.edu.au/~brent/pub/pub051.html) で分解する。
- Codon では 64-bit Montgomery 乗算、PyPy では組み込みの `pow(a,b,n)` と `math.gcd` を使う。rho の積は Codon で最大 256 回、PyPy で最大 128 回ごとに gcd を取る。

## 検証

[Library Checker の公式ジェネレータ](https://github.com/yosupo06/library-checker-problems)を 2026-11-07 に実行した。`factorize` 31 ファイル、計 2,635 数、`primality_test` 13 ファイル、計 801,129 数について Codon・PyPy の出力が公式解と一致した。高速素数判定も全 13 ファイルで一致し、PyPy 高速版はさらにランダムな 64-bit 整数 200,000 個で通常版と一致した。

Miller–Rabin 中の因数抽出は、分解ケースの最初の 2,635 数に対して 95 回成功した。うち 93 回は Carmichael ケースで、大きな半素数 400 個では 0 回だった。したがって、この工夫は安価なので入れているが、最も重い半素数を速くする中心策にはならない。近い因数を持つ `big2` 系では Fermat 法が 400 個中 312 個を rho なしで分解した。

指定された [Baillie–PSW の記事](https://note.com/vunu/n/n273765af77d6)に対応する強い Lucas テストも PyPy で試作した。公式 `all_prime` 10 万件の関数本体は、試作 BPSW が約 1.39 秒、7 基底 Miller–Rabin が約 0.5–0.7 秒だった。BPSW 自体の普遍的な速度比較ではなく、今回の実装と入力での比較である。SQUFOF と Pollard p−1 も大きな半素数で試したが、今回の実装では rho より速くならなかった。18 桁の整数に一般数体篩法を使う意義は小さく、[FLINT の 64-bit 分解方針](https://github.com/flintlib/flint/blob/main/doc/src/algorithms/number-theory/integer-factoring.md)も rho、Hart 法、SQUFOF の組み合わせである。

オンラインの最速提出は 2026-11-07 時点で、[factorize](https://judge.yosupo.jp/submissions/?problem=factorize&order=%2Btime&status=AC) が C++ 13 ms、PyPy 237 ms、[primality_test](https://judge.yosupo.jp/submissions/?problem=primality_test&order=%2Btime&status=AC) が C++ 30 ms、PyPy 331 ms。Codon の提出言語は Library Checker にない。ローカル値とオンライン値は CPU・入出力が違うため直接比較しない。

ローカルの関数本体だけを測ると、Codon の `all_prime` 10 万件は通常版が約 0.44 秒、高速版が約 0.25 秒だった。PyPy の同ケースは通常版が約 0.5 秒、高速版が約 0.25–0.4 秒だった。実際の提出速度は入力・出力方式にも左右される。
