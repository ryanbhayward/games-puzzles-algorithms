/* copy of John Tromp's program: comments added by Jake Hennig 2024*/
/* C program to solve 2x2 go with area rules and positional superko */
/* note that suicide is not possible in this case */
/* trying moves before passes slows search dramatically */

#include <stdio.h>
#define NSHOW 4  /* the max depth that output of searches is displayed */
#define NMOVES 4 /* # of possible moves player can make */
#define CUT 1    /* CUT set to 1 allows for pruneing otherwise if set to 0 it just uses minimax */

char h[256];    /* bitmap of positions in game history */
int nodes[99];  /* number of nodes visited at each depth */
long ngames;    /* total # of games played */

void show(int n, int black, int white, int alpha, int beta, int passed)
  /* print 2-line ASCII representation of position */
{
  int i;
  printf("%d (%d,%d)%s\n", n, alpha, beta, passed ? " pass" : ""); /* prints current depth, alpha, beta, and if player passed turn */
  for (i = 0; i < 4; i++) {
    printf(" %c", ".XO#"[(black >> i & 1) + 2 * (white >> i & 1)]); /* prints the board state (X - black, O - white) */
    if (i & 1)
      putchar('\n'); /* place new line after every two characters - 2x2 board */
  }
} /* 1000 top-left, 0100 top-right, 0010 bottom-left, 0001 bottom-right*/

void visit(int black, int white)
{
  h[black + 16 * white] = 1; /* marks position as visited in game history bitmap */
}

void unvisit(int black, int white)
{
  h[black + 16 * white] = 0; /* marks position as unvisited in game histroy bitmap */
}

int visited(int black, int white)
{
  return h[black + 16 * white]; /* checks if position is already visited */
}

int owns(int bb)
{
  return bb == (1 | 8) || bb == (2 | 4); /* checks if one player has both corners of the board (control over it) */
}

int popcnt[16] = {0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4}; /* number of 1 bits in the binary representation of numbers from 0 to 15 */
/* 0000, 0001, 0010, 0011, 0100, 0101... 1110, 1111 */
/* used to count stones of each player */

int score(int black, int white)
{
  ngames++; /* counts number of games played */
  if (black == 0)
    return white ? -4 : 0; /* black has no stones, white wins (-4), unless white also has no pieces left then it's a draw (0) */
  if (white == 0)
    return 4; /* white has no pieces left, black wins (+4) */
  else
    return popcnt[black] - popcnt[white]; /* calculates score based on the number of pieces each player has */
}

int xhasmove(int black, int white, int move, int *newblack, int *newwhite) /* checks if black has a valid move */
{
  move = 1 << move; /* get binary representation of the move */
  /* 
   Check if the move position is already occupied by black or white, if black has
   already placed three stones (that's the max), and if white owns the entire board.
  */
  if ((black | white) & move || popcnt[black] == 3 || owns(white)) /* checks if move is legal for black */
    return 0; /* move impossible */
  *newblack = black | move; /* updates black's position after move */
  *newwhite = (*newblack | white) == 15 || owns(*newblack) ? 0 : white; /* updates white's position after move */
  return !visited(*newblack, *newwhite); /* checks if new position has been visited before */
}

int ohasmove(int black, int white, int move, int *newblack, int *newwhite) /* checks if white has a valid move */
{
  move = 1 << move; /* get binary representation of the move */
  /* 
   Check if the move position is already occupied by black or white, if white has
   already placed three stones (that's the max), and if black owns the entire board.
  */
  if ((black | white) & move || popcnt[white] == 3 || owns(black)) /* checks if move is legal for white */
    return 0; /* move impossible */
  *newwhite = white | move; /* updates white's position after move */
  *newblack = (*newwhite | black) == 15 || owns(*newwhite) ? 0 : black; /* updates black's position after move */
  return !visited(*newblack, *newwhite); /* checks if new position has been visited before */
}

int xab(int n, int black, int white, int alpha, int beta, int passed) /* alpha-beta search for black's turns */
{
  int i, s, newblack, newwhite;
  int oab(int, int, int, int, int, int); /* forward declaration of the function for white's turns */

  nodes[n]++; /* counts nodes visited at this depth */
  if (n < NSHOW)
    show(n, black, white, alpha, beta, passed); /* displays board state if within NSHOW depth */

  s = passed ? score(black, white) : oab(n + 1, black, white, alpha, beta, 1); /* calculates score or explores further for black's turn */
  /* check if score is greater than alpha (updating alpha if necessary),
  and if alpha is >= to beta, and if CUT flag is set */
  if (s > alpha && (alpha = s) >= beta && CUT)
    /* prune if current score (s) is > than alpha, and after updating alpha it's still >= to beta */
    return alpha;

  for (i = 0; i < NMOVES; i++) { /* loop through possible moves */
    if (xhasmove(black, white, i, &newblack, &newwhite)) { /* checks if the move is possible */
      visit(newblack, newwhite); /* visits the new position */
      s = oab(n + 1, newblack, newwhite, alpha, beta, 0); /* explores opponent's response */
      unvisit(newblack, newwhite); /* unvisit the new position */
      if (s > alpha && (alpha = s) >= beta && CUT)
        return alpha; /* prune if current score (s) is > than alpha, and after updating alpha it's still >= to beta */
    }
  }

  return alpha;
}

int oab(int n, int black, int white, int alpha, int beta, int passed) /* alpha-beta search for white's turns */
{
  int i, s, newblack, newwhite;

  nodes[n]++; /* counts nodes visited at this depth */
  if (n < NSHOW)
    show(n, black, white, alpha, beta, passed); /* displays board state if within NSHOW depth */

  s = passed ? score(black, white) : xab(n + 1, black, white, alpha, beta, 1); /* calculates score or explores further for white's turn */
  if (s < beta && (beta = s) <= alpha && CUT)
    return beta; /* prune if current score (s) is < than beta, and after updating beta it's still <= to alpha */

  for (i = 0; i < NMOVES; i++) { /* loop through possible moves */
    if (ohasmove(black, white, i, &newblack, &newwhite)) { /* checks if the move is possible */
      visit(newblack, newwhite); /* visits the new position */
      s = xab(n + 1, newblack, newwhite, alpha, beta, 0); /* explores opponent's response */
      unvisit(newblack, newwhite); /* unvisit the new position */
      if (s < beta && (beta = s) <= alpha && CUT)
        return beta; /* prune if current score (s) is < than beta, and after updating beta, it's still <= to alpha */
    }
  }

  return beta;
}

int main()
{
  int i, c, s;
  c = xab(0, 0, 0, -4, 4, 0); /* starts the alpha-beta search from the initial position */
  for (i = s = 0; nodes[i]; i++) {
    s += nodes[i]; /* counts total nodes visited */
    printf("%d: %d\n", i, nodes[i]); /* prints nodes visited at each depth */
  }
  printf("total: %d\nngames: %ld\nx wins by %d\n", s, ngames, c); /* prints total nodes visited and game stats */
  return 0;
}
