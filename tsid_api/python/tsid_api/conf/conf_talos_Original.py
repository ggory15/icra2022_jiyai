from example_robot_data.robots_loader import getModelPath
import os
import numpy as np

# COM
time_set = True
MASS = 90.27
COM_SHIFT_Z = -0.13  # To make 0.75 of z-height ##
TIME_SHIFT_COM = 2.
DURATION_CONNECT_GOAL = 0.5

# EE
l_eeName = 'leg_left_sole_fix_joint'
r_eeName = 'leg_right_sole_fix_joint'

## Settings for end effectors :
EFF_T_PREDEF = 0.04  # duration during which the motion of the end effector is forced to be orthogonal to the contact surface, at the beginning and the end of the phase
EFF_T_DELAY = 0.0001  # duration at the beginning and the end of the phase where the effector don't move
FEET_MAX_VEL = 0.5  # maximal linear velocity of the effector, if the current duration of the phase lead to a greater velocity than this setting, the duration of the phase is increased
FEET_MAX_ANG_VEL = 0.5  # maximal angular velocity of the effectors
p_max = 0.08  #setting used to compute the default height of the effector trajectory. end_effector/bezier_predef.py : computePosOffset()

#Robot
urdf = "/talos_data/robots/talos_reduced.urdf"
path = getModelPath(urdf)
urdf = path + urdf
path = os.path.join(path, '../..')

## TSID
## predef duration of contact phases :
DURATION_INIT = 2.  # Time to init the motion
DURATION_FINAL = 2.  # Time to stop the robot
DURATION_FINAL_SS = 1.  # duration of the final phase if it's a single support phase
DURATION_SS = 0.2  # duration of the single support phases
DURATION_DS = 0.1  # duration of the double support phases
DURATION_TS = 0.4  # duration of the triple support phases
DURATION_CONNECT_GOAL = 2.  # duration to try to connect the last points in the CoM trajectory with the goal position given to planning
# Hardcoded height change of the COM before the beginning of the motion (value in m and time allowed to make this motion)
# This is used because for some robot, the reference configuration is really close to the kinematic limits of the robot.
COM_SHIFT_Z = -0.10
TIME_SHIFT_COM = 2.

## weight and gains used by TSID
fMin = 1.0  # minimum normal force
fMax = 2000.  # maximum normal force
w_com = 1.0  # weight of center of mass task
w_am = 2e-2 # weight used for the minimization of the Angular momentum
w_am_track = 2e-2 # weight used for the tracking of the Angular momentum
w_posture = 0.1  # weight of joint posture task
w_rootOrientation = 1.  # weight of the root's orientation task
w_forceRef = 1e-3  # weight of force regularization task
w_eff = 1.0  # weight of the effector motion task
kp_contact = 30.0  # proportional gain of contact constraint
kp_com = 20.  # proportional gain of center of mass task
kp_am = 10. # gain used for the minimization of the Angular momentum
kp_am_track = 10. # gain used for the tracking of the Angular momentum
kp_posture = 0.5  # proportional gain of joint posture task
kp_rootOrientation = 1.  # proportional gain of the root's orientation task
kp_Eff = 20.  # proportional gain of the effectors motion task
level_eff = 0
level_com = 0
level_posture = 1
level_rootOrientation = 1
level_am = 1

## Friction cone
lxp = 0.11                                  # foot length in positive x direction
lxn = 0.11                                  # foot length in negative x direction
lyp = 0.06                                  # foot length in positive y direction
lyn = 0.06                                  # foot length in negative y direction
lz = 0.                                     # foot sole height with respect to ankle joint
friction = 0.43                                 # friction coefficient
contactNormal = np.array([0., 0., 1.])      # direction of the normal to the contact surface
contact_points = np.ones((3, 4)) * lz
contact_points[0, :] = [-lxn, -lxn, lxp, lxp]
contact_points[1, :] = [-lyn, lyp, -lyn, lyp]

#IK_dt = 0.001
# IK_eff_size = Robot.dict_size.copy()
PLOT_CIRCLE_RADIUS = 0.05 # radius of the circle used to display the contacts
# IK_eff_size={rfoot:[0.1 , 0.06], lfoot:[0.1 , 0.06]}

import numpy as np
gain_vector = np.array(  # gain vector for postural task
    [
        10.,
        5.,
        5.,
        1.,
        1.,
        10.,  # lleg  #low gain on axis along y and knee
        10.,
        5.,
        5.,
        1.,
        1.,
        10.,  #rleg
        5000.,
        5000.,  #chest
        5000.,
        1000,
        100.,
        100.,
        500.,
        10.,
        100.,
        50.,  #larm
        5000.,
        1000.,
        100.,
        100.,
        500.,
        10.,
        100.,
        50.,  #rarm
        1000.,
        1000.  
    ]  #head
)

masks_posture = np.array(np.ones(32))
# masks_posture[:16] = 0.0 
# gain_vector[12:14] *= 100.0
gain_vector[14:] *= 50.0

# Reference config used by the wholeBody script, may be different than the one used by the planning (default value is the same as planning)
YAW_ROT_GAIN = 1.  # gain for the orientation task of the root orientation, along the yaw axis (wrt to the other axis of the orientation task)
IK_trackAM = False #If True, the Wb algorithm take the Angular momentum computed by te centroidal block as reference. If False it try to minimize the angular momentum
WB_STOP_AT_EACH_PHASE = False  # wait for user input between each phase
IK_dt = 0.001  # controler time step (in second)
IK_PRINT_N = 500  # print state of the problem every IK_PRINT_N time steps (if verbose >= 1)
CHECK_FINAL_MOTION = False 
