#include <bits/stdc++.h>

using namespace std;

const int mod = 786433;

int pw(int x, int k, int mod) {
  int ans = 1;
  for (;k; k >>= 1, x = 1ll*x*x%mod) 
    if (k & 1) ans = 1ll*ans*x%mod;
  return ans;
}

int main() {
  int t = 2;
  while (t < mod) {
    map<int, int> mp;
    mp[1] = 1;
    bool flag = 1;
    for (int i = 1; i < mod; i ++ ) 
      if (mp[pw(t, i, mod)]) {
        flag = 0;
        break;
      }else mp[pw(t, i, mod)] = 1;
    if (flag) {
      cout << t << endl;
      break;
    }
    t ++ ;
  }
  return 0;
}