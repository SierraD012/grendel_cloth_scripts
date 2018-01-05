# Authors: Brennan Mitchell, Sierra Davis, Ben Romney
# contact this guy: Ben Romney
# run this one BEFORE the sim script

import os

import maya
import maya.mel as mel #Allows for evaluation of MEL
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment

STARTANIM = 1
STARTPRE = -25
STARTPRE_0 = -50

# Rig Pefix:
prefix0 = 'viking_rig_main_Viking'
prefix1 = 'viking_with_facial_rig_main_Viking'
prefix2 = 'viking_with_facial_rig_main_mb29866846:Viking'

rigPrefix = prefix1


############################
# PRE-ROLL VIKING ANIMATION
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
def selectRig():
    print ">>SelectRig() starting"

    viking_main = [
    rigPrefix + '_main_cc_01',
    rigPrefix + '_secondary_global_cc_01',
    rigPrefix + '_primary_global_cc_01']

    viking_head = [
    rigPrefix + '_head_cc_01',
    rigPrefix + '_jaw_cc_01',
    rigPrefix + '_head_settings_cc_01']

    viking_eyes = [
    rigPrefix + '_LFT_eye_rotate_cc_01', 	#Left
    rigPrefix + '_LFT_LOW_eyelid_cc_01',
    rigPrefix + '_LFT_UPP_eyelid_cc_01',
    rigPrefix + '_LFT_OUT_eyebrow_cc_01',
    rigPrefix + '_LFT_MID_eyebrow_cc_01',
    rigPrefix + '_LFT_INN_eyebrow_cc_01',
    rigPrefix + '_LFT_MAIN_eyebrow_cc_01',
    rigPrefix + '_RGT_eye_rotate_cc_01',		#Right
    rigPrefix + '_RGT_LOW_eyelid_cc_01',
    rigPrefix + '_RGT_UPP_eyelid_cc_01',
    rigPrefix + '_RGT_OUT_eyebrow_cc_01',
    rigPrefix + '_RGT_MID_eyebrow_cc_01',
    rigPrefix + '_RGT_INN_eyebrow_cc_01',
    rigPrefix + '_RGT_MAIN_eyebrow_cc_01',
    rigPrefix + '_LFT_eye_aim_cc_01',
    rigPrefix + '_RGT_eye_aim_cc_01',
    rigPrefix + '_both_eyes_aim_cc_01']

    viking_mouth = [
    rigPrefix + '_tongue_tip_cc_01',
    rigPrefix + '_tongue_middle_cc_01',
    rigPrefix + '_tongue_root_cc_01',
    rigPrefix + '_LOW_teeth_cc_01',
    rigPrefix + '_UPP_teeth_cc_01']

    viking_neck = [
    rigPrefix + '_UPP_neck_cc_01',
    rigPrefix + '_MID_neck_cc_01',
    rigPrefix + '_LOW_neck_cc_01',
    rigPrefix + '_neck_base_cc_01',
    rigPrefix + '_neck_settings_cc_01']

    viking_torso = [
    rigPrefix + '_spine_settings_cc_01',
    rigPrefix + '_chest_cc_01',
    rigPrefix + '_UPP_belly_cc_01',
    rigPrefix + '_MID_belly_cc_01',
    rigPrefix + '_LOW_belly_cc_01',
    rigPrefix + '_COG_cc_01']

    viking_arms = [
    rigPrefix + '_LFT_arm_settings_cc_01',	#Left
    rigPrefix + '_LFT_IK_arm_cc_01',
    rigPrefix + '_LFT_arm_pole_vector_cc_01',
    rigPrefix + '_LFT_clavicle_cc_01',
    rigPrefix + '_LFT_FK_wrist_cc_01',
    rigPrefix + '_LFT_FK_lower_arm_cc_01',
    rigPrefix + '_LFT_FK_upper_arm_cc_01',
    rigPrefix + '_LFT_upper_arm_bendy_cc_01',          #NEW
    rigPrefix + '_LFT_elbow_bendy_cc_01',              #NEW
    rigPrefix + '_LFT_lower_arm_bendy_cc_01',          #NEW
    rigPrefix + '_RGT_arm_settings_cc_01',	#Right
    rigPrefix + '_RGT_IK_arm_cc_01',
    rigPrefix + '_RGT_arm_pole_vector_cc_01',
    rigPrefix + '_RGT_clavicle_cc_01',
    rigPrefix + '_RGT_FK_wrist_cc_01',
    rigPrefix + '_RGT_FK_lower_arm_cc_01',
    rigPrefix + '_RGT_FK_upper_arm_cc_01',
    rigPrefix + '_RGT_upper_arm_bendy_cc_01',          #NEW
    rigPrefix + '_RGT_elbow_bendy_cc_01',              #NEW
    rigPrefix + '_RGT_lower_arm_bendy_cc_01']

    viking_hands = [
    #Note: Viking has no ring finger
    rigPrefix + '_LFT_hand_cupping_splaying_cc_01',     #Left
    rigPrefix + '_LFT_thumb_primary_cc_01',
    rigPrefix + '_LFT_thumb_DIS_secondary_cc_01',
    rigPrefix + '_LFT_index_finger_primary_cc_01',
    rigPrefix + '_LFT_index_finger_DIS_secondary_cc_01',
    rigPrefix + '_LFT_index_metacarpal_secondary_cc_01',
    rigPrefix + '_LFT_middle_finger_DIS_secondary_cc_01',
    rigPrefix + '_LFT_middle_finger_primary_cc_01',
    rigPrefix + '_LFT_middle_metacarpal_secondary_cc_01',
    rigPrefix + '_LFT_pinky_finger_DIS_secondary_cc_01',
    rigPrefix + '_LFT_pinky_finger_primary_cc_01',
    rigPrefix + '_LFT_pinky_metacarpal_secondary_cc_01',
    rigPrefix + '_RGT_hand_cupping_splaying_cc_01',	#Right
    rigPrefix + '_RGT_thumb_primary_cc_01',
    rigPrefix + '_RGT_thumb_DIS_secondary_cc_01',
    rigPrefix + '_RGT_index_finger_primary_cc_01',
    rigPrefix + '_RGT_index_finger_DIS_secondary_cc_01',
    rigPrefix + '_RGT_index_metacarpal_secondary_cc_01',
    rigPrefix + '_RGT_middle_finger_DIS_secondary_cc_01',
    rigPrefix + '_RGT_middle_finger_primary_cc_01',
    rigPrefix + '_RGT_middle_metacarpal_secondary_cc_01',
    rigPrefix + '_RGT_pinky_finger_DIS_secondary_cc_01',
    rigPrefix + '_RGT_pinky_finger_primary_cc_01',
    rigPrefix + '_RGT_pinky_metacarpal_secondary_cc_01']

    viking_hips = [
    rigPrefix + '_hips_cc_01']

    viking_legs_feet = [
    rigPrefix + '_LFT_leg_settings_cc_01',	#Left
    rigPrefix + '_LFT_FK_ankle_cc_01',
    rigPrefix + '_LFT_FK_lower_leg_cc_01',
    rigPrefix + '_LFT_FK_upper_leg_cc_01',
    rigPrefix + '_LFT_leg_pole_vector_cc_01',
    rigPrefix + '_LFT_IK_leg_cc_01',
    rigPrefix + '_LFT_foot_splaying_cc_01',
    rigPrefix + '_LFT_foot_ball_cc_01',
    rigPrefix + '_LFT_big_toe_DIS_secondary_cc_01',
    rigPrefix + '_LFT_big_toe_MED_secondary_cc_01',
    rigPrefix + '_LFT_big_toe_primary_cc_01',
    rigPrefix + '_LFT_foot_ball_cc_01',
    rigPrefix + '_RGT_leg_settings_cc_01',	#Right
    rigPrefix + '_RGT_FK_ankle_cc_01',
    rigPrefix + '_RGT_FK_lower_leg_cc_01',
    rigPrefix + '_RGT_FK_upper_leg_cc_01',
    rigPrefix + '_RGT_leg_pole_vector_cc_01',
    rigPrefix + '_RGT_IK_leg_cc_01',
    rigPrefix + '_RGT_foot_splaying_cc_01',
    rigPrefix + '_RGT_foot_ball_cc_01',
    rigPrefix + '_RGT_big_toe_DIS_secondary_cc_01',
    rigPrefix + '_RGT_big_toe_MED_secondary_cc_01',
    rigPrefix + '_RGT_big_toe_primary_cc_01',
    rigPrefix + '_RGT_foot_ball_cc_01']

    #viking_main +
    fullRig = viking_head + viking_mouth + viking_neck + viking_torso + viking_arms + viking_hands + viking_hips + viking_legs_feet

    #Create Selection from 'fullRig'
    mc.select(fullRig, replace=True)
    return fullRig


def keyArmFK():
    print ">>KeyArmFK() starting"
    #mc.setAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', 1)
    mc.setAttr(rigPrefix + '_LFT_arm_settings_cc_01.FK_IK', 0)  #FK mode

    if (mc.getAttr(rigPrefix + '_LFT_arm_settings_cc_01.FK_IK', keyable=True) or mc.getAttr(rigPrefix + '_LFT_arm_settings_cc_01.FK_IK', channelBox=True)):
        mc.setKeyframe(rigPrefix + '_LFT_arm_settings_cc_01.FK_IK');

    #mc.setAttr('ten_rig_main_r_arm_switch_CTL.IKFK_Switch', 1)
    mc.setAttr(rigPrefix + '_RGT_arm_settings_cc_01.FK_IK', 0)  #really not sure about this

    if (mc.getAttr(rigPrefix + '_RGT_arm_settings_cc_01.FK_IK', keyable=True) or mc.getAttr(rigPrefix + '_RGT_arm_settings_cc_01.FK_IK', channelBox=True)):
        mc.setKeyframe(rigPrefix + '_RGT_arm_settings_cc_01.FK_IK');

def fingerNames():
    #Note: Viking has no ring finger
    return [
    rigPrefix + '_LFT_thumb_primary_cc_01',
    rigPrefix + '_LFT_index_metacarpal_secondary_cc_01',
    rigPrefix + '_LFT_middle_metacarpal_secondary_cc_01',
    rigPrefix + '_LFT_pinky_metacarpal_secondary_cc_01',
    rigPrefix + '_RGT_thumb_primary_cc_01',
    rigPrefix + '_RGT_index_metacarpal_secondary_cc_01',
    rigPrefix + '_RGT_middle_metacarpal_secondary_cc_01',
    rigPrefix + '_RGT_pinky_metacarpal_secondary_cc_01'
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
    mc.rotate(0, 0, -45, rigPrefix + '_LFT_FK_upper_arm_cc_01')
    mc.rotate(0, 0, -45, rigPrefix + '_RGT_FK_upper_arm_cc_01')


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

def clearKeys(rig, startFrame, endFrame):
    cmds.cutKey(rig, time=(startFrame, endFrame))

def translateRig(x, y, z):
    mc.setAttr(rigPrefix + '_primary_global_cc_01.translateX', x)
    mc.setAttr(rigPrefix + '_primary_global_cc_01.translateY', y)
    mc.setAttr(rigPrefix + '_primary_global_cc_01.translateZ', z)

###########################################
#### MAIN ####
###########################################

fullRig = selectRig()

#Remember anim start position
startX = mc.getAttr(rigPrefix + '_primary_global_cc_01.translateX')
startY = mc.getAttr(rigPrefix + '_primary_global_cc_01.translateY')
startZ = mc.getAttr(rigPrefix + '_primary_global_cc_01.translateZ')

#Clear any unnecessary animation (Be Careful!)
#clearKeys(fullRig, STARTPRE_0, STARTANIM - 1)

#Keyframe Initial Frame
mc.currentTime(STARTANIM)
#KEY ARM FK.IK here so it will be at STARTANIM in the mode it's supposed to be (NEW)
mc.setKeyframe(rigPrefix + '_LFT_arm_settings_cc_01.FK_IK');
mc.setKeyframe(rigPrefix + '_RGT_arm_settings_cc_01.FK_IK');

setRigKey(fullRig)

#Get some frames at start pose
mc.currentTime(STARTPRE)
setRigKey(fullRig)

#Clear Transformations
mc.currentTime(STARTPRE_0)
selectRig()
keyArmFK() #this forces it to be in FK mode - could cause an issue if it wasn't originally in that mode

clearRotate(fullRig)
clearTranslate(fullRig)
clearScale(fullRig)

#Move rig to anim start position position
translateRig(startX, startY, startZ)

#APose() -- No need to call APose() because Viking was built in A-Pose
setRigKey(fullRig)

mc.setKeyframe(rigPrefix + '_COG_cc_01', at='translateX')
mc.setKeyframe(rigPrefix + '_COG_cc_01', at='translateY')
mc.setKeyframe(rigPrefix + '_COG_cc_01', at='translateZ')

mc.setKeyframe(rigPrefix + '_COG_cc_01', at='rotateX')
mc.setKeyframe(rigPrefix + '_COG_cc_01', at='rotateY')
mc.setKeyframe(rigPrefix + '_COG_cc_01', at='rotateZ')

#Export Alembic (Requires User Input - Select Viking's Rig)
mc.playbackOptions(animationStartTime=STARTPRE_0)
import alembic_exporter
reload(alembic_exporter)
alembic_exporter.go(cfx=True)
