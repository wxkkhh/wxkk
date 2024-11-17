#include <bits/stdc++.h>

using namespace std;
#define int long long
typedef long long LL;

const int mod = 1e9+7;

int poww(int x, int k) {
  int ans = 1;
  for ( ; k; x = 1ll*x*x%mod, k >>= 1) 
    if (k & 1) ans = 1ll*ans*x%mod;
  return ans;
}

signed main() {
  int n;
  cin >> n;
  vector<int> a(n);
  int mx = 0;
  for (int i = 0; i < n; i ++ ) cin >> a[i], mx = max(a[i], mx);
  vector<int> cnt(mx+4);
  for (int i = 0; i < n; i ++ ) cnt[a[i]] ++ ;
  for (int i = 1; i < mx; i ++ ) 
    for (int j = i*2; j <= mx; j += i) 
      cnt[i] += cnt[j];
  vector<int> f(mx+4), g(mx+4);
  
  

  for (int i = 1; i <= mx; i ++ ) 
    if (cnt[i]) f[i] = cnt[i]*poww(2, cnt[i]-1)%mod;
  
  for (int i = mx; i; i -- ) {
    g[i] = f[i];
    for (int j = 2*i; j <= mx; j += i) 
      g[i] = (g[i]+mod-g[j]) % mod;
  }
  // for (int i = 1; i <= mx; i ++ ) cout << g[i] << " ";
  // cout << endl;
  int ans = 0;
  for (int i = 2; i <= mx; i ++ ) ans = 1ll*(ans + i*g[i]) % mod;
  cout << ans << endl;
  return 0;
}