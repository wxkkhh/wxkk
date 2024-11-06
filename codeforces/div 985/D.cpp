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

  for (int i = 0; i < n; i ++ ) in[i] = 0;

  for (int i = 0; i < m; i ++ ) {
    int a, b;
    cin >> a >> b;
    a -- , b -- ;
    add(a, b);
    in[a] ++ , in[b] ++ ;
  }
  if (m == 0) {
    puts("0");
    return;
  }
  set<node> q;
  for (int i = 0; i < n; i ++ ) 
    if (in[i] > 1) q.insert((node){i});
  vector<array<int, 3>> ops;
  auto output = [&]() {
    cout << ops.size() << endl;
    for (auto [a, b, c] : ops) cout << a+1 << " " << b+1 << " " << c+1 << endl;
  };
  while (!q.empty()) {
    int a = (*q.begin()).a, b, c;
    b = *E[a].begin(), E[a].erase(b);
    c = *E[a].begin(), E[a].erase(c);
    in[a] -= 2;
    if (E[b].find(c) == E[b].end()) add(b, c);
    else {
      E[b].erase(c), E[c].erase(b);
      in[b] -= 2, in[c] -= 2;
    }
    if (in[a] < 2) q.erase((node){a});
    if (in[b] < 2) q.erase((node){b});
    if (in[b] < 2) q.erase((node){b});
    ops.push_back({a, b, c});
  }

  {
    bool flag = 1;
    for (int i = 0; i < n; i ++ ) 
      if (in[i]) {
        flag = 0;
        break;
      }
    if (flag)  { output(); return; }
  }
  vector<int> q0;
  int a = -1, b = -1;
  for (int i = 0; i < n; i ++ ) 
    if (in[i] == 0) q0.push_back(i);
  for (int i = 0; i < n; i ++ ) 
    if (in[i]) {
      a = i, b = *E[a].begin();
      break;
    }
  // printf("----%d %d\n", a, b);
  while (!q0.empty()) {
    int t = q0.back(); q0.pop_back();
    ops.push_back({t, a, b});
    b = t;
  }
  
  output();
  return;
}

int main() {
  int T = 1;
  cin >> T;
  while (T -- ) {
    solve();
  }
  return 0;
}