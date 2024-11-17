#include <bits/stdc++.h>

using namespace std;

typedef complex<double> cp;
typedef long long LL;
const double pi = acos(-1);

using cd = complex<long double>;
const double PI = acos(-1);

void fft(vector<cd> & a, bool invert) {
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
        long double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len / 2; j++) {
                cd u = a[i+j], v = a[i+j+len/2] * w;
                a[i+j] = u + v;
                a[i+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }

    if (invert) {
        for (cd & x : a)
            x /= n;
    }
}

vector<LL> multiply(vector<int> const& a, vector<int> const& b) {
    vector<cd> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    int n = 1;
    while (n < a.size() + b.size()) 
        n <<= 1;
    fa.resize(n);
    fb.resize(n);

    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < n; i++)
        fa[i] *= fb[i];
    fft(fa, true);

    vector<LL> result(n);
    for (int i = 0; i < n; i++)
        result[i] = round(fa[i].real());
    return result;
}

int main() {
  string a, b;
  cin >> a >> b;
  int cnt = 0;
  if (a[0] == '-') cnt ++ , a = a.substr(1);
  if (b[0] == '-') cnt ++ , b = b.substr(1);
  int n = a.size(), m = b.size();
  vector<int> A(n), B(m);
  
  for (int i = 0; i < n; i ++ ) A[i] = a[n-i-1]-'0';
  for (int i = 0; i < m; i ++ ) B[i] = b[m-i-1]-'0';
  
  auto ans = multiply(A, B);
  
  int t = 0;
  for (int i = n+m-2; ~i; i -- ) t += (ans[i] == 0);
  if (t == n+m-1) {
    cout << 0 << endl;
    return 0;
  }
  else if (cnt&1) cout << "-";
  vector<LL> finalans(n+m-1);
  for (int i = 0; i < n+m-1; i ++ ) 
    for (int j = 0; ans[i]; j ++ ) 
      finalans[i+j] = ans[i]%10, ans[i] /= 10;
  for (int i = n+m-2, flag = 1; ~i; i -- )
    if (flag && finalans[i] == 0) continue;
    else cout << finalans[i];
  cout << endl;
  return 0;
}