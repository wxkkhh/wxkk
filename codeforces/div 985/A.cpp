#include <bits/stdc++.h>

using namespace std;

void solve() {
  int a, b, k;
  cin >> a >> b >> k;
  cout << max(b/k - a+1, 0) << endl;
}

int main() {
  int T = 1;
  cin >> T;
  while (T -- ) {
    solve();
  }
  return 0;
}