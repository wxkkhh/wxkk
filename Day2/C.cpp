#include <bits/stdc++.h>

using namespace std;

typedef long long LL;

LL qmi(LL x, int k, int p) {
  LL ans = 1;
  for (; k; k >>= 1, x = 1ll*x*x%p) 
    if (k & 1) ans = 1ll*ans*x%p;
  return ans;
}

const int mod = 998244353;
const int root = 3;
const int root_1 = qmi(3, mod-2, mod);
const int root_pw = 1 << 23;



void fft(vector<LL> & a, bool invert) {
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
        LL wlen = invert ? root_1 : root;
        // for (int i = len; i < root_pw; i <<= 1)
        //     wlen = wlen * wlen % mod;
        // printf("%d\n", qmi(wlen, len, mod));
        // printf("%d-%d\n", wlen, qmi(invert ? root_1 : root, (mod-1)/len, mod));
        wlen = qmi(wlen, (mod-1)/len, mod);
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

    if (invert) {
        LL n_1 = qmi(n, mod-2, mod);
        for (auto & x : a)
            x = x * n_1 % mod;
    }
}

vector<LL> multiply(vector<int> const& a, vector<int> const& b) {
    vector<LL> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    int n = 1;
    while (n < a.size() + b.size()) 
        n <<= 1;
    fa.resize(n);
    fb.resize(n);

    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < n; i++)
        fa[i] = fa[i] * fb[i] % mod;
    fft(fa, true);

    vector<LL> result(fa.begin(), fa.end());
    
    return fa;
}

int main() {
  int n;
  cin >> n;
  n = 1<<n;
  vector<int> a(n), b(n);
  for (auto &t : a) cin >> t;
  for (auto &t : b) cin >> t;
  auto ans = multiply(a, b);
  for (int i = 0; i <= n+n-1; i ++ ) cout << ans[i]%mod << " ";
     
  return 0;
}