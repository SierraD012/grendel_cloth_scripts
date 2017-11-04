#Authors: Daniel Fuller, Brennan Mitchell, Trevor Barrus, Ben Romney
### contact this guy: Ben Romney
# run this one BEFORE the sim script

import os

import maya
import maya.mel as mel #Allows for evaluation of MEL
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment

STARTANIM = -5
STARTPRE = -25


############################
## PRE-ROLL VIKING ANIMATION ##
# this version has each rig control name with the prefix "viking_rig_main_" 
# because the layout scenes have that (the rig file doesn't)
############################

#Clears Rotation on a List of Objects
def clearRotate(list):
    print '>>ClearRotate() starting'
    for i in list:
        if mc.getAttr(i + '.rotateX', settable=True):
            mc.setAttr(i + '.rotateX', 0)
        else:
            print '************ Skipping ' + str(i) + '.rotateX'

        if mc.getAttr(i + '.rotateY', settable=True):
            mc.setAttr(i + '.rotateY', 0)
        else:
            print '************ Skipping ' + str(i) + '.rotateY'

        if mc.getAttr(i + '.rotateZ', settable=True):
            mc.setAttr(i + '.rotateZ', 0)
        else:
            print '************ Skipping ' + str(i) + '.rotateZ'

#Clears Translation on a List of Objects
def clearTranslate(list):
    print ">>ClearTranslate() starting"
    for i in list:
        if mc.getAttr(i + '.translateX', settable=True):
            mc.setAttr(i + '.translateX', 0)
        else:
	    print '************ Skipping ' + str(i) + '.translateX' 
        
	if mc.getAttr(i + '.translateY', settable=True):   
            mc.setAttr(i + '.translateY', 0)
        else:
	    print '************ Skipping ' + str(i) + '.translateY'
       
	if mc.getAttr(i + '.translateZ', settable=True):
            mc.setAttr(i + '.translateZ', 0)
        else:
	    print '************ Skipping ' + str(i) + '.translateZ'

#Clears Scale on a List of Objects
def clearScale(list):
    print ">>ClearScale() starting"
    for i in list:
        if mc.getAttr(i + '.scaleX', settable=True):
            mc.setAttr(i + '.scaleX', 1)

        else:
	    print '************ Skipping ' + str(i) + '.scaleX' 
        
	if mc.getAttr(i + '.scaleY', settable=True):   
            mc.setAttr(i + '.scaleY', 1)
        else:
	    print '************ Skipping ' + str(i) + '.scaleY'
       
	if mc.getAttr(i + '.scaleZ', settable=True):

            mc.setAttr(i + '.scaleZ', 1)
        else:
	    print '************ Skipping ' + str(i) + '.scaleZ'


#Selects/Returns Full Rig
#TODO: What about accessories? do we need to clear transformations on those too?
# update: it looks like all the accessories + beard go with the transformation, so that's cool 
def selectRig():
    print ">>SelectRig() starting"

    viking_main = [
    'viking_rig_main_Viking_main_cc_01',
    'viking_rig_main_Viking_secondary_global_cc_01',
    'viking_rig_main_Viking_primary_global_cc_01']

    viking_head = [
    'viking_rig_main_Viking_head_cc_01',
    'viking_rig_main_Viking_jaw_cc_01',
    'viking_rig_main_Viking_head_settings_cc_01']

    viking_eyes = [
    'viking_rig_main_Viking_LFT_eye_rotate_cc_01', 	#Left
    'viking_rig_main_Viking_LFT_LOW_eyelid_cc_01',	
    'viking_rig_main_Viking_LFT_UPP_eyelid_cc_01',
    'viking_rig_main_Viking_LFT_OUT_eyebrow_cc_01',
    'viking_rig_main_Viking_LFT_MID_eyebrow_cc_01',
    'viking_rig_main_Viking_LFT_INN_eyebrow_cc_01',
    'viking_rig_main_Viking_LFT_MAIN_eyebrow_cc_01',
    'viking_rig_main_Viking_RGT_eye_rotate_cc_01',		#Right
    'viking_rig_main_Viking_RGT_LOW_eyelid_cc_01',	
    'viking_rig_main_Viking_RGT_UPP_eyelid_cc_01',
    'viking_rig_main_Viking_RGT_OUT_eyebrow_cc_01',
    'viking_rig_main_Viking_RGT_MID_eyebrow_cc_01',
    'viking_rig_main_Viking_RGT_INN_eyebrow_cc_01',
    'viking_rig_main_Viking_RGT_MAIN_eyebrow_cc_01',
    'viking_rig_main_Viking_LFT_eye_aim_cc_01',
    'viking_rig_main_Viking_RGT_eye_aim_cc_01',
    'viking_rig_main_Viking_both_eyes_aim_cc_01']
    
    viking_mouth = [
    'viking_rig_main_Viking_tongue_tip_cc_01',
    'viking_rig_main_Viking_tongue_middle_cc_01',
    'viking_rig_main_Viking_tongue_root_cc_01',
    'viking_rig_main_Viking_LOW_teeth_cc_01',
    'viking_rig_main_Viking_UPP_teeth_cc_01']

    viking_neck = [
    'viking_rig_main_Viking_UPP_neck_cc_01',
    'viking_rig_main_Viking_MID_neck_cc_01',
    'viking_rig_main_Viking_LOW_neck_cc_01',
    'viking_rig_main_Viking_neck_base_cc_01',
    'viking_rig_main_Viking_neck_settings_cc_01']

    viking_torso = [
    'viking_rig_main_Viking_spine_settings_cc_01',
    'viking_rig_main_Viking_chest_cc_01',
    'viking_rig_main_Viking_UPP_belly_cc_01',
    'viking_rig_main_Viking_MID_belly_cc_01',
    'viking_rig_main_Viking_LOW_belly_cc_01',
    'viking_rig_main_Viking_COG_cc_01']

    viking_arms = [
    'viking_rig_main_Viking_LFT_arm_settings_cc_01',	#Left
    'viking_rig_main_Viking_LFT_IK_arm_cc_01',
    'viking_rig_main_Viking_LFT_arm_pole_vector_cc_01',
    'viking_rig_main_Viking_LFT_clavicle_cc_01',
    'viking_rig_main_Viking_LFT_FK_wrist_cc_01',
    'viking_rig_main_Viking_LFT_FK_lower_arm_cc_01',
    'viking_rig_main_Viking_LFT_FK_upper_arm_cc_01',
    'viking_rig_main_Viking_RGT_arm_settings_cc_01',	#Right
    'viking_rig_main_Viking_RGT_IK_arm_cc_01',
    'viking_rig_main_Viking_RGT_arm_pole_vector_cc_01',
    'viking_rig_main_Viking_RGT_clavicle_cc_01',
    'viking_rig_main_Viking_RGT_FK_wrist_cc_01',
    'viking_rig_main_Viking_RGT_FK_lower_arm_cc_01',
    'viking_rig_main_Viking_RGT_FK_upper_arm_cc_01']    

    viking_hands = [
    'viking_rig_main_Viking_LFT_hand_cupping_splaying_cc_01',     #Left
    'viking_rig_main_Viking_LFT_thumb_primary_cc_01',
    'viking_rig_main_Viking_LFT_thumb_MED_secondary_cc_01',
    'viking_rig_main_Viking_LFT_thumb_DIS_secondary_cc_01',
    'viking_rig_main_Viking_LFT_index_finger_primary_cc_01',
    'viking_rig_main_Viking_LFT_index_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_LFT_index_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_LFT_index_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_LFT_middle_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_LFT_middle_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_LFT_middle_finger_primary_cc_01',
    'viking_rig_main_Viking_LFT_middle_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_LFT_ring_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_LFT_ring_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_LFT_ring_finger_primary_cc_01',
    'viking_rig_main_Viking_LFT_ring_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_LFT_pinky_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_LFT_pinky_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_LFT_pinky_finger_primary_cc_01',
    'viking_rig_main_Viking_LFT_pinky_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_hand_cupping_splaying_cc_01',	#Right
    'viking_rig_main_Viking_RGT_thumb_primary_cc_01',
    'viking_rig_main_Viking_RGT_thumb_MED_secondary_cc_01',
    'viking_rig_main_Viking_RGT_thumb_DIS_secondary_cc_01',
    'viking_rig_main_Viking_RGT_index_finger_primary_cc_01',
    'viking_rig_main_Viking_RGT_index_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_RGT_index_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_RGT_index_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_middle_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_RGT_middle_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_RGT_middle_finger_primary_cc_01',
    'viking_rig_main_Viking_RGT_middle_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_ring_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_RGT_ring_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_RGT_ring_finger_primary_cc_01',
    'viking_rig_main_Viking_RGT_ring_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_pinky_finger_DIS_secondary_cc_01',
    'viking_rig_main_Viking_RGT_pinky_finger_MED_secondary_cc_01',
    'viking_rig_main_Viking_RGT_pinky_finger_primary_cc_01',
    'viking_rig_main_Viking_RGT_pinky_metacarpal_secondary_cc_01']

    viking_hips = [
    'viking_rig_main_Viking_hips_cc_01']

    viking_legs_feet = [
    'viking_rig_main_Viking_LFT_leg_settings_cc_01',	#Left
    'viking_rig_main_Viking_LFT_FK_ankle_cc_01',
    'viking_rig_main_Viking_LFT_FK_lower_leg_cc_01',
    'viking_rig_main_Viking_LFT_FK_upper_leg_cc_01',
    'viking_rig_main_Viking_LFT_leg_pole_vector_cc_01',
    'viking_rig_main_Viking_LFT_IK_leg_cc_01',
    'viking_rig_main_Viking_LFT_foot_splaying_cc_01',
    'viking_rig_main_Viking_LFT_foot_ball_cc_01',
    'viking_rig_main_Viking_LFT_big_toe_DIS_secondary_cc_01',
    'viking_rig_main_Viking_LFT_big_toe_MED_secondary_cc_01',
    'viking_rig_main_Viking_LFT_big_toe_primary_cc_01',
    'viking_rig_main_Viking_LFT_foot_ball_cc_01',
    'viking_rig_main_Viking_RGT_leg_settings_cc_01',	#Right
    'viking_rig_main_Viking_RGT_FK_ankle_cc_01',
    'viking_rig_main_Viking_RGT_FK_lower_leg_cc_01',
    'viking_rig_main_Viking_RGT_FK_upper_leg_cc_01',
    'viking_rig_main_Viking_RGT_leg_pole_vector_cc_01',
    'viking_rig_main_Viking_RGT_IK_leg_cc_01',
    'viking_rig_main_Viking_RGT_foot_splaying_cc_01',
    'viking_rig_main_Viking_RGT_foot_ball_cc_01',
    'viking_rig_main_Viking_RGT_big_toe_DIS_secondary_cc_01',
    'viking_rig_main_Viking_RGT_big_toe_MED_secondary_cc_01',
    'viking_rig_main_Viking_RGT_big_toe_primary_cc_01',
    'viking_rig_main_Viking_RGT_foot_ball_cc_01']

    fullRig = viking_main + viking_head + viking_mouth + viking_neck + viking_torso + viking_arms + viking_hands + viking_hips + viking_legs_feet
    
    #Create Selection from 'fullRig'
    mc.select(fullRig, replace=True)
    return fullRig


def keyArmFK():
    print ">>KeyArmFK() starting"
    #mc.setAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', 1)
    mc.setAttr('viking_rig_main_Viking_LFT_arm_settings_cc_01.FK_IK', 0)  #FK mode

    if (mc.getAttr('viking_rig_main_Viking_LFT_arm_settings_cc_01.FK_IK', keyable=True) or mc.getAttr('viking_rig_main_Viking_LFT_arm_settings_cc_01.FK_IK', channelBox=True)):
        mc.setKeyframe('viking_rig_main_Viking_LFT_arm_settings_cc_01.FK_IK');
        

   # mc.setAttr('ten_rig_main_r_arm_switch_CTL.IKFK_Switch', 1) 
    mc.setAttr('viking_rig_main_Viking_RGT_arm_settings_cc_01.FK_IK', 0)  #really not sure about this 

    if (mc.getAttr('viking_rig_main_Viking_RGT_arm_settings_cc_01.FK_IK', keyable=True) or mc.getAttr('viking_rig_main_Viking_RGT_arm_settings_cc_01.FK_IK', channelBox=True)):
        mc.setKeyframe('viking_rig_main_Viking_RGT_arm_settings_cc_01.FK_IK');

def fingerNames():
    return [
    'viking_rig_main_Viking_LFT_thumb_primary_cc_01',
    'viking_rig_main_Viking_LFT_index_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_LFT_middle_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_LFT_ring_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_LFT_pinky_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_thumb_primary_cc_01',
    'viking_rig_main_Viking_RGT_index_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_middle_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_ring_metacarpal_secondary_cc_01',
    'viking_rig_main_Viking_RGT_pinky_metacarpal_secondary_cc_01'
]
    
def scaleFingers():
    print ">>ScaleFingers() starting"
    for i in fingerNames():
        mc.setAttr(i + '.scaleX', 1)
        mc.setKeyframe(i, at='scaleX')

def keyFingers():
    print ">>KeyFingers() starting"
    for i in fingerNames():
	mc.setKeyframe(i, at='scaleX')
    

def APose():
    print ">>APose() starting"
    #Handle Right Arm
    #   mc.rotate(0, 0, -45, 'ten_rig_main_r_armRoot_FK_CTL')
    mc.rotate(0, 0, -5, 'viking_rig_main_Viking_LFT_FK_upper_arm_cc_01') #45 degrees seems to be too straight for A-pose...
    #Handle Left Arm
    #   mc.rotate(0, 0, -45, 'ten_rig_main_l_armRoot_FK_CTL')
    mc.rotate(0, 0, -5, 'viking_rig_main_Viking_RGT_FK_upper_arm_cc_01') 


def setRigKey(fullRig):
    print ">>SetRigKey() starting"
    #Key Translation
    mc.setKeyframe(fullRig, at='translateX')
    mc.setKeyframe(fullRig, at='translateY')
    mc.setKeyframe(fullRig, at='translateZ')
    #Key Rotation
    mc.setKeyframe(fullRig, at='rotateX')
    mc.setKeyframe(fullRig, at='rotateY')
    mc.setKeyframe(fullRig, at='rotateZ')
    
    keyFingers()


###########################################
#### MAIN ####
###########################################

#Keyframe Initial Frame
mc.currentTime(STARTANIM)
fullRig = selectRig()
setRigKey(fullRig)

#Set T-Pose (Clear Transformations)
mc.currentTime(STARTPRE)

selectRig()
keyArmFK()

clearRotate(fullRig)
clearTranslate(fullRig)
clearScale(fullRig)


#scaleFingers() #Scale Fingers (Only Scalable Control)
 #might not need this since we have clearScale()

#Key APose (Adjust Arms, Keyframe)
APose()
setRigKey(fullRig)



mc.setKeyframe('viking_rig_main_Viking_COG_cc_01', at='translateX')
mc.setKeyframe('viking_rig_main_Viking_COG_cc_01', at='translateY')
mc.setKeyframe('viking_rig_main_Viking_COG_cc_01', at='translateZ')
#mc.setKeyframe('ten_rig_main_m_COG_CTL', at='translateX') #Hip Controller Not Working?  <-- existing comment
#mc.setKeyframe('ten_rig_main_m_COG_CTL', at='translateY')
#mc.setKeyframe('ten_rig_main_m_COG_CTL', at='translateZ')

mc.setKeyframe('viking_rig_main_Viking_COG_cc_01', at='rotateX')
mc.setKeyframe('viking_rig_main_Viking_COG_cc_01', at='rotateY')
mc.setKeyframe('viking_rig_main_Viking_COG_cc_01', at='rotateZ')
#mc.setKeyframe('ten_rig_main_m_COG_CTL', at='rotateX')
#mc.setKeyframe('ten_rig_main_m_COG_CTL', at='rotateY')
#mc.setKeyframe('ten_rig_main_m_COG_CTL', at='rotateZ')

# I'm not sure why these are in here, just the right shoulder?
#mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='translateX') #Shoulder Controller Not Working?   <-- existing comment
#mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='translateY')
#mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='translateZ')

#Export Alembic (Requires User Input - Select Ten's Rig)
mc.playbackOptions(animationStartTime=STARTPRE)
import alembic_exporter
alembic_exporter.go()

