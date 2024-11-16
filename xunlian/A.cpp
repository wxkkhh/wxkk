#include <bits/stdc++.h>
#define int long long
using namespace std;

typedef long long LL;

signed main() {
  int n;
  cin >> n;
  vector<int> primes, st(n+5, 0), ist(n+5, 1);
  for (int i = 2; i <= n+1; i ++ ) {
    if (!st[i]) primes.push_back(i);
    for (int j = 0; j < primes.size() && i * primes[j] <= n+1; j ++ ) {
      st[i*primes[j]] = 1;
      if (i % primes[j] == 0) break;
    }
  }
  LL l = 1ll*n*n, r = l+n;
  for (auto p : primes) {
    LL fi = 1ll*(l+p-1)/p*p, la = r/p*p;
    for (LL x = fi; x <= la; x += p) 
      ist[x-l] = 0;
  }
  int ans = 0;
  for (int i = 0; i <= n; i ++ ) ans += ist[i];
  cout << ans << endl;
  return 0;
}