#include <bits/stdc++.h>

using namespace std;

typedef complex<double> cp;
typedef long long LL;

const int mod = 786433;
const int g = 10;
const int _g = 235930;


int pw(int x, int k, int mod) {
  int ans = 1;
  for (;k; k >>= 1, x = 1ll*x*x%mod) 
    if (k & 1) ans = 1ll*ans*x%mod;
  return ans;
}

void FFT(vector<int> &a, bool tag) {
  int n = a.size();
  for (int i = 1, j = 0; i < n; i ++ ) {
    int bit = n >> 1;
    for (; j & bit; bit >>= 1) 
      j ^= bit;
    j ^= bit;
    if (i < j) swap(a[i], a[j]);
  }
  for (int len = 2; len <= n; len <<= 1) {
    int wlen = pw((tag?_g:g), (mod-1)/len, mod);
    for (int i = 0; i < n; i += len) {
      int w = 1;
      for (int j = 0; j < len/2; j ++ ) {
        int u = a[i+j]%mod, v = 1ll*w*a[i+j+len/2]%mod;
        a[i+j] = (u+v)%mod;
        a[i+j+len/2] = (u-v+mod)%mod;
        w = 1ll*w*wlen%mod;
      }
    }
  }
  if (tag) {
    int _n = pw(n, mod-2, mod);
    //for (int i = 0; i < n; i ++ ) a[i] = 1ll*a[i]*_n%mod;
    for (auto &t : a) t = 1ll*t*_n%mod;
  }
}

/*
void FFT(vector<int> &a, int tag) {
  int n = a.size();

    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1)
            j ^= bit;
        j ^= bit;

        if (i < j)
            swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        LL wlen = tag ? _g : g;
        // for (int i = len; i < root_pw; i <<= 1)
        //     wlen = wlen * wlen % mod;
        // printf("%d\n", qmi(wlen, len, mod));
        // printf("%d-%d\n", wlen, qmi(invert ? root_1 : root, (mod-1)/len, mod));
        wlen = pw(wlen, (mod-1)/len, mod);
        // cout << qmi(wlen, len, mod) << endl;
        for (int i = 0; i < n; i += len) {
            LL w = 1;
            for (int j = 0; j < len / 2; j++) {
                LL u = a[i+j] % mod, v = a[i+j+len/2] * w % mod;
                a[i+j] = (u + v) % mod;
                a[i+j+len/2] = (u - v + mod) % mod;
                w = w * wlen % mod;
            }
        }
    }

    if (tag) {
        LL n_1 = pw(n, mod-2, mod);
        for (auto & x : a)
            x = x * n_1 % mod;
    }
}
*/
vector<int> mul(vector<int> a, vector<int> b) {
  vector<int> fa(a.begin(), a.end()), fb(b.begin(), b.end());
  int n = 1;
  while (n < a.size() + b.size()) n <<= 1;
  fa.resize(n), fb.resize(n);
  FFT(fa, 0), FFT(fb, 0);
  for (int i = 0; i < n; i ++ ) fa[i] = 1ll*fa[i]*fb[i]%mod;
  FFT(fa, 1);
  return fa;
}

int main() {
  int n, H;
  // cout << pw(_g, mod-2, mod) << endl;
  cin >> n >> H;
  vector<vector<int>> f(H+4, vector<int>(n+4, 0));
  f[0][0] = 1, f[1][1] = 1;
  for (int h = 2; h <= H+1; h ++ ) {
    vector<int> A(f[h-1].begin(), f[h-1].end()), B(f[h-1].begin(), f[h-1].end());
    if (h > 1) {
      for (int i = 0; i <= n; i ++ ) 
        (B[i] += 2ll*f[h-2][i]) %= mod;
    }
    auto ans = mul(A, B);
    for (int i = 1; i <= n; i ++ ) f[h][i] = ans[i-1];
    // for (int i = 0; i <= n; i ++ ) cout << A[i] << " ";
    // cout << "A" << endl;
    // for (int i = 0; i <= n; i ++ ) cout << B[i] << " ";
    // cout << "B" << endl;
    // for (int i = 0; i <= n; i ++ ) cout << ans[i] << " ";
    // cout << "ans" << endl;
  }
  // for (int h = 0; h <= H+1; h ++ ) {
  //   for (int i = 0; i <= n; i ++ ) cout << f[h][i] << " ";
  //   cout << endl;
  // }
  cout << f[H+1][n] << endl;
  return 0;
}