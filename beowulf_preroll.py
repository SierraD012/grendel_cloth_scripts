#Authors: Daniel Fuller, Brennan Mitchell,

import os

import maya
import maya.mel as mel #Allows for evaluation of MEL
import maya.cmds as mc

from byuam.project import Project
from byuam.environment import Department, Environment

STARTANIM = -5 
STARTPRE = -50


############################
## PRE-ROLL BEOWULF ANIMATION ##
# this version (2) has each rig control name with the prefix "_"
# because the layout scenes have that (the rig file doesn't)
############################

# If you come across a shot where the rig's primary control is far away from the actual mesh for some reason
# you can go far back in the preroll and set a keyframe on the primary control at a position really close to
# where the mesh will start at frame 0, so then when you run this script the character mesh will be at A-pose
# really close to where it should be at frame 0. This makes it so you don't have to deal with the mesh
# flying 500 units over to its start point during preroll.


#Clears Rotation on a List of Objects
def clearRotate(list):
    print (">>ClearRotate() starting")
    for i in list:
        if mc.getAttr(i + '.rotateX', settable=True):
            mc.setAttr(i + '.rotateX', 0)
        else:
            print ('************ Skipping ' + str(i) + '.rotateX')

        if mc.getAttr(i + '.rotateY', settable=True):
            mc.setAttr(i + '.rotateY', 0)
        else:
            print ('************ Skipping ' + str(i) + '.rotateY')

        if mc.getAttr(i + '.rotateZ', settable=True):
            mc.setAttr(i + '.rotateZ', 0)
        else:
            print ('************ Skipping ' + str(i) + '.rotateZ')

#Clears Translation on a List of Objects
def clearTranslate(list):
    print (">>ClearTranslate() starting")
    for i in list:
        if mc.getAttr(i + '.translateX', settable=True):
            mc.setAttr(i + '.translateX', 0)
        else:
            print ('************ Skipping ' + str(i) + '.translateX')

        if mc.getAttr(i + '.translateY', settable=True):
            mc.setAttr(i + '.translateY', 0)
        else:
            print ('************ Skipping ' + str(i) + '.translateY')

        if mc.getAttr(i + '.translateZ', settable=True):
            mc.setAttr(i + '.translateZ', 0)
        else:
	        print ('************ Skipping ' + str(i) + '.translateZ')

#Clears Scale on a List of Objects
def clearScale(list):
    print (">>ClearScale() starting")
    for i in list:
        if mc.getAttr(i + '.scaleX', settable=True):
            mc.setAttr(i + '.scaleX', 1)
        else:
            print ('************ Skipping ' + str(i) + '.scaleX')

        if mc.getAttr(i + '.scaleY', settable=True):
            mc.setAttr(i + '.scaleY', 1)
        else:
            print ('************ Skipping ' + str(i) + '.scaleY')

        if mc.getAttr(i + '.scaleZ', settable=True):
            mc.setAttr(i + '.scaleZ', 1)
        else:
            print ('************ Skipping ' + str(i) + '.scaleZ')


#Selects/Returns Full Rig
# update: it looks like all the accessories + beard go with the transformation, so that's cool
def selectRig():
    print (">>SelectRig() starting")

    #these are what moves the entire rig group - if we skip these the rig will move from A-pose to scene start pose without flying back from origin
    #beowulf_main = [
    #'Beowulf_main_cc_01',
    #'Beowulf_secondary_global_cc_01',
    #'Beowulf_primary_global_cc_01']

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

    #beowulf_main +
    fullRigNoPrefix = beowulf_head + beowulf_mouth + beowulf_neck + beowulf_torso + beowulf_arms + beowulf_hands + beowulf_hips + beowulf_legs_feet
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
    print (">>KeyArmFK() starting")
    leftArmFK = rigPrefix + 'Beowulf_LFT_arm_settings_cc_01.FK_IK'

    mc.setAttr(leftArmFK, 0)  #FK mode

    if (mc.getAttr(leftArmFK, keyable=True) or mc.getAttr(leftArmFK, channelBox=True)):
        mc.setKeyframe(leftArmFK);


    rightArmFK = rigPrefix + 'Beowulf_RGT_arm_settings_cc_01.FK_IK'

    mc.setAttr(rightArmFK, 0)

    if (mc.getAttr(rightArmFK, keyable=True) or (mc.getAttr(rightArmFK, channelBox=True))):
        mc.setKeyframe(rightArmFK);

def fingerNames():
    baseFingerNames = [
    'Beowulf_LFT_thumb_primary_cc_01',
    'Beowulf_LFT_index_metacarpal_secondary_cc_01',
    'Beowulf_LFT_middle_metacarpal_secondary_cc_01',
    'Beowulf_LFT_ring_metacarpal_secondary_cc_01',
    'Beowulf_LFT_pinky_metacarpal_secondary_cc_01',
    'Beowulf_RGT_thumb_primary_cc_01',
    'Beowulf_RGT_index_metacarpal_secondary_cc_01',
    'Beowulf_RGT_middle_metacarpal_secondary_cc_01',
    'Beowulf_RGT_ring_metacarpal_secondary_cc_01',
    'Beowulf_RGT_pinky_metacarpal_secondary_cc_01' ]
    completeFingerNames = []

    for i in baseFingerNames:
         # Add name prefix to each finger name
        i = rigPrefix + i
        completeFingerNames.append(i)

    return completeFingerNames

def scaleFingers():
    print (">>ScaleFingers(): starting")
    for i in fingerNames():
        mc.setAttr(i + '.scaleX', 1)
        mc.setKeyframe(rigPrefix + i, at='scaleX')

def keyFingers():
    print (">>KeyFingers(): starting")
    for i in fingerNames():
	    mc.setKeyframe(i, at='scaleX')


def APose():
    print (">>APose(): starting")
    #Handle Right Arm
    mc.rotate(0, 0, 0, rigPrefix + 'Beowulf_LFT_FK_upper_arm_cc_01') #so far, we don't seem to need to rotate the arms to get them to match the collision mesh arms
    #Handle Left Arm
    mc.rotate(0, 0, 0, rigPrefix + 'Beowulf_RGT_FK_upper_arm_cc_01')
    print (">>APose(): done")


def setRigKey(fullRig):
    print (">>SetRigKey(): starting")
    #Key Translation
    mc.setKeyframe(fullRig, at='translateX')
    mc.setKeyframe(fullRig, at='translateY')
    mc.setKeyframe(fullRig, at='translateZ')
    #Key Rotation
    mc.setKeyframe(fullRig, at='rotateX')
    mc.setKeyframe(fullRig, at='rotateY')
    mc.setKeyframe(fullRig, at='rotateZ')

    keyFingers()
    print (">>SetRigKey(): done")

#Used to constrain the clasps/chain on the front of the cape to Beowulf's chest rig control
#this is kind of a fake sim, we should probably just use it when the chain is not directly visible!
def constrainCapeChain():
    # Create a global position locator for Beowulf's main rig control location
    globalPos = mc.spaceLocator(p=[0,0,0])
    globPos = mc.rename(globalPos, "beowulfGlobalPos")
    mc.select(rigPrefix+"Beowulf_primary_global_cc_01")
    mc.select(globPos, add=True)
    mc.pointConstraint(offset=[0,0,0], weight=1) #constrains the globPos position to where Beowulf's rig_main is
    mc.orientConstraint(offset=[0,0,0], weight=1) #orients the globPos to match Beowulf's rig_main (I think it just does the rotation)

    # Get transformation variables from globPos locator
    tx = mc.getAttr(globPos+".translateX")
    ty = mc.getAttr(globPos+".translateY")
    tz = mc.getAttr(globPos+".translateZ")
    rx = mc.getAttr(globPos+".rotateX")
    ry = mc.getAttr(globPos+".rotateY")
    rz = mc.getAttr(globPos+".rotateZ")
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.translateX", tx)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.translateY", ty)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.translateZ", tz)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.rotateX", rx)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.rotateY", ry)
    mc.setAttr("beowulf_cape_model_main_Beowulf_Cape.rotateZ", rz)

    #Hide meshes we don't want to work with right now
    mc.hide('beowulf_cape_model_main_beowulf_cape_simMesh')
    mc.hide('beowulf_cape_model_main_beowulf_cape_beautyMesh')

    #Select & combine the clasps & chain meshes
    mc.select("beowulf_cape_model_main_beowulf_cape_clasps", replace=True)
    mc.select("beowulf_cape_model_main_beowulf_cape_clasp_chain", add=True) #not really necessary to select these two
    mc.polyUnite("beowulf_cape_model_main_beowulf_cape_clasps", "beowulf_cape_model_main_beowulf_cape_clasp_chain", name="beowulf_cape_model_main_beowulf_capeChain_combined")
    #center the combined object's pivot so we can rotate it to look more normal
    mc.xform("beowulf_cape_model_main_beowulf_capeChain_combined", centerPivots=True)
    #mc.setAttr("beowulf_cape_model_main_beowulf_capeChain_combined.rotateZ", -16.0) #probably need to tweak this every time

    #Select the rig control we want to parent the chain/clasp to
    mc.select(rigPrefix+"Beowulf_chest_cc_01", replace=True)
    #Now select the chainCombined object
    mc.select("beowulf_cape_model_main_beowulf_capeChain_combined", add=True)

    #Create parent constraint: (targetObject, childObject)
    mc.parentConstraint(rigPrefix+"Beowulf_chest_cc_01", "beowulf_cape_model_main_beowulf_capeChain_combined", maintainOffset=1, weight=1.0)
    mc.select("beowulf_cape_model_main_beowulf_capeChain_combined", replace=True)
    mc.rotate(-7.8375, 0.4445, 6.725, 'beowulf_cape_model_main_beowulf_capeChain_combined', objectSpace=True)

    #Hide original chain/clasp because we don't need them for this part
    mc.hide('beowulf_cape_model_main_beowulf_cape_clasps')
    mc.hide('beowulf_cape_model_main_beowulf_cape_clasp_chain')

    #Export an alembic of just the chaingroup in the ANIM folder for this shot with the name:  beowulf_cape_chain_main.abc - you probably have to do this manually

###########################################
#### MAIN ####
###########################################
# Reference Beowulf's Cape - it comes with both sim and beauty meshes
project = Project()
environment = Environment()
body = project.get_body("beowulf_cape")
element = body.get_element(Department.MODEL)
cape_sim_file = element.get_app_filepath()
mc.file(cape_sim_file, reference=True)
global rigPrefix
rigPrefix = "beowulf_rig_main_"  #concatenate this with every other control name

#Keyframe Initial Frame
mc.currentTime(STARTANIM)
fullRig = selectRig()
setRigKey(fullRig)

#KEY ARM FK.IK here so it will be at frame 0 in the mode the animators intended - this may not be necessary every time
mc.setKeyframe(rigPrefix + 'Beowulf_LFT_arm_settings_cc_01.FK_IK');
mc.setKeyframe(rigPrefix + 'Beowulf_RGT_arm_settings_cc_01.FK_IK');

#Set T-Pose (Clear Transformations)
mc.currentTime(STARTPRE)
mc.playbackOptions(minTime=STARTPRE)

selectRig()
keyArmFK()

clearRotate(fullRig)
clearTranslate(fullRig)
clearScale(fullRig)

#Key APose (Adjust Arms, Keyframe)
APose() #this may not be necessary for Beowulf's model
setRigKey(fullRig)

mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='translateX')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='translateY')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='translateZ')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='rotateX')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='rotateY')
mc.setKeyframe(rigPrefix + 'Beowulf_COG_cc_01', at='rotateZ')


#Since we have Beowulf's rig available right now, let's constrain the cape chain/clasps
#to his rig right now and export an alembic of that (you probs need to do that manually since we can't ABC tag it)
constrainCapeChain()

#Export full mesh alembic - Just Beowulf's geo
mc.playbackOptions(animationStartTime=STARTPRE)
#Tag Beowulf's geo only for alembic export:
mc.select(rigPrefix + "Beowulf_geo_GRP_01", replace = True)
import alembic_tagger;
alembic_tagger.go()
#Export alembic of just Beowulf's geo
import alembic_exporter
alembic_exporter.go(dept=Department.CFX) # puts abc in the cfx file instead

#Export alembic of just the cape chain - might need do this manually because the ABC Exporter doesn't know how to find the tag on this one since it's not a reference
#AbcExport -j "-frameRange -30 120 -step 0.25 -dataFormat ogawa -root |beowulf_cape_model_main_beowulf_capeChain_combined -file /groups/grendel/production/shots/b023/anim/main/cache/beowulf_capeChain.abc";
#EXPORT TO CFX FOLDER WITH THIS NAME: beowulf_cape_chain_main.abc
#Now you should probably publish this shot too
