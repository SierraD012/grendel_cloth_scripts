#Authors: Daniel Fuller, Brennan Mitchell
import os

'''
This script should be run in a FINISHED (or at least splined) animation file.

The Final line of code opens the alembic exporter, so I've commented it out. MAKE SURE THE PRE-ROLL IS SMOOTH/CLEAN. No self-collisions, no stepping.

Once that's all set up you can run the Alembic Exporter personally from the toolbar or with the last line of code.
'''


import maya
import maya.mel as mel #Allows for evaluation of MEL
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment


############################
## PRE-ROLL TEN ANIMATION ##
############################

#This code is brought to you in part by Daniel Fuller and the number 7

#Clears Rotation on a List of Objects
def clearRotate(list):
    for i in list:
        if mc.getAttr(i + '.rotateX', settable=True):
            mc.setAttr(i + '.rotateX', 0)
        else:
            print "*******************************************" + str(i) + '.rotateX'
        if mc.getAttr(i + '.rotateY', settable=True):
            mc.setAttr(i + '.rotateY', 0)
        else:
            print "*******************************************" + str(i) + '.rotateX'
        if mc.getAttr(i + '.rotateZ', settable=True):
            mc.setAttr(i + '.rotateZ', 0)
        else:
            print "*******************************************" + str(i) + '.rotateX'

#Clears Translation on a List of Objects
def clearTranslate(list):
    for i in list:
        if mc.getAttr(i + '.translateX', settable=True):
            mc.setAttr(i + '.translateX', 0)
        else:
            print "*******************************************" + str(i) + '.translateX'
        if mc.getAttr(i + '.translateY', settable=True):   
            mc.setAttr(i + '.translateY', 0)
        else:
            print "*******************************************" + str(i) + '.translateY'
        if mc.getAttr(i + '.translateZ', settable=True):
            mc.setAttr(i + '.translateZ', 0)
        else:
            print "*******************************************" + str(i) + '.translateZ'

#Selects/Returns Full Rig
def selectRig():
    ten_head = [
    'ten_rig_main_head_cc_01',
    'ten_rig_main_head_top_squash_cc_01',
    'ten_rig_main_head_mid_squash_cc_01',
    'ten_rig_main_head_bottom_squash_cc_01']
    
    ten_eyebrows = [
    'ten_rig_main_eyebrow_r_full_cc_01', #Right
    'ten_rig_main_eyebrow_r_OUT_cc_01',
    'ten_rig_main_eyebrow_r_MID_cc_01',
    'ten_rig_main_eyebrow_r_INN_cc_01',
    'ten_rig_main_eyebrow_l_full_cc_01', #Left
    'ten_rig_main_eyebrow_l_OUT_cc_01',
    'ten_rig_main_eyebrow_l_MID_cc_01',
    'ten_rig_main_eyebrow_l_INN_cc_01']
    
    ten_eyes = [
    'ten_rig_main_eye_r_full_cc_01', #Right
    'ten_rig_main_r_upper_eyelid_CTL',
    'ten_rig_main_r_upper_eyelid_tweaker_CTL', #Legacy: suffix '1'
    'ten_rig_main_r_lower_eyelid_CTL',
    'ten_rig_main_r_lower_eyelid_tweaker_CTL',
    'ten_rig_main_eye_r_cc_01',
    'ten_rig_main_pupil_r_cc_01',
    'ten_rig_main_eye_l_full_cc_01', #Left
    'ten_rig_main_l_upper_eyelid_CTL',
    'ten_rig_main_l_upper_eyelid_tweaker_CTL',
    'ten_rig_main_l_lower_eyelid_CTL',
    'ten_rig_main_l_lower_eyelid_tweaker_CTL',
    'ten_rig_main_eye_l_cc_01',
    'ten_rig_main_pupil_l_cc_01',
    'ten_rig_main_m_eyes_CTL', #Lookat
    'ten_rig_main_r_eye_CTL',
    'ten_rig_main_l_eye_CTL']
    
    ten_squint = [
    'ten_rig_main_squint_r_full_cc_01', #Right
    'ten_rig_main_squint_r_OUT_cc_01',
    'ten_rig_main_squint_r_MID_cc_01',
    'ten_rig_main_squint_r_INN_cc_01',
    'ten_rig_main_squint_l_full_cc_01', #Left
    'ten_rig_main_squint_l_OUT_cc_01',
    'ten_rig_main_squint_l_MID_cc_01',
    'ten_rig_main_squint_l_INN_cc_01']
    
    ten_ears = [
    'ten_rig_main_ear_r_cc_01', #Right
    'ten_rig_main_earlobe_r_cc_01',
    'ten_rig_main_ear_l_cc_01', #Left
    'ten_rig_main_earlobe_l_cc_01']
    
    ten_nose = [
    'ten_rig_main_nose_full_cc_01',
    'ten_rig_main_nostril_sneer_r_cc_01',
    'ten_rig_main_nostril_sneer_l_cc_01',
    'ten_rig_main_nose_tip_cc_01']
    
    ten_mouth = [
    'ten_rig_main_mouth_full_cc_01',
    'ten_rig_main_lips_r_corner_cc_01',
    'ten_rig_main_lips_l_corner_cc_01']
    
    ten_lips = [
    'ten_rig_main_upper_lip_full_cc_01', #Top
    'ten_rig_main_upper_lip_RGT_cc_01',
    'ten_rig_main_upper_lip_MID_cc_01',
    'ten_rig_main_upper_lip_LFT_cc_01',
    'ten_rig_main_lower_lip_full_cc_01', #Bottom
    'ten_rig_main_lower_lip_RGT_cc_01',
    'ten_rig_main_lower_lip_MID_cc_01',
    'ten_rig_main_lower_lip_LFT_cc_01']
    
    ten_cheeks_chin = [
    'ten_rig_main_cheek_r_cc_01',
    'ten_rig_main_cheek_l_cc_01',
    'ten_rig_main_jaw_cc_01']
    
    ten_neck_abdomen = [
    'ten_rig_main_m_neck_CTL',
    'ten_rig_main_m_spine_FKchest_CTL',
    'ten_rig_main_m_IKSpinyThing_CTL',
    'ten_rig_main_m_spine_FKstomach_CTL']
    
    ten_arms = [
    'ten_rig_main_r_shoulder_CTL', #Right
    'ten_rig_main_r_armRoot_FK_CTL',
    'ten_rig_main_r_armMid_FK_CTL',
    'ten_rig_main_r_armEnd_FK_CTL',
    'ten_rig_main_r_arm_switch_CTL',
    'ten_rig_main_l_shoulder_CTL', #Left
    'ten_rig_main_l_armRoot_FK_CTL',
    'ten_rig_main_l_armMid_FK_CTL',
    'ten_rig_main_l_armEnd_FK_CTL',
    'ten_rig_main_l_arm_switch_CTL']
    
    ten_hands = [
    'ten_rig_main_r_hand_CTL', #Right
    'ten_rig_main_r_thumb_CTL',
    'ten_rig_main_r_index_CTL',
    'ten_rig_main_r_middle_CTL',
    'ten_rig_main_r_ring_CTL',
    'ten_rig_main_r_pinky_CTL',
    'ten_rig_main_l_hand_CTL', #Left
    'ten_rig_main_l_thumb_CTL',
    'ten_rig_main_l_index_CTL',
    'ten_rig_main_l_middle_CTL',
    'ten_rig_main_l_ring_CTL',
    'ten_rig_main_l_pinky_CTL']
    
    ten_hips = [
    'ten_rig_main_m_spine_hips_CTL',
    'ten_rig_main_m_COG_CTL']
    
    ten_legs_feet = [
    'ten_rig_main_r_legIK_CTL', #Right
    'ten_rig_main_r_foot_CTL',
    'ten_rig_main_r_legPV_CTL',
    'ten_rig_main_l_legIK_CTL', #Left
    'ten_rig_main_l_foot_CTL',
    'ten_rig_main_l_legPV_CTL']
    
    fullRig = ten_head + ten_eyebrows + ten_eyes + ten_squint + ten_ears + ten_nose + ten_mouth + ten_lips + ten_cheeks_chin + ten_neck_abdomen + ten_arms + ten_hands + ten_hips + ten_legs_feet
    
    #Create Selection from 'fullRig'
    mc.select(fullRig, replace=True)
    return fullRig

def keyArmFK():
    mc.setAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', 1)

    if (mc.getAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', keyable=True) or mc.getAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', channelBox=True)):
        mc.setKeyframe('ten_rig_main_l_arm_switch_CTL.IKFK_Switch');
        
    mc.setAttr('ten_rig_main_r_arm_switch_CTL.IKFK_Switch', 1)

    if (mc.getAttr('ten_rig_main_r_arm_switch_CTL.IKFK_Switch', keyable=True) or mc.getAttr('ten_rig_main_r_arm_switch_CTL.IKFK_Switch', channelBox=True)):
        mc.setKeyframe('ten_rig_main_r_arm_switch_CTL.IKFK_Switch');

def scaleFingers():
    fingers = [
    'ten_rig_main_l_hand_CTL',
    'ten_rig_main_l_thumb_CTL',
    'ten_rig_main_l_index_CTL',
    'ten_rig_main_l_middle_CTL',
    'ten_rig_main_l_ring_CTL',
    'ten_rig_main_l_pinky_CTL',
    'ten_rig_main_r_hand_CTL',
    'ten_rig_main_r_thumb_CTL',
    'ten_rig_main_r_index_CTL',
    'ten_rig_main_r_middle_CTL',
    'ten_rig_main_r_ring_CTL',
    'ten_rig_main_r_pinky_CTL']
    
    for i in fingers:
        mc.setAttr(i + '.scaleX', 1)
	mc.setKeyframe(i, at='scaleX')


def APose():
    #Handle Right Arm
    mc.rotate(0, 0, -45, 'ten_rig_main_r_armRoot_FK_CTL')
    #Handle Left Arm
    mc.rotate(0, 0, -45, 'ten_rig_main_l_armRoot_FK_CTL')

def setRigKey(fullRig):
    #Key Translation
    mc.setKeyframe(fullRig, at='translateX')
    mc.setKeyframe(fullRig, at='translateY')
    mc.setKeyframe(fullRig, at='translateZ')
    #Key Rotation
    mc.setKeyframe(fullRig, at='rotateX')
    mc.setKeyframe(fullRig, at='rotateY')
    mc.setKeyframe(fullRig, at='rotateZ')

#Keyframe Initial Frame
mc.currentTime(0)
fullRig = selectRig()
setRigKey(fullRig)

#Set T-Pose (Clear Transformations)
mc.currentTime(-20)

selectRig()
keyArmFK()

clearRotate(fullRig)
clearTranslate(fullRig)

scaleFingers() #Scale Fingers (Only Scalable Control)

#Key APose (Adjust Arms, Keyframe)
APose()
setRigKey(fullRig)


mc.setKeyframe('ten_rig_main_m_COG_CTL', at='translateX') #Hip Controller Not Working?
mc.setKeyframe('ten_rig_main_m_COG_CTL', at='translateY')
mc.setKeyframe('ten_rig_main_m_COG_CTL', at='translateZ')

mc.setKeyframe('ten_rig_main_m_COG_CTL', at='rotateX')
mc.setKeyframe('ten_rig_main_m_COG_CTL', at='rotateY')
mc.setKeyframe('ten_rig_main_m_COG_CTL', at='rotateZ')

mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='translateX') #Shoulder Controller Not Working?
mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='translateY')
mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='translateZ')

mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='rotateX')
mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='rotateY')
mc.setKeyframe('ten_rig_main_r_shoulder_CTL', at='rotateZ')


#Export Alembic (Requires User Input - Select Ten's Rig)
mc.playbackOptions(animationStartTime=-20)
import alembic_exporter
#alembic_exporter.go() #This is the alembic exporter. Use at own risk.
