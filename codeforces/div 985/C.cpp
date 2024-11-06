#include <bits/stdc++.h>

using namespace std;

void solve() {
  int n;
  cin >> n;
  vector<int> a(n);
  for (int i = 0; i < n; i ++ ) cin >> a[i];
  // for (auto t : a) cout << t << " ";
  // cout << endl;
  // return;
  vector<int> p(n), lp(n);
  for (int i = 0, x = 0; i < n; p[i] = x, i ++ ) 
    if (a[i] < x) x -- ;
    else if (a[i] > x) x ++ ;
  for (int i = 1; i < n; i ++ ) p[i] = max(p[i-1], p[i]);

  int l = 0, r = n;
  while (l < r) {
    int mid = l + r + 1 >> 1;
    for (int i = n-1, x = mid; i >= 0; lp[i] = x, i -- ) 
      if (a[i] > x-1) x -- ;
      else if (a[i] < x+1) x ++ ;
    bool flag = (lp[1] <= 0);
    for (int i = 2; i < n; i ++ ) 
      if (p[i-2] >= lp[i]) {
        flag = 1;
        break;
      }
    if (flag) l = mid;
    else r = mid-1;
  }
  int ans = l;
  for (int i = 0; i < n-1; i ++ ) ans = max(ans, p[i]);
  cout << ans << endl;
  return;
}

int main() {
  int T;
  cin >> T;
  // cout << T << endl;
  while (T -- ) {
    solve();
  }

  return 0;
}