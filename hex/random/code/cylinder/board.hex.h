// RxN board
#define N 5  // width of each row
#define R 10  // number of rows
#define Np1 (N+1)
#define Np2 (N+2)
#define Np3 (N+3)
#define NR (N*R)
#define Np2Rp2 (Np2*(R+2))
#define P2moves (NR/2) //  max number 2nd player moves
#define EMPTY 0
#define BLACK 1
#define WHITE 2
#define FIRST_TOP 1  // first cell in unguarded top row
#define LAST_BTM (Np2Rp2-2) // last cell in unguarded bottom row

#define fatten(j) (Np3+(j)+2*((j)/N))  // replace with fat-board index
#define unfatten(j) (-1+j%Np2+N*(-1+j/Np2))  // replace with fat-board index
#define myrand(n) (rand()%(n))     // pseudo-uniform-random in [0.. n-1]

extern const int Offsets[6];
extern const int Offsets1[6];  // cylindrical board, col 0
extern const int Offsetsn[6];  // cylindrical board, col n-1

extern void init_locations(int L[]) ;

extern void shuffle(int X[Np2Rp2]) ;

extern void fatShuffle(int X[Np2Rp2]) ;

extern void showAsFatBoard(int X[]) ;

extern void showUnguarded(int X[]) ;

extern void showForGnuplot(int X[], int s) ;

//extern void dfs(int M[], int fatV[], int v) ;

//extern int dfsConnect(int fatV[]) ;

extern void init_guard_brd(int fV[Np2Rp2]) ;

extern void put_black_stones(int fV[Np2Rp2]) ;

extern int myFind(int Parents[Np2Rp2], int x) ;

extern void myUnion(int Parents[Np2Rp2], int x, int y) ;

//extern int UFConnect(int fatV[], int Par[Np2Rp2]) ;

extern void init_UF_guard_brd(int fV[Np2Rp2], int P[Np2Rp2]) ;
