#################LIBRERIAS######################
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import time

################################################


def find_all(wmat, start, end=-1):
    n = len(wmat)
    inf = 999999
    dist = [inf]*n
    dist[start] = wmat[start][start]  # 0

    spVertex = [False]*n
    parent = [-1]*n

    path = [{}]*n

    for count in range(n-1):
        minix = inf
        u = 0

        for v in range(len(spVertex)):
            if spVertex[v] == False and dist[v] <= minix:
                minix = dist[v]
                u = v

        spVertex[u] = True
        for v in range(n):
            if not(spVertex[v]) and wmat[u][v] != 0 and dist[u] + wmat[u][v] < dist[v]:
                parent[v] = u
                dist[v] = dist[u] + wmat[u][v]

    for i in range(n):
        j = i
        s = []
        while parent[j] != -1:
            s.append(j)
            j = parent[j]
        s.append(start)
        path[i] = s[::-1]

    return (dist[end], path[end]) if end >= 0 else (dist, path)


def F(txt):
    return float(txt)
def matriz(m):
    txt="   "
    for i in range(len(m)):
        txt=txt+" "
        if i<10:
            txt=txt+" "
        txt=txt+str(i)
    txt=txt+"\n"
    for i in range(len(m)):
        txt=txt+str(i)
        if i<10:
            txt=txt+" "
        txt=txt+":"
        for j in  range(len(m[i])):
            txt=txt+"  "+str(m[i][j])
        txt=txt+"\n"
    return txt       



##################ESTRUCTURA DE DATOS###########
nomDes=[] #["Peru","Venezuela"]
xDes=[]#[100,400]
yDes=[]#[50,250]
mAdy=[]
mCam=[]
aristas=[]#()



##################INTERFAZ GRAFICA###############
window = Tk()
window.geometry("1050x650")
window.title("NODOS")
window.resizable(False,False)
window.config(background="#213141")


salida=StringVar()
llegada=StringVar()
#######
W=650
H=300

R =20

canvas =Canvas(width=W, height=H, bg='white')
canvas.place(x=350,y=320)
def dibujar():
    print(xDes)
    canvas.delete("all")
    for i in range(len(nomDes)):
        x=xDes[i]
        y=yDes[i]
        if x>W:
            x=W
        if y>H:
            y=H
        
        canvas.create_oval(x-R,y-R,x+R,y+R,fill= 'red')
        canvas.create_text(x,y,text= nomDes[i])
    for i in range(len(aristas)):
        s = aristas[i][0]
        l = aristas[i][1]
        norma=((xDes[l]-xDes[s])**2+(yDes[l]-yDes[s])**2)**0.5
        vectorX=(xDes[l]-xDes[s])/norma
        vectorY=(yDes[l]-yDes[s])/norma
        canvas.create_line(xDes[s]+R*vectorX,yDes[s]+R*vectorY,xDes[l]-R*vectorX,yDes[l]-R*vectorY,arrow=LAST)
    

def camino():
    dibujar()
    S=nomDes.index(salida.get())
    L=nomDes.index(llegada.get())
    visitas = (find_all(mAdy,S)[1][L])   
    ##archi2=PhotoImage(file="avion.png")
    ##canvas.create_image(140, 100, image=archi2, anchor="nw")
    vx = xDes[visitas[0]]
    vy = yDes[visitas[0]]
    avion = canvas.create_polygon(0+vx,0+vy,40+vx,20+vy,0+vx,40+vy, fill= 'green' , outline='blue')
    for v in range(len(visitas)-1):
        P = 10
        nx = xDes[visitas[v+1]]
        ny = yDes[visitas[v+1]]
        px = (nx-vx)/P
        py = (ny-vy)/P
        for i in range(P):
            canvas.move(avion,px,py)
            window.update()
            time.sleep(0.1)
        vx=nx
        vy=ny
    time.sleep(0.5)
    dibujar()


        
    


consola = scrolledtext.ScrolledText(window,width="80",height="8")
consola.place(x=350,y=120)
def imprimir():
    txt = "Destinos: \n"
    i=0
    for n in nomDes:
        txt=txt+n+" = "+str(i)+"\n"
        i=1+i
    txt = txt+"\nMatriz adyasencia: \n"
    txt = txt+matriz(mAdy)
    txt = txt+"\nMatriz Camino: \n"
    txt = txt+matriz(mCam)
    limpiar()
    consola.insert("1.0", txt)
def limpiar():
    consola.delete("1.0","end")
    
def calcularMatcam():
    global mCam
    for i in range(len(mAdy)):
        for j in range(len(mAdy[i])):
            mCam[i][j]=mAdy[i][j]
    for i in range(len(mAdy)):
        #mCam[i][i]=1
        for j in range(len(mAdy[i])):
            if (mCam[i][j]==1):
                for k in range(len(mAdy[i])):
                    if(mCam[k][i]==1):
                        mCam[k][j]=1
    print(mCam)



destinos = scrolledtext.ScrolledText(window,width="35",height="31")
destinos.place(x=20,y=120)
def ingresarDestinos():
    global nomDes
    global xDes
    global yDes
    global mAdy
    global mCam
    global aristas
    aristas=[]
    nomDes=[] #["Peru","Venezuela"]
    xDes=[]#[100,400]
    yDes=[]#[50,250]
    mAdy=[]
    mCam=[]
    entrada = destinos.get("1.0","end")
    entrada = entrada.split("\n")
    for i in range(len(entrada)):
        entrada[i]=entrada[i].split(";")
        if(len(entrada[i])==3):
            if( entrada[i][0]  not in nomDes):
                nomDes.append(entrada[i][0])
                xDes.append(F(entrada[i][1]))
                yDes.append(F(entrada[i][2]))
    for i in range(len(nomDes)):
        mAdy.append([])
        mCam.append([])
        for j in range(len(nomDes)):
            mAdy[i].append(0)
            mCam[i].append(0)
    
    imprimir()
    dibujar()
    
def conectar():
    S=nomDes.index(salida.get())
    L=nomDes.index(llegada.get())
    print(S,L)
    mAdy[S][L]=1
    if (S,L) not in aristas and S!=L:
        aristas.append((S,L))    
    calcularMatcam()
    imprimir()
    dibujar()  
    
Label(text="Formato: Nombre ; coordenada en X ; coordenada en Y  ",bg="#213141",fg="white").place(x=20,y=70)
Label(text="Salida  ",bg="#213141",fg="white").place(x=400,y=30)
Label(text="Legada  ",bg="#213141",fg="white").place(x=700,y=30)

Entry(textvariable=salida,width="20").place(x=450,y=30)
Entry(textvariable=llegada,width="20").place(x=750,y=30)
Button(window,text="Ingresar destinos",command=ingresarDestinos, width="33",height="1").place(x=20,y=30)
Button(window,text="Conectar",command=conectar, width="33",height="1").place(x=350,y=80)
Button(window,text="Animacion de camino",command=camino, width="33",height="1").place(x=650,y=80)
Label(text="GRAFICO  ",bg="#213141",fg="white").place(x=350,y=280)
window.mainloop()