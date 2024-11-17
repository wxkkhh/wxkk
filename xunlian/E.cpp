#include <bits/stdc++.h>

using namespace std;
// #define int long long
typedef long long LL;

const int mod = 1e9+7;

int qmi(int x, int k) {
  x %= mod;
  LL ans = 1;
  for ( ; k; x = 1ll*x*x%mod, k >>= 1) 
    if (k & 1) ans = 1ll*ans*x%mod;
  return ans;
}

int main() {
  int n, m, c, x;
  cin >> n >> m >> c;
  x = qmi(c, n*n);
  LL ans = 0;
  for (int i = 0; i < m; i ++ ) {
    ans = (ans + qmi(x, __gcd(i, m))) % mod;
  }
  ans = ans * qmi(m, mod-2) % mod;
  cout << ans << endl;
  return 0;
}