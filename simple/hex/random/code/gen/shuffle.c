// shuffle the subset, print some stats to show that
//  everything works, and then output a black-winning position
#include <stdio.h>
#include <stdlib.h>
#define N 35
#define Np1 (N+1)
#define Np2 (N+2)
#define Np3 (N+3)
#define Np2sq (Np2*Np2)
#define Nsq (N*N)
#define K ((Nsq+1)/2) //  number black (1st player) stones 
//#define K ((Nsq-1)/2)  // number white (2nd player) stones
#define Samples 1000
#define WHITE 0
#define BLACK 1
#define GUARD 2

const int Offsets[6] = { -Np2, 1, N, 2, N, 1 };

// pseudo-uniform-random in [0.. n-1]
int myrand(int n) { return rand()%n; }

int fatten(int j) { return Np3+j+2*(j/N); }

// shuffle a fat vector
void fatShuffle(int X[Np2sq]) {
  int j,k,tmp;
  for (k = Nsq-1; k > 0; k--) {
    j = myrand(k+1);  //printf("rand %d\n", j);
    tmp = X[fatten(j)]; X[fatten(j)] = X[fatten(k)]; X[fatten(k)] = tmp;
  }
}

// display vector as fat/guarded hex board
void showAsFatBoard(int X[]) { int j,k;
  for (j = 0; j < Np2; j++) {
    for (k = 0; k < j; k++) 
      printf(" ");
    for (k = 0; k < Np2; k++) 
      printf("%2d", X[j*Np2+k]);
    printf("\n");
  }
}

void showAsBoard(int X[]) { int j,k;
  for (j = 1; j < Np1; j++) {
    for (k = 1; k < j; k++) 
      printf(" ");
    for (k = 1; k < Np1; k++) 
      printf("%2d", X[j*Np2+k]);
    printf("\n");
  }
}

void dfs(int M[], int fatV[], int v){ int t;
  M[v]=1; // mark v
  for (t=0; t<6; t++) {
    v += Offsets[t];
    if ((BLACK==fatV[v]) && (!M[v]))
      dfs(M,fatV,v);
  }
}

int dfsConnect(int fatV[]){ int Mark[Np2sq]; int j;
  for (j = 0; j < Np2sq; j++) Mark[j]=0;    
  for (j = Np3; j < N+Np3; j++)
    if ((BLACK==fatV[j]) && (!Mark[j])) 
      dfs(Mark,fatV,j);
  for (j = Np1*Np1; j<Np1*Np1+N; j++) 
    if (Mark[j]) return 1;
  return 0;
}

void guardInit(int fV[Np2sq]) { int j,k;
  for (j=0; j<Np2sq; j++)
    fV[j] = WHITE;
  for (j=0; j<Np2; j++) {
    fV[j] = GUARD; 
    fV[Np2*Np1 + j] = GUARD;
    fV[j*Np2] = GUARD;
    fV[j*Np2-1] = GUARD;
  }
  j = Np2+1;
  for (k=0; k<K; k++) {
    fV[j] = BLACK; j++;
    if (Np1==(j%Np2)) j+=2;
  }
}

int main(void) {
  srand(9913985);
  int fatV[Np2sq];
  guardInit(fatV); //showAsFatBoard(fatV); showAsBoard(fatV);
  int j,wins=0;
  for (j=0; j<Samples; j++) {
    fatShuffle(fatV); 
    wins += dfsConnect(fatV); 
  }
  printf("shuffled %d wins %d samples\n",wins,Samples);
  wins = 0;
  for (j=0; !wins ; j++) {
    fatShuffle(fatV); 
    wins = dfsConnect(fatV); 
    printf("%d try\n",j);
  }
  showAsBoard(fatV);
  return 0;
}
