import cv2
import numpy as np
import random
def getRoundDots(n,center,radius):
    step = 360/n
    current_angle=0
    temp_dots = np.zeros((n,2),np.uint32)
    for i in range(n):
        temp_dots[i][0] = int(center[0]+radius*np.cos(np.pi*current_angle/180))
        temp_dots[i][1] = int(center[1]+radius*np.sin(np.pi*current_angle/180))
        current_angle+=step
    return temp_dots
def getNetDots(n,left_corner):
    temp_dots = np.zeros((n*n,2),np.uint32)
    count=0
    for i in range(n):
        for j in range(n):
            temp_dots[count][0] = i*(left_corner[0]/n)
            temp_dots[count][1] = j*(left_corner[1]/n)
            count+=1
    return temp_dots
def getSquareDots(n,left_corner):
    temp_dots = np.zeros((n*4-2,2),np.uint32)
    count=0
    for i in range(n):
        for j in range(n):
            if(i==0 or j==0 or i == n-1 or j == n-1):
                temp_dots[count][0] = i*(left_corner[0]/n)
                temp_dots[count][1] = j*(left_corner[1]/n)
                count+=1
    return temp_dots
def getRandomDots(n,size):
    temp_dots = np.zeros((n,2),np.uint32)
    count=0
    for i in range(n):
        temp_dots[count][0] = random.randint(0,size[0])
        temp_dots[count][1] = random.randint(0,size[1])
        count+=1
    return temp_dots
xSize = 400
ySize = 400
white_color = (255,255,255)
gray_color = (32,32,32)
black_color = (0,0,0)
draw_color = gray_color
dots = getRoundDots(250,(xSize/2,ySize/2),xSize/2-5)
image = cv2.imread("nishiki.jpg")
image = cv2.resize(image,(xSize,ySize))
black_image = np.zeros((xSize,ySize),np.uint8)
white_image = np.full((xSize,ySize),255).astype(np.uint8)
grayImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
goalImage = np.copy(grayImage)
grayImage[grayImage>255]=255
grayImage[grayImage<0]=0
grayImage = grayImage.astype(np.uint8)
resultImage = np.copy(white_image)

def drawStringArt(canvas,goalImage,dots,steps,output_file_name,max_connects):
    current_nail = 0
    prev_nail = -1
    prev_max=0
    dotsUses = np.zeros(np.size(dots,axis=0))
    output_file = open(output_file_name,"w")
    output_file.write("round\n")
    output_file.write(str(np.size(dots))+"\n")
    for i in range(steps):
        maximum=0
        maximum_index=0
        for j in range(np.size(dots,axis=0)):
            if(j!=current_nail and j!=prev_nail and np.abs(j-current_nail)>1) and dotsUses[j]<max_connects:
                mean =np.mean(np.bitwise_and((255-goalImage),cv2.line(np.copy(black_image),dots[current_nail],dots[j],white_color,1)))
                if mean > maximum and mean != prev_max:
                    maximum = mean
                    maximum_index=j
        cv2.imshow("Image",canvas)
        cv2.waitKey(1)
        print("%.2f"%((i/steps)*100)+"%",end='\r')
        dotsUses[maximum_index]+=1
        canvas=np.subtract(canvas.astype(np.int32),cv2.line(np.copy(black_image),dots[current_nail],dots[maximum_index],draw_color,1))
        goalImage=np.add(goalImage.astype(np.int32),cv2.line(np.copy(black_image),dots[current_nail],dots[maximum_index],draw_color,1))
        goalImage[goalImage>255]=255
        canvas[canvas<0]=0
        goalImage = goalImage.astype(np.uint8)
        canvas = canvas.astype(np.uint8)
        prev_nail=current_nail
        current_nail=maximum_index
        output_file.write(str(current_nail)+"\n")
    output_file.close()
    return canvas
def readFile(filename,dots,canvas):
    file = open(filename,"r")
    type = file.readline()
    if np.size(dots) != int(file.readline()):
        print("1")
        return canvas
    prev_dot = 0
    for dot in file:
        dot = int(dot)
        canvas=np.subtract(canvas.astype(np.int32),cv2.line(np.copy(black_image),dots[prev_dot],dots[dot],draw_color,1))
        canvas[canvas<0]=0
        canvas = canvas.astype(np.uint8)
        prev_dot=dot
    return canvas
def getCenterPoint(point1,point2):
    point = ((point1[0]+point2[0])/2),((point1[1]+point2[1])/2)
    print(type(point1[0]))
    print(type(point[0]))
    return np.asarray(point,np.uint32)
def drawPattern(filename,dots,canvas):
    file = open(filename,"r")
    center = (np.size(canvas,axis=0)/2,np.size(canvas,axis=1)/2)
    type = file.readline()
    if np.size(dots) != int(file.readline()):
        print("1")
        return canvas
    prev_dot = 0
    text_pos = 2
    for dot in file:
        dot = int(dot)
        temp_canvas = np.copy(canvas)
        temp_canvas = cv2.circle(temp_canvas,dots[prev_dot],4,black_color,-1)
        temp_canvas = cv2.circle(temp_canvas,dots[dot],4,black_color,-1)
        temp_canvas = cv2.line(temp_canvas,dots[prev_dot],dots[dot],black_color,1)
        temp_canvas = cv2.putText(temp_canvas,str(prev_dot),getCenterPoint(dots[prev_dot],getCenterPoint(dots[prev_dot],center)),cv2.FONT_HERSHEY_COMPLEX,1,black_color,1)
        temp_canvas = cv2.putText(temp_canvas,str(dot),getCenterPoint(dots[dot],getCenterPoint(dots[dot],center)),cv2.FONT_HERSHEY_COMPLEX,1,black_color,1)
        cv2.imshow("Image",temp_canvas)
        cv2.waitKey(-1)
        prev_dot=dot
#resultImage = drawPattern("output.txt",dots,white_image)
resultImage = readFile("nishiki.txt",dots,white_image)
#resultImage = drawStringArt(white_image,grayImage,dots,2500,"nishiki.txt",20)
cv2.imshow("Image",resultImage)
cv2.waitKey(-1)
