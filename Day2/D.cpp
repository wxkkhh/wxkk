#include <bits/stdc++.h>

using namespace std;

const int mod = 786433;
const int g = 10;
const int _g = 235930;


int pw(int x, int k, int mod) {
  int ans = 1;
  for (;k; k >>= 1, x = 1ll*x*x%mod) 
    if (k & 1) ans = 1ll*ans*x%mod;
  return ans;
}

int main() {
  return 0;
}