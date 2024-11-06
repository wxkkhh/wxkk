#include <bits/stdc++.h>

using namespace std;

void solve() {
  int n;
  cin >> n;
  string S, R;
  cin >> S >> R;
  int cnt0 = 0, cnt1 = 0;
  for (int i = 0; i < n; i ++ ) 
    if (S[i] == '0') cnt0 ++ ;
    else cnt1 ++ ;
  for (int i = 0; i < n-1; i ++ ) {
    if (!cnt0 || !cnt1) {
      puts("NO");
      return;
    }
    cnt0 --, cnt1 -- ;
    if (R[i] == '0') cnt0 ++ ;
    else cnt1 ++ ;
  }
  puts("YES");
}

int main() {
  int T = 1;
  cin >> T;
  while (T -- ) {
    solve();
  }
  return 0;
}