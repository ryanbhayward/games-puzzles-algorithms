/* John Tromp program */
/* C program to solve 2x2 go with area rules and positional superko */
/* note that suicide is not possible in this case */
/* trying moves before passes slows search dramatically */

#include <stdio.h>
#define NSHOW 4
#define NMOVES 4
#define CUT 1   /* 0 for plain minimax */

char h[256];   /* bitmap of positions in game history */
int nodes[100]; /* number of nodes visited at each depth */
long ngames;
long ngamesatdepth[100];

void show(int n, int black, int white, int alpha, int beta, int passed)
	/* print 2-line ascii representation of position */
{
  int i;
  printf("%d (%d,%d)%s\n", n, alpha, beta, passed?" pass":"");
  for (i=0; i<4; i++) {
    printf(" %c", ".XO#"[(black>>i&1)+2*(white>>i&1)]);
    if (i&1)
      putchar('\n');
  }
}

void visit(int black, int white)
{
  h[black +16* white] = 1;
}

void unvisit(int black, int white)
{
  h[black +16* white] = 0;
}

int visited(int black, int white)
{
  return h[black +16* white];
}

int owns(int bb)
{
  return bb == (1|8) || bb == (2|4);
}

int popcnt[16] = {0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4}; /* number of 1 bits */

int score(int depth, int black, int white)
{
  ngames++;
  ngamesatdepth[depth]++;
  if (black==0)
    return white ? -4 : 0;
  if (white==0)
    return 4;
  else return popcnt[black]-popcnt[white];
}

int xhasmove(int black, int white, int move, int *newblack, int *newwhite)
{
  move = 1<<move;
  if ((black|white)&move || popcnt[black]==3 || owns(white))
    return 0;
  *newblack = black|move;
  *newwhite = (*newblack|white)==15 || owns(*newblack) ? 0 : white;
  return !visited(*newblack,*newwhite);
}

int ohasmove(int black, int white, int move, int *newblack, int *newwhite)
{
  move = 1<<move;
  if ((black|white)&move || popcnt[white]==3 || owns(black))
    return 0;
  *newwhite = white|move;
  *newblack = (*newwhite|black)==15 || owns(*newwhite) ? 0 : black;
  return !visited(*newblack,*newwhite);
}

int xab(int n, int black, int white, int alpha, int beta, int passed)
{
  int i,s,newblack,newwhite;
  int oab(int, int, int, int, int, int);

  nodes[n]++;
  if (n<NSHOW)
    show(n,black,white,alpha,beta,passed);

  s = passed ? score(n, black, white) : oab(n,black,white,alpha,beta,1);
  if (s > alpha && (alpha=s) >= beta && CUT) return alpha;

  for (i=0; i<NMOVES; i++) {
    if (xhasmove(black,white,i,&newblack,&newwhite)) {
      visit(newblack,newwhite);
      s = oab(n+1, newblack, newwhite, alpha, beta, 0);
      unvisit(newblack,newwhite);
      if (s > alpha && (alpha=s) >= beta && CUT) return alpha;
    }
  }

  return alpha;
}

int oab(int n, int black, int white, int alpha, int beta, int passed)
{
  int i,s,newblack,newwhite;

  nodes[n]++;
  if (n<NSHOW)
    show(n,black,white,alpha,beta,passed);

  s = passed ? score(n, black, white) : xab(n,black,white,alpha,beta,1);
  if (s < beta && (beta=s) <= alpha && CUT) return beta;

  for (i=0; i<NMOVES; i++) {
    if (ohasmove(black,white,i,&newblack,&newwhite)) {
      visit(newblack,newwhite);
      s = xab(n+1, newblack, newwhite, alpha, beta, 0);
      unvisit(newblack,newwhite);
      if (s < beta && (beta=s) <= alpha && CUT) return beta;
    }
  }

  return beta;
}

int main()
{
  int i,c,s;
  c = xab(0, 0, 0, -4, 4, 0);
  for (i=s=0; nodes[i]; i++) {
    s += nodes[i];
    printf("%d: %d\n", i, nodes[i]);
  }
  for (i=0; i<100; i++)
    printf("%2d: nodes %ld games %ld\n", i, nodes[i], ngamesatdepth[i]);
  printf("total: %d\nngames: %ld\nx wins by %d\n", s, ngames, c);
  return 0;
}
