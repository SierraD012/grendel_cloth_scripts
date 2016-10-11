import maya.mel as mel #Allows for evaluation of MEL
import pymel.core as pc #Allows for evaluation of MEL
import maya.cmds as mc

#Clears Rotation on a List of Objects
def clearRotate(list):
    for i in list:
        if mc.getAttr(i + '.rotateX', settable=True):
            mc.setAttr(i + '.rotateX', 0)
        if mc.getAttr(i + '.rotateY', settable=True):
            mc.setAttr(i + '.rotateY', 0)
        if mc.getAttr(i + '.rotateZ', settable=True):
            mc.setAttr(i + '.rotateZ', 0) 

#Clears Translation on a List of Objects
def clearTranslate(list):
    for i in list:
        if mc.getAttr(i + '.translateX', settable=True):
            mc.setAttr(i + '.translateX', 0)
        if mc.getAttr(i + '.translateY', settable=True):   
            mc.setAttr(i + '.translateY', 0)
        if mc.getAttr(i + '.translateZ', settable=True):
            mc.setAttr(i + '.translateZ', 0)

#Selects/Returns Full Rig
def selectRig():

    ten_body_controls = [
    "ten_rig_main_l_armEnd_FK_CTL",
    "ten_rig_main_l_armIK_CTL",
    "ten_rig_main_l_armMid_FK_CTL",
    "ten_rig_main_l_armPV_CTL",
    "ten_rig_main_l_armRoot_FK_CTL",
    "ten_rig_main_l_arm_switch_CTL",
    "ten_rig_main_l_eye_CTL",
    "ten_rig_main_l_foot_CTL",
    "ten_rig_main_l_hand_CTL",
    "ten_rig_main_l_index_CTL",
    "ten_rig_main_l_legIK_CTL",
    "ten_rig_main_l_legPV_CTL",
    "ten_rig_main_l_leg_end_FK_CTL",
    "ten_rig_main_l_leg_mid_FK_CTL",
    "ten_rig_main_l_leg_root_FK_CTL",
    "ten_rig_main_l_lower_eyelid_CTL",
    "ten_rig_main_l_middle_CTL",
    "ten_rig_main_l_pinky_CTL",
    "ten_rig_main_l_ring_CTL",
    "ten_rig_main_l_shoulder_CTL",
    "ten_rig_main_l_thumb_CTL",
    "ten_rig_main_m_COG_CTL",
    "ten_rig_main_m_IKSpinyThing_CTL",
    "ten_rig_main_m_eyes_CTL",
    #"ten_rig_main_m_global_CTL", TEN'S POSITION - DO NOT PREROLL
    "ten_rig_main_m_head_CTL",
    "ten_rig_main_m_jaw_CTL",
    #"ten_rig_main_m_mouth_position_CTL",
    "ten_rig_main_m_neck_CTL",
    "ten_rig_main_m_spine_FKchest_CTL",
    "ten_rig_main_m_spine_FKstomach_CTL",
    "ten_rig_main_m_spine_hips_CTL",
    "ten_rig_main_r_armEnd_FK_CTL",
    "ten_rig_main_r_armIK_CTL",
    "ten_rig_main_r_armMid_FK_CTL",
    "ten_rig_main_r_armPV_CTL",
    "ten_rig_main_r_armRoot_FK_CTL",
    "ten_rig_main_r_arm_switch_CTL",
    "ten_rig_main_r_eye_CTL",
    "ten_rig_main_r_foot_CTL",
    "ten_rig_main_r_hand_CTL",
    "ten_rig_main_r_index_CTL",
    "ten_rig_main_r_legIK_CTL",
    "ten_rig_main_r_legPV_CTL",
    "ten_rig_main_r_leg_end_FK_CTL",
    "ten_rig_main_r_leg_mid_FK_CTL",
    "ten_rig_main_r_leg_root_FK_CTL",
    "ten_rig_main_r_lower_eyelid_CTL",
    "ten_rig_main_r_middle_CTL",
    #"ten_rig_main_r_mouth_corner_CTL",
    "ten_rig_main_r_pinky_CTL",
    "ten_rig_main_r_ring_CTL",
    "ten_rig_main_r_shoulder_CTL",
    "ten_rig_main_r_thumb_CTL"]
    
    ten_head_controls = [
    "ten_rig_main_cheek_l_cc_01",
    "ten_rig_main_cheek_r_cc_01",
    "ten_rig_main_ear_l_cc_01",
    "ten_rig_main_ear_r_cc_01",
    "ten_rig_main_earlobe_l_cc_01",
    "ten_rig_main_earlobe_r_cc_01",
    "ten_rig_main_eye_l_cc_01",
    "ten_rig_main_eye_l_full_cc_01",
    "ten_rig_main_eye_r_cc_01",
    "ten_rig_main_eye_r_full_cc_01",
    "ten_rig_main_eyebrow_l_INN_cc_01",
    "ten_rig_main_eyebrow_l_MID_cc_01",
    "ten_rig_main_eyebrow_l_OUT_cc_01",
    "ten_rig_main_eyebrow_l_full_cc_01",
    "ten_rig_main_eyebrow_r_INN_cc_01",
    "ten_rig_main_eyebrow_r_MID_cc_01",
    "ten_rig_main_eyebrow_r_OUT_cc_01",
    "ten_rig_main_eyebrow_r_full_cc_01",
    "ten_rig_main_head_bottom_squash_cc_01",
    "ten_rig_main_head_cc_01","ten_rig_main_head_mid_squash_cc_01",
    "ten_rig_main_head_top_squash_cc_01",
    "ten_rig_main_intermediate_ear_l_cc_01",
    "ten_rig_main_intermediate_ear_r_cc_01",
    "ten_rig_main_intermediate_earlobe_l_cc_01",
    "ten_rig_main_intermediate_earlobe_r_cc_01",
    "ten_rig_main_intermediate_eye_l_full_cc_01",
    "ten_rig_main_intermediate_eye_r_full_cc_01",
    "ten_rig_main_intermediate_head_bottom_squash_cc_01",
    "ten_rig_main_intermediate_head_mid_squash_cc_01",
    "ten_rig_main_intermediate_head_top_squash_cc_01",
    "ten_rig_main_intermediate_mouth_full_cc_01",
    "ten_rig_main_jaw_cc_01",
    "ten_rig_main_lips_l_corner_cc_01",
    "ten_rig_main_lips_r_corner_cc_01",
    "ten_rig_main_lower_lip_LFT_cc_01",
    "ten_rig_main_lower_lip_MID_cc_01",
    "ten_rig_main_lower_lip_RGT_cc_01",
    "ten_rig_main_lower_lip_full_cc_01",
    "ten_rig_main_mouth_full_cc_01",
    "ten_rig_main_nose_full_cc_01",
    "ten_rig_main_nose_tip_cc_01",
    "ten_rig_main_nostril_sneer_l_cc_01",
    "ten_rig_main_nostril_sneer_r_cc_01",
    "ten_rig_main_pupil_l_cc_01",
    "ten_rig_main_pupil_r_cc_01",
    "ten_rig_main_squint_l_INN_cc_01",
    "ten_rig_main_squint_l_MID_cc_01",
    "ten_rig_main_squint_l_OUT_cc_01",
    "ten_rig_main_squint_l_cc_01",
    "ten_rig_main_squint_l_full_cc_01",
    "ten_rig_main_squint_r_INN_cc_01",
    "ten_rig_main_squint_r_MID_cc_01",
    "ten_rig_main_squint_r_OUT_cc_01",
    "ten_rig_main_squint_r_cc_01",
    "ten_rig_main_squint_r_full_cc_01",
    "ten_rig_main_upper_lip_LFT_cc_01",
    "ten_rig_main_upper_lip_MID_cc_01",
    "ten_rig_main_upper_lip_RGT_cc_01",
    "ten_rig_main_upper_lip_full_cc_01"]
    
    #Assemble Full Rig
    fullRig = ten_head_controls + ten_body_controls
    
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

def oldKeyArmIKFK(preRoll):
    #Right Arm
    #Check initial IKFK State
    mc.currentTime(0)
    if mc.getAttr('ten_rig_main_r_arm_switch_CTL.IKFK_Switch') == 0:
        #Set Arm as FK
        mc.setAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', 1)
        
        if (mc.getAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', keyable=True) or mc.getAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', channelBox=True)):
            mc.setKeyframe('ten_rig_main_l_arm_switch_CTL.IKFK_Switch');
        
        
        
        #Set IKFK at zero
        mc.setKeyframe('ten_rig_main_r_arm_switch_CTL.IKFK_Switch')
        #Set IKFK at preRoll
        mc.currentTime(preRoll)
        mc.setAttr('ten_rig_main_r_arm_switch_CTL.IKFK_Switch', 1)
        mc.setKeyframe('ten_rig_main_r_arm_switch_CTL.IKFK_Switch')
    
    #Left Arm
    #Check initial IKFK State
    mc.currentTime(0)
    if mc.getAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch') == 0:
        #Set IKFK at zero
        mc.setKeyframe('ten_rig_main_l_arm_switch_CTL.IKFK_Switch')
        #Set IKFK at preRoll
        mc.currentTime(preRoll)
        mc.setAttr('ten_rig_main_l_arm_switch_CTL.IKFK_Switch', 1)
        mc.setKeyframe('ten_rig_main_l_arm_switch_CTL.IKFK_Switch')

def APose():
    #Handle Right Arm
    mc.rotate(0, 0, -40, 'ten_rig_main_r_armRoot_FK_CTL')
    #Handle Left Arm
    mc.rotate(0, 0, -40, 'ten_rig_main_l_armRoot_FK_CTL')

def setRigKey(fullRig):
    #Key Translation
    mc.setKeyframe(fullRig, at='translateX')
    mc.setKeyframe(fullRig, at='translateY')
    mc.setKeyframe(fullRig, at='translateZ')
    #Key Rotation
    mc.setKeyframe(fullRig, at='rotateX')
    mc.setKeyframe(fullRig, at='rotateY')
    mc.setKeyframe(fullRig, at='rotateZ')
    
def alignToRigLoc(object):
    mc.setAttr(object + '.translateX', mc.getAttr('ten_rig_main_m_global_CTL.translateX'))
    mc.setAttr(object + '.translateY', mc.getAttr('ten_rig_main_m_global_CTL.translateY'))
    mc.setAttr(object + '.translateZ', mc.getAttr('ten_rig_main_m_global_CTL.translateZ'))
    
    mc.setAttr(object + '.rotateX', mc.getAttr('ten_rig_main_m_global_CTL.rotateX'))
    mc.setAttr(object + '.rotateY', mc.getAttr('ten_rig_main_m_global_CTL.rotateY'))
    mc.setAttr(object + '.rotateZ', mc.getAttr('ten_rig_main_m_global_CTL.rotateZ'))
    
##############
# BEGIN CODE #
##############

#Set current time to -20
mc.currentTime(-20)

#Collect Full Rig
fullRig = selectRig()

#Keyframe Arm IKFK
keyArmFK()

#Set TPose (Clear Transformations)
clearRotate(fullRig)
clearTranslate(fullRig)

#Clear Move CTL Rotation
mc.setAttr('ten_rig_main_m_global_CTL.rotateX', 0)
mc.setAttr('ten_rig_main_m_global_CTL.rotateY', 0)
mc.setAttr('ten_rig_main_m_global_CTL.rotateZ', 0)

#Set APose (Adjust Arms)
APose()

#Key fullRig
setRigKey(fullRig)

#Key Move CTL
mc.setKeyframe('ten_rig_main_m_global_CTL', at='rotateX')
mc.setKeyframe('ten_rig_main_m_global_CTL', at='rotateY')
mc.setKeyframe('ten_rig_main_m_global_CTL', at='rotateZ')

#Import/Move Cloth OBJ
mc.file('/groups/dusk/production/assets/ten_robe_sim/model/main/ten_robe_sim_model_main.mb', i=True)
alignToRigLoc('ten_Robe_Sim')
alignToRigLoc('ten_Pants_Sim')
alignToRigLoc('ten_Collider')
alignToRigLoc('ten_Mittens')
alignToRigLoc('ten_Sash_Sim')

#Wrap Ten Collider to Rig
mc.select('ten_Collider', replace=True)
mc.select('ten_rig_main_Ten_Skin_RENDER', add=True)
mc.CreateWrap()

#Wrap Mittens to Collider
mc.select('ten_Mittens', replace=True)
mc.select('ten_Collider', add=True)
mc.CreateWrap()

#Set Up Ten Collider
mc.select('ten_Collider', replace=True)
mel.eval('makeCollideNCloth;')

#Set Up Mittens Collider
mc.select('ten_Mittens', replace=True)
mel.eval('makeCollideNCloth;')

#Set Up Cloth
mc.select('ten_Robe_Sim', replace=True)
mel.eval('createNCloth 0;')

#Set Cloth Parameters
mc.setAttr('nClothShape1.thickness', 0.003)
mc.setAttr('nClothShape1.stretchResistance', 200)
mc.setAttr('nClothShape1.friction', .3)
mc.setAttr('nClothShape1.bendAngleDropoff', 0.4)
mc.setAttr('nClothShape1.pointMass', 0.6)
mc.setAttr('nClothShape1.damp', 0.8)
mc.setAttr('nClothShape1.scalingRelation', 1) #Scaling Relation to "Object Space"

#Set Nucleus Parameters
mc.setAttr('nucleus1.startFrame', -20)
mc.setAttr('nucleus1.spaceScale', 0.45)
mc.setAttr('nucleus1.subSteps', 6)
mc.setAttr('nucleus1.maxCollisionIterations', 8)

#Set Up Pin Constraints
mc.select('ten_Robe_Sim.vtx[2310:2334]', 'ten_Robe_Sim.vtx[3088:3111]', replace=True)
mc.select('ten_Robe_Sim.vtx[699:701]', 'ten_Robe_Sim.vtx[1652]', 'ten_Robe_Sim.vtx[1691]', 'ten_Robe_Sim.vtx[1694]', 'ten_Robe_Sim.vtx[1725]', add=True)
mc.select('ten_Collider', toggle=True)
mel.eval('createNConstraint pointToSurface 0;')

#Cache Out the Cloth Sim
filepath = '/users/animation/mitchbre/Documents/Cloth_Script_Files/Test_Cache'
shapeRelatives = mc.listRelatives('ten_Robe_Sim', shapes=True)
print shapeRelatives
mc.cacheFile(fileName='tenRobe_cache', format='OneFilePerFrame', startTime=-20, endTime=186, points=shapeRelatives[1], directory=filepath)

#Connect the Cloth Cache
mc.currentTime(-20)
pc.mel.doImportCacheFile(filepath + '/tenRobe_cache.xml', '', ['ten_Robe_Sim'], list())


#Group Colliders
mc.group(['ten_Collider', 'ten_ColliderBase', 'ten_Mittens', 'nRigid1', 'nRigid2'], name='colliders')

#Group Robe
mc.group(['ten_Robe_Sim','ten_Sash_Sim'], name='robe_Objects' ) #Objects
mc.group(['nCloth1','dynamicConstraint1'], name='robe_Sim' ) #Group Robe Sim
mc.group(['robe_Objects', 'robe_Sim'], name='robe') #Group All Robe Groups

#Group Pants
mc.group(['ten_Pants_Sim'], name='pants_Objects') #Objects
mc.group(['pants_Objects'], name='pants') #Group All Pants Groups

#Group All
mc.group(['colliders', 'robe', 'pants', 'nucleus1'], name='ClothSim')

#Hide Unnescessary Objects
mc.hide(['colliders', 'robe_Sim'])
mc.hide(['pants', 'ten_Sash_Sim']) #TEMPORARY

#Resources:
    #stackoverflow.com/questions/27104218/maya-different-behaviours-in-standalone-and-embedded-mode
    #unblogdecolin.blogspot.com/2012/06/pyton-pymel-cachefile.html
