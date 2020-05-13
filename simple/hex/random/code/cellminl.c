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
#define Samples 50000000

void cellWinnerProbs(void) { int j,k,t,v,lcn;
  srand(9913987);
  int Locations[Nsq], cellWins[Nsq], gameLength[Nsq],
      fatBrd[Np2sq], parent[Np2sq];
  init_locations(Locations);

  for (j=0; j<10; j++) shuffle(Locations);
  for (j=0; j<Nsq; j++) { cellWins[j] = 0; gameLength[j] = 0; }

   // now I want to iterate over all moves
  int numMoves = (Nsq+1)/2;
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
      for (t=0; t<6; t++) {
        v += Offsets[t]; //printf("v = %d\n",v);
        if (BLACK==fatBrd[v])
          myUnion(parent,lcn,v); //printf("k %d  v %d\n",k,v);
      }
      x = myFind(parent,FIRST_TOP);
      y = myFind(parent,LAST_BTM);
      done = (x==y)?1:0;
    }
    //showAsFatBoard(fatBrd);
    if (done) {
      cellWins[unfatten(lcn)]++;
      gameLength[k+1]++;
      wins ++;
    }
    for (k=0; k<numMoves; k++) {
      fatBrd[Locations[k]] = EMPTY;
    }
  }
  printf("%f black win rate, %dx%d board",(1.0*wins)/(1.0*Samples),N,N);
  printf("  %d samples\n\n",Samples);
  showUnguarded(cellWins);

  int sum = 0; 
  double length = 0.0;
  for (j=0; j< Nsq; j++) {
    sum+= cellWins[j];
    length+= (1.0*gameLength[j]*j)/(1.0*wins);
  }
  assert(sum==wins);
  printf("%f avg black moves (among black wins)\n\n",length);
  //showUnguarded(gameLength);
  showForGnuplot(gameLength,Samples);

  printf("\nuni-random game, percentx100 prob. cell is black-win last-move\n");
  double s = 0.0; double p;
  for (j = 0; j < N; j++) {
    for (k = 0; k<j; k++)
      printf("  ");
    for (k = 0; k < N; k++) {
      p = (1.0*cellWins[j+N*k])/(1.0*Samples);
      s+=p;
      printf("%3d   ",(int) (10000*p+0.5));
      //printf("%0.5f  ", (p));
    }
    printf("\n");
  }
  printf("\n%f prob. sum\n",s);
}

int main(void) {
  cellWinnerProbs();
  return 0;
}
