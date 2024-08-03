import cv2
import numpy as np 
import mediapipe as mp
import pygame
import time 
# Initializing Pygame mixer
pygame.mixer.init()
# Load the sound
s1=pygame.mixer.Sound("Plants vs Zombies Soundtrack. .mp3")
s2=pygame.mixer.Sound("Pop Bubble Sound Effect 2022.mp3")
#######################
audio_started = False
##### sound system##############
start=0
change =1
score=0
life=5
toe=1
hand=mp.solutions.hands
p=hand.Hands(model_complexity=0,min_detection_confidence=.5,min_tracking_confidence=.5)
vid=cv2.VideoCapture(0)
 
#######################
start_time = time.time()
#######################

bubble1=cv2.imread("download.jpeg")
bubble1=cv2.resize(bubble1,(100,100))
bubble2=cv2.imread("OIP.jpeg")
bubble2=cv2.resize(bubble2,(100,100))
bubble3=cv2.imread("download.jpeg")
bubble3=cv2.resize(bubble3,(100,100))
bubble4=cv2.imread("OIP.jpeg")
bubble4=cv2.resize(bubble4,(100,100))
co_1=0
co_2=0
co_3=0
co_4=0
axis1=np.random.randint(20,280)
axis2=np.random.randint(60,350)
axis3=np.random.randint(120,420)
axis4=np.random.randint(220,450)
while vid.isOpened()==True:
    r,f=vid.read()
    if r==True:
        if co_1>=485 or co_2 >=485 or co_3 >=485 or co_4>=485:#max increament is 15 in co_
            co_1=0
            co_2=0
            co_3=0
            co_4=0
        f=cv2.flip(f,1)
        x1,y1=co_1,co_1+100
        x2,y2=co_2,co_2+100
        x3,y3=co_3,co_3+100
        x4,y4=co_4,co_4+100
        xx1,yy1=axis1-50,axis1+50
        xx2,yy2=axis2-50,axis2+50
        xx3,yy3=axis3-50,axis3+50
        xx4,yy4=axis4-50,axis4+50
        imp=np.ones((600,600,3),dtype=np.uint8)*255
        ex1,ey1,_=imp[x1:y1,xx1:yy1].shape
        ex2,ey2,_=imp[x2:y2,xx2:yy2].shape
        ex3,ey3,_=imp[x3:y3,xx3:yy3].shape
        ex4,ey4,_=imp[x4:y4,xx4:yy4].shape
        # if ex1 !=100 or ex2!=100 or ex3!=100 or ex4 !=100 or ey1 !=100 or ey2 !=100 or ey3!=100 or ey4 !=100:
        #     print("pass")
        #     continue
        imp[x1:y1,xx1:yy1]=bubble1 
        imp[x2:y2,xx2:yy2]=bubble2 
        imp[x3:y3,xx3:yy3]=bubble3 
        imp[x4:y4,xx4:yy4]=bubble4
       
        imp=cv2.copyMakeBorder(imp,10,10,10,10,cv2.BORDER_REFLECT_101)
        cv2.flip(f,-1)
        f=cv2.resize(f,(620,620))
        #cv2.imshow("imAGE",imp)
        f=cv2.bitwise_and(f,imp)
        f=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        final=p.process(f)#1
        f=cv2.cvtColor(f,cv2.COLOR_RGB2BGR)
        x8=y8=0
        if final.multi_hand_landmarks:#2
            for l in final.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(f,l,hand.HAND_CONNECTIONS)
                h,w,_=f.shape
                x8,y8=int(l.landmark[8].x*w),int(l.landmark[8].y*h)
        ###
	     
        cv2.circle(f,(x8,y8),3,(0,255,0),-1)
        cv2.rectangle(f,(450,3),(600,73),(0,255,0),2)
        cv2.putText(f,"START",(450,30),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),4)
        cv2.rectangle(f,(50,3),(240,73),(0,255,0),2)
        cv2.putText(f,f"SCORE={score}",(50,30),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),4)
        cv2.rectangle(f,(280,3),(420,73),(0,255,0),2)
        cv2.putText(f,f"LIVES={life}",(280,30),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),4)
        # cv2.rectangle(f,(axis1-50,co_1),(axis1+50,co_1+100),(255,0,0),2)
        if life<=0:
            start =0
            cv2.rectangle(f,(100,200),(500,400),(45,78,213),-1)
            cv2.putText(f,"GAME OVER ",(100,250),cv2.FONT_ITALIC,1,(202,25,120),4)
            cv2.putText(f,f" HIGH SCORE ={score}",(100,300),cv2.FONT_ITALIC,1,(202,25,120),4)
            #########    retry option  ##########
        if 450<x8<600 and 3<y8<73:
            start=1
            toe=0
            co_1=0
            co_2=0
            co_3=0
            co_4=0
            life=5
            score=0
        if start ==1:
            if axis1-50<x8<axis1+50 and co_1<y8<co_1+100:
                co_1=0
                s2.play()
                score=score+1
                axis1=np.random.randint(50,450)
                 
            elif co_2<y8<co_2+100 and axis2-50<x8<axis2+50:
                co_2=0
                s2.play()
                score=score+1
                axis2=np.random.randint(50,450)
                 
            elif co_3<y8<co_3+100 and axis3-50<x8<axis3+50:
                co_3=0
                s2.play()
                score=score+1
                axis3=np.random.randint(50,450)
                 
            elif co_4<y8<co_4+100 and axis4-50<x8<axis4+50:
                co_4=0
                s2.play()
                score=score+1
                axis4=np.random.randint(50,450)
                 
            if change:
                cv2.rectangle(f,(450,3),(600,73),(255,0,0),2)
                cv2.putText(f,"START",(450,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),4)
                change =(change+1)%10
            else:
                cv2.rectangle(f,(450,3),(600,73),(0,0,255),2)
                cv2.putText(f,"START",(450,30),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),4)
                change =change+1
                
        ###
        if toe==1:
            cv2.rectangle(f,(100,200),(500,400),(45,78,213),-1)
            cv2.putText(f,"CREATED BY ",(100,250),cv2.FONT_ITALIC,1,(102,25,120),4)
            cv2.putText(f,"   Yogendra kumawat",(100,300),cv2.FONT_ITALIC,1,(202,25,120),4)    
            cv2.putText(f,"      2023 KUEC 2018",(100,350),cv2.FONT_ITALIC,1,(202,25,120),4)    

        
        f=cv2.resize(f,(1370,700))        
        cv2.imshow("fg",f)
        # Play the sound
        if not audio_started:
            s1.play(-1)
            audio_started=True
        # cv2.imshow("f",imp)
        if co_1>470:
            co_1=co_1+1
        else:    
            co_1=co_1+7
        if co_1>=485:
            co_1=0
            if start==1:
                life=life-1
                if life<=0:
                    start =0
            axis1=np.random.randint(50,450)
        if co_2>470:
            co_2=co_2+1
        else:    
            co_2=co_2+7
        if co_2>=485:
            co_2=0
            if start==1:
                life=life-1
                if life<=0:
                    start =0
            axis2=np.random.randint(50,450) 
        if co_3>470:
            co_3=co_3+1
        else:    
            co_3=co_3+7
        if co_3>=485:
            if start==1:
                life=life-1
                if life<=0:
                    start =0
            co_3=0
            axis3=np.random.randint(50,450)
        if co_4>470:
            co_4=co_4+1
        else: 
            co_4=co_4+7
        
        if co_4>=485:
            if start==1:
                life=life-1
                if life<=0:
                    start =0
            co_4=0
            axis4=np.random.randint(50,450) 
        if score>100:
            co_1=co_1+7
            co_2=co_2+7
            co_3=co_3+7
            co_4=co_4+7
        elif score>200:
            co_1=co_1+9
            co_2=co_2+9
            co_3=co_3+9
            co_4=co_4+9
        elif score>300:
            co_1=co_1+11
            co_2=co_2+11
            co_3=co_3+11
            co_4=co_4+11   
        cv2.waitKey(1) & 0xff==ord(" ")
                   
    else:
        break
vid.release()
s1.stop()

cv2.destroyAllWindows()
