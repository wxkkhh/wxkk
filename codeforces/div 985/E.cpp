#include <bits/stdc++.h>
using namespace std;

const int N = 4e5+10;

bool st[N];
int primes[N], cnt, di[N];

void solve() {
  int n;
  cin >> n;
  vector<int> a(n);
  for (int i = 0; i < n; i ++ ) cin >> a[i];
  int flag = 0;
  st[2] = 0;
  int x = 0;
  for (int i = 0; i < n; i ++ ) 
    if (!st[a[i]]) {
      x += a[i];
      flag ++ ;
    }
  if (flag == 0) {
    cout << 2 << endl;
  }else if (flag == 1) {
    for (int i = 0; i < n; i ++ ) 
      if (a[i] % x) {
        if (a[i]-di[a[i]] < 2*x) { x = -1; break; }
      }
    cout << x << endl;
  }else cout << -1 << endl;
  
}

int main() {
  int T;
  cin >> T;
  for (int i = 2; i < N-5; i ++ ) {
    if (!st[i]) primes[++cnt] = i;
    for (int j = 1; j <= cnt && i * primes[j] < N-5; j ++ ) {
      st[i * primes[j]] = 1;
      di[i * primes[j]] = primes[j];
      if (i % primes[j] == 0) break;
    }
  }
  while (T -- ) {
    solve();
  }
  return 0;
}