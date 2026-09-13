#include <algorithm>
#include <array>
#include <cassert>
#include <limits>
#include <numeric>
#include <vector>
#include <iostream>

using namespace std;

struct OnlineTwoEdgeConnectivity {
private:
    static_assert(sizeof(int) == 4, "This implementation assumes 32-bit int.");
    static constexpr int INF_TIME = numeric_limits<int>::max();
    // Columns = 2: {time, size}; Columns = 3: {time, size, 2ECC count}.
    // Histories are created only for roots whose state has changed.
    template <size_t Columns>
    struct ComponentForest {
        using Event = array<int, Columns>;
        // Historical roots have parent == -1. A parent link, once set, is
        // immutable. current_parent stores -size at roots and compressible
        // parent links elsewhere; negative sizes are not historical links.
        vector<int> parent, parent_time, next, history_id;
        mutable vector<int> current_parent;
        // 最新の1件は直接保持する。最初の更新では previous の確保が不要。
        // previous は latest より前の更新を、時刻の昇順で格納する。
        struct History {
            Event latest;
            vector<Event> previous;
        };
        vector<History> histories;
        explicit ComponentForest(int n)
            : parent(n, -1), parent_time(n, INF_TIME), next(n),
              history_id(n, -1), current_parent(n, -1) {
            iota(next.begin(), next.end(), 0);
        }
        // Path halving changes only the current-state cache.
        int root(int v) const {
            while (current_parent[v] >= 0) {
                const int p = current_parent[v];
                if (current_parent[p] < 0) return p;  // No redundant store.
                v = current_parent[v] = current_parent[p];
            }
            return v;
        }

        int root_at(int v, int t) const {
            while (parent_time[v] <= t) v = parent[v];
            return v;
        }
        int root_size(int r) const {
            assert(current_parent[r] < 0);
            return -current_parent[r];
        }

        // Also valid for former roots; their last event is retained.
        int final_size(int r) const {
            if (parent[r] < 0) return -current_parent[r];
            const int id = history_id[r];
            return id == -1 ? 1 : histories[id].latest[1];
        }
        int block_count(int r) const {
            static_assert(Columns == 3);
            const int id = history_id[r];
            return id == -1 ? 1 : histories[id].latest[2];
        }
        // Attach a known smaller root; member-list splicing is separate,
        // because CC joins use endpoint handles rather than DSU roots.
        void attach(int big, int small, int t) {
            assert(big != small);
            assert(parent[big] < 0 && parent[small] < 0);
            assert(root_size(big) >= root_size(small));
            current_parent[big] += current_parent[small];
            parent[small] = big;
            parent_time[small] = t;
            current_parent[small] = big;
        }
        void splice(int a, int b) { swap(next[a], next[b]); }
        void record(int r, int t, int blocks = 0) {
            Event event{};
            event[0] = t;
            event[1] = root_size(r);
            if constexpr (Columns == 3) event[2] = blocks;
            const int id = history_id[r];
            if (id == -1) {
                history_id[r] = static_cast<int>(histories.size());
                histories.push_back({event, {}});
            } else {
                auto& history = histories[id];
                assert(history.latest[0] < t);
                history.previous.push_back(history.latest);
                history.latest = event;
            }
        }
        Event state_at(int v, int t) const {
            const int id = history_id[root_at(v, t)];
            if (id != -1) {
                const auto& history = histories[id];
                if (history.latest[0] <= t) return history.latest;
                const auto& previous = history.previous;
                int lo = 0, hi = static_cast<int>(previous.size());
                while (lo < hi) {
                    const int mid = lo + (hi - lo) / 2;
                    if (previous[mid][0] <= t) lo = mid + 1;
                    else hi = mid;
                }
                if (lo != 0) return previous[lo - 1];
            }
            Event initial;
            initial.fill(1);
            initial[0] = 0;
            return initial;
        }
        // Merge the two chronological ancestor chains directly. Distinct
        // final roots are detected by INF_TIME, without preliminary finds.
        int first_same_time(int a, int b) const {
            int answer = 0;
            while (a != b) {
                if (parent_time[a] > parent_time[b]) swap(a, b);
                const int t = parent_time[a];
                if (t == INF_TIME) return -1;
                answer = t;  // Traversed parent-edge times are nondecreasing.
                a = parent[a];
            }
            return answer;
        }
        int first_size_time(int v, int need) const {
            if (need <= 1) return 0;
            if (need > static_cast<int>(parent.size())) return -1;
            int entered_at = 0;
            while (final_size(v) < need) {
                if (parent_time[v] == INF_TIME) return -1;
                entered_at = parent_time[v];
                v = parent[v];
            }
            const int id = history_id[v];
            assert(id != -1);
            const auto& history = histories[id].previous;
            int lo = 0, hi = static_cast<int>(history.size());
            while (lo < hi) {
                const int mid = lo + (hi - lo) / 2;
                if (history[mid][1] < need) lo = mid + 1;
                else hi = mid;
            }
            const int reached_at = lo < static_cast<int>(history.size())
                ? history[lo][0] : histories[id].latest[0];
            return max(entered_at, reached_at);
        }
        // No root search: any vertex is a valid entry into its member cycle.
        vector<int> members(int v, int known_size = 0) const {
            vector<int> result;
            if (known_size > 0) result.reserve(known_size);
            const int start = v;
            do {
                result.push_back(v);
                v = next[v];
            } while (v != start);
            return result;
        }
        vector<vector<int>> groups(int count) const {
            vector<vector<int>> result;
            result.reserve(count);
            for (int r = 0; r < static_cast<int>(parent.size()); ++r) {
                if (parent[r] < 0)
                    result.push_back(members(r, -current_parent[r]));
            }
            return result;
        }
    };
    int n_;
    int time_ = 0;
    int cc_count_, ecc_count_;
    ComponentForest<3> cc_;
    ComponentForest<2> ecc_;
    vector<int> bridge_parent_, visit_time_;
    array<vector<int>, 2> paths_;
    // Dense storage preserves O(1) historical global-count queries.
    vector<array<int, 2>> count_history_;
    static int checked_n(int n) { assert(n >= 0); return n; }
    void check_vertex(int v) const { assert(0 <= v && v < n_); (void)v; }
    void check_time(int t) const { assert(0 <= t && t <= time_); (void)t; }
    // Only bridge-parent handles and current DSU caches are shortened.
    int bridge_parent(int r) {
        const int p = bridge_parent_[r];
        if (p == -1) return -1;
        const int resolved = ecc_.root(p);
        assert(resolved != r);
        return bridge_parent_[r] = resolved;
    }
    // r is already a current 2ECC root in the smaller ordinary component.
    void reroot(int r) {
        int child = -1;
        while (r != -1) {
            const int parent = bridge_parent(r);
            bridge_parent_[r] = child;
            child = r;
            r = parent;
        }
    }
    int collect_path(int a, int b, int pa, int pb) {
        paths_[0].clear();
        paths_[1].clear();
        paths_[0].push_back(a);
        paths_[1].push_back(b);
        visit_time_[a] = visit_time_[b] = time_;
        a = pa;
        b = pb;
        int lca = -1;
        while (lca == -1) {
            if (a != -1) {
                paths_[0].push_back(a);
                if (visit_time_[a] == time_) { lca = a; break; }
                visit_time_[a] = time_;
                a = bridge_parent(a);
            }
            if (b != -1) {
                paths_[1].push_back(b);
                if (visit_time_[b] == time_) { lca = b; break; }
                visit_time_[b] = time_;
                b = bridge_parent(b);
            }
        }
        // Discard overshoot once. Keep the LCA only in the first path;
        // traversal order and equal-size tie breaking match the original.
        for (auto& path : paths_) {
            while (path.back() != lca) path.pop_back();
        }
        paths_[1].pop_back();
        return lca;
    }
    // 縮約後の共通処理。各成分の履歴への追記は同じ時刻に1回だけ。
    void finish_merge(int big, int parent_above, int cc_root, int removed) {
        ecc_.record(big, time_);
        bridge_parent_[big] = parent_above;
        ecc_count_ -= removed;
        cc_.record(cc_root, time_, cc_.block_count(cc_root) - removed);
    }
    // 橋1本で隣接する2成分。LCA探索・作業配列・最大成分探索を省く。
    // 同サイズなら a を残し、元実装と列挙順を合わせる。
    void merge_adjacent(int a, int b, int parent_above, int cc_root) {
        if (ecc_.root_size(a) < ecc_.root_size(b)) swap(a, b);
        ecc_.attach(a, b, time_);
        ecc_.splice(a, b);
        finish_merge(a, parent_above, cc_root, 1);
    }
    void merge_path(int a, int b, int cc_root) {
        // 先に最初の親を解決し、隣接しなければ探索にも再利用する。
        const int pa = bridge_parent(a);
        if (pa == b) {
            merge_adjacent(a, b, bridge_parent(b), cc_root);
            return;
        }
        const int pb = bridge_parent(b);
        if (pb == a) {
            merge_adjacent(a, b, pa, cc_root);
            return;
        }
        const int lca = collect_path(a, b, pa, pb);
        const int parent_above = bridge_parent(lca);
        int big = paths_[0].front();
        int biggest_size = ecc_.root_size(big);
        for (const auto& path : paths_) {
            for (int r : path) {
                const int size = ecc_.root_size(r);
                if (size > biggest_size) { biggest_size = size; big = r; }
            }
        }
        for (const auto& path : paths_) {
            for (int r : path) {
                if (r == big) continue;
                ecc_.attach(big, r, time_);
                ecc_.splice(big, r);
            }
        }
        const int removed = static_cast<int>(paths_[0].size() + paths_[1].size()) - 1;
        finish_merge(big, parent_above, cc_root, removed);
    }
public:
    explicit OnlineTwoEdgeConnectivity(int n, int expected_additions = 0)
        : n_(checked_n(n)), cc_count_(n_), ecc_count_(n_), cc_(n_), ecc_(n_),
          bridge_parent_(n_, -1), visit_time_(n_, 0) {
        reserve_additions(expected_additions);
        count_history_.push_back({n_, n_});
    }

    int time() const noexcept { return time_; }
    void reserve_additions(int expected_total_additions) {
        assert(time_ <= expected_total_additions && expected_total_additions < INF_TIME);
        count_history_.reserve(static_cast<size_t>(expected_total_additions) + 1);
        const int capacity = min(n_, expected_total_additions + 1);
        for (auto& path : paths_) path.reserve(capacity);
    }
    // Amortized O(log(N+1)); a single insertion may traverse a long path.
    void add_edge(int u, int v) {
        check_vertex(u);
        check_vertex(v);
        assert(time_ < INF_TIME - 1);
        ++time_;
        if (u != v) {
            int a = ecc_.root(u), b = ecc_.root(v);
            if (a != b) {
                int ca = cc_.root(u), cb = cc_.root(v);
                if (ca != cb) {
                    if (cc_.root_size(ca) < cc_.root_size(cb)) {
                        swap(ca, cb);
                        swap(a, b);
                    }
                    const int blocks = cc_.block_count(ca) + cc_.block_count(cb);
                    reroot(b);
                    bridge_parent_[b] = a;
                    cc_.attach(ca, cb, time_);
                    cc_.splice(a, b);
                    cc_.record(ca, time_, blocks);
                    --cc_count_;
                } else {
                    merge_path(a, b, ca);
                }
            }
        }
        count_history_.push_back({cc_count_, ecc_count_});
    }
    // Current state: root searches use a separate path-compressed DSU.
    int query(int a, int b) const {
        check_vertex(a); check_vertex(b);
        if (ecc_.root(a) == ecc_.root(b)) return 2;
        return cc_.root(a) == cc_.root(b) ? 1 : 0;
    }
    int connected_component_size(int v) const {
        check_vertex(v); return cc_.root_size(cc_.root(v));
    }
    int two_edge_connected_component_size(int v) const {
        check_vertex(v); return ecc_.root_size(ecc_.root(v));
    }
    int connected_component_count() const noexcept { return cc_count_; }
    int two_edge_connected_component_count() const noexcept { return ecc_count_; }
    int two_edge_connected_component_count_in_connected_component(int v) const {
        check_vertex(v); return cc_.block_count(cc_.root(v));
    }
    // Historical state: use the immutable union forest, never current_parent.
    int query(int a, int b, int t) const {
        check_vertex(a); check_vertex(b); check_time(t);
        if (cc_.root_at(a, t) != cc_.root_at(b, t)) return 0;
        return ecc_.root_at(a, t) == ecc_.root_at(b, t) ? 2 : 1;
    }
    int connected_component_size(int v, int t) const {
        check_vertex(v); check_time(t); return cc_.state_at(v, t)[1];
    }
    int two_edge_connected_component_size(int v, int t) const {
        check_vertex(v); check_time(t); return ecc_.state_at(v, t)[1];
    }
    int connected_component_count(int t) const {
        check_time(t); return count_history_[t][0];
    }
    int two_edge_connected_component_count(int t) const {
        check_time(t); return count_history_[t][1];
    }
    int two_edge_connected_component_count_in_connected_component(int v, int t) const {
        check_vertex(v); check_time(t); return cc_.state_at(v, t)[2];
    }
    // Earliest-time queries: O(log(N+1)), not binary search over all times.
    int first_connected_time(int a, int b) const {
        check_vertex(a); check_vertex(b); return cc_.first_same_time(a, b);
    }
    int first_two_edge_connected_time(int a, int b) const {
        check_vertex(a); check_vertex(b); return ecc_.first_same_time(a, b);
    }
    int first_connected_component_size_at_least_time(int v, int need) const {
        check_vertex(v); return cc_.first_size_time(v, need);
    }
    int first_two_edge_connected_component_size_at_least_time(int v, int need) const {
        check_vertex(v); return ecc_.first_size_time(v, need);
    }
    // Current members: O(K); all current components: O(N).
    vector<int> connected_component_vertices(int v) const {
        check_vertex(v); return cc_.members(v);
    }
    vector<int> two_edge_connected_component_vertices(int v) const {
        check_vertex(v); return ecc_.members(v);
    }
    vector<vector<int>> connected_components() const {
        return cc_.groups(cc_count_);
    }
    vector<vector<int>> two_edge_connected_components() const {
        return ecc_.groups(ecc_count_);
    }
};




int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, Q;
    cin >> N >> Q;

    OnlineTwoEdgeConnectivity graph(N);

    for (int i = 0; i < Q; ++i) {
        int A, B;
        cin >> A >> B;
        graph.add_edge(A, B);
    }
    
    auto tmp = graph.two_edge_connected_components();
    cout << tmp.size() << "\n";
    for (auto& arr:tmp){
        cout << arr.size() << " ";
        for (auto a:arr){
            cout << a << " ";
        }
        cout << "\n";
    }

    return 0;
}
