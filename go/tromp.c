/* John Tromp's program (comments Jake Hennig and rbh 2024) */
/* C program to solve 2x2 go with area rules and positional superko */
/* note that suicide is not possible in this case */
/* trying moves before passes slows search dramatically */

#include <stdio.h>
#define NSHOW 4  /* output of search displayed to this depth */
#define NMOVES 4 /* max number of non-pass moves */
#define CUT 1    /* CUT 1: pruning, CUT 0: minimax */

char h[256];    /* bitmap of positions in game history */
int nodes[99];  /* number nodes visited at each depth */
long ngames;    /* total number games played */

void show(int n, int black, int white, int alpha, int beta, int passed) /* position's 2-line ASCII rep'n */
{
  int i;
  printf("%d (%d,%d)%s\n", n, alpha, beta, passed ? " pass" : ""); /* depth, alpha, beta, whether player passed */
  for (i = 0; i < 4; i++) {
    printf(" %c", ".XO#"[(black >> i & 1) + 2 * (white >> i & 1)]); /* boardstate (X-black O-white) */
    if (i & 1)
      putchar('\n'); /* 2x2 board, so new_line after each two characters */
  }
} /* 1000 top-left  0100 top-right  0010 bottom-left  0001 bottom-right*/

void visit(int black, int white)
{
  h[black + 16 * white] = 1; /* mark position visited in game history bitmap */
}

void unvisit(int black, int white)
{
  h[black + 16 * white] = 0; /* mark position unvisited in game histroy bitmap */
}

int visited(int black, int white)
{
  return h[black + 16 * white]; /* whether position already visited */
}

int owns(int bb)
{
  return bb == (1 | 8) || bb == (2 | 4); /* whether player owns both board corners */
}

int popcnt[16] = {0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4}; /* number 1-bits in bin-rep, numbers 0..15 */
/* 0000, 0001, 0010, 0011, 0100, 0101... 1110, 1111 */
/* used to count stones of each player */

int score(int black, int white)
{
  ngames++; /* number of games played */
  if (black == 0)          /* no black stones */
    return white ? -4 : 0; /* white wins (-4) unless also no white stones (draw: 0) */
  if (white == 0)          /* no white stones */
    return 4;              /* black wins (+4) */
  else
    return popcnt[black] - popcnt[white]; /* score is diff in stone count */
}

int xhasmove(int black, int white, int move, int *newblack, int *newwhite) /* whether black has valid move */
{
  move = 1 << move; /* shift move left 1 bit */
  /*  position already occupied? black has 3 stones? white owns board?  */
  if ((black | white) & move || popcnt[black] == 3 || owns(white)) 
    return 0; /* move invalid */
  *newblack = black | move; /* updates black position after move */
  *newwhite = (*newblack | white) == 15 || owns(*newblack) ? 0 : white; /* updates white position after move */
  return !visited(*newblack, *newwhite); /* whether position already visited */
}

int ohasmove(int black, int white, int move, int *newblack, int *newwhite) /* see above: xhasmove() */
{
  move = 1 << move; 
  if ((black | white) & move || popcnt[white] == 3 || owns(black)) 
    return 0; 
  *newwhite = white | move; 
  *newblack = (*newwhite | black) == 15 || owns(*newwhite) ? 0 : black; 
  return !visited(*newblack, *newwhite); 
}

int xab(int n, int black, int white, int alpha, int beta, int passed) /* black alphabeta search */
{
  int i, s, newblack, newwhite;
  int oab(int, int, int, int, int, int); /* forward declaration for white ab-search */

  nodes[n]++; /* nodes visited at this depth */
  if (n < NSHOW)
    show(n, black, white, alpha, beta, passed); /* display position if within NSHOW depth */

  s = passed ? score(black, white) : oab(n + 1, black, white, alpha, beta, 1); 
  /* if opponent passed and we pass then calculate score, otw call oab() */
  /* whether score greater than alpha (update alpha if necessary)
     and whether alpha >= beta and whether CUT flag set */
  if (s > alpha && (alpha = s) >= beta && CUT)
    /* prune if current score > alpha and after update whether alpha still >= beta */
    return alpha;

  for (i = 0; i < NMOVES; i++) { /* loop over moves */
    if (xhasmove(black, white, i, &newblack, &newwhite)) { /* whether move valid */
      visit(newblack, newwhite); 
      s = oab(n + 1, newblack, newwhite, alpha, beta, 0); /* explore opponent response */
      unvisit(newblack, newwhite); 
      if (s > alpha && (alpha = s) >= beta && CUT)
        return alpha; /* same as above */
    }
  }

  /* search pass move last? move lines 91-98 here */

  return alpha;
}

int oab(int n, int black, int white, int alpha, int beta, int passed) /* see above xab() */
{
  int i, s, newblack, newwhite;

  nodes[n]++; 
  if (n < NSHOW)
    show(n, black, white, alpha, beta, passed); 

  s = passed ? score(black, white) : xab(n + 1, black, white, alpha, beta, 1); 
  if (s < beta && (beta = s) <= alpha && CUT)
    return beta; 

  for (i = 0; i < NMOVES; i++) { 
    if (ohasmove(black, white, i, &newblack, &newwhite)) { 
      visit(newblack, newwhite); 
      s = xab(n + 1, newblack, newwhite, alpha, beta, 0); 
      unvisit(newblack, newwhite); 
      if (s < beta && (beta = s) <= alpha && CUT)
        return beta; 
    }
  }

  /* search pass move last? move lines 122-125 here */

  return beta;
}

int main()
{
  int i, c, s;
  c = xab(0, 0, 0, -4, 4, 0); /* start alphabeta search from empty board */
  for (i = s = 0; nodes[i]; i++) {
    s += nodes[i]; /* total nodes visited */
    printf("%d: %d\n", i, nodes[i]); /* nodes visited at each depth */
  }
  printf("total: %d\nngames: %ld\nx wins by %d\n", s, ngames, c); /* total nodes visited and game stats */
  return 0;
}
