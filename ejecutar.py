# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 07:17:32 2018

@author: Usuario
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class Principal(object):
    def __init__(self):
        self.data = pd.read_csv("fondotorunos.txt", header=0, delim_whitespace=True, decimal=".")
        self.df=pd.DataFrame(self.data)
        self.r=0
        self.ultimo=len(self.df)-1
    


  
    def normalizacion(self,pos,car):
        #----------------------normaizacion de la carta usando formula-------------
        #si dmin es diferente de 0 entonces ejecute esto
        dmin=np.min(pos)
        dmax=np.max(pos)
        smin=np.min(car)
        smax=np.max(car)
        dnlist=[]
        lnlist=[]
        for i in range(len(self.df)):
            dn=(pos[i]-dmin)/(dmax-dmin)
            ln=(car[i]-smin)/(smax-smin)
            dnlist.append(dn)
            lnlist.append(ln)
        #else vaya y grafique
        return lnlist,dnlist #si pos y car varian lnlist,dnlist varian
        
        
    
    
    def angulo(self,lnlist,dnlist): 
        #----------------------calculo angulo-------------------------------------
        global l1;
        l1=len(self.df)-1
        An=[]
        for i in range(0, len(self.df)-1):
            Ang =np.arctan2(lnlist[i+1] - lnlist[i], dnlist[i+1]-dnlist[i])* 180 / np.pi
            An.append(Ang)
        
        Ang1 =np.arctan2(lnlist[0] - lnlist[l1], dnlist[0]-dnlist[l1])* 180 / np.pi
        An.append(Ang1)
        return An
        
    

     
    def codigo(self,An,poss,carr):
        #-------------------------calcula el codigo de cadena-----------------
        codcadena=[]
        for i in range(0,len(An)): 
            if (-200<An[i]<-45): 
                codcadena.append(3)
                
            elif (-45<An[i]<45):
                codcadena.append(0)
            
            elif (45<= An[i] <=135):
                codcadena.append(1)
                
            elif (An[i]>135):
                codcadena.append(2)
        print("\033[1;34m" + "el codigo de cadena es  : "+'\033[0;m',codcadena)
        print("\033[1;34m" + "la longitud del codcadena es : "+'\033[0;m',len(codcadena))
        return codcadena
    
    
    
    
                
    def codigocomprimido(self,codcadena,x1,y1):
        #------------------------calcula el codigo de cadena comprimido---------------------
        vx=[] #vertices en x
        vy=[] #vertices en y
        kk=[]
        l=len(codcadena)
        k=0
        self.cdccomprimido=[]
        for k in range(0, l-1):
            if (codcadena[k]==codcadena[k+1]):
                k=k+1
            else:
                #self.graficarvertices(f,c,N,k,x1,y1)#  grafico dos
                self.cdccomprimido.append(codcadena[k])
                vx.append(x1[k])
                vy.append(y1[k])
                kk.append(k)
    
        self.numver=(len(vx))
        u=codcadena[-1] #ultimo elemento de la lista
        self.cdccomprimido.append(u)
        self.cadena=(codcadena)
        print("\033[1;34m" + "el comprimido es  : "+'\033[0;m',self.cdccomprimido)
        print("\033[1;34m" + "soy kk : "+'\033[0;m',kk)
        print("\033[1;34m" + "soy la otra cadena : "+'\033[0;m',self.cadena)
        return vx,vy,self.numver
        




    def filtro(self,x,y):
        #--------------------------filtro-----------------------------------
        dnfilt=[]
        lnfilt=[]
        for i in range(0,len(self.df)-2): #0->>171  #0-->>lend-3
            dnf=(x[i]+x[i+1]+x[i+2])/3
            lnf=(y[i]+y[i+1]+y[i+2])/3
            dnfilt.append(dnf)
            lnfilt.append(lnf)
        l1=len(self.df)-1
        l2=len(self.df)-2 
        dnf_pen=(x[l2]+x[l1]+x[0])/3  
        dnf_ult=(x[l1]+x[0]+x[1])/3 
        dnfilt.extend([dnf_pen,dnf_ult])
        lnf_pen=(y[l2]+y[l1]+y[0])/3  
        lnf_ult=(y[l1]+y[0]+y[1])/3
        lnfilt.extend([lnf_pen,lnf_ult])
        
        lnlist,dnlist = self.normalizacion(dnfilt,lnfilt)
        An = self.angulo(lnlist,dnlist)
        codcadena = self.codigo(An,dnfilt,lnfilt)
        vx,vy,self.numver=self.codigocomprimido(codcadena,dnfilt,lnfilt)
        return dnfilt,lnfilt,vx,vy,self.numver

    
    
    
    def Ejecutar(self):
        posicion=self.data.iloc[:,0]
        carga=self.data.iloc[:,1]
        lnlist,dnlist = self.normalizacion(posicion,carga)
        An = self.angulo(lnlist,dnlist)
        codcadena = self.codigo(An,posicion,carga)
        vx,vy,self.numver=self.codigocomprimido(codcadena,posicion,carga)
        dnfilt,lnfilt,vx,vy,self.numver=self.filtro(posicion,carga)
        sx,sy=self.Autofiltrar(dnfilt,lnfilt)
        
        
    
        

    def Autofiltrar(self,f1,f2):
        for i in range(0,(800)): #0-->4
            self.r=self.r+1 #5
            print("numero de recursividad",self.r)
            if self.numver==4:
               self.numrecur=self.r
               return (0,0)
            else:
                dnfilt,lnfilt,vx,vy,self.numver=self.filtro(f1,f2)
                self.sx=(vx)
                self.sy=(vy)
                self.du=(dnfilt)
                self.lu=(lnfilt)
                self.cdc=(self.cdccomprimido)
                print("esto es sx",self.sx)
                print("codigo comprimido finalll",self.cdccomprimido)
                dnfilt,lnfilt = self.Autofiltrar(dnfilt,lnfilt) 
                
             
                
                

    def ABCD(self,x,y): #ENCUNTRA LOS PUNTOS A,B,C,D EN ORDEN PARA UN CODIGO DE CADENA DE cdc==[1, 0, 3, 2, 1]:
        g=len(self.cadena)
        k=0
        for k in range(0,g-1):
            if self.cadena[k]==1 and self.cadena[k+1]==0:
                self.Bx=(x[k])
                self.By=(y[k])
                print("esto es B",self.Bx,self.By)
            
            elif self.cadena[k]==0 and self.cadena[k+1]==3:
                self.Cx=(x[k])
                self.Cy=(y[k])
                print("esto es C",self.Cx,self.Cy)
 
            elif self.cadena[k]==3 and self.cadena[k+1]==2:
                self.Dx=(x[k])
                self.Dy=(y[k])
                print("esto es D",self.Dx,self.Dy)
                
            elif self.cadena[k]==2 and self.cadena[k+1]==1:
                self.Ax=(x[k])
                self.Ay=(y[k])
                print("esto es A",self.Ax,self.Ay)
                
            else:
                k=k+1
                
    def ABCD2(self,x,y):# ENCUENTRA LOS PUNTOS ABCD PARA UN CODIGO DE CADENA DE cdc==[0, 3, 2, 1, 0]:
        g=len(self.cadena)
        k=0
        for k in range(0,g-1):
            if self.cadena[k]==0 and self.cadena[k+1]==3:
                self.Cx=(x[k])
                self.Cy=(y[k])
                print("esto es C",self.Cx,self.Cy)
            
            elif self.cadena[k]==3 and self.cadena[k+1]==2:
                self.Dx=(x[k])
                self.Dy=(y[k])
                print("esto es D",self.Dx,self.Dy)
 
            elif self.cadena[k]==2 and self.cadena[k+1]==1:
                self.Ax=(x[k])
                self.Ay=(y[k])
                print("esto es A",self.Ax,self.Ay)
                
            elif self.cadena[k]==1 and self.cadena[k+1]==0:
                self.Bx=(x[k])
                self.By=(y[k])
                print("esto es B",self.Bx,self.By)
                
            else:
                k=k+1
      
    
    
    
    def distanciasABCD(self):
        dAB= (self.Bx-self.Ax)**2+(self.By-self.Ay)**2
        AB=np.sqrt(dAB)
        print("esto es AB",AB)
        
        
        dBC= (self.Cx-self.Bx)**2+(self.Cy-self.By)**2
        BC=np.sqrt(dBC)
        print("esto es BC",BC)
        

        dCD= (self.Dx-self.Cx)**2+(self.Dy-self.Cy)**2
        CD=np.sqrt(dCD)
        print("esto es CD",CD)
        

        dDA= (self.Ax-self.Dx)**2+(self.Ay-self.Dy)**2
        DA=np.sqrt(dDA)
        print("esto es DA",DA)
        return AB,BC,CD,DA
    
    
    
    
    def segmentosCarta(self,AB,BC,CD,DA):
        E=BC-DA
        CMP=DA+E #Carrera de la Barra pulida
        print("CMP (Carrera Maxima de Piston): ",CMP)
        
        CEP=DA
        print("CEP (Carrera Efectiva del Piston) :",CEP)
        
        Fo=AB #Carrera del embolo
        print("Fo (Carga de Fluido): ",Fo)

        Pr=self.Ay #Peso del embolo dentro del fluido
        print("Pr (Peso del embolo dentro del fluido): ",Pr)
        
        P1=AB #peso del Embolo sobre el fluido
        print("P1 (Peso del Embolo sobre el fluido): ",P1)
        
        Pd=Pr+P1 # Carga Estática en la Barra pulida
        print("Pd (Carga Estatica en la Barra pulida): ",Pd)
        return CMP,CEP
    
                
        
        
    def eje2(self,f,c,N):
        posicion=self.data.iloc[:,0]
        carga=self.data.iloc[:,1]
        if self.cdc==[1, 0, 3, 2, 1]: #Poligono A
            self.ABCD(self.du,self.lu)
            self.graficoABCD(f,c,N,posicion,carga,self.Ax,self.Ay,self.Bx,self.By,self.Cx,self.Cy,self.Dx,self.Dy)
            AB,BC,CD,DA=self.distanciasABCD()
            self.segmentosCarta(AB,BC,CD,DA)
            self.graficofiltro(f,c,N,self.du,self.lu,self.sx,self.sy,self.Ax,self.Ay,self.Bx,self.By,self.Cx,self.Cy,self.Dx,self.Dy)
            print("POLIGONO A")
            
        elif self. cdc==[0, 3, 2, 1, 0]:
            self.ABCD2(self.du,self.lu) #Poligono B
            self.graficoABCD(f,c,N,posicion,carga,self.Ax,self.Ay,self.Bx,self.By,self.Cx,self.Cy,self.Dx,self.Dy)
            AB,BC,CD,DA=self.distanciasABCD()
            self.segmentosCarta(AB,BC,CD,DA)
            self.graficofiltro(f,c,N,self.du,self.lu,self.sx,self.sy,self.Ax,self.Ay,self.Bx,self.By,self.Cx,self.Cy,self.Dx,self.Dy)
            print("POLIGONO B")
        else:
            self.graficoOtraCarta(1,1,1,posicion,carga,self.sx,self.sy) #Poligono None
        
            
      
        
        
        
        
        #=============================================================================
        #Grafica de la Carta Dinagrafica Original con Vertices
    def graficoABCD(self,a,b,j,xx,yy,ax,ay,bx,by,cx,cy,dx,dy):
        # =================== GRAFICA=================================================
        fig4 = plt.figure("Carta Dinagrafica Original con Vertices")
        fig4.subplots_adjust(hspace=0.5, wspace=0.5)
        wy = fig4.add_subplot(a, b, j)
        wy.plot(xx, yy,"b--")
        wy.fill(xx, yy, "w", edgecolor="black", linewidth=1)
        wy.set_xlabel(r"$CARRERA-Pulgadas$", fontsize = 12, color = (1,0,0))
        wy.set_ylabel(r"$PESO-LBS$", fontsize = 12, color = (1,0,0))
        wy.set_title("Carta Dinagrafica Original con Vertices")
        wy.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
        wy.axhline(0, color='black', linewidth=0.5)
        
        #impresion del punto inicial del funcionamiento de la bomba
        puntoi =wy.plot(xx[0], yy[0], 'md')
        nota = plt.annotate(r'$ inicio(Bomba)$',
        xy=(xx[0], yy[0]), xycoords='data',
        xytext=(20, 0.4), fontsize=9,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        
        #impresion del punto final del funcionamiento de la bomba
        puntof =wy.plot(xx[self.ultimo], yy[self.ultimo], 'g^')
        nota = plt.annotate(r'$fin(Bomba)$',
        xy=(xx[self.ultimo], yy[self.ultimo]), xycoords='data',
        xytext=(-10, -0.1), fontsize=9,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        
        #puntos de los vertices en rojo
        puntoa =wy.plot(ax,ay, 'ro')
        puntob =wy.plot(bx,by, 'ro')
        puntoc =wy.plot(cx,cy, 'ro')
        puntod =wy.plot(dx,dy, 'ro')
        
        #impresion de las letras
        textoA = text(ax,ay, r'$A$', fontsize=11)
        textoB = text(bx,by, r'$B$', fontsize=11)
        textoC = text(cx,cy, r'$C$', fontsize=11)
        textoD = text(dx,dy, r'$D$', fontsize=11)
        
        #=============================================================================
        #grafico de la Aproximacion poligonal
    def graficofiltro(self,fr,cr,z,x1,y1,vx,vy,ax,ay,bx,by,cx,cy,dx,dy):
        # =================== GRAFICA=================================================
        fig3 = plt.figure("Aproximacion Poligonal")
        fig3.subplots_adjust(hspace=0.5, wspace=0.5)
        cz = fig3.add_subplot(fr, cr, z)
        cz.plot(x1, y1,"b--")
        cz.fill(x1, y1, "w", edgecolor="black", linewidth=1)
        cz.set_xlabel(r"$CARRERA-Pulgadas$", fontsize = 12, color = (1,0,0))
        cz.set_ylabel(r"$PESO-LBS$", fontsize = 12, color = (1,0,0))
        cz.set_title("Aproximacion Poligonal")
        cz.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
        cz.axhline(0, color='black', linewidth=0.5)
        punto =cz.plot(vx, vy, 'ro')
        
        #impresion de letras
        textoA = text(ax,ay, r'$A$', fontsize=11)
        textoB = text(bx,by, r'$B$', fontsize=11)
        textoC = text(cx,cy, r'$C$', fontsize=11)
        textoD = text(dx,dy, r'$D$', fontsize=11)
        
        #=============================================================================
        #grafica Carta que no entá presentes en los casos de poligonos A y B
    def graficoOtraCarta(self,a,b,j,xx,yy,lx,ly):
        # =================== GRAFICA=================================================
        fig2 = plt.figure("Carta Dinagrafica Original con Vertices")
        fig2.subplots_adjust(hspace=0.5, wspace=0.5)
        zx = fig2.add_subplot(a, b, j)
        zx.plot(xx, yy,"b--")
        zx.fill(xx, yy, "w", edgecolor="black", linewidth=1)
        zx.set_xlabel(r"$Carrera(pulgadas)$", fontsize = 12, color = (1,0,0))
        zx.set_ylabel(r"$Peso(LBS)$", fontsize = 12, color = (1,0,0))
        zx.set_title("Carta Dinagrafica Original con Vertices")
        zx.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
        zx.axhline(0, color='black', linewidth=0.5)
        puntos =zx.plot(lx,ly, 'ko')
        
        #impresion del punto inicial del funcionamiento de la bomba
        puntoi =zx.plot(xx[0], yy[0], 'rd')
        nota = plt.annotate(r'$ inicio(Bomba)$',
        xy=(xx[0], yy[0]), xycoords='data',
        xytext=(20, 0.4), fontsize=9,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        #impresion del punto final del funcionamiento de la bomba
        puntof =zx.plot(xx[self.ultimo], yy[self.ultimo], 'm^')
        nota = plt.annotate(r'$fin(Bomba)$',
        xy=(xx[self.ultimo], yy[self.ultimo]), xycoords='data',
        xytext=(-10, -0.1), fontsize=9,
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    




P=Principal()
P.Ejecutar()
P.eje2(1,1,1)





