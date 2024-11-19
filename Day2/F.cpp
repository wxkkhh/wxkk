#include <bits/stdc++.h>

using namespace std;

typedef complex<double> cp;

const double PI = acos(-1);

void fft(vector<cp> &a, bool flag) {
  int n = a.size();
  for (int i = 1, j = 0; i < n; i ++ ) {
    int bit = n >> 1;
    for (; j & bit; bit >>= 1) 
      j ^= bit;
    j ^= bit;
    if (i < j) swap(a[i], a[j]);
  }

  for (int len = 2; len <= n; len <<= 1) {
    double ang = 2*PI/len*(flag?-1:1);
    cp wlen(cos(ang), sin(ang));
    for (int i = 0; i < n; i += len) {
      cp w(1);
      for (int j = 0; j < len/2; j ++ ) {
        cp u = a[i+j], v = a[i+j+len/2]*w;
        a[i+j] = u+v;
        a[i+j+len/2] = u-v;
        w *= wlen;
      }
    }
  }
  if (flag) {
    for (int i = 0; i < n; i ++ ) 
      a[i] /= n;
  }
}

vector<int> multiply(vector<int> A, vector<int> B) {
  int n = 1;
  while (n < A.size() + B.size()) n <<= 1;
  vector<cp> fa(A.begin(), A.end()), fb(B.begin(), B.end());
  fa.resize(n), fb.resize(n);
  fft(fa, 0), fft(fb, 0);
  for (int i = 0; i < n; i ++ ) fa[i] *= fb[i];
  fft(fa, 1);
  vector<int> ans(n);
  for (int i = 0; i < n; i ++ ) ans[i] = round(fa[i].real());
  return ans;
}

int find(vector<int> &p, int x) {
  if (p[x] != x) p[x] = find(p, p[x]);
  return p[x];
}

int main() {
  string S, T;
  cin >> S >> T;
  int n = S.size(), m = T.size();
  reverse(T.begin(), T.end());

  auto get = [](string X, int c) {
    vector<int> ans(X.size());
    for (int i = 0; i < X.size(); i ++ ) 
      ans[i] = X[i] == c+'a';
    return ans;
  };

  array<vector<int>, 6> p;
  for (int t = 0; t < 6; t ++ ) 
    for (int i = 0; i < n; i ++ ) p[t][i] = i;
  vector<int> ans(n, 0);
  for (int i = 0; i < 6; i ++ )   
    for (int j = 0; j < 6; j ++ ) 
      if (i != j) {
        auto A = get(S, i), B = get(T, j);
        auto C = multiply(A, B);
        for (int t = 0; t < n; t ++ ) 
          if (C[i]) {
            if (find(p[i], t) != find(p[j], t)) 
              p[i][find(p[i], t)] = find(p[j], t), ans[t] ++ ;
          }
      }
  for (int i = m-1; i < n; i ++ ) cout << ans[i] << endl;
  
  return 0;
}