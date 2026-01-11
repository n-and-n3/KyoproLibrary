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
#define vall(A) A.begin(),A.end()
#define vrall(A) A.rbegin(),A.rend()
#define slice(A, l, r) next((A).begin(), (l)), next((A).begin(), (r))
#define vin(A) for (ll iiii = 0, szszszsz = A.size(); iiii < szszszsz; iiii++){cin >> A[iiii];}
#define vout(A) for (ll iiii = 0, szszszsz = A.size(); iiii < szszszsz; iiii++){cout << A[iiii] << " \n"[iiii == szszszsz-1];}
#define vin2d(A) for (ll iiii = 0; iiii < A.size(); iiii++){for (ll jjjj = 0; jjjj < A[iiii].size(); jjjj++){cin >> A[iiii][jjjj];}}
#define vout2d(A) for (ll iiii = 0; iiii < A.size(); iiii++){for (ll jjjj = 0; jjjj < A[iiii].size(); jjjj++){cout << A[iiii][jjjj] << " \n"[jjjj==A[iiii].size()-1];}}
#define encode(i,j) ((i)<<32)+j
#define decode(v,w) (w ? (v)%4294967296 : (v)>>32)
#define vinc(A) for (auto &vvvv : A){vvvv++;}
#define vdec(A) for (auto &vvvv : A){vvvv--;}
#define graphin0(C, M) int aaaa,bbbb;for (int iiii = 0; iiii < (M); iiii++){cin >> aaaa >> bbbb; C[aaaa].push_back(bbbb); C[bbbb].push_back(aaaa);}
#define graphin1(C, M) int aaaa,bbbb;for (int iiii = 0; iiii < (M); iiii++){cin >> aaaa >> bbbb; C[aaaa-1].push_back(bbbb-1); C[bbbb-1].push_back(aaaa-1);}

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

ll powll(ll a, ll n, ll m){
    if (n == 0){return 1;}
    if (n == 1){return a % m;}
    LL ans = 1;
    LL p = a;
    while(n > 0){
        if (n & 1 == 1){
            ans *= p;
            ans %= m;
        }
        n >>= 1;
        p *= p;
        p %= m;
    }
    return (ll)ans;
}

// ===============================================================================


template <typename T>
struct PartialPersistentArray {
    struct Record{
        vector<pair<unsigned int,T>> history;

        Record(){}
        Record(T x): history(vector<pair<unsigned int,T>>(1,make_pair(0U,x))){}

        T get(unsigned int v){
            // 指定されたバージョンの数値に対して、それ以下の履歴の中で最大のものを探す
            int ok=0;
            int ng=history.size();
            int mid=0;
            while (ng - ok > 1){
                mid = (ok + ng)/2;
                if (history[mid].first <= v){
                    ok = mid;
                } else {
                    ng = mid;
                }
            }
            return history[ok].second;
        }

        void write(unsigned int v, T x){
            assert(history.back().first < v); // 最新版より大きい数値でないと、バージョンとして認めない。要するに二分探索がバグらないように単調性を要請する
            if (history.back().second != x){
                history.push_back({v,x});
            }
        }

        T current(unsigned int v){
            return history.back().second;
        }
    };

    struct Data{
        vector<Record> data;
        Data(vector<T> array){
            int N = array.size();
            data.resize(N); 
            for (int i=0; i<N; i++){
                this->data[i] = Record(array[i]);
            }
        }

        T get(unsigned int v, int ind){
            return this->data[ind].get(v);
        }

        void write(unsigned int v, int ind, T x){
            this->data[ind].write(v,x);
        }

        T current(unsigned int v, int ind){
            return this->data[ind].current(v);
        }
        
    };

    Data* data;
    unsigned int version;
    bool is_original;
    size_t _size;

    // 通常定義用 1
    PartialPersistentArray(vector<T> array){
        Data* new_data = new Data{array};
        this->data = new_data;
        this->is_original = true;
        this->version = 0U;
        this->_size = this->data->data.size();
    }

    // 通常定義用 2
    PartialPersistentArray(int N){
        Data* new_data = new Data{vector<T>(N)};
        this->data = new_data;
        this->is_original = true;
        this->version = 0U;
        this->_size = this->data->data.size();
    }

    // 通常定義用 3
    PartialPersistentArray(int N, T initial){
        Data* new_data = new Data{vector<T>(N,initial)};
        this->data = new_data;
        this->is_original = true;
        this->version = 0U;
        this->_size = this->data->data.size();
    }

    // リスト初期化用
    PartialPersistentArray(std::initializer_list<T> init): PartialPersistentArray(std::vector<T>(init)) {}

    // コピー用
    PartialPersistentArray(Data* data, unsigned int version){
        this->data = data;
        this->is_original = false;
        this->version = version;
        this->_size = this->data->data.size();
    }

    struct NodeRef {
        PartialPersistentArray<T>* st;
        int idx;

        NodeRef(PartialPersistentArray<T>* st, int idx) : st(st), idx(idx) {}

        NodeRef& operator=(const T& val) {st->write(idx, val); return *this;}
        NodeRef& operator=(const NodeRef& other) {st->write(idx, (T)other);return *this;}
        
        #define DEFINE_COMPOUND_OP(OP, BI_OP) \
        NodeRef& operator OP (const T& val) {st->write(idx, st->get(idx) BI_OP val); return *this;} \
        NodeRef& operator OP (const NodeRef& other) {st->write(idx, st->get(idx) BI_OP (T)other); return *this;} 

        DEFINE_COMPOUND_OP(+=, +)
        DEFINE_COMPOUND_OP(-=, -)
        DEFINE_COMPOUND_OP(*=, *)
        DEFINE_COMPOUND_OP(/=, /)
        DEFINE_COMPOUND_OP(%=, %)
        DEFINE_COMPOUND_OP(|=, |)
        DEFINE_COMPOUND_OP(&=, &)
        DEFINE_COMPOUND_OP(^=, ^)
        DEFINE_COMPOUND_OP(<<=, <<)
        DEFINE_COMPOUND_OP(>>=, >>)

        #undef DEFINE_COMPOUND_OP
        
        NodeRef& operator++() {st->write(idx, st->get(idx) + 1);return *this;}
        T operator++(int) {T old = st->get(idx);st->write(idx, old + 1);return old;}
        NodeRef& operator--() {st->write(idx, st->get(idx) - 1);return *this;}
        T operator--(int) {T old = st->get(idx);st->write(idx, old - 1);return old;}

        operator T() const {return st->get(idx);}
    };

    NodeRef operator[](int i) {
        return NodeRef(this, i);
    }

    T get(int ind){
        assert(0 <= ind && ind < _size);
        return data->get(this->version,ind);
    }

    void write(int ind, T x){
        assert(0 <= ind && ind < _size);
        assert(this->is_original);
        this->version++;
        data->write(this->version,ind,x);
    }

    T current(int ind){
        assert(0 <= ind && ind < _size);
        return data->current(this->version,ind);
    }

    size_t size(){
        return _size;
    }

    PartialPersistentArray<T> copy(){
        return PartialPersistentArray<T>(this->data,this->version);
    }

    operator vector<T>(){
        vector<T> ans(_size);
        for (int i=0; i<_size;i++){
            ans[i] = get(i);
        }
        return ans;
    }
};


// ===============================================================================


int main(){
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    vector<int> A = {1,2,3,4,5};
    PartialPersistentArray<int> PPA = {1,2,3,4,5};
    auto PPA_copy = PPA.copy();

    cout << "original :"; vout(PPA);
    cout << "copy :"; vout(PPA_copy);

    PPA[0] = 100;
    cout << "original :";vout(PPA);
    cout << "copy :";vout(PPA_copy);

    cout << PPA[2] << endl;

}