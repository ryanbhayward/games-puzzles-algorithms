
# coding: utf-8

# In[1]:


from heapq import *
import time


# In[34]:


#open the file and read lines
def get_board_from_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    
    #could be improved using lambda
    lines = [x.replace(' \n ', '\n').replace(' \n', '\n').replace('\n ', '\n').replace('  ', ' ') for x in lines]

    #read the shape of the board
    height, width = lines[0][:-1].split(' ')
    height, width = int(height), int(width)
    board = []
    
    #fill the board with the integers discovered
    for i in range(1, height + 1):
        board.append([int(x) for x in lines[i][:-1].split(' ')])

    return Board(board)


# In[44]:


class Board:
    #We choose to store the puzzle as a matrix, however this is not the most efficient way to do it
    def __init__(self, board=[], empty=None, parent=None, g=0):
        self.empty = empty
        self.board = board
        self.parent = parent
        self.solution = None
        self.h = len(self.board)
        self.w = len(self.board[0])
        self.g = g
        self.stringfied = None
        
        if empty == None: self.find_empty()
    
    def __lt__(self, other):
        return self.count_inversions() < other.count_inversions()
    
    def __eq__(self, other):
        return type(self) == type(other) and self.board == other.board
    
    #Find the position where is the empty tile 0
    #returns an array [x,y]
    def find_empty(self):
        for i in range(len(self.board)):
            try:
                j = self.board[i].index(0)
                self.empty = [i, j]
                return [i, j]
            except:
                pass
    
    
    #returns the manhattan distance between the current board and the solution board
    #manhattan = |x2-x1|+|y2-y1|
    def manhattan(self):
        m_sum = 0
        h = len(self.board)
        w = len(self.board[0])
        
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    m_sum += abs(i - (self.board[i][j]-1) // h) + abs(j - (self.board[i][j]-1) % w)
                else:
                    m_sum += abs(i - (h-1)) + abs(j - (w-1))
                    
        return m_sum
    
    
    #gets the solution board
    def get_solution(self):
        if self.solution:
            return self.solution
        return self.create_solution()
    
    
    #creates the solution board
    def create_solution(self):
        if self.solution:
            return self.solution
        
        h = len(self.board)
        w = len(self.board[0])
        b = []
        l = []
        for i in range(1, h * w):
            l.append(i)
            if i % w == 0:
                b.append(l)
                l = []
        l.append(0)
        b.append(l)
        self.solution = Board(b)
        
        return self.solution
        
        
    #prints the board in a nice form
    def __str__(self):
        s = ''
        for i in self.board:
            s += str(i) + '\n'
        return s
    
    
    #transforms a board into an array.
    #e.g. [[1,2][3,0]] becomes [1,2,3,0]
    def arrayfy(self):
        s = []
        for i in self.board:
            for j in i:
                s.append(j)
        return s
    
    
    #returns the number of inversions present in the board
    #an inversion is when a>b but a appears before b
    #THIS CAN HAVE TIME O(nlogn) if implemented with mergesort, current is O(n^2)
    def count_inversions(self, board=None):
        if board == None: board = self.arrayfy()
        count = 0
        for i in range(len(board)):
            for j in range(i+1, len(board)):
                if board[i] != 0 and board[j] != 0 and board[i] > board[j]: count = count + 1
        return count
    
    
    #puzzle is solved when there is 0 inversions and the empty square is in the right-down corner
    def is_solved(self):
        return self.count_inversions() == 0 and self.empty == [self.h-1, self.w-1]
    
    
    #Verifies if the puzzle is solvable
    def is_solvable(self):
        self.find_empty()
        flat_board = self.arrayfy()
        grid_odd = self.w % 2 != 0
        inversions_even = self.count_inversions(flat_board) % 2 == 0
        return (grid_odd and inversions_even) or (not grid_odd and ((((self.h - self.empty[0]) % 2) != 0) == inversions_even))
    
    
    #transforms a board into a string.
    #e.g. [[1,2][3,0]] becomes '1230'
    def stringify(self):
        if self.stringfied != None: return self.stringfied
        s = ''
        for i in self.board:
            for j in i:
                s += str(j)
        return s
    
    
    #generates the valid moves for the game.
    #the move have shape [x,y] where 0 will move to
    def get_valid_moves(self):
        if self.empty == None:
            self.empty = self.find_empty()

        moves = []

        if self.empty[0] + 1 < self.h:
            moves.append([self.empty[0] + 1, self.empty[1]])
        if self.empty[1] + 1 < self.w:
            moves.append([self.empty[0], self.empty[1] + 1])
        if self.empty[0] - 1 >= 0:
            moves.append([self.empty[0] - 1, self.empty[1]])
        if self.empty[1] - 1 >= 0:
            moves.append([self.empty[0], self.empty[1] - 1])

        return moves
    
    
    #creates a deep copy of the board, simulates the move and returns the new board
    #parameter move is an array [x,y] where the 0 must move to.
    #if an invalid move is given returns error
    def simulate_move(self, move):
        if move not in self.get_valid_moves(): return -1
        new_board = []
        for i in self.board:
            k = []
            for h in i:
                k.append(h)
            new_board.append(k)
        #print(move)
        new_board[self.empty[0]][self.empty[1]], new_board[move[0]][move[1]] = new_board[move[0]][move[1]], new_board[self.empty[0]][self.empty[1]]
        child = Board(new_board, move, self, self.g + 1)
        return child


# In[49]:


#shows the moves done to solve the puzzle
def rebuild_path(state):
    path = []
    while state.parent != None:
        path.insert(0, state)
        state = state.parent
    path.insert(0, state)
    print("Number of steps to solve: {}".format(len(path) - 1))
    print('Solution')
    for i in path:
        print(i)
        print()

        
#A BFS search that solves the puzzle        
def BFS(b):
    print("BFS")
    start_time = time.time()
    queue = [b]
    bib = {}
    bib[b.stringify()] = b
    print(queue[0].stringify())
    while len(queue) > 0 and not queue[0].is_solved():
        current_state = queue.pop(0)
        moves = current_state.get_valid_moves()
        for i in moves:
            m = current_state.simulate_move(i)
            if not m.stringify() in bib.keys():
                queue.append(m)
                bib[m.stringify()] = m
    try:
        print("Number of explored states: {}".format(len(bib)))
        elapsed_time = time.time() - start_time
        print("Execution time {}".format(elapsed_time))
        rebuild_path(queue[0])
    except:
        elapsed_time = time.time() - start_time
        print("Execution time {}".format(elapsed_time))
        print('No Solution')


# In[38]:


#An A* search that solves the puzzle
#g(n) = 1, h(n) = #inversions
def a_star(b):
    print("A*")
    start_time = time.time()
    heap = [(-1, b)]
    bib = {}
    bib[b.stringify()] = b
    
    while len(heap) > 0:
        current_state = heappop(heap)[1]
        
        if current_state.is_solved():
            print("Number of explored states: {}".format(len(bib)))
            elapsed_time = time.time() - start_time
            print("Execution time {}".format(elapsed_time))
            return rebuild_path(current_state)
        
        moves = current_state.get_valid_moves()
        for i in moves:
            m = current_state.simulate_move(i)
            if not m.stringify() in bib.keys():
                heappush(heap, (m.g + m.manhattan(), m))
                bib[m.stringify()] = m
    elapsed_time = time.time() - start_time
    print("Execution time {}".format(elapsed_time))
    print('No Solution')


# In[37]:


#Iterative Deepening algorithm
#g(n) = 1, h(n) = inversions
def ida_star(root):
    print("IDA*")
    start_time = time.time()
    bound = root.count_inversions()
    path = [root]
    solved = False
    while not solved:
        t = search(path, 0, bound)
        if type(t) == Board:
            solved = True
            elapsed_time = time.time() - start_time
            print("Execution time {}".format(elapsed_time))
            rebuild_path(t)
            return t
        elif t == 9999: return None
        bound = t

def search(path, g, bound):
    node = path[-1]
    f = g + node.count_inversions()
    
    if f > bound: return f
    if node.is_solved():
        return node
    
    min_cost = 9999
    #Generates all successors and insert them in a heap (max 3)
    #In the PhD thesis he does arbitrarily, heap is my personal choice.
    heap = []
    for i in node.get_valid_moves():
        m = node.simulate_move(i)
        if m not in path:
            heappush(heap, (m.g + m.count_inversions(), m))
    
    #Remove the sucessors from a heap and explore them according to min(f(n)) policy
    while len(heap) > 0:
        path.append(heappop(heap)[1])
        t = search(path, g + 1, bound)
        if type(t) == Board: return t
        elif t < min_cost: min_cost = t
        path.pop()
    return min_cost


# In[64]:


b = get_board_from_file('st.25.0.txt')
print(b)

print("Is solvable?", b.is_solvable())
if (b.is_solvable()):
    #ida_star(b)
    #BFS(b)
    a_star(b)

