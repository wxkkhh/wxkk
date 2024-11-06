#include <bits/stdc++.h>

using namespace std;

int main() {
  int T;
  cin >> T;
  while (T -- ) {
    int n;
    cin >> n;
    vector<int> a(n), pre(n), sum(n+n, 0);
    for (auto &x : a) cin >> x;
    for (int i = 0; i < n; i ++ ) pre[i] = a[(i+1)%n]-a[i];
    int mx = -1e9;
    for (int i = 0; i < n; i ++ ) mx = max(mx, pre[i]);
    for (int i = 0; i < n; i ++ ) {
      int add = mx-pre[i];
      sum[i+1] += add;
      sum[i+n] -= add;
    }
    for (int i = 2; i < n*2; i ++ ) sum[i] += sum[i-2];
    for (int i = 0; i < n; i ++ ) cout << pre[i] << " ";
    cout << endl;
    for (int i = 0; i < n*2; i ++ ) cout << sum[i] << " ";
    cout << endl;
  }
  return 0;
}