import numpy as np
import cv2
import matplotlib.pyplot as plt
path="test_image.jpg"
Original=cv2.imread(path)
test_image=np.copy(Original)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Now image is converted into 3D array
Gray_image=cv2.cvtColor(test_image,cv2.COLOR_BGR2GRAY)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Now the image is converted into Gray scal Having 2D array
Edge_detection=cv2.Canny(Gray_image,50,125)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Now the Edge is Detected from the image canny by default uses the Smoothning algoritham like  Gaussion Blure.
test=Edge_detection

def Region_Of_Interest():
    """This function is used for Selectin the n number of coordinates
    from the given image by pyplot module"""
    y=[]
    def coordinats():
        n=int(input("Enter the Number of clicks: "))
        if n>2:
            plt.imshow(Edge_detection,cmap='gray')
            plt.title("coordinats")
            clicks=plt.ginput(n)
            return clicks
        else:
            print("Enter value more then 2:")
            coordinats()
    coordinat=coordinats()
    for i in coordinat:
        temp=[]
        for j in i:
            temp.append(int(j))
        y.append(tuple(temp))
    y=np.array([y])
    return y
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Region Of Interest is Selected by the help of coordinates manually.
def Masking():
    """In this method we will create a polynomial and mask it on Edged image"""
    # coordinat=Region_Of_Interest()# use when you need to select the coordinats from Region_Of_Interest.
    coordinat = np.array([[(574, 283), (293, 688), (994, 690)]])
    mask=np.zeros_like(Edge_detection)
    # print(coordinat)
    cv2.fillPoly(mask,coordinat,255)
    test=cv2.bitwise_and(Edge_detection,mask)
    return test
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Create a mask of zero array and coppy the Region of interest over it.
masking_image=Masking()
print("\nDetecting Lines......")
lines = cv2.HoughLinesP(masking_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
lines=np.array(lines)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Using parabolic Hough Transformation
def displayLine(image,line):
    line_image=np.zeros_like(image)#Remember this Array is vary usefull in blending the line on it choos RBG one.
    if line is not None:
        print(line)
        for i in line:
            x1,y1,x2,y2=i.reshape(4)
            print("x1={},y1={},x2={},y2={}".format(x1, y1, x2, y2))
            cv2.line(line_image,(x1,y1),(x2,y2),(0,255,),10)
    return line_image
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>create a zeros materix of same shape and create a line over it which is later get blanded over the original image.
LineImage=displayLine(test_image,lines)
lineblendimage=cv2.addWeighted(test_image,0.8,LineImage,1,1)
cv2.imshow("Test",lineblendimage)
cv2.waitKey(0)
