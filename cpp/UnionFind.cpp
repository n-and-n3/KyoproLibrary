#include <vector>
#include <iostream>

using namespace std;

// https://atcoder.jp/contests/atc001/submissions/70817243
// https://atcoder.jp/contests/abc364/submissions/71087452

struct UnionFind{
    vector<int> parent;
    int c;

    UnionFind(int n) : parent(n,-1),c(n){ }

    int root(int x){
        int tmp = x;
        while (parent[tmp] >= 0){
            tmp = parent[tmp];
        }

        while (parent[x] >= 0){
            parent[x] = tmp;
            x = parent[x];
        }

        return tmp;
    }

    int same(int x,int y){
        return root(x) == root(y);
    }

    int size(int x){
        return -parent[root(x)];
    }

    bool marge(int x,int y){
        int xr = root(x),yr = root(y);
        if (xr == yr){
            return false;
        }
        if (parent[xr] <= parent[yr]){
            parent[xr] += parent[yr];
            parent[yr] = xr;
        } else {
            parent[yr] += parent[xr];
            parent[xr] = yr;
        }
        c -= 1;
        return true;
    }

    int group_count(){
        return c;
    }

    vector<int> label(){
        vector<int> res(parent.size());
        for (int i=0;i<parent.size();i++){
            res[i] = root(i);
        }
        return res;
    }

    vector<int> comped_label(){
        vector<int> A = label();
        vector<int> B = A;
        sort(B.begin(), B.end());
        B.erase(unique(B.begin(), B.end()), B.end());

        vector<int> res(parent.size());
        for (int i = 0; i < parent.size(); i++) {
            res[i] = lower_bound(B.begin(), B.end(), A[i]) - B.begin();
        }
        return res;
    }

    vector<vector<int>> groups(){
        vector<int> A = label();
        vector<int> B = A;
        sort(B.begin(), B.end());
        B.erase(unique(B.begin(), B.end()), B.end());

        vector<vector<int>> res(c);
        for (int i = 0; i < parent.size(); i++) {
            res[lower_bound(B.begin(), B.end(), A[i]) - B.begin()].push_back(i);
        }
        return res;
    }

    vector<int> group_sizes(){
        vector<int> A = label();
        vector<int> B = A;
        sort(B.begin(), B.end());
        B.erase(unique(B.begin(), B.end()), B.end());

        vector<int> res(c,0);
        for (int i = 0; i < parent.size(); i++) {
            res[lower_bound(B.begin(), B.end(), A[i]) - B.begin()] += 1;
        }
        return res;
    }

    void print(){
      cout << "{";
        for (int i = 0; i < parent.size(); i++){
            cout << parent[i] << ", ";
        }
      cout << "}" << "\n";
    }
};

void print(vector<int> A){
    cout << "{";
    for (int i = 0; i < A.size(); i++){
        cout << A[i] << ", ";
    }
    cout << "}" << "\n";
}
void print(vector<vector<int>> A){
    cout << "{";
    for (int i = 0; i < A.size(); i++){
        print(A[i]);
        cout << "," << "\n";
    }
    cout << "}" << "\n";
}

int main(){
    UnionFind UF(10);


}