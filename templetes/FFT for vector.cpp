#include <bits/stdc++.h>

using namespace std;

typedef complex<double> cp;

const double PI = acos(-1);

void FFT(vector<cp> &a, bool tag) {
  int n = a.size();
  for (int i = 1, j = 0; i < n; i ++ ) {
    int bit = n >> 1;
    for (; j & bit; bit >>= 1) 
      j ^= bit;
    j ^= bit;
    if (i < j) swap(a[i], a[j]);
  }

  for (int len = 2; len <= n; len >>= 1) {
    double ang = 2.0*PI*len/n;
    cp wlen(cos(ang), sin(ang));
    for (int i = 0; i < n; i += len) {
      cp w(1);
      for (int j = 0; j < len/2; j ++ ) {
        cp u = a[i+j], v = w*a[i+j+len/2];
        a[i+j] = u+v, a[i+j+len] = u-v;
        w *= wlen;
      }
    }
  }
  if (tag) {
    for (int i = 0; i < n; i ++ ) a[i] /= n;
  }
}

vector<int> mul(vector<int> a, vector<int> b) {
  vector<cp> fa(a.begin(), a.end()), fb(b.begin(), b.end());
  int n = 1;
  while (n < a.size() + b.size()) n <<= 1;
  fa.resize(n), fb.resize(n);
  FFT(fa, 0), FFT(fb, 0);
  for (int i = 0; i < n; i ++ ) fa[i] *= fb[i];
  FFT(fa, 1);
  vector<int> ans(n);
  for (int i = 0; i < n; i ++ ) ans[i] = round(fa[i].real());
  return ans;
}

int main() {
  
  return 0;
}