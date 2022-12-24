import pygame as pg

pg.init()

font = pg.font.SysFont('arial', 40)

pg.mixer.init()

def checkB(pos, posB,size):
    return True if pos[0]>posB[0] and pos[0]<posB[0]+size[0] and pos[1]>posB[1] and pos[1]<posB[1]+size[1] else False

def min(ns):
    mn = ns[0]
    for _ in ns:
        if mn > _:
            mn = _

def max(ns):
    mn = ns[0]
    for _ in ns:
        if mn < _:
            mn = _


class TextBox():
    def __init__(self,name,pos,size,napr,text,maxlen,n,font = None):
        self.name = name
        self.pos = pos
        self.size = size
        self.pos1 = (0,0)
        self.size1 = (0,0)
        self.napr = napr
        self.text = text
        self.maxlen = maxlen
        self.defa = n
        self.x1 = 0
        self.x2 = 0
        self.inFocus = False
        self.font = pg.font.SysFont('arial', size[1]-50)
        self.rtx = ''
        self.sdpos=(0,0)
        if font != None:
            self.font = font
    
    def update(self,e):
        if e.type==pg.MOUSEBUTTONDOWN:
            p = e.pos
            p = (p[0]-self.sdpos[0],p[1]-self.sdpos[1])
            if checkB(p,self.pos1,self.size1):
                self.inFocus = True
                pg.key.start_text_input()
        elif e.type == pg.KEYDOWN:
            if self.inFocus:
                if e.key == pg.K_RETURN:
                    self.defa(self.text)
                    self.text = ''
                    pg.key.stop_text_input()
                    self.inFocus = False
                elif e.key == pg.K_DELETE:
                    self.text = self.text[:len(self.text)-1]
                else:
                    self.text+=e.unicode
    
    def render(self,surf):
        self.rtx = self.text if self.text != '' else self.name
        self.x1 = 0
        if self.napr == 'right':
            self.x2 = len(self.rtx)
            lentx = self.font.render(self.rtx,1,(255,255,255)).get_rect()[2]
            self.pos1 = self.pos
            if lentx < self.size[0]:
                self.size1 = self.size
            elif lentx > self.maxlen:
                self.size1 = (self.maxlen,self.size[1])
                while self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2] > self.maxlen-30:
                    self.x1 += 1
            else:
                self.size1 = (self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2]+40, self.size[1])
                
        else:
            lentx = self.font.render(self.rtx,1,(255,255,255)).get_rect()[2]
            self.x2 = len(self.rtx)
            if lentx < self.size[0]:
                self.size1 = self.size
            elif lentx > self.maxlen:
                self.size1 = (self.maxlen,self.size[1])
                while self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2] > self.maxlen-30:
                    self.x1 += 1
            else:
                self.size1 = (self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255)).get_rect()[2]+40, self.size[1])
            self.pos1 = (self.pos[0] - self.size1[0]-100,self.pos[1])
        
        
        surfacea = pg.Surface(self.size1)
        pg.draw.rect(surfacea,(20,20,10),((0,0),self.size1))
        surfacea.set_alpha(150)
        surf.blit(surfacea,(self.pos1))
        pg.draw.rect(surf,(255,255,255),(self.pos1,self.size1),10)
        rtxb = self.font.render(self.rtx[self.x1:self.x2], 1, (255,255,255))
        surf.blit(rtxb,(self.pos1[0]+20,self.pos1[1]+20))
            

class Buttons():
    def __init__(self, pos, size, colors, type, text, defa, font = None, sound = None, img1 = None, img2 = None):
        self.pos = pos
        self.size = size
        self.sdpos=(0,0)
        self.type = type
        self.text = text
        self.defa = defa
        self.colors = colors
        self.img1 = img1
        self.img2 = img2
        self.img = img1
        self.sound = sound
        self.n = 0
        self.draw = True if img1 != None and img2 != None else False
        self.mpos = (0,0)
        self.click = False
        self.clb = 0
        self.font = pg.font.SysFont('arial', int(size[1]-20))
        self.on = False
        if font != None:
            self.font = font
    
    def update(self,e):
        if e.type == pg.MOUSEBUTTONDOWN:
            self.clb = 0
            self.mpos = e.pos
            self.mpos = (self.mpos[0]-self.sdpos[0],self.mpos[1]-self.sdpos[1])
            if checkB(self.mpos,self.pos,self.size):
                self.click = True
                if self.sound != None:
                    self.sound.play()
            else:
                self.click = False
        elif e.type == pg.MOUSEBUTTONUP:
            self.clb = 1
            if self.click:
                self.click = False
                if checkB(self.mpos,self.pos,self.size):
                    if self.type == 'click':
                        self.defa()
                    if self.type == 'switch':
                        self.on = True
                        self.defa()
                    if self.type == 'switch+':
                        self.on = not(self.on)
                        self.defa()
        elif e.type == pg.MOUSEMOTION:
            self.mpos = e.pos
            self.mpos = (self.mpos[0]-self.sdpos[0],self.mpos[1]-self.sdpos[1])
            if checkB(self.mpos,self.pos,self.size):
                if self.clb == 1:
                    if self.sound != None:
                        self.sound.play()
                        self.clb = 2
                if self.clb == 0:
                    self.clb = 1
                self.click = True
            else:
                self.click = False
                self.clb = 0
    
    def render(self,surf):
        if self.click:
            if self.type == 'press':
                self.defa()
        if self.clb == 1:
            self.n = 1
            self.img = self.img2
        elif self.clb == 0:
            self.n = 0
            self.img = self.img1
        if self.type=='switch' or self.type == 'switch+':
            if self.on or self.clb != 0:
                self.n = 1
                self.img = self.img2
            else:
                self.n = 0
                self.img = self.img1
            
        o = (255,255,255) if self.colors[self.n][0] < 100 and self.colors[self.n][1] > 100 and self.colors[self.n][2] < 100 else (255,255,255) if self.colors[self.n][0] < 100 and self.colors[self.n][1] < 100 and self.colors[self.n][2] < 100 else (0,0,0)
            
        pg.draw.rect(surf, (self.colors[self.n]),(self.pos,self.size))
        pg.draw.rect(surf, o,(self.pos,self.size),4)
        if self.draw:
            surf.blit(self.img,(self.pos[0]+4, self.pos[1]+4))
            
        if self.text != '' and self.text != None:
            try:
                n = self.font.render(self.text,1,o)
            except:
                f = pg.font.SysFont('arial', int(self.size[1]-40))
            surf.blit(n,((self.pos[0]+self.size[0]//2)-(n.get_rect()[2]//2)-6,(self.pos[1]+self.size[1]//2)-n.get_rect()[3]//2))


class Slider():
    def __init__(self,pos,size,colors,n,input,font = None):
        self.pos = pos
        self.size = size
        self.sdpos=(0,0)
        self.colors = colors
        self.znach = range(n[0],n[1],n[2])
        self.perspos = self.size[0]/len(self.znach)
        self.input = input
        self.n = 1
        self.click = False
        self.i = 0
        self.click = False
        self.font = font if font != None else pg.font.SysFont('arial',int(size[1]//1.8))
    
    def update(self,e):
        if e.type == pg.MOUSEBUTTONDOWN:
            pos = e.pos
            pos = (pos[0]-self.sdpos[0],pos[1]-self.sdpos[1])
            if checkB(pos,self.pos,self.size):
                self.click=True
                for i in range(len(self.znach)):
                    if pos[0] > self.perspos*i+self.pos[0] and pos[0] < self.perspos*(i+1)+self.pos[0]:
                        self.input = self.znach[i]
    
        if e.type == pg.MOUSEMOTION and self.click:
            pos = e.pos
            pos = (pos[0]-self.sdpos[0],pos[1]-self.sdpos[1])
            if checkB(pos,self.pos,self.size):
                for i in range(len(self.znach)):
                    if pos[0] > self.perspos*i+self.pos[0] and pos[0] < self.perspos*(i+1)+self.pos[0]:
                        self.input = self.znach[i]
        if e.type == pg.MOUSEBUTTONUP:
            self.click = False
    
    def render(self,surf):
            self.i = self.znach.index(self.input)
            s = self.font.render(str(self.input),1,(20,20,20))
            x = s.get_rect()[2]
            pg.draw.rect(surf,self.colors[0],((self.pos[0],self.pos[1] + self.size[1]*0.2),(self.size[0]+60,self.size[1]*0.60)))
            pg.draw.rect(surf,self.colors[self.n],((self.pos[0] + self.i*self.perspos+self.perspos//2-x//2,self.pos[1]),(x+20,self.size[1])))
            surf.blit(s,(self.pos[0] + self.i*self.perspos+self.perspos//2-x//2+10,self.pos[1]*1.05))


class gHotbar():
    def __init__(self,pos,num,ac,img1,img2,imgItems,numbers,font = None):
        self.pos = pos
        self.sdpos=(0,0)
        self.num = num
        self.active = ac
        self.img1 = img1
        self.img2 = img2
        self.x = img1.get_rect()[2]
        self.y = img1.get_rect()[3]
        self.imgs = imgItems
        self.numbers = numbers
        self.font = font if font != None else pg.font.SysFont('arial',64)
    
    def update(self,e):
        if e.type == pg.MOUSEBUTTONDOWN:
            p = e.pos
            p = (p[0]-self.sdpos[0],p[1]-self.sdpos[1])
            if checkB(p,self.pos,(self.x * self.num,self.y)):
                for i in range(self.num):
                    if e.pos[0] > self.pos[0]+self.x*i and e.pos[0] < self.pos[0]+self.x*(i+1):
                        self.ac = i
        elif e.type == pg.MOUSEMOTION:
            p = e.pos
            p = (p[0]-self.sdpos[0],p[1]-self.sdpos[1])
            if checkB(p,self.pos,(self.x * self.num,self.y)):
                for i in range(self.num):
                    if e.pos[0] > self.pos[0]+self.x*i and e.pos[0] < self.pos[0]+self.x*(i+1):
                        self.active = i
     
    def render(self,surf):
        for i in range(self.num):
            if i == self.active:
                surf.blit(self.img2,(self.pos[0]+self.x*i, self.pos[1]))
            else:
                surf.blit(self.img1,(self.pos[0]+self.x*i, self.pos[1]))
            if self.imgs[i] != None:
                surf.blit(self.imgs[i],(self.pos[0]+self.x*i+self.x//2-self.imgs[i].get_rect()[2]//2, self.pos[1]+self.y//2-self.imgs[i].get_rect()[3]//2))
            if self.numbers[i] != 1:
                n = self.font.render(str(self.numbers[i]),1,(255,255,255))
                surf.blit(n,(self.pos[0]+self.x*(i+1)-20-n.get_rect()[2], self.pos[1]+self.y-4-n.get_rect()[3]))

class Rect():
    def __init__(self,color,pos,size,r=-1):
        self.c = color
        self.p = pos
        self.s = size
        self.r = r
    
    def render(self,surf):
        pg.draw.rect(surf,self.c,(self.p,self.s),r)

class Circle():
    def __init__(self,color,pos,r,r1):
        self.c = color
        self.p = pos
        self.r = r
        self.r1 = r1
    
    def render(self,surf):
        pg.draw.circle(surf,self.c,self.p,self.r,r1)

class label():
    def __init__(self,pos,text,font = None,s = 24,c = None):
        self.text = text
        self.pos = pos
        self.c = (255,255,255) if c == None else  c
        self.font = font if font != None else pg.font.SysFont('arial',s)
        self.l = self.font.render(self.text,1,self.c)
        self.size = self.l.get_size()
    
    def render(self,surf):
        surf.blit(self.l, self.pos)

class Img():
    def __init__(self,img,pos):
        self.img = img
        self.pos = pos
    
    def render(self, surf):
        surf.blit(self.img, self.pos)

class BoxWithWG():
    def __init__(self,pos,size,colors, type, defa = None, sound = None):
        self.p = pos
        self.s = size
        self.cs = colors
        self.cl = False
        self.defa = defa
        self.sound = sound
        self.WGs = []
        self.type = type
        self.blocked = False
        self.on = 0
        self.ups = ("<class 'pgWitgets.Buttons'>", "<class 'pgWitgets.TextBox'>", "<class 'pgWitgets.Slider'>","<class '__main__.Buttons'>", "<class '__main__.TextBox'>", "<class '__main__.Slider'>")
    
    def add(self,obj):
        self.WGs.append(obj)
    
    def update(self,e):
        if self.type:
            for _ in self.WGs:
                if str(type(_)) in self.ups:
                    if str(type(_)) in ("<class 'pgWitgets.Buttons'>","<class '__main__.Buttons'>"):
                        if self.blocked:
                            _.click = False
                    _.sdpos=self.p
                    _.update(e)
        else:
            if e.type == pg.MOUSEBUTTONDOWN:
                self.mpos = e.pos
                if checkB(self.mpos,self.p,self.s):
                    self.cl = True
                    self.on = 1
                    if self.sound != None:
                        self.sound.play()
            elif e.type == pg.MOUSEBUTTONUP:
                self.click = False
                self.on = 0
                if checkB(self.mpos,self.p,self.s):
                    if self.defa != None:
                        if not(self.blocked):
                            self.defa()
                        self.blocked = False
            elif e.type == pg.MOUSEMOTION:
                self.mpos = e.pos
                if checkB(self.mpos,self.p,self.s):
                    if self.click == False:
                        if self.sound != None:
                            self.sound.play()
                    self.click = True
                    self.on = 1
                else:
                    self.click = False
                    self.on = 0
        self.blocked = False
    
    def render(self,surf,pos = None):
        pos = self.p if pos == None else pos
        s = pg.Surface(self.s)
        s.fill(self.cs[self.on])
        for _ in self.WGs:
            _.render(s)
        surf.blit(s,(pos))
        
        
class Swip():
    def __init__(self, pos, size, color):
        self.p = pos
        self.s = size
        self.sw = 0
        self.tab = False
        self.swiped = False
        self.c = color
        self.bs = []
    
    def add(self,obj):
        self.bs.append(obj)
    
    def update(self, e):
        if self.swiped:
            for _ in self.bs:
                _.blocked = True
        if e.type == pg.MOUSEBUTTONDOWN:
            p = e.pos
            if checkB(p,self.p,self.s):
                self.tab = True
            
        elif e.type == pg.MOUSEBUTTONUP:
            self.tab = False
            self.swiped = False
        
        elif e.type == pg.MOUSEMOTION:
            p = e.pos
            self.swiped = True
            if self.tab:
                self.sw += e.rel[1]
        self.sw = -5 if self.sw > -5 else self.sw
        for _ in self.bs:
            _.update(e)
            
    def render(self,surf):
        i = 0
        for _ in self.bs:
            _.p = (self.p[0]+_.p[0],self.p[1] + 25 + i + self.sw)
            i += _.s[1] + 10
        s = pg.Surface(self.s)
        s.fill(self.c)
        for _ in self.bs:
            _.render(s,(_.p[0],_.p[1] - self.p[1]))
        surf.blit(s,self.p)


def surfUpdate(m):
    if m == 0:
        surf.fill(pg.Color('black'))
    if m == 1:
        pg.display.flip()
        clock.tick()
        
if __name__ == "__main__":
    import random

    surf = pg.display.set_mode((2000, 1000))

    bgC = [0,0,0]
    
    def f1():
        global bgC
        bgC = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    b1 = Buttons((40, 40), (200, 40), ((40, 40, 40), (40, 250, 40)), 'click', 'click for magic', f1)

    while True:
        surf.fill(bgC)
        
        for e in pg.event.get():
            b1.update(e)

        b1.render(surf)

        pg.display.update()

















        
