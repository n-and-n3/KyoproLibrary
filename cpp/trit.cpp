#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <set>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <queue>
#include <deque>
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

// ===========================================================================

// 平衡三進数を扱うクラス
struct trint{
    int val;
    deque<char> trits; // trits[i] is i-th trit (i=0 is least significant)

    trint():val(0), trits({'0'}){}
    trint(int v): val(v){
        rebuild_trits_from_val();
    }

    static int char_to_trit(char c){
        if (c == '+') return 1;
        if (c == '-') return -1;
        return 0;
    }

    static char trit_to_char(int t){
        if (t > 0) return '+';
        if (t < 0) return '-';
        return '0';
    }

    static int pow3(int i){
        assert(0 <= i && i <= 19);
        static const array<int, 20> p = {
            1,
            3,
            9,
            27,
            81,
            243,
            729,
            2187,
            6561,
            19683,
            59049,
            177147,
            531441,
            1594323,
            4782969,
            14348907,
            43046721,
            129140163,
            387420489,
            1162261467,
        };
        return p[i];
    }

    void normalize_trits(){
        while(trits.size() > 1 && trits.back() == '0') trits.pop_back();
        if (trits.empty()) trits.push_back('0');
    }

    void rebuild_trits_from_val(){
        trits.clear();
        if (val == 0){
            trits.push_back('0');
            return;
        }
        int c = val;
        while(c != 0){
            int k = pop_trit(c);
            trits.push_back(trit_to_char(k));
        }
        normalize_trits();
    }

    static trint build_from_raw(int v, deque<char>&& raw){
        trint t;
        t.val = v;
        t.trits = std::move(raw);
        t.normalize_trits();
        return t;
    }

    struct trit_ref{
        trint* self;
        int idx;

        operator int() const{
            return self->get_trit(idx);
        }

        trit_ref& operator=(int digit){
            self->set_trit(idx, digit);
            return *this;
        }

        trit_ref& operator=(const trit_ref& other){
            return (*this) = (int)other;
        }
    };

    bool operator==(const trint& other) const{
        return val == other.val;
    }

    bool operator!=(const trint& other) const{
        return val != other.val;
    }

    bool operator<=(const trint& other) const{
        return val <= other.val;
    }

    bool operator>=(const trint& other) const{
        return val >= other.val;
    }

    bool operator<(const trint& other) const{
        return val < other.val;
    }

    bool operator>(const trint& other) const{
        return val > other.val;
    }

    static int pop_trit(int &c){
        int r = c % 3;
        c /= 3;
        if (r == 2){
            r = -1;
            c += 1;
        } else if (r == -2){
            r = 1;
            c -= 1;
        }
        return r;
    }

    int get_trit(int i) const{
        assert(i >= 0);
        if (i >= (int)trits.size()) return 0;
        return char_to_trit(trits[i]);
    }

    void set_trit(int i, int digit){
        assert(i >= 0);
        assert(-1 <= digit && digit <= 1);
        int current = get_trit(i);
        if (i >= (int)trits.size()) trits.resize(i+1, '0');
        trits[i] = trit_to_char(digit);

        val = val + (digit - current) * pow3(i);
        normalize_trits();
    }

    trit_ref operator[](int i){
        return trit_ref{this, i};
    }

    int operator[](int i) const{
        return get_trit(i);
    }

    trint operator&(const trint& other) const{
        int n = max((int)trits.size(), (int)other.trits.size());
        deque<char> res_trits;
        res_trits.resize(n, '0');
        int res_val = val;
        for(int i=0;i<n;i++){
            int a = (i < (int)trits.size()) ? char_to_trit(trits[i]) : 0;
            int b = (i < (int)other.trits.size()) ? char_to_trit(other.trits[i]) : 0;
            int r = min(a,b);
            res_trits[i] = trit_to_char(r);
            if (r != a) res_val += (r - a) * pow3(i);
        }
        return build_from_raw(res_val, std::move(res_trits));
    }

    trint operator|(const trint& other) const{
        int n = max((int)trits.size(), (int)other.trits.size());
        deque<char> res_trits;
        res_trits.resize(n, '0');
        int res_val = val;
        for(int i=0;i<n;i++){
            int a = (i < (int)trits.size()) ? char_to_trit(trits[i]) : 0;
            int b = (i < (int)other.trits.size()) ? char_to_trit(other.trits[i]) : 0;
            int r = max(a,b);
            res_trits[i] = trit_to_char(r);
            if (r != a) res_val += (r - a) * pow3(i);
        }
        return build_from_raw(res_val, std::move(res_trits));
    }

    trint operator>>(int other) const{
        if (other <= 0) return *this;
        if (val == 0) return trint(0);
        if (other >= (int)trits.size()) return trint(0);
        deque<char> res_trits;
        res_trits.insert(res_trits.end(), trits.begin() + other, trits.end());

        int res_val = 0;
        for(int i=0;i<(int)res_trits.size();i++){
            int d = char_to_trit(res_trits[i]);
            res_val += d * pow3(i);
        }
        return build_from_raw(res_val, std::move(res_trits));
    }

    trint operator<<(int other) const{
        if (other <= 0) return *this;
        if (val == 0) return trint(0);
        deque<char> res_trits = trits;
        for(int i=0;i<other;i++) res_trits.push_front('0');
        int res_val = val * pow3(other);
        return build_from_raw(res_val, std::move(res_trits));
    }

    trint operator+(const trint& other) const {
        return trint(val + other.val);
    }

    trint operator-(const trint& other) const{
        return trint(val - other.val);
    }

    trint operator*(const trint& other) const{
        return trint(val * other.val);
    }

    trint operator/(const trint& other) const{
        return trint(val / other.val);
    }

    trint operator++(int){
        trint tmp = *this;
        val += 1;
        rebuild_trits_from_val();
        return tmp;
    }

    trint operator--(int){
        trint tmp = *this;
        val -= 1;
        rebuild_trits_from_val();
        return tmp;
    }

    operator string() const{
        string res;
        res.reserve(trits.size());
        for(int i=(int)trits.size()-1;i>=0;i--){
            res.push_back(trits[i]);
        }
        if (res.empty()) return "0";
        return res;
    }

    operator int() const{
        return val;
    }

    int operator= (int x){
        this->val = x;
        rebuild_trits_from_val();
        return x;
    }


};

istream &operator>>(istream &is, trint &i){int t; is >> t; i = t; return is;}
ostream &operator<<(ostream &os, const trint &i){ os << (string)i; return os;}

// ===========================================================================

// 座標を負の方向に伸ばせるvector、デキューのインデックスがズレていかないもの、と解釈できる
template <typename T>
struct devector{
    deque<T> devec;
    int offset;

    devector(){}
    devector(int start,int goal, T init_val) : devec(goal-start+1,init_val), offset(start){}

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

    void assing(int s,int g,T value){
        devec.assign(g-s+1, value);
        offset = s;
    }

};

// ==========================================================================

// @brief TernaryIndexedTree
struct TIT {
    devector<ll> table;
    int _start;
    int _goal;
    int count;

    TIT(devector<int> array) : _start(array.start()), _goal(array.goal()){
        int N = 1;
        chmax(N, -array.start());
        chmax(N, array.goal());
        int tmp = 1;
        count = 1;
        while (tmp < N){
            tmp = 3*tmp+1;
            count += 1;
        }
        N = tmp;

        while (array.goal() < N){
            array.push_back(0);
        }

        while (-N < array.start()){
            array.push_front(0);
        }

        table.assing(-N,N,0);

        for (int i=0;i<=count;i++){
            if (i == 0){
                for(int j=-N;j<=N;j++){
                    table[j] = array[j];
                }
            } else {
                auto tmp = (trint(1)<<(i-1));
                for (int j=((trint(-N)>>i)<<i);j<=((trint(N)<<i)>>i);j+=(trint(1)<<i)){
                    table[j] = table[j-tmp] + table[j] + table[j+tmp];
                }
            }
        }
    }

    int prod(trint l, trint r){
        int ans1 = 0;
        int ans2 = 0;

        trint t = 1;

        for (int i = 0; (r!=l && r != trint(0) && l !=  trint(0)) || i<count;i++){
            if (l[i] == 0){
                l=l-t;
                ans1 = ans1 + (-table[l]);
            } else if (l[i] == 1){
                ans1 = ans1 + table[l];
                l=l+t;
            }
            l[i] = 0;

            if (r[i] == 0){
                r=r+t;
                ans2 = (-table[r]) + ans2;
            } else if (r[i] == -1){
                ans2 = table[r] + ans2;
                r=r-t;
            }
            r[i] = 0;
            t = t * trint(3);
        }

        return ans1 + table[l] + ans2;
    }

    int get(trint ind){
        return prod(ind,ind);
    }

    void write(trint ind, int x){
        int pre = get(ind);
        for (int i=0;i<=count;i++){
            table[(ind>>i)<<i] += x - pre;
        }
    }

    int start(){
        return _start;
    }
    
    int goal(){
        return _goal;
    }


    
};

// ===============================================================================


int main(){
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    devector<int> arr(-4,4,0);
    arr[-4] = 1;
    arr[-3] = 2;
    arr[-2] = 3;
    arr[-1] = 4;
    arr[0] = 5;
    arr[1] = 6;
    arr[2] = 7;
    arr[3] = 8;
    arr[4] = 9;

    TIT TT(arr);
    // arr = {1,2,3,4,5,6,7,8,9}

    cout << TT.prod(-3,3) << endl;
    cout << TT.prod(0,0) << endl;
    cout << TT.prod(0,4) << endl;
    cout << TT.prod(-4,4) << endl;

    
    cout << TT.prod(4,4) << endl;
    TT.write(4,0);
    // arr = {1,2,3,4,5,6,7,8,0}
    cout << TT.prod(4,4) << endl;

}



/*
int main(){
    ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    for (trint t=-29;t<30;t++){
        cout << (int)t << " = " << t << "\t # " << (t >> 1) << "\t # " << (t << 1) << "\n";
    }

    cout << endl;

    devector<int> devec(-3,4,0);
    devec[-3] = 2;
    devec[-2] = 3;
    devec[-1] = 5;
    devec[0] = 7;
    devec[1] = 11;
    devec[2] = 13;
    devec[3] = 17;
    devec[4] = 19;

    for (trint i=devec.start(); i<=devec.goal();i++){
        cout << devec[i] << " \n"[i == devec.goal()];
    }

    devec.push_back(-1);
    devec.push_front(-1);

    devec[0] = 100;

    for (trint i=devec.start(); i<=devec.goal();i++){
        cout << devec[i] << " \n"[i == devec.goal()];
    }

    
} 

*/