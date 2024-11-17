#include <iostream>
#include <vector>
#include <complex>
#include <cmath>
using namespace std;
#define ll long long
#define ld long double
#define cp complex<ld>
#define endl '\n'
#define FOR(i, l, r) for (ll i = (l); i <= (r); i++)
const double PI = acos(-1);
void FFT(vector<cp> &p, ll n, ll inv)
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
    ll n, m, tmp, pown = 1;
    cin >> n >> m;
    while (pown < n + m)
        pown <<= 1;
    vector<cp> a(pown, 0), b(pown, 0), c(pown, 0);
    FOR(i, 0, n - 1)
    {
        cin >> tmp;
        a[i] = cp(tmp, 0);
    }
    FOR(i, 0, m - 1)
    {
        cin >> tmp;
        b[i] = cp(tmp, 0);
    }
    FFT(a, pown, 1);
    FFT(b, pown, 1);
    FOR(i, 0, pown - 1)
    c[i] = a[i] * b[i];
    FFT(c, pown, -1);
    FOR(i, 0, pown - 1)
    c[i] /= pown;
    ll sum = 0;
    FOR(i, 0, pown - 1)
    sum += (ll)round(c[i].real());
    cout << sum;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0), cout.tie(0);
    ll T = 1;
    // cin >> T;
    while (T--)
    {
        solve();
    }
    return 0;
}
