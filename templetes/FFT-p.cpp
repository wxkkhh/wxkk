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
void FFT(vector<cp> &a, int n, int inv)
{
}
void solve()
{
    int n, tmp, pown;
    cin >> n;
    pown = 1 << (int)ceil(log2(n));
    vector<cp> a(pown), b(pown), c(pown);
    FOR(i, 1, pown - n)
    {
        a[i] = cp(0, 0);
        b[i] = cp(0, 0);
    }
    FOR(i, pown - n + 1, pown - 1)
    cin >> tmp, a[i] = cp(tmp, 0);
    FOR(i, pown - n + 1, pown - 1)
    cin >> tmp, b[i] = cp(tmp, 0);
    FFT(a, pown, 1);
    FFT(b, pown, 1);
    FOR(i, 0, pown - 1)
    c[i] = a[i] * b[i];
    FFT(c, pown, -1);
    FOR(i, 0, pown - 1)
    cout << (int)(c[i].real() / pown + 0.5) << ' ';
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
