#include <bits/stdc++.h>

using namespace std;
#define int long long
typedef long long LL;

// const int mod = 1e9+7;

int qmi(LL x, LL k, LL mod) {
  x %= mod;
  LL ans = 1;
  for ( ; k; x = 1ll*x*x%mod, k >>= 1) 
    if (k & 1) ans = 1ll*ans*x%mod;
  return ans;
}

bool f(LL x, int p) {
  if (qmi(p, x-1, x) != 1) return 0;
  if (x & 1 == 0) return 0;
  
}

bool ck(LL x) {
  if (x == 2 || x == 3 || x == 71 || x == 23 || x == 43) return 1;
  return f(x, 2) && f(x, 3) && f(x, 71) && f(x, 23) && f(x, 43);
}

int main() {
  int n;
  cin >> n;
  while (n -- ) {
    LL x;
    cin >> x;
    if (ck(x)) puts("YES");
    else puts("NO");
  }
  return 0;
}