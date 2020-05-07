// find exact 1st/2nd-player winning prob, random play nxn hex
// largest value of n is 5 :(
#include <stdio.h>
#include <assert.h>
#define N 3
#define Nsq 9
#define Nsqp1 10
#define K 5
#define StackMax Nsqp1

// display
void show(int X[]) { int j;
  for (j = 0; j < Nsq; j++) 
    printf("%2d", X[j]);
  printf("\n");
}

// display vector as hex board
void showBoard(int X[]) { int j,k;
  for (j = 0; j < N; j++) {
    for (k = 0; k < j; k++) 
      printf(" ");
    for (k = 0; k < N; k++) 
      printf("%2d", X[j*N+k]);
    printf("\n");
  }
}

// stack
void stackInit(int S[]) {
  S[0]=0;
}

void stackPush(int S[], int x) {
  S[0]++;
  assert(S[0]<StackMax);
  S[S[0]] = x;
  //printf("push %2d\n", x);
}

int stackPop(int S[]) { 
  int j = S[0]--;
  assert(j>0);
  return S[j];
}

// subsets
void vectInit(int X[Nsqp1]) { int j;
  for (j=0; j < K;   j++)  X[j] = 1;
  for (   ; j < Nsqp1; j++)  X[j] = 0;
}

void increment(int X[Nsqp1]) { int first1, next0, j;
  for (first1 = 0;     X[first1] == 0; first1++) ;
  for (next0 = first1; X[next0] == 1; next0++) ;
  assert(next0 < Nsqp1);
  //printf("first1 %2d\n", first1);
  //printf("next0  %2d\n", next0);
  X[next0] = 1; X[next0 - 1] = 0;
  if (first1 > 0)
    for (j=0; j < (next0 - first1) - 1; j++) {
      X[j] = 1; X[j + first1] = 0;
    }
}

// true if top-to-bottom hex connection
// which is true if dfs from 1st row reaches top row
int connection(int S[], int V[]) {
  int j,k,wins;
  int M[Nsqp1]; 
  // all nxn board cells unmarked
  stackInit(S); 
  //printf("stack "); show(S);
  for (j = 0; j < Nsq; j++) 
    M[j]=0;    
  for (j = 0; j < N; j++)
    if (V[j]==1) {
      stackPush(S,j);
      M[j]=1;
    }
  //printf("stack "); show(S);
  while (S[0] > 0) {
    j = stackPop(S);
    //printf("popped %2d\n",j);
    k = j-N;
    if (k>0 && V[k] && 1-M[k]) {
      stackPush(S,k); M[k] = 1; }
    k++;
    if (k>0 && 0!=k%N && V[k] && 1-M[k]) {
      stackPush(S,k); M[k] = 1; }
    k = j-1;
    if (0!=j%N && V[k] && 1-M[k]) {
      stackPush(S,k); M[k] = 1; }
    k= j+1;
    if (0!=k%N && V[k] && 1-M[k]) {
      stackPush(S,k); M[k] = 1; }
    k=j+N-1;
    if (k<Nsq && 0!=j%N && V[k] && 1-M[k]) {
      stackPush(S,k); M[k] = 1; }
    k++;
    if (k<Nsq && V[k] && 1-M[k]) {
      stackPush(S,k); M[k] = 1; }
  }
  //showBoard(M);
  for (j = Nsq-N; j<Nsq; j++) 
    if (M[j]) return 1;
  return 0;
}

int main(void) {
  int y = 6;
  int S[StackMax];
  //stackInit(S); show(S);
  //stackPush(S,y); show(S);
  //stackPush(S,3); show(S);
  //printf("popped  %2d\n", stackPop(S)); show(S);
  //printf("popped  %2d\n", stackPop(S)); show(S);
  //for (y=0; y < 12; y++) {
    //stackPush(S,y); show(S);
  //}

  int V[Nsqp1]; 
  int j,k,t;
  int w=0;
  int cuts=0;
  vectInit(V);
  for (j=0; V[Nsq] < 1; j++) {
  //for (j=0; j<30; j++) {
    //showBoard(V);
    y = connection(S,V); //printf("wins? %1d\n\n",y);
    w +=y;
    // count number of times each 1-cell is a cutset
    if (y) { 
      k=0;
      for (t=0; t<K; t++) {
        while (1-V[k]) k++;  // find next node (there are K)
        V[k] = 0; // remove node
        y = connection(S,V);  // still connected ?
        cuts += 1-y;  // no <==> a cut node
        V[k] = 1; //restore V[k]
        k++;
      }
    }
    increment(V);
  }
  printf("patterns %d  wins %d \n",j,w);
  printf("cutnodes %d  total nodes %d \n",cuts,w*K);
}
