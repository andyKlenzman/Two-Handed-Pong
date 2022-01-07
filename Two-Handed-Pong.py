#okay Im trying to get a paddle to correspond to the hands. Maybe do an if statment inside
#of the class to discern between left and right....Will somehow need to parse the label
#and have the data paired with it.

#got the second paddle. Time to add the ball. I will simplify the movement and make it cognizant of the paddles
#you know what, Im going to make a distinction between the movemnent and animation.
#next time, build a simple ball animation library and then another
#one for the movement.

#Right now Im working on breaking the code into simpler classes...maybe now would be a good time to do
#some better planning. 
#Ill keep working on this tomorrow, the planning was actually quite fun to do, I love seeing the machines I am building on paper.
#next up, I will start building up. It will be difficult integrating it with all the arrays and experimental formatting
#stretch yourself by being as precise as possible on these sketches, 
#

#made some progress trying to focus on transmitting data with arrays. needless to say, I am confused, but over time it will begin to work
#
#
#


import cv2
import time

width=640
height=360
paddleHitMarker=0


class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        
        if results.multi_hand_landmarks != None:
            
            for hand in results.multi_handedness:
                handType=hand.classification[0].label

                print(handType)
                handsType.append(handType)
            
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        
        return(myHands,handsType)


class Paddle:
    def __init__(self, pw, ph, pc, pl, hc):
        self.paddleWidth=pw
        self.paddleHeight=ph
        self.paddleColor=pc
        self.paddleLine=pl
        self.handControl=hc
        self.paddlePos=0

    def rpaddlePlay(self,frame,handData, handsType):
        for hand,handType in zip(handData,handsType):
            self.paddlePos=int(hand[self.handControl][1]-self.paddleWidth/2)
            if handType=="Right":

                cv2.rectangle(frame,(width,(self.paddlePos)),(width-self.paddleWidth,(self.paddlePos+self.paddleHeight)),self.paddleColor,
                self.paddleLine)

        #defining the far left, far right, and height of the paddle.... 
        #added double to the far paddle positions for some fucking reason.
        self.paddlePosLeft=self.paddlePos-(self.paddleLine*2)
        self.paddlePosRight=self.paddlePos+self.paddleWidth+(self.paddleLine*2)
        self.paddlePosSurface=self.paddleHeight+self.paddleLine

        return(self.paddlePosRight,self.paddlePosLeft,self.paddlePosSurface) 
    
    def lpaddlePlay(self,frame,handData,handsType):
        for hand,handType in zip(handData,handsType):
            
            self.paddlePos=int(hand[self.handControl][1]-self.paddleWidth/2)

            if handType=="Left":
                cv2.rectangle(frame,(0,(self.paddlePos)),(0+self.paddleWidth,(self.paddlePos+self.paddleHeight)),self.paddleColor,self.paddleLine)

        #defining the far left, far right, and height of the paddle.... 
        #added double to the far paddle positions for some fucking reason.
        self.paddlePosLeft=self.paddlePos-(self.paddleLine*2)
        self.paddlePosRight=self.paddlePos+self.paddleWidth+(self.paddleLine*2)
        self.paddlePosSurface=self.paddleHeight+self.paddleLine

        return(self.paddlePosRight,self.paddlePosLeft,self.paddlePosSurface) 


#ball characteristics
#color, radius, thickness, line
ballFeatures=[[0,255,0],5,1,1]



class Ball:
    def __init__(self, ballFeatures):
        self.ballFeatures=ballFeatures
        
    def ballAnimation(self, frame, ballFeatures, ballPosition):
        self.ballFeatures=ballFeatures
        #create variables from the parsed out array, could I use a dictionary here to make it more readable?
        cv2.circle(frame,ballPosition,ballFeatures[1],ballFeatures[0],ballFeatures[2],ballFeatures[3])      

class ballMove:
    def __init__(self):
        #ballPosition is half the width and height
        self.ballPosition=[width/2,height/2]

    def ballPhysics(self):

        def xFunction(self, ballPosition, xPace):
            self.xPos=self.ballPosition[0]
            self.xPos=self.xPos+xPace
            if self.xPos >= width or self.xPos <= 0:
                xPace=-(xPace)
            self.ballPosition[0]=self.xPos
        
        def yFunction(self, ballPosition, yPace):
            self.yPos=self.ballPosition[1]
            self.yPos=self.yPos+yPace
            if self.yPos >= height or self.yPos <= 0:
                yPace=-(yPace)
            self.ballPosition[1]=self.yPos

        self.xVal=xFunction(self.ballPosition, xPace=10)
        self.yVal=yFunction(self.ballPosition, yPace=10)

        self.ballPosition[0]=self.xVal
        self.ballPosition[1]=self.yVal
        return(self.ballPosition)


rPaddleWidth=10
rPaddleHeight=75
rPaddleColor=(100,255,100)
rPaddleLine=10
rPaddleHandControl=12
rPaddlePos=0


ball=Ball(ballFeatures)
movement=ballMove()
paddleR=Paddle(rPaddleWidth,rPaddleHeight,rPaddleColor,rPaddleLine,rPaddleHandControl)
paddleL=Paddle(rPaddleWidth,rPaddleHeight,rPaddleColor,rPaddleLine,rPaddleHandControl)
findHands=mpHands()
cam=cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
handColor=(0,0,0)

while True:
    ignore, frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    frame = cv2.flip(frame, 1)
    
    handData, handsType=findHands.Marks(frame)
    for hand,handType in zip(handData,handsType):
        if handType=='Right':
            handColor=(255,0,0)
        if handType=='Left':
            handColor=(0,255,0)
        for ind in [9]:
            cv2.circle(frame,hand[ind],15, handColor ,2)

    finalBallPosition=movement.ballPhysics()
    ball.ballAnimation(frame,ballFeatures,finalBallPosition)
    paddleR.rpaddlePlay(frame, handData, handsType)
    paddleL.lpaddlePlay(frame, handData, handsType)


    
    cv2.imshow('beauty',frame)
    cv2.moveWindow('beauty', 0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()