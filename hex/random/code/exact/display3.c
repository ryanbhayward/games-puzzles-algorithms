// display all 3x3 positions with 4 stones
#include <stdio.h>
#include <assert.h>
#define N 3
#define Nsq 9
#define Nsqp1 10 
#define K 4
#define Numsubs 126
#define boardsperline 9  // must divide Numsubs

void subsInit(int A[Numsubs][Nsq]) { int j,k,t;
  for (j=0; j < Numsubs;   j++)  
    for (k=0; k< Nsq; k++) {
      scanf("%d", &t);
      A[j][k] =t;
    }
}

void subsShow(int A[Numsubs][Nsq]) { int j,k;
  for (j=0; j < Numsubs;   j++)  {
    for (k=0; k< Nsq; k++)
      printf("%2d", A[j][k]);
    printf("\n");
  }
}

// print boardsperline boards across each "line"
void subsPretty(int A[Numsubs][Nsq]) { int j,k,n,row,b;
  for (n=0; n*boardsperline < Numsubs; n++) {
    for (row = 0; row < 3; row++) {
      for (j=0; j<row; j++)
        printf(" ");
      for (b = 0; b<boardsperline; b++) {
        for (k=0; k<N; k++)
          //printf("%2d",A[n*boardsperline+b][row*N + k]);
          if (A[n*boardsperline+b][row*N + k])
            printf(" 1");
          else
            printf(" .");
        printf("   ");
      }
    printf("\n");
    }
  printf("\n");
  }
}

int main(void) {
  int A[Numsubs][Nsq];
  subsInit(A);
//  subsShow(A);
  subsPretty(A);
}
