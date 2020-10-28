# GUI.py
import pygame
from Suduko import solve_board, valid, print_board
pygame.font.init()


class Grid:
    # board = [
    #     [7, 8, 0, 4, 0, 0, 1, 2, 0],
    #     [6, 0, 0, 0, 7, 5, 0, 0, 9],
    #     [0, 0, 0, 6, 0, 1, 0, 7, 8],
    #     [0, 0, 7, 0, 4, 0, 2, 6, 0],
    #     [0, 0, 1, 0, 5, 0, 9, 3, 0],
    #     [9, 0, 4, 0, 6, 0, 0, 0, 5],
    #     [0, 7, 0, 3, 0, 0, 0, 1, 2],
    #     [1, 2, 0, 0, 0, 7, 4, 0, 0],
    #     [0, 4, 9, 2, 0, 6, 0, 0, 7]
    # ]
    
    board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.boxes = [[Box(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        
    def clear_board(self):
        for i in range(self.rows):
             for j in range(self.cols):
                 self.boxes[i][j].value = 0
        self.update_model()
    
    def update_model(self):
        self.model = [[self.boxes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
        
    def assign(self,value,row,col):
        self.boxes[row][col].value = value
        

    def complete_solve(self):
        self.update_model()
        solve_board(self.model)
        print(self.model)
        print("test2")
        for i in range(self.rows):
             for j in range(self.cols):
                 self.assign(self.model[i][j], i, j)

        
    def draw(self, win):
        gap = self.width / 9
        for i in range(self.rows+1):
            if i%3==0 and i!=0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0,i*gap+60),(self.width,i*gap+60),thick)
            pygame.draw.line(win, (0,0,0), (i*gap,0+60),(i*gap,self.height+60),thick)
            
        for i in range(self.rows):
            for j in range(self.cols):
                    self.boxes[i][j].draw(win)
                
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].selected = False
        self.boxes[row][col].selected = True
        self.selected = (row,col)
        
    def click(self,pos):
        if pos[0] < self.width and pos[1]<self.height and pos[1] > 60:
            gap = self.width/9
            print( pos[1])
            x = pos[0] // gap
            y = (pos[1] -60) // gap
            print(int(x),int(y))
            return (int(y),int(x))
        else:
            return None
            
class Box:  
    def __init__(self,value,row,col,width,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    def draw(self,win):
        fnt = pygame.font.SysFont("comicsanc",40)
        gap = self.width/9
        x= self.col*gap
        y = self.row*gap
        
        text = fnt.render(str(self.value), 1, (128,0,0))
        if self.value != 0:
            win.blit (text,(x+(gap/2-text.get_width()/2), 60+y+(gap/2-text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win,(255,0,0),(x,y+60,gap,gap),3)
        
    def set(self,val):
        self.value = val

def redraw_window(win, board, solved):
    if not solved:
        win.fill((255,255,255))
        fnt = pygame.font.SysFont("comicsans", 30)
        text = fnt.render("Please Enter Starting Numbers:", 1, (0,0,0))
        win.blit(text, (0, 20))
        
        start = fnt.render("Solve:", 1, (0,0,255))
        win.blit(start, (460, 20))
        pygame.draw.rect(win,(0,0,255),(450,10,80,40),3)
        
        clear = fnt.render("Clear:", 1, (255,0,0))
        win.blit(clear, (360, 20))
        pygame.draw.rect(win,(255,0,0),(350,10,80,40),3)
        board.draw(win)
    if solved:
        win.fill((255,255,255))
        fnt = pygame.font.SysFont("comicsans", 30)
        text = fnt.render("Solved Grid:", 1, (0,0,0))
        win.blit(text, (0, 20))

        clear = fnt.render("Clear:", 1, (255,0,0))
        win.blit(clear, (360, 20))
        pygame.draw.rect(win,(255,0,0),(350,10,80,40),3)
        
        board.draw(win)
        


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 600)
    solved = False
    pause = False
    key = None
    clicked = None
  
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if solved == True:
                if not pause:
                    board.complete_solve()
                    board.select(0,0)
                    pause=True
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if pos[0] < 430 and pos[0] > 350 and pos[1] > 10 and pos[1] < 50:
                            board.clear_board()
                            solved = False
                            pause = False
                    

            else:
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if pos[0] < 430 and pos[0] > 350 and pos[1] > 10 and pos[1] < 50:
                            board.clear_board()
                    if pos[0] < 530 and pos[0] > 450 and pos[1] > 10 and pos[1] < 50:
                        solved = True
                        clicked = board.click(pos)
                    else:
                        clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0],clicked[1])    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        key = 1
                    if event.key == pygame.K_2:
                        key = 2
                    if event.key == pygame.K_3:
                        key = 3
                    if event.key == pygame.K_4:
                        key = 4
                    if event.key == pygame.K_5:
                        key = 5
                    if event.key == pygame.K_6:
                        key = 6
                    if event.key == pygame.K_7:
                        key = 7
                    if event.key == pygame.K_8:
                        key = 8
                    if event.key == pygame.K_9:
                        key = 9

                    if key != None and clicked != None:
                        board.assign(key, clicked[0],clicked[1])
        
        redraw_window(win, board, solved)
        pygame.display.update()


main()
pygame.quit()