import sqlite3
import pygame
import sys
import random
from pygame.locals import *


#ZETONY : 
def is_red(n):
    colorRed = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)
    if colorRed.count(n) == 1:
        return True
    
    return False 

def is_odd(n):
    if n % 2 == 1:
        return True
    return False

def check_spin(bets, number, player):

    winer_rates = {'number': 36, 'red': 2 , 'black': 2, 'even': 2, 'odd': 2, \
                   '1st12': 3 , '2nd12': 3 ,'3rd12': 3 }
    win = 0;
    for x in bets.keys():
        if type(x) is int and x == number:
            player.win(winer_rates['number'] * bets[x])
            win+=1
            
        elif x == 'red' and  is_red(number) :
            player.win(winer_rates['red'] * bets[x])
            win+=1
            
        elif x == 'black' and not is_red(number):
            player.win(winer_rates['black'] * bets[x])
            win+=1
            
        elif x == 'odd' and is_odd(number):
            player.win(winer_rates['odd'] * bets[x])
            win+=1
            
        elif x == 'even' and not is_odd(number):
            player.win(winer_rates['even'] * bets[x])
            win+=1
            
        elif x == '1st12' and number <= 12:
            player.win(winer_rates['1st12'] * bets[x])
            win+=1
            
        elif x == '2nd12' and number <= 24 and number > 12:
            player.win(winer_rates['2nd12'] * bets[x])
            win+=1
            
        elif x == '3rd12' and number <= 36 and number > 24:
            player.win(winer_rates['3rd12'] * bets[x])
            win+=1
    return win

def set_font_pos(token_value,x,y):
    if token_value == 1 or token_value == 5:
        return (x-6,y-13)
    elif(token_value == 10):
        return(x-14, y-13)
    elif(token_value == 25 or token_value == 50):
        return(x-13, y-13)
    else:
        return(x-20,y-13)
    
def spin_circle():
    return int(random.random() * 36 + 1)

def draw_random_number(screen, number):
    font = pygame.font.SysFont('Arial', 100) 
    screen.blit(font.render(str(number), True, (250,250,250)),\
                                         (0+20,315+50))
def draw_token(screen,color,pos, value):
    #rysowanie zetonu o okreslonym kolorze, wartosci
    font = pygame.font.SysFont('Arial', 20)
    font.set_bold(True)
    x,y = pos

    pygame.draw.circle(screen, color, pos, 25, 0)
    pygame.draw.circle(screen, (255,250,250), pos, 24, 0)
    pygame.draw.circle(screen, color, pos, 20, 0)
   
    pygame.draw.circle(screen, color, (x+21,y), 4, 0)
    pygame.draw.circle(screen, color, (x-21,y), 4, 0)
    pygame.draw.circle(screen, color, (x,y+21), 4, 0)
    pygame.draw.circle(screen, color, (x,y-21), 4, 0)

    pygame.draw.circle(screen, color, (x+15,y-17), 4, 0)
    pygame.draw.circle(screen, color, (x-15,y+17), 4, 0)
    pygame.draw.circle(screen, color, (x-15,y-17), 4, 0)
    pygame.draw.circle(screen, color, (x+15,y+17), 4, 0) 
    screen.blit(font.render(str(value), True, (250,250,250)), set_font_pos(value,x,y))
    
class Table(object):
    #wyrysowanie stolu
    def __init__(self, player):
        self.screen = pygame.display.set_mode((900, 550), DOUBLEBUF) #wyrysowanie okna
        pygame.display.set_caption('Ruletka')
        self.screen.fill((139,131,120))                                 #wypelnienie okna 
        self.font = pygame.font.SysFont('Arial', 30)                    #czcionka do stolu
        self.fontmin = pygame.font.SysFont('Arial', 15)
        self.fontmin.set_bold(True)

        self.random_number = 0
        
        self.token_x = 600
        self.token_y = 350
        
        self.table_x = 280
        self.table_y = 60

        self.zero_x = 280
        self.zero_y = 209
        
        self.even_x = 280
        self.even_y = 10

        self.twelve_x = 280
        self.twelve_y = 209

        self.spin_x = 0
        self.spin_y = 315

        self.press_spin = False
        self.grabing_token = False

        self.tokens = [((255,0,0), 100), ((65,105,225), 50), ((173,255,47), 25),
                  ((255,165,0), 10), ((255,20,147), 5), ((200,200,0), 1)] # (color, value)

        self.token_color = None
        self.token_value = None

        self.bets = {}
        self.player = player
        
    def draw_table(self):

        self.screen.fill((87,166,57))
        pygame.draw.rect(self.screen, (34,139,34), (0,0,900,300), 0 ) # 0  caly zamalowany
        pygame.draw.rect(self.screen, (118,60,40), (0,0,900,300), 15 )   

        x1 = 110
        y1 = 150
                        #kolo do gry
        pygame.draw.circle(self.screen, (139,69,19), (x1,y1), 100, 0)
        pygame.draw.circle(self.screen, (205,133,63), (x1,y1), 90, 0)
        pygame.draw.circle(self.screen, (255,255,255), (x1,y1), 73, 0)
        pygame.draw.circle(self.screen, (205,133,63), (x1,y1), 65, 0)

        pygame.draw.circle(self.screen, (255,0,0), (x1,y1+70), 10, 0)
        pygame.draw.circle(self.screen, (255,0,0), (x1-70,y1), 10, 0) 
        pygame.draw.circle(self.screen, (255,0,0), (x1+70,y1), 10, 0)
        pygame.draw.circle(self.screen, (255,0,0), (x1,y1-70), 10, 0)

        pygame.draw.polygon(self.screen, (255,0,0), [[x1+5, y1], [x1, y1-70], [x1-5, y1]], 0)
        pygame.draw.polygon(self.screen, (255,0,0), [[x1+5, y1], [x1, y1+70], [x1-5, y1]], 0)
        pygame.draw.polygon(self.screen, (255,0,0), [[x1, y1+5], [x1-70, y1], [x1, y1-5]], 0)
        pygame.draw.polygon(self.screen, (255,0,0), [[x1, y1+5], [x1+70, y1], [x1, y1-5]], 0)
                                                                        #wyrysowanie prostokatow:
        a = self.table_x
        b = self.table_y + 100
        
        number = 1;
        for y in range(1,4):
            for x in range(1,13):
                pygame.draw.rect(self.screen, (255,255,255), (a,b,50,50 ), 1 )
                if is_red(number) == True:
                    pygame.draw.circle(self.screen, (255,0,0), (a+25,b+25), 23, 0)
                else:
                    pygame.draw.circle(self.screen, (0,0,0), (a+25,b+25), 23, 0)
                if number > 9 and number <20:
                    self.screen.blit(self.font.render(str(number), True, (250,250,250)), (a+8, b+8))
                elif number >= 20:
                    self.screen.blit(self.font.render(str(number), True, (250,250,250)), (a+9, b+8))
                else:
                     self.screen.blit(self.font.render(str(number), True, (250,250,250)), (a+15, b+8))
                a+=50
                number+=3
            a=280
            number= y+1
            b=160-y*50
            
        a = self.zero_x #280
        b = self.zero_y #200
        
        #wyrysowanie zera:
        pygame.draw.lines(self.screen, (250,250,250), False, [[a, b], \
            [a-25, b],[a-45,b-75],[a-25,b-75*2 + 1],[a-0.5,b-75*2 + 1]], 1)
                                                                                          
        self.screen.blit(self.font.render('0', True, (250,250,250)), (a-25, b-90))

        #wyrysowanie EVEN, czerw, czarne, ODD
        pygame.draw.rect(self.screen, (255,255,255), (self.even_x,self.even_y+1,3*50,50 ), 1 )        
        self.screen.blit(self.font.render('EVEN', True, (250,250,250)), (self.even_x + 35, self.even_y+10))

        pygame.draw.rect(self.screen, (255,255,255), (self.even_x+3*50,self.even_y+1,3*50,50 ), 1 )        
        pygame.draw.circle(self.screen, (255,0,0), (self.even_x+3*50+70,self.even_y+1+25), 15, 0)
        

        pygame.draw.rect(self.screen, (255,255,255), (self.even_x+6*50,self.even_y+1,3*50, 50 ), 1 )        
        pygame.draw.circle(self.screen, (0,0,0), (self.even_x+6*50+70,self.even_y+1+25), 15, 0)

        pygame.draw.rect(self.screen, (255,255,255), (self.even_x+9*50,self.even_y+1,3*50,50 ), 1 )        
        self.screen.blit(self.font.render('ODD', True, (250,250,250)), (self.even_x +9*50+ 35, self.even_y+10))

        
                                                                            #wyrysowac 12+
        a = self.twelve_x
        b = self.twelve_y
        pygame.draw.rect(self.screen, (255,255,255), (a,b,4*50, 50 ), 1 )
        self.screen.blit(self.font.render('1st 12', True, (250,250,250)), (a+50, b+2))
        pygame.draw.rect(self.screen, (255,255,255), (a+4*50,b,4*50, 50 ), 1 )
        self.screen.blit(self.font.render('2nd 12', True, (250,250,250)), (a+80*3+20, b+2))
        pygame.draw.rect(self.screen, (255,255,255), (a+8*50,b,4*50,50 ), 1 )
        self.screen.blit(self.font.render('3rd 12', True, (250,250,250)), (a+80*5+50, b+2))
                                                                            #podstawka na zetony
        pygame.draw.rect(self.screen, ( 100,100,90), (560,318, 260+70, 70 ), 0 )
        pygame.draw.rect(self.screen,(118,60,40), (560,318, 260+70, 70 ), 5 )

        token_x = self.token_x
        token_y = self.token_y

                                                                 #zetony :
        draw_token(self.screen, self.tokens[0][0], (token_x, token_y), self.tokens[0][1]) #czerwony zeton 100
        draw_token(self.screen, self.tokens[1][0], (token_x+50, token_y), self.tokens[1][1]) #zielony 50
        draw_token(self.screen, self.tokens[2][0], (token_x+100, token_y), self.tokens[2][1]) #niebieski 25
        draw_token(self.screen, self.tokens[3][0], (token_x+150, token_y), self.tokens[3][1]) #pomaranczowy 10
        draw_token(self.screen, self.tokens[4][0], (token_x+200, token_y), self.tokens[4][1]) #rozowy 5
        draw_token(self.screen, self.tokens[5][0], (token_x+250, token_y), self.tokens[5][1]) #zolty 1

        #przycisk losuj:
        a = 0
        b = 315 
        pygame.draw.rect(self.screen, (90,90,90), (a,b,150,250), 0 )
        pygame.draw.rect(self.screen, (204,6,5), (a+1,b,150,50), 0 )
        
        pygame.draw.rect(self.screen, (118,60,40), (a,b,150,250), 4 )
        pygame.draw.rect(self.screen, (118,60,40), (a,b,150,50), 4 )
        self.screen.blit(self.font.render('SPIN', True, (250,210,1)), (a+35, b+7))        
        
        if self.grabing_token:
            draw_token(self.screen, self.token_color, pygame.mouse.get_pos(), self.token_value)

        if self.random_number :
            draw_random_number(self.screen, self.random_number)
            if self.flag == True:
                self.screen.blit(self.font.render('WIN !', True, (250,0,1)), (a+35, b+150+20))
            else:
                self.screen.blit(self.font.render('Try Again!', True, (250,0,0)), (a+10, b+150+20))
        

        
#panel user
    def draw_user_panel(self):
        a = 560
        b = 318+80
        font = pygame.font.SysFont("comicsansms", 30 )
        pygame.draw.rect(self.screen, ( 100,100,90), (a,b, 260+70, 70*2 ), 0 )
        pygame.draw.rect(self.screen,(118,60,40), (a,b, 260+70, 70*2), 5 )

        self.screen.blit(font.render('USER: ', True, (250,210,1)), (a+10, b+10))
        s = self.player.nick
        self.screen.blit(font.render(s, True, (250,0,1)), (a+80, b+10))
        
        self.screen.blit(font.render('BALANCE AMOUNT:', True, (250,210,1)), (a+10, b+10+30))
        m = self.player.money
        font2 = pygame.font.SysFont('Arial', 40)
        self.screen.blit(font2.render(str(m)+" $", True, (250,0,1)), (a+20, b+80))

#bet
        pygame.draw.rect(self.screen,(118,60,40), (190,b-80, 260+70, 70*2+80), 5 )
        self.screen.blit(font.render('...GAME...', True, (250,210,1)), (190+120, b-70))

        #draw bet
        #postawiono na :
        self.screen.blit(font.render('Bet:', True, (250,210,1)), (190+10, b-50))
        k=b-30
        for x in self.bets.keys():
               self.screen.blit(font.render( str(x) + " : " + str(self.bets[x] ) , True, (250,210,1)), (190+10, k))
               k+=20;   

         
    def get_key_from_click_position(self, pos_x, pos_y):
        if self.table_x < pos_x and self.table_y < pos_y and \
                    self.table_x + 50*12 > pos_x and self.table_y + 150 > pos_y :
            value = 3*(pos_x - self.table_x)/50 + 2 - (pos_y - self.table_y)/50
            return value
    
        elif(self.zero_x > pos_x and self.zero_x-25 < pos_x and \
                self.zero_y > pos_y and self.zero_y-75*2 <  pos_y):
            return 0
        
        elif(self.even_x < pos_x and self.even_x + 3*50 > pos_x and \
                self.even_y < pos_y and self.even_y+50 > pos_y):
            return 'even'
        
        elif(self.even_x+3*50 < pos_x and self.even_x + 6*50 > pos_x and \
                self.even_y < pos_y and self.even_y+50 > pos_y):
            return 'red'
        
        elif(self.even_x+6*50 < pos_x and self.even_x + 9*50 > pos_x and\
                self.even_y < pos_y and self.even_y+50 > pos_y):
            return 'black'
        
        elif(self.even_x+9*50 < pos_x and self.even_x + 12*50 > pos_x and \
                self.even_y < pos_y and self.even_y+50 > pos_y):
            return 'odd'
        
        elif(self.twelve_x < pos_x and self.twelve_x + 4*50 > pos_x and \
                self.twelve_y < pos_y and self.twelve_y+50 > pos_y):
            return '1st12'

        elif(self.twelve_x+4*50 < pos_x and self.twelve_x + 8*50 > pos_x and\
                self.twelve_y < pos_y and self.twelve_y+50 > pos_y):
            return '2nd12'

        elif(self.twelve_x+8*50 < pos_x and self.twelve_x + 12*50 > pos_x and\
                         self.twelve_y < pos_y and self.twelve_y+50 > pos_y):
            return '3rd12'
        else:
            return None
    
    def handle_events(self,events):
        for event in events:
            if  event.type == pygame.MOUSEBUTTONUP:
                (pos_x, pos_y) = pygame.mouse.get_pos()
                
                if not self.grabing_token:
                    if pos_y >= self.token_y - 25 and pos_y <= self.token_y + 25 \
                       and pos_x >= self.token_x - 25 and pos_x <= self.token_x + 275:
                        # klinkieto w tokeny
                        self.grabing_token = True

                        (self.token_color, self.token_value) = self.tokens[(pos_x - self.token_x + 25) / 50]

                        print self.token_color
                        print self.token_value

                        #kliknieto zakrec spin
                    elif (self.spin_x < pos_x and self.spin_x + 150 > pos_x and \
                                  self.spin_y < pos_y and self.spin_y+50 > pos_y):
                        self.random_number = spin_circle()
                        print self.random_number
                       
                        mon = check_spin(self.bets, self.random_number, self.player)
                        self.player.db_con.update((self.player.money,self.player.nick,))
                        if mon == 0 :
                            self.flag = False
                        else:
                            self.flag = True
                        print self.player.money
                        self.bets.clear()           
                        
                else:
                    self.grabing_token = False
                    value = self.get_key_from_click_position(pos_x, pos_y)
                    
                    try:
                        if self.player.bet_money(self.token_value):
                            self.bets[value] += self.token_value
                    except KeyError:
                        self.bets[value] = self.token_value 
                        print self.bets[value] 
                        
            elif event.type == pygame.QUIT:
                self.player.db_con.update((self.player.money,self.player.nick,))
                pygame.quit()
                sys.exit(0)

class ConnectBd(object):

    def __init__(self):
        try:
            self.connection = sqlite3.connect('players.db')
            self.cur = self.connection.cursor()  # define cursor'
            self.cur.execute('CREATE TABLE IF NOT EXISTS players( id INTEGER PRIMARY KEY AUTOINCREMENT, nick text, money real );')


        except sqlite3.DatabaseError, e:
            print 'Error %s' % e  #Can not connect with Database;
            self.connection.close()
            sys.exit(1)

    def insert(self, data): # odrazu mozna krotke przeslac
        query = "INSERT INTO players (nick, money) VALUES (?,?);"

        self.cur.execute(query, data)
        self.connection.commit()

    def update(self, data):
        query = "UPDATE players SET money = ? WHERE nick = ?;"

        self.cur.execute(query , data)
        self.connection.commit()

    def write(self):
        self.cur.execute('SELECT * FROM players')
        for ver in self.cur:
            print ver
            
    def find_user(self, nick):
        query = "SELECT * FROM players WHERE nick = ?;"
        
        self.cur.execute("SELECT * FROM players WHERE nick = ?;" , (nick,))
        ver = self.cur.fetchone()
        
        return ver

    def __del__(self):
        if self.connection:
            self.connection.close()
            print 'connection destroy'


class Player(object):
    
    def __init__(self, player_nick, player_money=1000):
        self.db_con = ConnectBd()
        vers = self.db_con.find_user(player_nick)
        if vers == None:
           self.db_con.insert((player_nick, player_money))
           vers = self.db_con.find_user(player_nick)
           print vers
           (self.id, self._nick, self._money) = vers
           
        else:
            (self.id, self._nick, self._money) = vers

    @property
    def nick(self):
        return self._nick
    
    @property
    def money(self):
        return self._money

    def bet_money(self,value):
        if(self._money < value ):
            return False
        self._money -= value
        return True

    def win(self, value):
        self._money += value
    
    def __del__(self):
        class_name = self.__class__.__name__
        print class_name, "destroyed"


def main(user_nick):
    pygame.init()
    pygame.font.init()
    
    player = Player(user_nick)
    gameTable = Table(player)

    while True: #MAIN LOOP
        gameTable.handle_events(pygame.event.get())
        gameTable.draw_table()
        gameTable.draw_user_panel()
        pygame.display.flip()
    


