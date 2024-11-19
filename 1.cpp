#include <bits/stdc++.h>

// (...) fun((...) ,(...) ) {
//   if (...) return (...);
//   if (...) return (...);
//   else return fun((...), (...));
// }

char s[10];

bool fun(int i, int len) { 
  if (i > len/2) return 1;
  if (s[i] != s[len-i-1]) return 0;
  else return fun(i+1, len);
}

int main() {
  std::cin >> s;
  std::cout << fun(0, strlen(s)) << std::endl;;
  int len = strlen(s);

  int flag[len] = {0};
  for (int i = 0; i <= len/2; i ++ )
    flag[i] = (s[i] == s[len-i-1]);
  int ans = 1;
  for (int i = 0; i <= len/2; i ++ ) ans &= flag[i];
  std::cout << ans;
  return 0;
}