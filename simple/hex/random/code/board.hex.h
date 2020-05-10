// NxN board
#define N 7
#define Np1 (N+1)
#define Np2 (N+2)
#define Np3 (N+3)
#define Np2sq (Np2*Np2)
#define Np2sqm2 (Np2sq-2)
#define Nsq (N*N)
#define K ((Nsq+1)/2) //  number black (2nd player) stones
//#define K ((Nsq-1)/2)  // number white (1st player) stones
#define EMPTY 0
#define BLACK 1
#define WHITE 2
//#define GUARD 2 // guard positions are ignored
//#define TOP 3
//#define BOTTOM 4
//#define LEFT 5
//#define RIGHT 6
#define FIRST_TOP 1  // first cell in unguarded top row
#define LAST_BTM Np2sqm2 // last cell in unguarded bottom row

#define fatten(j) (Np3+(j)+2*((j)/N))  // replace with fat-board index
#define unfatten(j) (-1+j%Np2+N*(-1+j/Np2))  // replace with fat-board index
#define myrand(n) (rand()%(n))     // pseudo-uniform-random in [0.. n-1]

extern const int Offsets[6];

extern void init_locations(int L[]) ;

extern void shuffle(int X[Np2sq]) ;

extern void fatShuffle(int X[Np2sq]) ;

extern void showAsFatBoard(int X[]) ;

extern void showAsBoard(int X[]) ;

extern void showUnguarded(int X[]) ;

extern void showForGnuplot(int X[], int s) ;

extern void dfs(int M[], int fatV[], int v) ;

extern int dfsConnect(int fatV[]) ;

extern void init_guard_brd(int fV[Np2sq]) ;

extern void put_black_stones(int fV[Np2sq]) ;

extern int myFind(int Parents[Np2sq], int x) ;

extern void myUnion(int Parents[Np2sq], int x, int y) ;

extern int UFConnect(int fatV[], int Par[Np2sq]) ;

extern void init_UF_guard_brd(int fV[Np2sq], int P[Np2sq]) ;
