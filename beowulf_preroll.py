#Authors: Daniel Fuller, Brennan Mitchell,
### contact this guy: Trevor Barrus
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
## PRE-ROLL BEOWULF ANIMATION ##
# this version (2) has each rig control name with the prefix "_" 
# because the layout scenes have that (the rig file doesn't)
############################

#This code is brought to you in part by Daniel Fuller and the number 7

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

    beowulf_main = [
    'Beowulf_main_cc_01',
    'Beowulf_secondary_global_cc_01',
    'Beowulf_primary_global_cc_01']

    beowulf_head = [
    'Beowulf_head_cc_01',
    'Beowulf_jaw_cc_01',
    'Beowulf_head_settings_cc_01']

    beowulf_eyes = [
    'Beowulf_LFT_eye_rotate_cc_01', 	#Left
    'Beowulf_LFT_LOW_eyelid_cc_01',	
    'Beowulf_LFT_UPP_eyelid_cc_01',
    'Beowulf_LFT_OUT_eyebrow_cc_01',
    'Beowulf_LFT_MID_eyebrow_cc_01',
    'Beowulf_LFT_INN_eyebrow_cc_01',
    'Beowulf_LFT_MAIN_eyebrow_cc_01',
    'Beowulf_RGT_eye_rotate_cc_01',		#Right
    'Beowulf_RGT_LOW_eyelid_cc_01',	
    'Beowulf_RGT_UPP_eyelid_cc_01',
    'Beowulf_RGT_OUT_eyebrow_cc_01',
    'Beowulf_RGT_MID_eyebrow_cc_01',
    'Beowulf_RGT_INN_eyebrow_cc_01',
    'Beowulf_RGT_MAIN_eyebrow_cc_01',
    'Beowulf_LFT_eye_aim_cc_01',
    'Beowulf_RGT_eye_aim_cc_01',
    'Beowulf_both_eyes_aim_cc_01']
    
    beowulf_mouth = [
    'Beowulf_tongue_tip_cc_01',
    'Beowulf_tongue_middle_cc_01',
    'Beowulf_tongue_root_cc_01',
    'Beowulf_LOW_teeth_cc_01',
    'Beowulf_UPP_teeth_cc_01']

    beowulf_neck = [
    'Beowulf_UPP_neck_cc_01',
    'Beowulf_MID_neck_cc_01',
    'Beowulf_LOW_neck_cc_01',
    'Beowulf_neck_base_cc_01',
    'Beowulf_neck_settings_cc_01']

    beowulf_torso = [
    'Beowulf_spine_settings_cc_01',
    'Beowulf_chest_cc_01',
    'Beowulf_UPP_belly_cc_01',
    'Beowulf_MID_belly_cc_01',
    'Beowulf_LOW_belly_cc_01',
    'Beowulf_COG_cc_01']

    beowulf_arms = [
    'Beowulf_LFT_arm_settings_cc_01',	#Left
    'Beowulf_LFT_IK_arm_cc_01',
    'Beowulf_LFT_arm_pole_vector_cc_01',
    'Beowulf_LFT_clavicle_cc_01',
    'Beowulf_LFT_FK_wrist_cc_01',
    'Beowulf_LFT_FK_lower_arm_cc_01',
    'Beowulf_LFT_FK_upper_arm_cc_01',
    'Beowulf_RGT_arm_settings_cc_01',	#Right
    'Beowulf_RGT_IK_arm_cc_01',
    'Beowulf_RGT_arm_pole_vector_cc_01',
    'Beowulf_RGT_clavicle_cc_01',
    'Beowulf_RGT_FK_wrist_cc_01',
    'Beowulf_RGT_FK_lower_arm_cc_01',
    'Beowulf_RGT_FK_upper_arm_cc_01']    

    beowulf_hands = [
    'Beowulf_LFT_hand_cupping_splaying_cc_01',     #Left
    'Beowulf_LFT_thumb_primary_cc_01',
    'Beowulf_LFT_thumb_MED_secondary_cc_01',
    'Beowulf_LFT_thumb_DIS_secondary_cc_01',
    'Beowulf_LFT_index_finger_primary_cc_01',
    'Beowulf_LFT_index_finger_DIS_secondary_cc_01',
    'Beowulf_LFT_index_finger_MED_secondary_cc_01',
    'Beowulf_LFT_index_metacarpal_secondary_cc_01',
    'Beowulf_LFT_middle_finger_DIS_secondary_cc_01',
    'Beowulf_LFT_middle_finger_MED_secondary_cc_01',
    'Beowulf_LFT_middle_finger_primary_cc_01',
    'Beowulf_LFT_middle_metacarpal_secondary_cc_01',
    'Beowulf_LFT_ring_finger_DIS_secondary_cc_01',
    'Beowulf_LFT_ring_finger_MED_secondary_cc_01',
    'Beowulf_LFT_ring_finger_primary_cc_01',
    'Beowulf_LFT_ring_metacarpal_secondary_cc_01',
    'Beowulf_LFT_pinky_finger_DIS_secondary_cc_01',
    'Beowulf_LFT_pinky_finger_MED_secondary_cc_01',
    'Beowulf_LFT_pinky_finger_primary_cc_01',
    'Beowulf_LFT_pinky_metacarpal_secondary_cc_01',
    'Beowulf_RGT_hand_cupping_splaying_cc_01',	#Right
    'Beowulf_RGT_thumb_primary_cc_01',
    'Beowulf_RGT_thumb_MED_secondary_cc_01',
    'Beowulf_RGT_thumb_DIS_secondary_cc_01',
    'Beowulf_RGT_index_finger_primary_cc_01',
    'Beowulf_RGT_index_finger_DIS_secondary_cc_01',
    'Beowulf_RGT_index_finger_MED_secondary_cc_01',
    'Beowulf_RGT_index_metacarpal_secondary_cc_01',
    'Beowulf_RGT_middle_finger_DIS_secondary_cc_01',
    'Beowulf_RGT_middle_finger_MED_secondary_cc_01',
    'Beowulf_RGT_middle_finger_primary_cc_01',
    'Beowulf_RGT_middle_metacarpal_secondary_cc_01',
    'Beowulf_RGT_ring_finger_DIS_secondary_cc_01',
    'Beowulf_RGT_ring_finger_MED_secondary_cc_01',
    'Beowulf_RGT_ring_finger_primary_cc_01',
    'Beowulf_RGT_ring_metacarpal_secondary_cc_01',
    'Beowulf_RGT_pinky_finger_DIS_secondary_cc_01',
    'Beowulf_RGT_pinky_finger_MED_secondary_cc_01',
    'Beowulf_RGT_pinky_finger_primary_cc_01',
    'Beowulf_RGT_pinky_metacarpal_secondary_cc_01']

    beowulf_hips = [
    'Beowulf_hips_cc_01']

    beowulf_legs_feet = [
    'Beowulf_LFT_leg_settings_cc_01',	#Left
    'Beowulf_LFT_FK_ankle_cc_01',
    'Beowulf_LFT_FK_lower_leg_cc_01',
    'Beowulf_LFT_FK_upper_leg_cc_01',
    'Beowulf_LFT_leg_pole_vector_cc_01',
    'Beowulf_LFT_IK_leg_cc_01',
    'Beowulf_LFT_foot_splaying_cc_01',
    'Beowulf_LFT_foot_ball_cc_01',
    'Beowulf_LFT_big_toe_DIS_secondary_cc_01',
    'Beowulf_LFT_big_toe_MED_secondary_cc_01',
    'Beowulf_LFT_big_toe_primary_cc_01',
    'Beowulf_LFT_foot_ball_cc_01',
    'Beowulf_RGT_leg_settings_cc_01',	#Right
    'Beowulf_RGT_FK_ankle_cc_01',
    'Beowulf_RGT_FK_lower_leg_cc_01',
    'Beowulf_RGT_FK_upper_leg_cc_01',
    'Beowulf_RGT_leg_pole_vector_cc_01',
    'Beowulf_RGT_IK_leg_cc_01',
    'Beowulf_RGT_foot_splaying_cc_01',
    'Beowulf_RGT_foot_ball_cc_01',
    'Beowulf_RGT_big_toe_DIS_secondary_cc_01',
    'Beowulf_RGT_big_toe_MED_secondary_cc_01',
    'Beowulf_RGT_big_toe_primary_cc_01',
    'Beowulf_RGT_foot_ball_cc_01']

    fullRigNoPrefix = beowulf_main + beowulf_head + beowulf_mouth + beowulf_neck + beowulf_torso + beowulf_arms + beowulf_hands + beowulf_hips + beowulf_legs_feet
    fullRig = []
    
    #Create Selection from 'fullRig'
    mc.select(cl=True);
    for i in fullRigNoPrefix:
         # Add name prefix to each control
        i = rigPrefix + i
        fullRig.append(i)
        
    for i in fullRig:
        mc.select(i, add=True)

    return fullRig


def keyArmFK():
    print ">>KeyArmFK() starting"
    leftArmFK = rigPrefix + 'Beowulf_LFT_arm_settings_cc_01.FK_IK'
    
    mc.setAttr(leftArmFK, 0)  #FK mode

    if (mc.getAttr(leftArmFK, keyable=True) or mc.getAttr(leftArmFK, channelBox=True)):
        mc.setKeyframe(leftArmFK);
        

    rightArmFK = rigPrefix + 'Beowulf_RGT_arm_settings_cc_01.FK_IK'

    mc.setAttr(rigPrefix+'Beowulf_RGT_arm_settings_cc_01.FK_IK', 0)  #really not sure about this 

    if (mc.getAttr(rightArmFK, keyable=True) or (mc.getAttr(rightArmFK, channelBox=True))):
        mc.setKeyframe(rightArmFK);

def fingerNames():
    return [
    'Beowulf_LFT_thumb_primary_cc_01',
    'Beowulf_LFT_index_metacarpal_secondary_cc_01',
    'Beowulf_LFT_middle_metacarpal_secondary_cc_01',
    'Beowulf_LFT_ring_metacarpal_secondary_cc_01',
    'Beowulf_LFT_pinky_metacarpal_secondary_cc_01',
    'Beowulf_RGT_thumb_primary_cc_01',
    'Beowulf_RGT_index_metacarpal_secondary_cc_01',
    'Beowulf_RGT_middle_metacarpal_secondary_cc_01',
    'Beowulf_RGT_ring_metacarpal_secondary_cc_01',
    'Beowulf_RGT_pinky_metacarpal_secondary_cc_01'
]
    
def scaleFingers():
    print ">>ScaleFingers() starting"
    for i in fingerNames():
        mc.setAttr(rigPrefix + i + '.scaleX', 1)
        mc.setKeyframe(rigPrefix + i, at='scaleX')

def keyFingers():
    print ">>KeyFingers() starting"
    for i in fingerNames():
	mc.setKeyframe(rigPrefix + i, at='scaleX')
    

def APose():
    print ">>APose() starting"
    #Handle Right Arm
    #   mc.rotate(0, 0, -45, 'ten_rig_main_r_armRoot_FK_CTL')
    mc.rotate(0, 0, -5, rigPrefix + 'Beowulf_LFT_FK_upper_arm_cc_01') #45 degrees seems to be too straight for A-pose...
    #Handle Left Arm
    #   mc.rotate(0, 0, -45, 'ten_rig_main_l_armRoot_FK_CTL')
    mc.rotate(0, 0, -5, rigPrefix + 'Beowulf_RGT_FK_upper_arm_cc_01') 


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

global rigPrefix
rigPrefix = "grendel_rig_main_"  #concatenate this with every other control name

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

#Key APose (Adjust Arms, Keyframe)
APose()
setRigKey(fullRig)

mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='translateX')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='translateY')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='translateZ')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='rotateX')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='rotateY')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='rotateZ')

#Export Alembic (Requires User Input - Select Beowulf's Rig)
mc.playbackOptions(animationStartTime=STARTPRE)
import alembic_exporter
alembic_exporter.go()

