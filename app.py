import matplotlib.pyplot as plt
import numpy as np
import cv2, os

def onClick( event ):
    global clickNumber, screenPoints, controlPoints
    if clickNumber < 4 :
        point = [ int( event.xdata ), int( event.ydata ) ]
        screenPoints.append( point )
        clickNumber += 1
    elif clickNumber < 8 :
        point = [ int( event.xdata ), int( event.ydata ) ]
        controlPoints.append( point )
        clickNumber += 1
        if clickNumber == 8 :
            processData()
#--------------------------------------------------

def processData() :
    print( 'screenPoints:',  screenPoints )
    print( 'controlPoints:',  controlPoints )
    a = np.array([[screenPoints[0][0], screenPoints[0][1], 1, 0, 0, 0, -realPoints[0][0]*screenPoints[0][0], -realPoints[0][0]*screenPoints[0][1]],
    [screenPoints[1][0], screenPoints[1][1], 1, 0, 0, 0, -realPoints[1][0]*screenPoints[1][0], -realPoints[1][0]*screenPoints[1][1]],
    [screenPoints[2][0], screenPoints[2][1], 1, 0, 0, 0, -realPoints[2][0]*screenPoints[2][0], -realPoints[2][0]*screenPoints[2][1]],
    [screenPoints[3][0], screenPoints[3][1], 1, 0, 0, 0, -realPoints[3][0]*screenPoints[3][0], -realPoints[3][0]*screenPoints[3][1]],
    [0, 0, 0, screenPoints[0][0], screenPoints[0][1], 1, -realPoints[0][1]*screenPoints[0][0], -realPoints[0][1]*screenPoints[0][1]],
    [0, 0, 0, screenPoints[1][0], screenPoints[1][1], 1, -realPoints[1][1]*screenPoints[1][0], -realPoints[1][1]*screenPoints[1][1]],
    [0, 0, 0, screenPoints[2][0], screenPoints[2][1], 1, -realPoints[2][1]*screenPoints[2][0], -realPoints[2][1]*screenPoints[2][1]],
    [0, 0, 0, screenPoints[3][0], screenPoints[3][1], 1, -realPoints[3][1]*screenPoints[3][0], -realPoints[3][1]*screenPoints[3][1]]
    ])


    b = np.array([[realPoints[0][0]],
    [realPoints[1][0]],
    [realPoints[2][0]],
    [realPoints[3][0]],
    [realPoints[0][1]],
    [realPoints[1][1]],
    [realPoints[2][1]],
    [realPoints[3][1]]
    ])

    x = np.linalg.solve(a, b)
    print('Coefficients:\n', x)

    def xr(xm,ym):
        return (x[0]*xm+x[1]*ym+x[2])/(x[6]*xm+x[7]*ym+1)
    def yr(xm,ym):
        return (x[3]*xm+x[4]*ym+x[5])/(x[6]*xm+x[7]*ym+1)

    for point in controlPoints:
        xm = point[0]
        ym=point[1]
        print(point, int(10*xr(xm,ym))/10,int(10*yr(xm,ym))/10 )

    cv2.destroyAllWindows()
#--------------------------------------------------

inputFolder = 'img'
myFiles = os.listdir( inputFolder )
myFiles = [ file for file in myFiles if '.png' in file ]
myText = ''
myNumber = 0
for myFile in myFiles :
    myNumber += 1
    myText += '%2d - %s\n' % ( myNumber, myFile )
myText += 30 * '-' + '\n'
myText += 'select a file...'
myFileName = myFiles[ int( input( myText ) ) - 1 ]
print( myFileName )
myFile = os.path.join( inputFolder, myFileName )
#-------------------

clickNumber = 0
screenPoints = []
controlPoints = []
realPoints = [ [3,5], [19,4], [5,11], [15,10] ]

plt.figure().canvas.callbacks.connect( 'button_press_event', onClick )
myImage = plt.imread( myFile )
plt.imshow( myImage )
plt.axis( "off" )
plt.subplots_adjust( left = 0.0, right = 1.0, top = 1.0, bottom = 0.0 )
plt.show()