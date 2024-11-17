#include <iostream>
#include <vector>
#include <complex>
#include <cmath>
using namespace std;
#define ll long long
#define ld long double
#define cp complex<ld>
#define endl '\n'
#define FOR(i, l, r) for (int i = (l); i <= (r); i++)
const double PI = acos(-1);

void FFT(vector<cp> &p, int n, int inv)
{
    if (n == 1)
        return;
    vector<cp> a(n / 2), b(n / 2);
    FOR(i, 0, n / 2 - 1)
    a[i] = p[i * 2], b[i] = p[i * 2 + 1];
    FFT(a, n / 2, inv);
    FFT(b, n / 2, inv);
    ld ang = 2 * PI / n * inv;
    cp wn(cos(ang), sin(ang));
    cp w(1, 0);
    FOR(i, 0, n / 2 - 1)
    {
        p[i] = a[i] + w * b[i];
        p[i + n / 2] = a[i] - w * b[i];
        w *= wn;
    }
}

void solve()
{
    string s1, s2;
    cin >> s1 >> s2;
    int n = s1.size(), m = s2.size();
    int pown = 1;
    while (pown < n + m)
        pown <<= 1;
    vector<cp> a(pown, 0), b(pown, 0), c(pown, 0);
    FOR(i, 0, n - 1)
    a[i] = cp(s1[n - 1 - i] - '0', 0);
    FOR(i, 0, m - 1)
    b[i] = cp(s2[m - 1 - i] - '0', 0);
    FFT(a, pown, 1);
    FFT(b, pown, 1);
    FOR(i, 0, pown - 1)
    c[i] = a[i] * b[i];
    FFT(c, pown, -1);
    FOR(i, 0, pown - 1)
    c[i] /= pown;

    vector<int> ans(pown, 0);
    FOR(i, 0, pown - 1)
    ans[i] = round(c[i].real());

    int carry = 0;
    FOR(i, 0, pown - 1)
    {
        int total = ans[i] + carry;
        ans[i] = total % 10;
        carry = total / 10;
    }
    string result = "";
    bool started = false;
    for (int i = pown - 1; i >= 0; i--)
    {
        if (ans[i] != 0)
            started = true;
        if (started)
            result += to_string(ans[i]);
    }
    if (!started)
        result = "0";
    cout << result;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0), cout.tie(0);
    int T = 1;
    // cin >> T;
    while (T--)
    {
        solve();
    }
    return 0;
}
