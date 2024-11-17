#include <bits/stdc++.h>

using namespace std;
// #define int long long
typedef long long LL;

const int mod = 1e9+7, N = 1e6;

int main() {
  LL C;
  cin >> C;
  vector<int> primes, st(N+6, 0);
  for (int i = 2; i <= N+3; i ++ ) {
    if (!st[i]) primes.push_back(i);
    for (auto p : primes) {
      if (p * i > N) break;
      st[i * p] = 1;
      if (i % p == 0) break;
    }
  }
  LL x = 1;
  for (auto p : primes) {
    if (C % p == 0) {
      C /= p;
      if (C % p == 0) x *= p;
      while (C % p == 0) C /= p;
    }
  }
  LL t = sqrt(C);
  if (t > 1 && t * t == C) x *= t;
  // cout << x << endl;
  cout << x/2+1 << endl;
  return 0;
}