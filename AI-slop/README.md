# 64-bit 素数判定・素因数分解

Codon 0.19.3 用は [Codon/factorize.py](Codon/factorize.py)、PyPy 3.11 用は [PyPy/factorize.py](PyPy/factorize.py)。両方とも `is_prime(n) -> bool` と `factorize(n) -> list[int]` を公開する。`factorize` の結果は重複を含む昇順の素因数列で、`factorize(1) == []`。Codon 版は `1 <= n <= 10**18`、PyPy 版は `1 <= n < 2**64` を扱う。素数判定は 0 と負数に対して `False` を返す。

多数の素数判定だけを行う場合は、別の [Codon/is_prime_fast.py](Codon/is_prime_fast.py) と [PyPy/is_prime_fast.py](PyPy/is_prime_fast.py) にある同名の `is_prime` が速い。Forišek–Jančina の FJ32_256 と FJ64_16k ハッシュ表を使い、素数に対する Miller–Rabin を 32-bit 範囲では 1 回、64-bit 範囲では 3 回に減らす。約 145–200 KB のソースが増えるので、分解ライブラリには組み込んでいない。Codon 高速版は単一ファイルで完結している。

Codon には 4.2 KB の [Codon/is_prime_bpsw.py](Codon/is_prime_bpsw.py) もある。底 2 の強い Miller–Rabin と Selfridge の強い Lucas テストを組み合わせた単一ファイルで、`is_prime(n)` を公開する。ハッシュ表が必要ない小さいコードとして使える。

## 採用した方法

- 小さい素数で先に割り、残りを [決定的 64-bit Miller–Rabin](https://miller-rabin.appspot.com/) で判定する。小さい範囲では `{2,7,61}`、それ以外では 7 基底を使う。
- Codon の Miller–Rabin では基底が `n` 未満なら余分な剰余を取らない。公式の素数中心ケースを同一プロセス内で交互に測ると、判定部分が数 % 速くなった。
- 判定中に `x² ≡ 1 (mod n)` かつ `x ≠ ±1 (mod n)` となったら `gcd(x−1,n)` で因数を取り出す。例: `5461 = 43 × 127` では底 2 の途中で `x = 128` となり、`128² ≡ 1 (mod 5461)` と `gcd(127, 5461) = 127` から因数が得られる。因数が出ない合成数は、近い因数向けの短い Fermat 法を試し、残りを [Brent 版 Pollard rho](https://maths-people.anu.edu.au/~brent/pub/pub051.html) で分解する。
- Codon では 64-bit Montgomery 乗算、PyPy では組み込みの `pow(a,b,n)` と `math.gcd` を使う。rho の積は Codon で最大 256 回、PyPy で最大 512 回ごとに gcd を取る。

PyPy の gcd 間隔は 64、128、256、512、1024 を比較した。公式の大きな半素数 400 個と追加の半素数 1,000 個を、各入力で同じ乱数初期値にそろえ、各実装を交互に呼ぶ測定で 512 回を選んだ。法が `2**31` 未満か `2**63` 以上のときは `pow(y,2,n)` から `y*y%n` に切り替える。30-bit 前後の半素数 10,000 個では約 0.25 秒から 0.18 秒へ短縮した。PyPy 7.3.20 では `2**63` を超えると `pow` が急に遅くなり、`10**19` 付近の半素数 100 個で約 20 秒から約 3.5 秒になった。変更後は 1,000 個を約 35 秒で分解した。中間の法では `pow(y,2,n)+c` の後を条件付き減算にすると、通常の剰余より 2～4% 速かった。

## 検証

[Library Checker の公式ジェネレータ](https://github.com/yosupo06/library-checker-problems)を 2026-11-07 に実行した。`factorize` 31 ファイル、計 2,635 数、`primality_test` 13 ファイル、計 801,129 数について Codon・PyPy の出力が公式解と一致した。さらに 20,000 個の半素数でも両方の因数列を確認した。高速素数判定と Codon の BPSW 版も全 13 ファイルで一致した。Codon BPSW 版は 100 万以下の全整数と、ランダムな 20 万整数で通常版と一致した。PyPy 高速版はランダムな 64-bit 整数 200,000 個で通常版と一致した。PyPy の通常版は `2**64-1` の分解と `2**64-59` の素数判定も確認した。

Miller–Rabin 中の因数抽出は、分解ケースの最初の 2,635 数に対して 95 回成功した。うち 93 回は Carmichael ケースで、大きな半素数 400 個では 0 回だった。公式 2,635 数全体の PyPy 測定では、抽出ありの rho 呼び出しが 1,901 回、抽出なしが 2,022 回だった。Carmichael 100 件だけでは 82 回対 200 回で、分解時間は約 4 割減った。この工夫は構造のある合成数には効くが、最も重い半素数を速くする中心策にはならない。近い因数を持つ `big2` 系では、Fermat 法を 32 回試すと 400 個中 312 個、128 回なら全 400 個を rho なしで分解した。128 回に変更した結果、PyPy の `big2` 全 400 件の関数実行時間は約 0.28 秒から約 0.02 秒になった。平方数の 16 による剰余を先に調べることで、離れた因数を持つ 400 件の前処理も 100 回反復で約 0.8 秒から約 0.25 秒になった。

指定された [Baillie–PSW の記事](https://note.com/vunu/n/n273765af77d6)に対応する強い Lucas テストも調べた。[Baillie・Fiori・Wagstaff の論文](https://doi.org/10.1090/mcom/3616)には、この組み合わせの反例が `2**64` 未満では見つからなかったという網羅的な検証結果があり、一般の整数について反例が存在しないかは未解決とある。論文では Selfridge 法 A と A* の強い Lucas 判定の結果が同じことも示されており、Codon 版は A を使う。PyPy 試作の公式 `all_prime` 10 万件の関数本体は BPSW が約 1.39 秒、7 基底 Miller–Rabin が約 0.5–0.7 秒で、採用しなかった。一方 Codon では BPSW が 7 基底版の約 2 倍速く、FJ ハッシュ表版より約 5～10% 遅い程度だったので、小さいコードの選択肢として追加した。分解後に多い `10**9` 付近の素数は 3 基底 Miller–Rabin の方が速いため、分解ライブラリには組み込んでいない。これらは今回の実装と入力での比較である。SQUFOF と Pollard p−1 も大きな半素数で試したが、今回の実装では rho より速くならなかった。18 桁の整数に一般数体篩法を使う意義は小さく、[FLINT の 64-bit 分解方針](https://github.com/flintlib/flint/blob/main/doc/src/algorithms/number-theory/integer-factoring.md)も rho、Hart 法、SQUFOF の組み合わせである。

オンラインの最速提出は 2026-11-07 時点で、[factorize](https://judge.yosupo.jp/submissions/?problem=factorize&order=%2Btime&status=AC) が C++ 13 ms、PyPy 237 ms、[primality_test](https://judge.yosupo.jp/submissions/?problem=primality_test&order=%2Btime&status=AC) が C++ 30 ms、PyPy 331 ms。Codon の提出言語は Library Checker にない。ローカル値とオンライン値は CPU・入出力が違うため直接比較しない。

ローカルの関数本体だけを測ると、Codon の `all_prime` 10 万件は通常版が約 0.44 秒、高速版が約 0.25 秒だった。PyPy の同ケースは通常版が約 0.5 秒、高速版が約 0.25–0.4 秒だった。Codon 高速版は `n < 2**31` に 32-bit Montgomery 演算を使う。同じ素数 `1000000007` を 10 万回判定した場合、従来の 64-bit 演算が約 47 ms、32-bit 演算が約 23 ms だった。実際の提出速度は入力・出力方式にも左右される。
