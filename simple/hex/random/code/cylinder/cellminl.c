// estimate relative value of cells wrt winning moves ... rbh 2011

// over all winning subsets, estimate prob that each cell
// is in a minimal path in the subset   // how to compute:
// for each winning subset, 
//   consider cells in random order,
//   print first cell that forms a winning set...
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include "board.hex.h"
#define Samples 1000000

void cellWinnerProbs(void) { int j,k,t,v,lcn;
  srand(99913987);
  int Locations[NR], cellWins[NR], gameLength[NR],
      fatBrd[Np2Rp2], parent[Np2Rp2];
  init_locations(Locations);

  for (j=0; j<5; j++) shuffle(Locations);
  for (j=0; j<NR; j++) { cellWins[j] = 0; gameLength[j] = 0; }

  // ************************ //
  // cylindrical board: check for top-bottom 2nd player wins, so NR/2 //
  int numMoves = P2moves;
  // ************************ //
  int x,y,wins=0;
  for (j=0; j<Samples; j++) {
    shuffle(Locations);
    init_UF_guard_brd(fatBrd,parent); //showAsFatBoard(fatBrd);
    int done = 0; k = -1;
    while ((k<numMoves-1) && !done) {
      k++;
      lcn = Locations[k];
      fatBrd[lcn] = BLACK; //showAsFatBoard(fatBrd);
      v = lcn; 
      // ************************ //
      // cylindrical board: check for wraparound adjacency //
      int col = lcn%Np2;
      if (1==col) {  // leftmost column adjacency Offsets1
        for (t=0; t<6; t++) {
          v += Offsets1[t]; //printf("v = %d\n",v);
          if (BLACK==fatBrd[v])
            myUnion(parent,lcn,v); //printf("k %d  v %d\n",k,v);
        }
      }
      else if (N==col) { // rightmost column adjacency Offsetsn
        for (t=0; t<6; t++) {
          v += Offsetsn[t]; //printf("v = %d\n",v);
          if (BLACK==fatBrd[v])
            myUnion(parent,lcn,v); //printf("k %d  v %d\n",k,v);
        }
      }
      else {
        for (t=0; t<6; t++) { // usual adjacency Offsets
          v += Offsets[t]; //printf("v = %d\n",v);
          if (BLACK==fatBrd[v])
            myUnion(parent,lcn,v); //printf("k %d  v %d\n",k,v);
        }
      }
      // ************************ //
      x = myFind(parent,FIRST_TOP);
      y = myFind(parent,LAST_BTM);
      done = (x==y)?1:0;
    }
    //showAsFatBoard(fatBrd); showAsFatBoard(parent);
    if (done) {
      cellWins[unfatten(lcn)]++;
      gameLength[k+1]++;
      wins ++;
    }
    for (k=0; k<numMoves; k++) {
      fatBrd[Locations[k]] = EMPTY;
    }
  }
  printf("%f top-bottom cylhex win rate, %dx%d board",(1.0*wins)/(1.0*Samples),R,N);
  printf("  %d samples\n\n",Samples);
  showUnguarded(cellWins);

  int sum = 0; 
  double length = 0.0;
  for (j=0; j< NR; j++) {
    sum+= cellWins[j];
    length+= (1.0*gameLength[j]*j)/(1.0*wins);
  }
  assert(sum==wins);
  printf("%f avg black moves (among black wins)\n\n",length);
  showUnguarded(gameLength);
  //showForGnuplot(gameLength,Samples);

  printf("\nprob. cell in minimal winning black path\n");
  double s = 0.0; double p;
  int psn = 0;
  for (j = 0; j < R; j++) {
    for (k = 0; k<j; k++)
      printf("  ");
    for (k = 0; k < N; k++) {
      p = 1.0*cellWins[psn]/(1.0*Samples);
      psn++;
      s+=p;
      printf("%2.2f  ", (N*N*10*p+0.5));
    }
    printf("\n");
  }
  printf("\n%f prob. sum\n",s);
}

int main(void) {
  cellWinnerProbs();
  return 0;
}
