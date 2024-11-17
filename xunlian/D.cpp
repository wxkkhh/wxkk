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
  LL n, m;
  cin >> n >> m;
  if (m == 1) {
    cout << n << endl;
    return 0;
  }
  vector<LL> d;
  for (int i = 2; i <= sqrt(m); i ++ )
    if (m % i == 0) {
      while (m % i == 0) m/=i;
      d.push_back(i);
    }
  if (m > 1) d.push_back(m);
  LL ans = 0;
  for (int s = 0, cnt = d.size(); s < 1<<cnt; s ++ ) {
    int t = 0;
    LL base = 1;
    for (int j = 0; j < cnt; j ++ ) 
      if (s >> j & 1) base *= d[j], t ++ ;
    if (t & 1) ans -= n/base;
    else ans += n/base;
  }
  cout << ans << endl;
  return 0;
}