#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

const int mod = 1e9+7;

int main() {
  int n;
  cin >> n;
  vector<int> primes, u(n+5), st(n+5);
  u[1] = 1;
  for (int i = 2; i <= n+2; i ++ ) {
    if (!st[i]) primes.push_back(i), u[i] = -1;
    for (auto t : primes) {
      if (i*t > n+2) break;
      st[i*t] = 1;
      if (i % t == 0) {
        u[i*t] = 0;
        break;
      }
      u[i*t] = -u[i];
    }
  }
  // for (int i = 1; i <= n; i ++ ) cout << u[i] << " ";

  LL ans = 0;
  for (int d = 1; d <= n; d ++ ) 
    for (int i = 1; i <= n/d; i ++ ) 
      ans += 1ll*d*u[i]*(n/(d*i))*(n/(d*i));
  cout << ans << endl;
  return 0;
}