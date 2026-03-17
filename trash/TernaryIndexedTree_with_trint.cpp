#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <set>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <queue>
#include <algorithm>
#include <iomanip>
#include <functional>
#include <cassert>
#include <initializer_list>
#include <bit>
#include <array>
#include <atcoder/all>

using namespace std;
using namespace atcoder;
using mint = modint998244353;

#define ll long long
#define LL __int128
#define MOD 998244353
#define ld long double
#define INF 2251799813685248
#define rep(i, n) for (ll i = 0; i < (n); ++i)
#define reps(i, l, r) for(ll i = (l); i < (r); ++i)
#define foreach(c, A) for(auto c:(A))
#define vall(A) (A).begin(),(A).end()
#define vrall(A) (A).rbegin(),(A).rend()
#define slice(A, l, r) next((A).begin(), (l)), next((A).begin(), (r))
#define vin(A) for (ll iiii = 0, szszszsz = (A).size(); iiii < szszszsz; iiii++){cin >> (A)[iiii];}
#define vout(A) for (ll iiii = 0, szszszsz = (A).size(); iiii < szszszsz; iiii++){cout << (A)[iiii] << " \n"[iiii == szszszsz-1];}
#define vin2d(A) for (ll iiii = 0; iiii < (A).size(); iiii++){for (ll jjjj = 0; jjjj < (A)[iiii].size(); jjjj++){cin >> (A)[iiii][jjjj];}}
#define vout2d(A) for (ll iiii = 0; iiii < (A).size(); iiii++){for (ll jjjj = 0; jjjj < (A)[iiii].size(); jjjj++){cout << (A)[iiii][jjjj] << " \n"[jjjj==(A)[iiii].size()-1];}}
#define encode(i,j) (((i))<<32)+(j)
#define decode(v,w) ((w) ? (v)%4294967296 : (v)>>32)
#define vinc(A) for (auto &vvvv : (A)){vvvv++;}
#define vdec(A) for (auto &vvvv : (A)){vvvv--;}
#define graphin0(C, M) int aaaa,bbbb;for (int iiii = 0; iiii < (M); iiii++){cin >> aaaa >> bbbb; (C)[aaaa].push_back(bbbb); (C)[bbbb].push_back(aaaa);}
#define graphin1(C, M) int aaaa,bbbb;for (int iiii = 0; iiii < (M); iiii++){cin >> aaaa >> bbbb; (C)[aaaa-1].push_back(bbbb-1); (C)[bbbb-1].push_back(aaaa-1);}
#define lsegtype(name) name::S, name::F
#define lsegarg(name) name::op, name::e,name::comp, name::mapping, name::id

vector<ll> pow2ll{1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483648,4294967296,8589934592,17179869184,34359738368,68719476736,137438953472,274877906944,549755813888,1099511627776,2199023255552,4398046511104,8796093022208,17592186044416,35184372088832,70368744177664,140737488355328,281474976710656,562949953421312,1125899906842624,2251799813685248,4503599627370496,9007199254740992,18014398509481984,36028797018963968,72057594037927936,144115188075855872,288230376151711744,576460752303423488,1152921504606846976,2305843009213693952,4611686018427387904};
vector<ll> pow3ll{1,3,9,};
vector<ll> pow10ll{1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000,10000000000,100000000000,1000000000000,10000000000000,100000000000000,1000000000000000,10000000000000000,100000000000000000,1000000000000000000};
vector<ll> di{0,1,0,-1};
vector<ll> dj{1,0,-1,0};

istream &operator>>(istream &is, mint &i){long long t; is >> t; i = t; return is; }
ostream &operator<<(ostream &os, const mint &i){ os << i.val(); return os;}

template <typename T>
bool chmax(T &a, const T& b) { return a < b ? a = b, true : false; }
template <typename T>
bool chmin(T &a, const T& b) { return a > b ? a = b, true : false; }

unsigned int bit_length(ll n){ return n > 0 ? 64 - __builtin_clzll(n) : 0;}

template <typename T>
T sum(vector<T> A){
    T res = 0;
    for (size_t i=0;i<A.size();i++){
        res += A[i];
    }
    return res;
}

ll powll(ll a, ll n, ll m){
    if (n == 0){return 1;}
    if (n == 1){return a % m;}
    LL ans = 1;
    LL p = a;
    while(n > 0){
        if ((n & 1) == 1){
            ans *= p;
            ans %= m;
        }
        n >>= 1;
        p *= p;
        p %= m;
    }
    return (ll)ans;
}

// =========================================================================

class trint {
private:
    int val;
    // 3^20 = 3,486,784,401. 
    // 平衡三進数20桁の最大値は (3^20 - 1) / 2 = 1,743,392,200.
    // これは 32bit signed int (最大 2,147,483,647) に安全に収まる。
    static const int TRIT_WIDTH = 20; 

    // int -> 平衡三進数の配列(下位桁から順に格納)
    std::array<int, TRIT_WIDTH> to_trits() const {
        std::array<int, TRIT_WIDTH> trits = {0};
        long long n = val;
        for (int i = 0; i < TRIT_WIDTH; ++i) {
            int rem = n % 3;
            if (rem < 0) rem += 3;
            
            if (rem == 2) {
                trits[i] = -1;
                n = (n + 1) / 3;
            } else {
                trits[i] = rem;
                n = (n - rem) / 3;
            }
        }
        return trits;
    }

    // 平衡三進数の配列 -> int
    static int from_trits(const std::array<int, TRIT_WIDTH>& trits) {
        long long res = 0;
        long long p = 1;
        for (int i = 0; i < TRIT_WIDTH; ++i) {
            res += trits[i] * p;
            p *= 3;
        }
        return static_cast<int>(res);
    }

public:
    // コンストラクタ
    trint(int v = 0) : val(v) {}
    
    // 文字列からの初期化
    trint(const std::string& s) {
        std::array<int, TRIT_WIDTH> trits = {0};
        int len = s.length();
        for (int i = 0; i < len && i < TRIT_WIDTH; ++i) {
            char c = s[len - 1 - i]; // 下の桁(右側)からパース
            if (c == '+') trits[i] = 1;
            else if (c == '-') trits[i] = -1;
            else trits[i] = 0;
        }
        val = from_trits(trits);
    }

    // 暗黙のint型変換
    operator int() const { return val; }

    // --- トリット演算 ---

    trint operator-() const { return trint(-val); }

    // 単項~: 巡回シフト (+ -> -, 0 -> +, - -> 0)
    trint operator~() const {
        auto trits = to_trits();
        for (int i = 0; i < TRIT_WIDTH; ++i) {
            if (trits[i] == 1) trits[i] = -1;
            else if (trits[i] == 0) trits[i] = 1;
            else if (trits[i] == -1) trits[i] = 0;
        }
        return trint(from_trits(trits));
    }

    // 二項&: Trit-wise MIN
    trint operator&(const trint& other) const {
        auto t1 = to_trits();
        auto t2 = other.to_trits();
        std::array<int, TRIT_WIDTH> res;
        for (int i = 0; i < TRIT_WIDTH; ++i) {
            res[i] = std::min(t1[i], t2[i]);
        }
        return trint(from_trits(res));
    }

    // 二項|: Trit-wise MAX
    trint operator|(const trint& other) const {
        auto t1 = to_trits();
        auto t2 = other.to_trits();
        std::array<int, TRIT_WIDTH> res;
        for (int i = 0; i < TRIT_WIDTH; ++i) {
            res[i] = std::max(t1[i], t2[i]);
        }
        return trint(from_trits(res));
    }

    // 二項^: Trit-wise 積
    trint operator^(const trint& other) const {
        auto t1 = to_trits();
        auto t2 = other.to_trits();
        std::array<int, TRIT_WIDTH> res;
        for (int i = 0; i < TRIT_WIDTH; ++i) {
            res[i] = t1[i] * t2[i];
        }
        return trint(from_trits(res));
    }

    // シフト演算子
    trint operator<<(int shift) const {
        auto trits = to_trits();
        std::array<int, TRIT_WIDTH> res = {0};
        for (int i = 0; i < TRIT_WIDTH - shift; ++i) {
            res[i + shift] = trits[i];
        }
        return trint(from_trits(res));
    }

    trint operator>>(int shift) const {
        auto trits = to_trits();
        std::array<int, TRIT_WIDTH> res = {0};
        for (int i = shift; i < TRIT_WIDTH; ++i) {
            res[i - shift] = trits[i];
        }
        return trint(from_trits(res));
    }

    // --- 複合代入演算子 ---
    trint& operator&=(const trint& rhs) { *this = *this & rhs; return *this; }
    trint& operator|=(const trint& rhs) { *this = *this | rhs; return *this; }
    trint& operator^=(const trint& rhs) { *this = *this ^ rhs; return *this; }
    
    trint& operator+=(const trint& rhs) { val += rhs.val; return *this; }
    trint& operator-=(const trint& rhs) { val -= rhs.val; return *this; }
    trint& operator*=(const trint& rhs) { val *= rhs.val; return *this; }
    trint& operator/=(const trint& rhs) { val /= rhs.val; return *this; }
    trint& operator%=(const trint& rhs) { val %= rhs.val; return *this; }

    trint& operator<<=(int shift) { *this = *this << shift; return *this; }
    trint& operator>>=(int shift) { *this = *this >> shift; return *this; }

    // --- インクリメント・デクリメント ---
    trint& operator++() { ++val; return *this; }
    trint operator++(int) { trint temp = *this; ++val; return temp; }
    trint& operator--() { --val; return *this; }
    trint operator--(int) { trint temp = *this; --val; return temp; }

    // --- 表示用 ---
    std::string to_string() const {
        if (val == 0) return "0";
        auto trits = to_trits();
        std::string s = "";
        bool leading = true;
        for (int i = TRIT_WIDTH - 1; i >= 0; --i) {
            if (trits[i] != 0) leading = false;
            if (!leading) {
                if (trits[i] == 1) s += "+";
                else if (trits[i] == -1) s += "-";
                else s += "0";
            }
        }
        return s;
    }

    // friend関数としてストリーム演算子を定義
    friend std::istream& operator>>(std::istream& is, trint& t) {
        std::string s;
        is >> s;
        // 入力文字列が "+-0" のみで構成されているかチェック
        if (s.find_first_not_of("+-0") == std::string::npos) {
            t = trint(s); // 平衡三進数文字列としてパース
        } else {
            t = trint(std::stoi(s)); // 10進数整数としてパース
        }
        return is;
    }
};

// 算術演算子 (非メンバ関数)
trint operator+(trint lhs, const trint& rhs) { lhs += rhs; return lhs; }
trint operator-(trint lhs, const trint& rhs) { lhs -= rhs; return lhs; }
trint operator*(trint lhs, const trint& rhs) { lhs *= rhs; return lhs; }
trint operator/(trint lhs, const trint& rhs) { lhs /= rhs; return lhs; }
trint operator%(trint lhs, const trint& rhs) { lhs %= rhs; return lhs; }

// 出力ストリーム
std::ostream& operator<<(std::ostream& os, const trint& t) {
    os << t.to_string();
    return os;
}
// ==========================================================================

#include <vector>
#include <iostream>

// @brief 真のTernaryIndexedTree (Powered by trint)
template <typename T>
struct TIT {
    vector<T> array;
    size_t sz;
    TIT(initializer_list<T> init_list){
        init(init_list.begin(), init_list.end());
    }

    TIT(const vector<T>& init_vec){
        init(init_vec.begin(), init_vec.end());
    }

private:
    template <class It>
    void init(It first, It last){
        // 冒頭に0を挿入したうえで初期化
        array.clear();
        array.push_back(0);
        array.insert(array.end(), first, last); // 元の配列を代入

        // サイズを (3^k-1)/2 型 にする。3の累乗でもいいけど、平衡三進数的にはこれが自然。
        trint tmp = 1;
        while (tmp < (trint)array.size() - trint(1)) {
            tmp = (tmp << 1) + trint(1);
        }
        array.resize(tmp+trint(1), 0); // 1-indexed なので +1 する
        sz = array.size() - 1;

        // テーブルの構築
        trint pos = 2;
        trint p = 1;
        while (pos < (trint)array.size()) {
            for (trint i = pos; i <= (trint)sz; i+=trint(3)*p) {
                array[i] += array[i - p];
                array[i] += array[i + p];
            }
            pos = (pos << 1) - trint(1);
            p <<= 1;
        }
    }

public:

    T cum(trint ind){
        T res = 0;
        trint pos = 0;
        for (int i = 0; i < 60 && ind > 0; ++i) { // 60は適当な上限値
            if ((ind ^ trint(1)) == 1){
                res += array[(ind<<i) - pos];
                ind -= 1;
            } else if ((ind ^ trint(1)) == -1){
                ind += 1;
                res -= array[(ind<<i) - pos];
            }
            ind >>= 1;
            pos = (pos << 1) + trint(1);
        }
        return res;
    }

    T get(trint ind){
        return cum(ind) - cum(ind-trint(1));
    }

    void add(trint ind, T x){
        trint pos = 0;
        for (int i=0; (ind<<i) <= sz; i++){
            if ((ind ^ trint(1)) != -1){
                array[(ind<<i) - pos] += x;
            }
            ind = (ind-trint(1))/trint(3)+trint(1);  // ここはうまくtrit演算を使えなかった
            pos = (pos << 1) + trint(1);
        }
    }

    void write(trint ind, T x){
        add(ind, x - get(ind));
    }

    size_t size(){
        return sz;
    }


};


// ===============================================================================

int main(){
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N,Q;
    cin >> N >> Q;
    vector<ll> A(N);
    vin(A);
    TIT<ll> tit(A);

    int t,x,y;
    rep(i,Q){
        cin >> t >> x >> y;
        if (t == 0){
            tit.add(x+1,y);
        } else {
            cout << tit.cum(y) - tit.cum(x) << endl;
        }
    }
}