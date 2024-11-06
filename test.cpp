#include <bits/stdc++.h>

using namespace std;

int gcd(int a, int b) {
  return b ? gcd(b, a%b) : a;
}

int add(int a, int b) { 
  return a + b;
}

int mul(int a, int b) {
  return a * b;
}

int main() {
  int a = 23;
  int &b = a;
  cout << b << endl;
  b -- ;
  cout << b << endl;
  return 0;
}