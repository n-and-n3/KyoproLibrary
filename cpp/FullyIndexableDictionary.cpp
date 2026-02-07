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
#include <bit>
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

vector<ll> pow2ll{1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483648,4294967296,8589934592,17179869184,34359738368,68719476736,137438953472,274877906944,549755813888,1099511627776,2199023255552,4398046511104,8796093022208,17592186044416,35184372088832,70368744177664,140737488355328,281474976710656,562949953421312,1125899906842624,2251799813685248,4503599627370496,9007199254740992,18014398509481984,36028797018963968,72057594037927936,144115188075855872,288230376151711744,576460752303423488,1152921504606846976,2305843009213693952,4611686018427387904};
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

struct FullyIndexableDictionary{
    using u16 = unsigned short;
    using u32 = unsigned int;
    using u64 = unsigned long long;

    size_t sz,count;
    bool is_builded;

    vector<u64> data;  // 64bit区切りでデータを持っておく
    vector<u32> CT;  // チャンクテーブル、各チャンクの先頭の rank を前計算する。
    vector<u64> BT;  // ブロックテーブル、各ブロックが所属するチャンクの始点からの rank を前計算する。u9 * 7 を u64を使い違法圧縮している。展開用関数を作らねば...

    FullyIndexableDictionary(size_t sz):is_builded(false), sz(sz), count((sz+511)/512), data(((sz+511)/512)*8,0), CT((sz+511)/512,0), BT((sz+511)/512,0){};

    void set(int i, bool b){
        assert(!is_builded);
        if (b){ write1(i);} else { write0(i);}
    }

    void set(int i, char b){
        assert(!is_builded);
        if (b=='0'){ write0(i);} else { write1(i);}
    }

    void set(int i, int b){
        assert(!is_builded);
        if (b==0){ write0(i);} else { write1(i);}
    }

    void build(){
        assert(!is_builded);
        is_builded = true;

        int rank_all = 0;
        int rank_part = 0;
        for (int i=0; i<count ;i++){
            CT[i] = rank_all;
            rank_part = 0;
            for (int j=0;j<8;j++){
                write64(BT[i], rank_part, j);
                rank_part += __builtin_popcountll(data[(i<<3)+j]);
            }
            rank_all += rank_part;
        }
    }

    int rank(int n,int b){  // [0,n) までに含まれる b の個数
        if (b == 0){
            return n - rank1(n);
        } else {
            return rank1(n);
        }
    }

    private:
    inline void write1(int i){
        data[i>>6] |= ((u64)1)<<(i&((1<<6)-1));
    }

    inline void write0(int i){
        data[i>>6] &= ~(((u64)1)<<(i&((1<<6)-1)));
    }

    inline int read64(u64 bits, int i){
        // assert(0 <= i < 8)
        if (i == 0){
            return 0;
        } else {
            return (bits>>((i-1)*9))&((1<<9)-1);
        }
    }

    inline void write64(u64& bits, int num, int i){
        // assert(0 <= i < 8)
        if (i != 0){
            bits |= ((u64)num)<<((i-1)*9);
        }
    }

    inline int rank1(int n){
        return CT[n/512] + read64(BT[n/512],(n&511)>>6) + __builtin_popcountll((data[n/64] & ((((u64)1)<<(n&63))-1)));
    }
};


// ===============================================================================

int main(){
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    FullyIndexableDictionary bit_vector(10);

    bit_vector.set(0, 0);
    bit_vector.set(1, 0);
    bit_vector.set(2, 1);
    bit_vector.set(3, 1);
    bit_vector.set(4, 0);
    bit_vector.set(5, 0);
    bit_vector.set(6, 1);
    bit_vector.set(7, 1);
    bit_vector.set(8, 0);
    bit_vector.set(9, 1);

    bit_vector.build();

    cout << bit_vector.rank(0,1) << endl;
    cout << bit_vector.rank(1,1) << endl;
    cout << bit_vector.rank(2,1) << endl;
    cout << bit_vector.rank(3,1) << endl;
    cout << bit_vector.rank(4,1) << endl;
    cout << bit_vector.rank(5,1) << endl;
    cout << bit_vector.rank(6,1) << endl;
    cout << bit_vector.rank(7,1) << endl;
    cout << bit_vector.rank(8,1) << endl;
    cout << bit_vector.rank(9,1) << endl;
    cout << bit_vector.rank(10,1) << endl;

    cout << "end" << endl;
    
}