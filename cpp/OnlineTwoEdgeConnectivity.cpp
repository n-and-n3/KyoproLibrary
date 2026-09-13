#pragma once

#include <algorithm>
#include <array>
#include <cassert>
#include <limits>
#include <numeric>
#include <vector>
#include <iostream>

using namespace std;

// Incremental undirected graph with current and partially-persistent
// connectivity / 2-edge-connectivity information.
//
// Time t means the state after exactly t calls to add_edge().
// Time 0 is the edgeless initial graph.
//
// The whole implementation is contained in this one structure.  No field is
// bit-packed: every scalar stored in the arrays is a 32-bit int.  Current
// components are represented by the same union forests used for persistence,
// and their members are linked by circular permutations.  A circular
// permutation can be traversed from any member, so enumerating a current
// component of size K costs O(K); finding a union-find root is unnecessary.

struct OnlineTwoEdgeConnectivity {
private:
    static_assert(sizeof(int) == 4, "This implementation assumes 32-bit int.");
    static constexpr int INF_TIME = numeric_limits<int>::max();
    static constexpr int NO_HISTORY = -1;

    int n_ = 0;
    int current_time_ = 0;
    int cc_count_ = 0;
    int ecc_count_ = 0;

    // ------------------------------------------------------------------
    // Dynamic bridge forest.
    // ------------------------------------------------------------------
    // bridge_parent_[r] is meaningful when r is a current 2ECC root.  A
    // stored parent may later cease to be a root; ecc_root_now() resolves it.
    vector<int> bridge_parent_;

    // merge_bridge_path() is called at most once per add_edge() call, so the
    // current time itself is a sufficient visitation stamp.
    vector<int> lca_visit_time_;

    // Reused scratch buffers for the two upward paths used in LCA search.
    vector<int> path_a_;
    vector<int> path_b_;

    // ------------------------------------------------------------------
    // Partially-persistent ordinary connected-component union forest.
    // ------------------------------------------------------------------
    // No path compression is used, because parent links are historical.
    // Union by size keeps the height O(log N).
    vector<int> cc_parent_;
    vector<int> cc_parent_time_;

    // Members of every current connected component form one circular singly
    // linked list.  Joining two components only swaps two successor values;
    // no per-vertex current component ID is stored or rewritten.
    vector<int> cc_next_;

    // A root's history is stored sparsely.  -1 means that its state is still
    // the implicit initial state (time=0, size=1, 2ECC-count=1).
    vector<int> cc_history_id_;

    // Each event is {time, component size, number of 2ECCs in the CC}.
    // Every field is an independent 32-bit int.
    vector<vector<array<int, 3>>> cc_histories_;

    // ------------------------------------------------------------------
    // Partially-persistent 2-edge-connected-component union forest.
    // ------------------------------------------------------------------
    vector<int> ecc_parent_;
    vector<int> ecc_parent_time_;
    vector<int> ecc_next_;
    vector<int> ecc_history_id_;

    // Each event is {time, component size}.
    vector<vector<array<int, 2>>> ecc_histories_;

    // Total numbers of components at every time.  Index is time.
    vector<int> cc_count_history_;
    vector<int> ecc_count_history_;

    // ------------------------------------------------------------------
    // Validation.
    // ------------------------------------------------------------------
    void check_vertex(int v) const {
        assert(0 <= v && v < n_);
    }

    void check_time(int t) const {
        assert(0 <= t && t <= current_time_);
    }

    // ------------------------------------------------------------------
    // Union-forest root searches.
    // ------------------------------------------------------------------
    static int root_now(const vector<int>& parent, int v) {
        while (parent[v] != v) v = parent[v];
        return v;
    }

    static int historical_root(
        const vector<int>& parent,
        const vector<int>& parent_time,
        int v,
        int t
    ) {
        while (parent_time[v] <= t) v = parent[v];
        return v;
    }

    int cc_root_now(int v) const {
        return root_now(cc_parent_, v);
    }

    int ecc_root_now(int v) const {
        return root_now(ecc_parent_, v);
    }

    // ------------------------------------------------------------------
    // Sparse history access.
    // ------------------------------------------------------------------
    void append_cc_event(int root, int time, int size, int block_count) {
        int id = cc_history_id_[root];
        if (id == NO_HISTORY) {
            id = static_cast<int>(cc_histories_.size());
            cc_history_id_[root] = id;
            cc_histories_.emplace_back();
        }

        auto& history = cc_histories_[id];
        assert(history.empty() || history.back()[0] < time);
        history.push_back({time, size, block_count});
    }

    void append_ecc_event(int root, int time, int size) {
        int id = ecc_history_id_[root];
        if (id == NO_HISTORY) {
            id = static_cast<int>(ecc_histories_.size());
            ecc_history_id_[root] = id;
            ecc_histories_.emplace_back();
        }

        auto& history = ecc_histories_[id];
        assert(history.empty() || history.back()[0] < time);
        history.push_back({time, size});
    }

    // These functions are valid for every vertex that was once a root, not
    // only for a current root: the final event is the largest state attained
    // while that vertex was a root.
    int final_cc_size_while_root(int root) const {
        const int id = cc_history_id_[root];
        return id == NO_HISTORY ? 1 : cc_histories_[id].back()[1];
    }

    int final_cc_block_count_while_root(int root) const {
        const int id = cc_history_id_[root];
        return id == NO_HISTORY ? 1 : cc_histories_[id].back()[2];
    }

    int final_ecc_size_while_root(int root) const {
        const int id = ecc_history_id_[root];
        return id == NO_HISTORY ? 1 : ecc_histories_[id].back()[1];
    }

    int cc_event_index_at(int root, int t) const {
        const int id = cc_history_id_[root];
        if (id == NO_HISTORY) return -1;

        const auto& history = cc_histories_[id];
        int low = 0;
        int high = static_cast<int>(history.size());
        while (low < high) {
            const int mid = (low + high) >> 1;
            if (history[mid][0] <= t) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        return low - 1;
    }

    int ecc_event_index_at(int root, int t) const {
        const int id = ecc_history_id_[root];
        if (id == NO_HISTORY) return -1;

        const auto& history = ecc_histories_[id];
        int low = 0;
        int high = static_cast<int>(history.size());
        while (low < high) {
            const int mid = (low + high) >> 1;
            if (history[mid][0] <= t) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        return low - 1;
    }

    // ------------------------------------------------------------------
    // Historical / earliest-time queries shared by CC and 2ECC forests.
    // ------------------------------------------------------------------
    int first_same_time_impl(
        int x,
        int y,
        const vector<int>& parent,
        const vector<int>& parent_time
    ) const {
        if (x == y) return 0;
        if (root_now(parent, x) != root_now(parent, y)) return -1;

        int answer = 0;
        while (x != y) {
            int tx = parent_time[x];
            int ty = parent_time[y];

            // Parent-edge times increase toward the root.  Climbing the
            // earlier edge merges the two chronological ancestor chains.
            if (tx > ty) {
                swap(x, y);
                swap(tx, ty);
            }

            assert(tx != INF_TIME);
            answer = max(answer, tx);
            x = parent[x];
        }
        return answer;
    }

    int first_cc_size_at_least_time_impl(int v, int need) const {
        if (need <= 1) return 0;
        if (need > n_) return -1;

        int entered_at = 0;
        int u = v;

        while (final_cc_size_while_root(u) < need) {
            if (cc_parent_time_[u] == INF_TIME) return -1;
            entered_at = max(entered_at, cc_parent_time_[u]);
            u = cc_parent_[u];
        }

        const int id = cc_history_id_[u];
        assert(id != NO_HISTORY);
        const auto& history = cc_histories_[id];

        int low = 0;
        int high = static_cast<int>(history.size());
        while (low < high) {
            const int mid = (low + high) >> 1;
            if (history[mid][1] < need) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        assert(low < static_cast<int>(history.size()));
        return max(entered_at, history[low][0]);
    }

    int first_ecc_size_at_least_time_impl(int v, int need) const {
        if (need <= 1) return 0;
        if (need > n_) return -1;

        int entered_at = 0;
        int u = v;

        while (final_ecc_size_while_root(u) < need) {
            if (ecc_parent_time_[u] == INF_TIME) return -1;
            entered_at = max(entered_at, ecc_parent_time_[u]);
            u = ecc_parent_[u];
        }

        const int id = ecc_history_id_[u];
        assert(id != NO_HISTORY);
        const auto& history = ecc_histories_[id];

        int low = 0;
        int high = static_cast<int>(history.size());
        while (low < high) {
            const int mid = (low + high) >> 1;
            if (history[mid][1] < need) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        assert(low < static_cast<int>(history.size()));
        return max(entered_at, history[low][0]);
    }

    // ------------------------------------------------------------------
    // Current circular-permutation unions.
    // ------------------------------------------------------------------
    // If a and b lie in distinct cycles, swapping their outgoing arcs joins
    // the two cycles into one.  Neither a nor b has to be a union-find root.
    static void splice_cycles(vector<int>& next, int a, int b) {
        swap(next[a], next[b]);
    }

    // big and small are current CC roots, with size(big) >= size(small).
    // big_member and small_member are arbitrary vertices of the respective
    // components, used only as O(1) splice handles for cc_next_.
    void unite_cc_roots(
        int big,
        int small,
        int big_member,
        int small_member
    ) {
        assert(big != small);
        assert(cc_parent_[big] == big);
        assert(cc_parent_[small] == small);

        const int big_size = final_cc_size_while_root(big);
        const int small_size = final_cc_size_while_root(small);
        assert(big_size >= small_size);

        const int new_block_count =
            final_cc_block_count_while_root(big)
          + final_cc_block_count_while_root(small);

        cc_parent_[small] = big;
        cc_parent_time_[small] = current_time_;

        // Splice the two circular permutations in O(1).  The splice
        // handles need not coincide with the union-find roots.
        splice_cycles(cc_next_, big_member, small_member);

        append_cc_event(
            big,
            current_time_,
            big_size + small_size,
            new_block_count
        );
        --cc_count_;
    }

    // ------------------------------------------------------------------
    // Dynamic bridge forest operations.
    // ------------------------------------------------------------------
    // Re-root one bridge tree at v.  The caller chooses v in the smaller
    // ordinary connected component.
    void make_bridge_tree_root(int v) {
        v = ecc_root_now(v);
        int child = -1;

        while (v != -1) {
            int parent = bridge_parent_[v];
            if (parent != -1) parent = ecc_root_now(parent);
            bridge_parent_[v] = child;
            child = v;
            v = parent;
        }
    }

    // Finds the LCA in the current bridge forest.  path_a_ and path_b_ may
    // contain vertices above the LCA on one side; consumers stop at the LCA.
    int collect_bridge_path(int a, int b) {
        path_a_.clear();
        path_b_.clear();

        const int stamp = current_time_;
        int lca = -1;

        while (lca == -1) {
            if (a != -1) {
                a = ecc_root_now(a);
                path_a_.push_back(a);
                if (lca_visit_time_[a] == stamp) {
                    lca = a;
                    break;
                }
                lca_visit_time_[a] = stamp;
                a = bridge_parent_[a];
            }

            if (b != -1) {
                b = ecc_root_now(b);
                path_b_.push_back(b);
                if (lca_visit_time_[b] == stamp) {
                    lca = b;
                    break;
                }
                lca_visit_time_[b] = stamp;
                b = bridge_parent_[b];
            }
        }

        return lca;
    }

    // The new edge closes the unique bridge path from a to b.  All current
    // 2ECC roots on that path merge at current_time_.
    void merge_bridge_path(int a, int b, int cc_root) {
        const int lca = collect_bridge_path(a, b);
        assert(lca != -1);

        int parent_above = bridge_parent_[lca];
        if (parent_above != -1) parent_above = ecc_root_now(parent_above);

        int big = -1;
        int biggest_size = -1;
        int merged_count = 0;

        auto inspect = [&](const vector<int>& path, bool include_lca) {
            for (int root : path) {
                if (root == lca && !include_lca) break;

                const int size = final_ecc_size_while_root(root);
                if (size > biggest_size) {
                    biggest_size = size;
                    big = root;
                }
                ++merged_count;

                if (root == lca) break;
            }
        };

        // Count the LCA exactly once.
        inspect(path_a_, true);
        inspect(path_b_, false);

        assert(big != -1);
        assert(merged_count >= 2);
        assert(ecc_parent_[big] == big);

        int merged_size = biggest_size;

        auto absorb = [&](const vector<int>& path, bool include_lca) {
            for (int small : path) {
                if (small == lca && !include_lca) break;

                if (small != big) {
                    assert(ecc_parent_[small] == small);
                    const int small_size = final_ecc_size_while_root(small);
                    assert(merged_size >= small_size);

                    ecc_parent_[small] = big;
                    ecc_parent_time_[small] = current_time_;

                    // Splice the member cycles; any one vertex from each
                    // cycle would work.  These roots are merely the handles
                    // already available from the bridge-path traversal.
                    splice_cycles(ecc_next_, big, small);
                    merged_size += small_size;
                }

                if (small == lca) break;
            }
        };

        absorb(path_a_, true);
        absorb(path_b_, false);
        append_ecc_event(big, current_time_, merged_size);

        // The chosen union root need not be the bridge-tree LCA.  Transfer the
        // LCA's one meaningful upward bridge edge to the chosen largest root.
        bridge_parent_[big] = parent_above;

        const int reduction = merged_count - 1;
        ecc_count_ -= reduction;

        append_cc_event(
            cc_root,
            current_time_,
            final_cc_size_while_root(cc_root),
            final_cc_block_count_while_root(cc_root) - reduction
        );
    }

    void record_counts() {
        cc_count_history_.push_back(cc_count_);
        ecc_count_history_.push_back(ecc_count_);
    }

    // Every cycle of next[] is exactly one current component.  The starting
    // vertex may be any member of the component; it need not be a union-find
    // root.  The returned vector itself has size K, so O(K) is optimal.
    static vector<int> list_members(
        int start,
        const vector<int>& next
    ) {
        vector<int> result;

        int v = start;
        do {
            result.push_back(v);
            v = next[v];
        } while (v != start);

        return result;
    }

public:
    explicit OnlineTwoEdgeConnectivity(int n, int expected_additions = 0)
        : n_(n), current_time_(0), cc_count_(n), ecc_count_(n),
          bridge_parent_(n, -1),
          lca_visit_time_(n, 0),
          cc_parent_(n),
          cc_parent_time_(n, INF_TIME),
          cc_next_(n),
          cc_history_id_(n, NO_HISTORY),
          ecc_parent_(n),
          ecc_parent_time_(n, INF_TIME),
          ecc_next_(n),
          ecc_history_id_(n, NO_HISTORY) {
        assert(n >= 0);
        assert(expected_additions >= 0);
        assert(expected_additions < INF_TIME);

        iota(cc_parent_.begin(), cc_parent_.end(), 0);
        iota(cc_next_.begin(), cc_next_.end(), 0);
        iota(ecc_parent_.begin(), ecc_parent_.end(), 0);
        iota(ecc_next_.begin(), ecc_next_.end(), 0);

        if (expected_additions > 0) {
            cc_count_history_.reserve(
                static_cast<size_t>(expected_additions) + 1
            );
            ecc_count_history_.reserve(
                static_cast<size_t>(expected_additions) + 1
            );
            path_a_.reserve(min(n_, expected_additions + 1));
            path_b_.reserve(min(n_, expected_additions + 1));
        }

        cc_count_history_.push_back(n_);
        ecc_count_history_.push_back(n_);
    }

    // Time t is the state after the first t add_edge() calls.
    int time() const noexcept {
        return current_time_;
    }

    void reserve_additions(int expected_total_additions) {
        assert(expected_total_additions >= current_time_);
        assert(expected_total_additions < INF_TIME);

        cc_count_history_.reserve(
            static_cast<size_t>(expected_total_additions) + 1
        );
        ecc_count_history_.reserve(
            static_cast<size_t>(expected_total_additions) + 1
        );
        path_a_.reserve(min(n_, expected_total_additions + 1));
        path_b_.reserve(min(n_, expected_total_additions + 1));
    }

    void add_edge(int u, int v) {
        check_vertex(u);
        check_vertex(v);
        assert(current_time_ < INF_TIME - 1);
        ++current_time_;

        const int a = ecc_root_now(u);
        const int b = ecc_root_now(v);

        if (a == b) {
            // Self-loop, or an edge already internal to one current 2ECC.
            record_counts();
            return;
        }

        const int ca = cc_root_now(u);
        const int cb = cc_root_now(v);

        if (ca != cb) {
            int big_cc = ca;
            int small_cc = cb;
            int big_endpoint = a;
            int small_endpoint = b;

            if (final_cc_size_while_root(big_cc)
                    < final_cc_size_while_root(small_cc)) {
                swap(big_cc, small_cc);
                swap(big_endpoint, small_endpoint);
            }

            // Re-root only the smaller bridge tree, then add the new bridge.
            make_bridge_tree_root(small_endpoint);
            bridge_parent_[small_endpoint] = big_endpoint;
            unite_cc_roots(
                big_cc,
                small_cc,
                big_endpoint,
                small_endpoint
            );
        } else {
            merge_bridge_path(a, b, ca);
        }

        record_counts();
    }

    // ------------------------------------------------------------------
    // Current-state queries.
    // Root searches cost O(log N); global component counts remain O(1).
    // ------------------------------------------------------------------
    int query(int a, int b) const {
        check_vertex(a);
        check_vertex(b);

        if (cc_root_now(a) != cc_root_now(b)) return 0;
        return ecc_root_now(a) == ecc_root_now(b) ? 2 : 1;
    }

    int connected_component_size(int v) const {
        check_vertex(v);
        return final_cc_size_while_root(cc_root_now(v));
    }

    int two_edge_connected_component_size(int v) const {
        check_vertex(v);
        return final_ecc_size_while_root(ecc_root_now(v));
    }

    int connected_component_count() const noexcept {
        return cc_count_;
    }

    int two_edge_connected_component_count() const noexcept {
        return ecc_count_;
    }

    int two_edge_connected_component_count_in_connected_component(int v) const {
        check_vertex(v);
        return final_cc_block_count_while_root(cc_root_now(v));
    }

    // ------------------------------------------------------------------
    // Historical queries.
    // ------------------------------------------------------------------
    int query(int a, int b, int t) const {
        check_vertex(a);
        check_vertex(b);
        check_time(t);

        const int ca = historical_root(
            cc_parent_, cc_parent_time_, a, t
        );
        const int cb = historical_root(
            cc_parent_, cc_parent_time_, b, t
        );
        if (ca != cb) return 0;

        const int ea = historical_root(
            ecc_parent_, ecc_parent_time_, a, t
        );
        const int eb = historical_root(
            ecc_parent_, ecc_parent_time_, b, t
        );
        return ea == eb ? 2 : 1;
    }

    int connected_component_size(int v, int t) const {
        check_vertex(v);
        check_time(t);

        const int root = historical_root(
            cc_parent_, cc_parent_time_, v, t
        );
        const int index = cc_event_index_at(root, t);
        if (index == -1) return 1;
        return cc_histories_[cc_history_id_[root]][index][1];
    }

    int two_edge_connected_component_size(int v, int t) const {
        check_vertex(v);
        check_time(t);

        const int root = historical_root(
            ecc_parent_, ecc_parent_time_, v, t
        );
        const int index = ecc_event_index_at(root, t);
        if (index == -1) return 1;
        return ecc_histories_[ecc_history_id_[root]][index][1];
    }

    int connected_component_count(int t) const {
        check_time(t);
        return cc_count_history_[t];
    }

    int two_edge_connected_component_count(int t) const {
        check_time(t);
        return ecc_count_history_[t];
    }

    int two_edge_connected_component_count_in_connected_component(
        int v,
        int t
    ) const {
        check_vertex(v);
        check_time(t);

        const int root = historical_root(
            cc_parent_, cc_parent_time_, v, t
        );
        const int index = cc_event_index_at(root, t);
        if (index == -1) return 1;
        return cc_histories_[cc_history_id_[root]][index][2];
    }

    // ------------------------------------------------------------------
    // Earliest-time queries.
    // ------------------------------------------------------------------
    int first_connected_time(int a, int b) const {
        check_vertex(a);
        check_vertex(b);
        return first_same_time_impl(
            a, b, cc_parent_, cc_parent_time_
        );
    }

    int first_two_edge_connected_time(int a, int b) const {
        check_vertex(a);
        check_vertex(b);
        return first_same_time_impl(
            a, b, ecc_parent_, ecc_parent_time_
        );
    }

    int first_connected_component_size_at_least_time(
        int v,
        int need
    ) const {
        check_vertex(v);
        return first_cc_size_at_least_time_impl(v, need);
    }

    int first_two_edge_connected_component_size_at_least_time(
        int v,
        int need
    ) const {
        check_vertex(v);
        return first_ecc_size_at_least_time_impl(v, need);
    }

    // ------------------------------------------------------------------
    // Current-state enumeration.
    // ------------------------------------------------------------------
    // O(K), where K is the returned component size.  Since cc_next_ is a
    // circular permutation of each current CC, traversal starts directly at
    // v; no union-find root search is performed.
    vector<int> connected_component_vertices(int v) const {
        check_vertex(v);
        return list_members(v, cc_next_);
    }

    // O(K), for the same reason.
    vector<int> two_edge_connected_component_vertices(int v) const {
        check_vertex(v);
        return list_members(v, ecc_next_);
    }

    // O(N): current roots are exactly the self-parent vertices, and every
    // vertex is walked once among all circular lists.
    vector<vector<int>> connected_components() const {
        vector<vector<int>> result;
        result.reserve(cc_count_);

        for (int root = 0; root < n_; ++root) {
            if (cc_parent_[root] != root) continue;
            result.push_back(list_members(root, cc_next_));
        }
        return result;
    }

    // O(N).
    vector<vector<int>> two_edge_connected_components() const {
        vector<vector<int>> result;
        result.reserve(ecc_count_);

        for (int root = 0; root < n_; ++root) {
            if (ecc_parent_[root] != root) continue;
            result.push_back(list_members(root, ecc_next_));
        }
        return result;
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