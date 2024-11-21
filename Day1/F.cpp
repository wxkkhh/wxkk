#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

LL qmi(LL x, LL k, LL mod) {
  LL ans = 1;
  for (; k; k >>= 1, x = (__int128)x*x%mod) 
    if (k & 1) ans = (__int128)ans*x%mod;
  return ans;
}

LL f(LL x, LL c, LL mod) {
  return ((__int128)x*x%mod+c)%mod;
}

LL pollard_rho(LL n) {
  LL c = rand() % (n-1)+1;
  LL a = f(0, c, n), b = f(a, c, n);
  while (a != b) {
    LL d = gcd(llabs(a-b), n);
    if (d > 1) return d;
    a = f(a, c, n), b = f(a, c, n);
  }
  return n;
}

bool ck(LL x, LL p) {
  if (qmi(p, x-1, x) != 1) return 0;
  if (x != 2 && x & 1 == 0) return 0;
  LL y = x-1, z;
  while (~y & 1) {
    y >>= 1;
    z = qmi(p, y, x);
    if (z != 1 && z != x-1) return 0;
    if (z == x-1) return 1;
  }
  return 1;
}

bool miller_rabin(LL n) {
  if (n == 2 || n == 3 || n == 7 || n == 29 || n == 53) return 1;
  return ck(n, 2) && ck(n, 3) && ck(n, 7) && ck(n, 29) && ck(n, 53);
}

int main() {
  LL n;
  cin >> n;
  if (miller_rabin(n)) cout << -1 << endl;
  else {
    LL t = pollard_rho(n);
    // int cnt = 0;
    // while ((t == 1 || t == n) && cnt < 10) {
    //   t = pollard_rho(n);
    //   cnt ++ ;
    // }
    if (n == t) cout << -1 << endl;
    else cout << t << " " << n/t << endl;
  }
  return 0;
}