from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt  
import time


#declaracion de variables conversion RGB-HSV-RGB para encontrar markers color verde en cuerpo


timein=time.time()
rgb_img = Image.open('human_copia.jpg')
[rows,columns] = rgb_img.size
Nrgb_img=np.zeros((rows, columns, 3), int)
h=np.zeros((rows,columns),dtype=float)
s=np.zeros((rows,columns),dtype=float)
v=np.zeros((rows,columns),dtype=float)
red=np.zeros((rows,columns),dtype=np.uint8)
green=np.zeros((rows,columns),dtype=np.uint8)
blue=np.zeros((rows,columns),dtype=np.uint8)


#######          declaracion de variables algoritmo median filter       ######


window=np.zeros(9,dtype=np.uint8)


###### #         declaracion de variables algoritmo erode               #######


r=2;c=r;
wi=r+1;wj=c+1;
global I2;
I2=np.zeros((rows,columns),dtype=int)


####   declaracion de variables algoritmo Connected-component labeling  ####


component=0
global label;
label=np.zeros((rows,columns),dtype=np.uint8)
####global I;
I=np.zeros((rows,columns),dtype=np.uint8)
####variables para encontrar centroide
sum_i=np.zeros(7,dtype=np.uint32)
sum_j=np.zeros(7,dtype=np.uint32)
ci=np.zeros(7,dtype=np.uint32)
cj=np.zeros(7,dtype=np.uint32)
num_pxl=np.zeros(7,dtype=np.uint32)


##################              rgb_to_hsv fuction       ###################


def rgb_to_hsv(r,g,b):
    r=r/255
    g=g/255
    b=b/255
####vALOR MAXIMO
    mx=r
    if g>mx:
        mx=g
        if b>mx:
            mx=b        
#####VALOR MINIMO
    mn=r
    if g<mn:
        mn=g
        if b<mn:
            mn=b
#####CONVERSION
    df=mx-mn
    if mx==mn:
        h=0
    elif mx == r:
        h = (60*((g-b)/df) + 360)%360
    elif mx == g:
        h = (60*((b-r)/df) + 120)%360
    elif mx == b:
        h = (60*((r-g)/df) + 240)%360

    if mx==0:
        s=0
    else:
        s = df/mx
    h=h/2#de 0-360 a 0-180
    s=s*255#de 0-1 a 0-255
    v = mx*255#de 0-1 a 0-255
    return h,s,v


##################              hsv_to_rgb fuction       ###################


def hsv_to_rgb(h,s,v):
    h=h*2
    s=s/255
    v=v/255
    hsix=h/60
    hsixf=math.floor(hsix)
    hi=int(hsixf)%6
    f=hsix-hsixf;
    p=v*(1-s)
    q=v*(1-f*s)
    t=v*(1-(1-f)*s)
    r, g, b=0, 0, 0 
    if hi==0:
        r, g, b = v, t, p
    elif hi==1:
        r, g, b = q, v, p
    elif hi==2:
        r, g, b = p, v, t
    elif hi==3:
        r, g, b = p, q, v
    elif hi==4:
        r, g, b = t, p, v
    elif hi==5:
        r, g, b = v, p, q    
    r, g, b=int(r*255), int(g*255), int(b*255)
    return r, g, b


#####################              sort function             ###############


def sort(array,size):
    for k in range(1,size):
        key=array[k]
        p=k-1
        while p >= 0 and array[p] > key: 
            array[p + 1] = array[p] 
            p = p - 1
        array[p + 1] = key
        
        
############              conected component labeling function           ######


def CCL(x,y,c):
    global label
    global I2
    dx=np.array([-1,0,1,1,1,0,-1,-1])
    dy=np.array([1,1,1,0,-1,-1,-1,0])
    label[x,y]=c
    for i in range(0,8):
        nx=x+dx[i]
        ny=y+dy[i]
        if I2[nx,ny] and not(label[nx,ny]):
            CCL(nx,ny,c)
    return   

        
###      loop de llamado de funciones para encontrar color verde       #####
###############               y de binarizacion        #####################


for i in range(0,rows):
    for j in range(0,columns):
#####llamado de funcion rgb_to_hsv           
        rd,gn,bl=rgb_img.getpixel((i,j))
        h[i,j], s[i,j], v[i,j]= rgb_to_hsv(rd, gn, bl)
#####umbral en componentes h,s,v para filtrar color verde            
        if h[i,j]>=25 and h[i,j]<=110 and s[i,j]>=110 and s[i,j]<=255  and v[i,j]>=140 and v[i,j]<=255:
            h[i,j], s[i,j], v[i,j] =h[i,j], s[i,j], v[i,j]
        else:
            h[i,j], s[i,j], v[i,j] =0, 0, 255
#####llamado de funcion hsv_to_rgb
        red[i,j], green[i,j], blue[i,j]=hsv_to_rgb(h[i,j],s[i,j],v[i,j])
#####conversion a imagen binaria            
        if green[i,j] == 255:
            I[i,j]=0;
        else:
            I[i,j]=255;
            

######################         loop median filter       ####################


for i in range(0,rows):
    for j in range(0,columns):
        if i>0 and i<rows-1 and j>0 and j<columns-1:
            window[0] = I[i-1,j-1]
            window[1] = I[i-1,j] 
            window[2] = I[i-1,j+1] 
            window[3] = I[i,j-1] 
            window[4] = I[i,j] 
            window[5] = I[i,j+1] 
            window[6] = I[i+1,j-1] 
            window[7] = I[i+1,j]
            window[8] = I[i+1,j+1]
            sort(window,9)
            I[i,j]=window[4]
            

##########################      loop erode algorithm    ##################### 


for i in range(0,rows):
    for j in range(0,columns):        
        if i>wi and i<rows-r and j>wj and j<columns-c: #para ventana de 5x5  
            mn=I[i,j]
            mx= mn            
            for i1 in range(i-wi,i+wi):
                for j1 in range(j-wj,j+wj):
                    if mn>I[i1,j1]:
                        mn=I[i1,j1]                        
            I2[i,j]=mn


###################   loop conected component labeling  ######################
3################     variables para encontrar centroide #####################


for i in range(0,rows):
    for j in range(0,columns):
        if I2[i,j] and not(label[i,j]):
            component=component+1
            CCL(i,j,component)
            #if label[i,j] == 3
            #    disp[i]
            #    disp[j]            
        if label[i,j]==1:
            num_pxl[0]=num_pxl[0]+1
            sum_i[0] = sum_i[0] + i
            sum_j[0] = sum_j[0] + j
            ci[0] = round(sum_i[0]/num_pxl[0])
            cj[0]= round(sum_j[0]/num_pxl[0])   
        elif label[i,j]==2:
            num_pxl[1]=num_pxl[1]+1
            sum_i[1] = sum_i[1] + i
            sum_j[1] = sum_j[1] + j
            ci[1] = round(sum_i[1]/num_pxl[1])
            cj[1]= round(sum_j[1]/num_pxl[1])
        elif label[i,j]==3:
            num_pxl[2]=num_pxl[2]+1
            sum_i[2] = sum_i[2] + i
            sum_j[2] = sum_j[2] + j
            ci[2] = round(sum_i[2]/num_pxl[2])
            cj[2]= round(sum_j[2]/num_pxl[2])
        elif label[i,j]==4:
            num_pxl[3]=num_pxl[3]+1
            sum_i[3] = sum_i[3] + i
            sum_j[3] = sum_j[3] + j
            ci[3] = round(sum_i[3]/num_pxl[3])
            cj[3]= round(sum_j[3]/num_pxl[3])
        elif label[i,j]==5:
            num_pxl[4]=num_pxl[4]+1
            sum_i[4] = sum_i[4] + i
            sum_j[4] = sum_j[4] + j
            ci[4] = round(sum_i[4]/num_pxl[4])
            cj[4]= round(sum_j[4]/num_pxl[4])
        elif label[i,j]==6:
            num_pxl[5]=num_pxl[5]+1
            sum_i[5] = sum_i[5] + i
            sum_j[5] = sum_j[5] + j
            ci[5] = round(sum_i[5]/num_pxl[5])
            cj[5]= round(sum_j[5]/num_pxl[5])
        elif label[i,j]==7:
            num_pxl[6]=num_pxl[6]+1
            sum_i[6] = sum_i[6] + i
            sum_j[6] = sum_j[6] + j
            ci[6] = round(sum_i[6]/num_pxl[6])
            cj[6]= round(sum_j[6]/num_pxl[6])
            

#####################        output result  ##################################


Imout=np.zeros((rows,columns),dtype=np.uint8)
for i in range(0,rows):
    for j in range(0,columns):
         if label[i,j]!=0:
             Imout[i,j]=0
         else:
             Imout[i,j]=0#255;
             
Imout[ci[0],cj[0]]=255
Imout[ci[1],cj[1]]=255
Imout[ci[2],cj[2]]=255
Imout[ci[3],cj[3]]=255
Imout[ci[4],cj[4]]=255
Imout[ci[5],cj[5]]=255
Imout[ci[6],cj[6]]=255

print(ci)
print(cj)
green=green.transpose()#para arreglar problema de volteo de los ejes x,y que provoca Image.fromarray
green=Image.fromarray(green)
I=I.transpose()#para arreglar problema de volteo de los ejes x,y que provoca Image.fromarray
I=Image.fromarray(I)
I2=I2.transpose()#para arreglar problema de volteo de los ejes x,y que provoca Image.fromarray
I2=Image.fromarray(I2)
Imout=Imout.transpose()#para arreglar problema de volteo de los ejes x,y que provoca Image.fromarray
Imout=Image.fromarray(Imout)
rgb_img.show()
green.show()
I.show()
I2.show()
Imout.show()
timefin=time.time()
print(timefin-timein)
