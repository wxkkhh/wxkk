#include <bits/stdc++.h>

using namespace std;
// #define int long long
typedef long long LL;

const int mod = 1e9+7, N = 1e6;

int main() {
  LL C;
  cin >> C;
  if (C == 0) {
    puts("1");
    return 0;
  }
  vector<int> primes, st(N+10, 0);
  for (int i = 2; i <= N+3; i ++ ) {
    if (!st[i]) primes.push_back(i);
    for (auto p : primes) {
      if (p * i > N+3) break;
      st[i * p] = 1;
      if (i % p == 0) break;
    }
  }
  LL x = 1;
  // cout << primes.size() << endl;
  for (auto p : primes) {
    if (C % p == 0) {
      int cnt = 0;
      while (C % p == 0) cnt ++, C /= p;
      while (cnt > 1) cnt -= 2, x *= p;
    }
    if (p > C) break;
  }
  LL t = sqrt(C);
  if (t > 1 && t * t == C) x *= t;
  // cout << x << endl;
  cout << x/2+1 << endl;
  return 0;
}