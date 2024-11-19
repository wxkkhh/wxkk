#include <cstdio>
#include <iostream>
#include <set>
#include <algorithm>
#include <vector>
using namespace std;

#define af assert(false)
#define el printf("\n")
#define ff(x) cout <<#x<<" = "<<x<<", "
#define fff(x, l, r) { cout<<#x<<"["<<l<<", "<<r<<"]: ";for(int i=l;i<=r;++i)cout<<x[i]<<" ";cout<<"\n"; }

inline int read() {
    #define gc getchar();
    bool f = 0;
    int a = 0; 
    char c = gc;
    while (c < '0' || c > '9') {
        if (c == '-') f = 1;
        c = gc;
    }
    while (c >= '0' && c <= '9') {
        a = (a << 1) + (a << 3) + (c ^ 48);
        c = gc;
    }
    return f ? -a : a;
    #undef gc
}

#define ll long long

ll mul(ll x, ll y, const ll &p) {
    return (__int128) x * y % p;
}

ll pw(ll x, ll y, const ll &p) {
    ll ans = 1;
    for (; y; y >>= 1) {
        if (y & 1) ans = mul(ans, x, p);
        x = mul(x, x, p);
    }
    return ans;
}

int mr(ll x, ll p) {
    if (pw(x, p - 1, p) != 1) return 0;
    ll y = p - 1, z;
    while (~y & 1) {
        y >>= 1;
        z = pw(x, y, p);
        if (z != 1 && z != p - 1) return 0;
        if (z == p - 1) return 1;
    }
    return 1;
}

int ck(ll x) {
    if (x <= 1) return 0;
    if (x == 2 || x == 3 || x == 5 || x == 7 || x == 43) return 1; 
    return mr(2 ,x) && mr(3, x) && mr(5, x) && mr(7, x) && mr(43, x);
}

void solve() {
    ll x; 
    scanf("%lld", &x);
    printf("%s", ck(x) ? "YES\n" : "NO\n");
}

int main() {
    // freopen("1.in", "r", stdin);
    int t = read();
    while (t--) solve();
    
    return 0;
}