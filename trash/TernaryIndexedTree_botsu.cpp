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

// 座標を負の方向に伸ばせるvector、デキューのインデックスがズレていかないもの、と解釈できる
template <typename T>
struct devector{
    deque<T> devec;
    int offset;

    devector(){}
    devector(int start,int goal, T init_val) : devec(goal-start+1,init_val), offset(start){}
    devector(initializer_list<T> list) : devec(list), offset(0){}
    devector(initializer_list<T> list, int offset) : devec(list), offset(offset){}

    T& operator[] (int x){
        return devec[x-offset];
    }

    int start(){
        return offset;
    }

    int goal(){
        return devec.size() + offset - 1;
    }

    void push_back(const T& val){
        devec.push_back(val);
    }

    void push_front(const T& val){
        devec.push_front(val);
        offset -= 1;
    }

    void pop_back(){
        assert(!devec.empty());
        devec.pop_back();
    }

    void pop_front(){
        assert(!devec.empty());
        devec.pop_front();
        offset += 1;
    }

    size_t size(){
        return devec.size();
    }

    void assign(int s,int g,T value){
        devec.assign(g-s+1, value);
        offset = s;
    }

};

// ==========================================================================

// @brief TernaryIndexedTree
struct TIT {
    devector<ll> array;
    TIT(int s, int g) : array(devector<ll>(s,g,0)) {}
    TIT(initializer_list<ll> list, int offset) : array(devector<ll>(list, offset)) {build();}
    TIT(devector<ll> list) : array(list) {build();}

    // @brief 初期値にリストが与えられた場合の実装
    void build(){
        // 右端のindexの終端を、3の累乗-1の形にする
        int tmp = 1;
        while (tmp + 1 < array.goal()){
            tmp *= 3;
        }
        int diff = tmp - 1 - array.goal(); 
        if (diff > 0){
            for (int i = 0; i < diff; i++){
                array.push_back(0);
            }
        }
    }


};


// ===============================================================================

int main(){
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    TIT tit({1,2,3,4,5}, 0);
    cout << endl;
}