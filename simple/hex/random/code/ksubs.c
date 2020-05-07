// generate index vectors of k-element subsets of n-set 
// use 0th position as overflow indicator
#include <stdio.h>
#include <assert.h>
#define N 9
#define Np1 10
#define K 4

void vectInit(int X[Np1]) { int j;
  for (j=0; j < K;   j++)  X[j] = 1;
  for (   ; j < Np1; j++)  X[j] = 0;
}

void show(int X[Np1]) { int j;
  for (j=N-1; j >= 0; j--) 
    printf("%2d", X[j]);
  printf("\n");
}

void increment(int X[Np1]) { int first1, next0, j;
  for (first1 = 0;     X[first1] == 0; first1++) ;
  for (next0 = first1; X[next0] == 1; next0++) ;
  assert(next0 < Np1);
  //printf("first1 %2d\n", first1);
  //printf("next0  %2d\n", next0);
  X[next0] = 1; X[next0 - 1] = 0;
  if (first1 > 0)
    for (j=0; j < (next0 - first1) - 1; j++) {
      X[j] = 1; X[j + first1] = 0;
    }
}

int main(void) {
  int V[Np1]; 
  int j;
  vectInit(V);
  for (  ;V[N] < 1; ) {
    show(V);
    increment(V);
  }
}
