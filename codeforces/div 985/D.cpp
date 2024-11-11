#include <bits/stdc++.h>

using namespace std;

const int N = 3e5 + 10;

int in[N];

struct node {
  int a;
  bool operator < (const node &b) const {
    return in[a] < in[b.a];
  }
};

void solve() {
  int n, m;
  cin >> n >> m;
  vector<set<int>> E(n);

  auto add = [&](int a, int b) {
    E[a].insert(b);
    E[b].insert(a);
  };

  for (int i = 0; i < m; i ++ ) {
    int a, b;
    cin >> a >> b;
    a -- , b -- ;
    add(a, b);
  }
  vector<tuple<int, int, int>> ops;
  for (int i = 0; i < n; i ++ ) {
    while (E[i].size() > 1) {
      int a = *E[i].begin(); E[i].erase(E[i].begin());
      int b = *E[i].begin(); E[i].erase(E[i].begin());
      E[a].erase(i); E[b].erase(i);
      ops.emplace_back(i, a, b);
      if (E[a].count(b)) {
        E[a].erase(b);
        E[b].erase(a);
      }else add(a, b);
    }
  }
  vector<int> q0;
  vector<pair<int, int>> p;
  for (int i = 0; i < n; i ++ ) 
    if (E[i].empty()) q0.push_back(i);
    else if (*E[i].begin() > i) p.emplace_back(i, *E[i].begin());
  if (!p.empty()) {
    auto [x, y] = p.back();
    p.pop_back();
    for (auto u : q0) {
      ops.emplace_back(x, y, u);
      y = u;
    }
    for (auto [u, v] : p) {
      ops.emplace_back(y, u, v);
    }
  } 
  cout << ops.size() << endl;
  for (auto [x, y, z] : ops) cout << x+1 << " " << y+1 << " " << z+1 << " " << endl;
}

int main() {
  int T = 1;
  cin >> T;
  while (T -- ) {
    solve();
  }
  return 0;
}