import numpy as np
from numpy import cross
from numpy.linalg import norm
import pinocchio
from pinocchio import SE3, Quaternion, Motion
from pinocchio.utils import rpyToMatrix, rotate
from ndcurves import polynomial, SE3Curve, SO3Linear
import math
from ..conf import conf_talos as conf

from random import uniform
import types
pinocchio.switchToNumpyArray()


def distPointLine(p_l, x1_l, x2_l):
    p = np.matrix(p_l)
    x1 = np.matrix(x1_l)
    x2 = np.matrix(x2_l)
    return norm(cross(p - x1, p - x2)) / norm(x2 - x1)

def SE3toVec(M):
    v = np.zeros(12)
    for j in range(3):
        v[j] = M.translation[j]
        v[j + 3] = M.rotation[j, 0]
        v[j + 6] = M.rotation[j, 1]
        v[j + 9] = M.rotation[j, 2]
    return v


def MotiontoVec(M):
    v = np.zeros(6)
    for j in range(3):
        v[j] = M.linear[j]
        v[j + 3] = M.angular[j]
    return v


def SE3FromVec(vect):
    if vect.shape[0] != 12 or vect.shape[1] != 1:
        raise ValueError("SE3FromVect take as input a vector of size 12")
    placement = SE3.Identity()
    placement.translation = vect[0:3]
    rot = placement.rotation
    # depend if eigenpy.switchToNumpyArray() have been called, FIXME : there should be a better way to check this
    if len( rot[:, 0].shape ) == 1:
        rot[:, 0] = np.asarray(vect[3:6]).reshape(-1)
        rot[:, 1] = np.asarray(vect[6:9]).reshape(-1)
        rot[:, 2] = np.asarray(vect[9:12]).reshape(-1)
    else:
        rot[:, 0] = vect[3:6]
        rot[:, 1] = vect[6:9]
        rot[:, 2] = vect[9:12]
    placement.rotation = rot
    return placement


def MotionFromVec(vect):
    if vect.shape[0] != 6 or vect.shape[1] != 1:
        raise ValueError("MotionFromVec take as input a vector of size 6")
    m = Motion.Zero()
    m.linear = np.array(vect[0:3])
    m.angular = np.array(vect[3:6])
    return m



def numpy2DToList(m):
    """
    Convert a numpy array of shape (n,m) in a list of list.
    First list is of length m and contains list of length n
    :param m:
    :return:
    """
    l = []
    for i in range(m.shape[1]):
        p = m[:, i]
        if len(p.shape) == 1:  # array
            l += [p.tolist()]  # TODO : check this
        else:  # matrix
            l += [p.tolist()]
    return l


# assume that q.size >= 7 with root pos and quaternion(x,y,z,w)
def SE3FromConfig(q):
    if isinstance(q, list):
        q = np.array(q)
    placement = SE3.Identity()
    tr = np.array(q[0:3])
    placement.translation = tr
    r = Quaternion(q[6], q[3], q[4], q[5])
    placement.rotation = r.matrix()
    return placement


# rotate the given placement of 'angle' (in radian) along axis 'axis'
# axis : either 'x' , 'y' or 'z'
def rotatePlacement(placement, axis, angle):
    T = rotate(axis, angle)
    placement.rotation = placement.rotation @ T
    return placement


def rotateFromRPY(placement, rpy):
    trans = SE3.Identity()
    trans.rotation = rpyToMatrix(rpy)
    return placement.act(trans)


def effectorPositionFromHPPPath(fb, problem, eeName, pid, t):
    q = problem.configAtParam(pid, t)
    # compute effector pos from q :
    fb.setCurrentConfig(q)
    p = fb.getJointPosition(eeName)[0:3]
    return np.array(p)


def genAMTrajFromPhaseStates(phase, constraintVelocity = True):
    """
    Generate a cubic spline connecting (L_init, dL_init) to (L_final, dL_final) and set it as the phase AM trajectory
    :param phase: the ContactPhase to use
    :param constraintVelocity: if False, generate only a linear interpolation and ignore the values of dL
    :return:
    """
    if constraintVelocity:
        am_traj = polynomial(phase.L_init, phase.dL_init, phase.L_final, phase.dL_final,
                              phase.timeInitial, phase.timeFinal)
    else:
        am_traj = polynomial(phase.L_init, phase.L_final, phase.timeInitial, phase.timeFinal)
    phase.L_t = am_traj
    phase.dL_t = am_traj.compute_derivate(1)


def genCOMTrajFromPhaseStates(phase, constraintVelocity = True, constraintAcceleration = True):
    """
    Generate a quintic spline connecting exactly (c, dc, ddc) init to final
    :param phase:
    :param constraintVelocity: if False, generate only a linear interpolation and ignore ddc, and dc values
    :param constraintAcceleration: if False, generate only a cubic spline and ignore ddc values
    :return:
    """
    if constraintAcceleration and not constraintVelocity:
        raise ValueError("Cannot constraints acceleration if velocity is not constrained.")
    if constraintAcceleration:
        com_traj = polynomial(phase.c_init, phase.dc_init, phase.ddc_init,
                              phase.c_final, phase.dc_final, phase.ddc_final,phase.timeInitial, phase.timeFinal)
    elif constraintVelocity:
        com_traj = polynomial(phase.c_init, phase.dc_init, phase.c_final, phase.dc_final,
                              phase.timeInitial, phase.timeFinal)
    else:
        com_traj = polynomial(phase.c_init, phase.c_final, phase.timeInitial, phase.timeFinal)
    phase.c_t = com_traj
    phase.dc_t = com_traj.compute_derivate(1)
    phase.ddc_t = com_traj.compute_derivate(2)


def effectorPlacementFromPhaseConfig(phase, eeName, fullBody):
    if fullBody is None :
        raise RuntimeError("Cannot compute the effector placement from the configuration without initialized fullBody object.")
    if not phase.q_init.any():
        raise RuntimeError("Cannot compute the effector placement as the initial configuration is not initialized in the ContactPhase.")

    fullBody.setCurrentConfig(phase.q_init.tolist())
    return SE3FromConfig(fullBody.getJointPosition(eeName))


def computeEffectorTranslationBetweenStates(cs, pid):
    """
    Compute the distance travelled by the effector (suppose a straight line) between
    it's contact placement in pid+1 and it's previous contact placement
    :param cs:
    :param pid:
    :return:
    """
    phase = cs.contactPhases[pid]
    next_phase = cs.contactPhases[pid+1]
    eeNames = phase.getContactsCreated(next_phase)
    if len(eeNames) > 1:
        raise NotImplementedError("Several effectors are moving during the same phase.")
    if len(eeNames) == 0 :
        # no effectors motions in this phase
        return 0.
    eeName = eeNames[0]
    i = pid
    while not cs.contactPhases[i].isEffectorInContact(eeName) and i >= 0:
        i -= 1
    if i < 0:
        # this is the first phase where this effector enter in contact
        # TODO what should we do here ?
        return 0.

    d = next_phase.contactPatch(eeName).placement.translation -  cs.contactPhases[i].contactPatch(eeName).placement.translation
    return norm(d)


def computeEffectorRotationBetweenStates(cs, pid):
    """
    Compute the rotation applied to the effector  between
    it's contact placement in pid+1 and it's previous contact placement
    :param cs:
    :param pid:
    :return:
    """
    phase = cs.contactPhases[pid]
    next_phase = cs.contactPhases[pid + 1]
    eeNames = phase.getContactsCreated(next_phase)
    if len(eeNames) > 1:
        raise NotImplementedError("Several effectors are moving during the same phase.")
    if len(eeNames) == 0:
        # no effectors motions in this phase
        return 0.
    eeName = eeNames[0]
    i = pid
    while not cs.contactPhases[pid].isEffectorInContact(eeName) and i >= 0:
        i -= 1
    if i < 0:
        # this is the first phase where this effector enter in contact
        # TODO what should we do here ?
        return 0.

    P = next_phase.contactPatch(eeName).placement.rotation
    Q = cs.contactPhases[i].contactPatch(eeName).placement.rotation
    R = P.dot(Q.T)
    tR = R.trace()
    try:
        res = abs(math.acos((tR - 1.) / 2.))
    except ValueError as e:
        print("WARNING : when computing rotation between two contacts, got error : ", e)
        print("With trace value = ", tR)
        res = 0.
    return res



def createFullbodyStatesFromCS(cs, fb):
    """
    Create all the rbprm State corresponding to the given cs object, and add them to the fullbody object
    :param cs: a ContactSequence
    :param fb: the Fullbody object used
    :return: the first and last Id of the states added to fb
    """
    #lastId = fullBodyStatesExists(cs, fb)
    #if lastId > 0:
    #    print("States already exist in fullBody instance. endId = ", lastId)
    #    return 0, lastId
    phase_prev = cs.contactPhases[0]
    beginId = createStateFromPhase(fb, phase_prev)
    lastId = beginId
    print("CreateFullbodyStateFromCS ##################")
    print("beginId = ", beginId)
    for pid, phase in enumerate(cs.contactPhases[1:]):
        if not np.array_equal(phase_prev.q_init, phase.q_init):
            lastId = createStateFromPhase(fb, phase)
            print("add phase " + str(pid) + " at state index : " + str(lastId))
            phase_prev = phase
    return beginId, lastId

def perturbateContactNormal(fb, state_id, epsilon = 1e-2):
    """
    Add a small variation (+- epsilon) to the contact normals of the given state
    :param fb:
    :param state_id:
    :param epsilon:
    :return: the new state ID, -1 if fail
    """
    state = State(fb, state_id)
    for name in state.getLimbsInContact():
        p, n = state.getCenterOfContactForLimb(name)
        n[2] += uniform(-epsilon, epsilon)
        n = np.array(n)
        state, success = StateHelper.addNewContact(state,name, p, n.tolist())
        if not success:
            return -1
    return state.sId


def computeContactNormal(placement):
    """
    Compute the contact normal assuming that it's orthogonal to the contact orientation
    :param placement: the contact placement
    :return:
    """
    z_up = np.array([0., 0., 1.])
    contactNormal = placement.rotation @ z_up
    return contactNormal



def rootOrientationFromFeetPlacement(Robot, phase_prev, phase, phase_next):
    """
    Compute an initial and final root orientation for the ContactPhase
    The initial orientation is a mean between both feet contact position in the current (or previous) phase
    the final orientation is with considering the newt contact position of the feet
    :param phase_prev:
    :param phase:
    :param phase_next:
    :return:
    """
    #FIXME : extract only the yaw rotation
    qr = None
    ql = None
    patchR = None
    patchL = None
    if phase.isEffectorInContact(Robot.rfoot):
        patchR = phase.contactPatch(Robot.rfoot)
    elif phase_prev and phase_prev.isEffectorInContact(Robot.rfoot):
        patchR = phase_prev.contactPatch(Robot.rfoot)
    if patchR:
        qr = Quaternion(patchR.placement.rotation)
        qr.x = 0
        qr.y = 0
        qr.normalize()
    if phase.isEffectorInContact(Robot.lfoot):
        patchL = phase.contactPatch(Robot.lfoot)
    elif phase_prev and phase_prev.isEffectorInContact(Robot.lfoot):
        patchL = phase_prev.contactPatch(Robot.lfoot)
    if patchL:
        ql = Quaternion(patchL.placement.rotation)
        ql.x = 0
        ql.y = 0
        ql.normalize()
    if ql is not None and qr is not None:
        q_rot = qr.slerp(0.5, ql)
    elif qr is not None:
        q_rot = qr
    elif ql is not None:
        q_rot = ql
    else:
        raise RuntimeError("In rootOrientationFromFeetPlacement, cannot deduce feet initial contacts positions.")
    placement_init = SE3.Identity()
    placement_init.rotation = q_rot.matrix()

    # compute the final orientation :
    if phase_next:
        if not phase.isEffectorInContact(Robot.rfoot) and phase_next.isEffectorInContact(Robot.rfoot):
            qr = Quaternion(phase_next.contactPatch(Robot.rfoot).placement.rotation)
            qr.x = 0
            qr.y = 0
            qr.normalize()
        if not phase.isEffectorInContact(Robot.lfoot) and phase_next.isEffectorInContact(Robot.lfoot):
            ql = Quaternion(phase_next.contactPatch(Robot.lfoot).placement.rotation)
            ql.x = 0
            ql.y = 0
            ql.normalize()
    if ql is not None and qr is not None:
        q_rot = qr.slerp(0.5, ql)
    elif qr is not None:
        q_rot = qr
    elif ql is not None:
        q_rot = ql
    else:
        raise RuntimeError("In rootOrientationFromFeetPlacement, cannot deduce feet initial contacts positions.")
    placement_end = SE3.Identity()
    placement_end.rotation = q_rot.matrix()
    return placement_init, placement_end



def discretizeCurve(curve,dt):
    """
    Discretize the given curve at the given dt
    return the result as an array (one column per discret point)
    In case where the time interval of the curve is not a multiple of dt, the last point is still included
    This mean that the timestep between the two last points may be less than dt
    :param curve: a curve object, require operator (), min() and max()
    :param dt: the discretization step
    :return: an array of shape (curve.dim(), numPoints) and an array corresponding to the timeline
    """
    numPoints = round((curve.max() - curve.min()) / dt ) + 1
    res = np.zeros([curve.dim(), numPoints])
    timeline = np.zeros(numPoints)
    t = curve.min()
    for i in range(numPoints):
        res[:,i] = curve(t)
        timeline[i] = t
        t += dt
        if t > curve.max():
            t = curve.max()
    return res, timeline


def discretizeDerivateCurve(curve,dt, order):
    """
    Discretize the derivative of the given curve at the given dt
    return the result as an array (one column per discret point)
    In case where the time interval of the curve is not a multiple of dt, the last point is still included
    This mean that the timestep between the two last points may be less than dt
    :param curve: a curve object, require operator (), min() and max()
    :param dt: the discretization step
    :return: an array of shape (curve.dim(), numPoints) and an array corresponding to the timeline
    """
    numPoints = round((curve.max() - curve.min()) / dt ) + 1
    res = np.zeros([curve.dim(), numPoints])
    timeline = np.zeros(numPoints)
    t = curve.min()
    for i in range(numPoints):
        res[:,i] = curve.derivate(t, order)
        timeline[i] = t
        t += dt
        if t > curve.max():
            t = curve.max()
    return res, timeline


def discretizeSE3CurveTranslation(curve,dt):
    """
    Discretize the given curve at the given dt
    return the result as an array (one column per discret point)
    In case where the time interval of the curve is not a multiple of dt, the last point is still included
    This mean that the timestep between the two last points may be less than dt
    :param curve: a SE3 curve object, require operator (), min() and max() and translation()
    :param dt: the discretization step
    :return: an array of shape (3, numPoints) and an array corresponding to the timeline
    """
    numPoints = round((curve.max() - curve.min()) / dt ) + 1
    res = np.zeros([3, numPoints])
    timeline = np.zeros(numPoints)
    t = curve.min()
    for i in range(numPoints):
        res[:,i] = curve.translation(t)
        timeline[i] = t
        t += dt
        if t > curve.max():
            t = curve.max()
    return res, timeline


def discretizeSE3CurveQuaternion(curve,dt):
    """
    Discretize the given curve at the given dt
    return the result as an array (one column per discret point)
    In case where the time interval of the curve is not a multiple of dt, the last point is still included
    This mean that the timestep between the two last points may be less than dt
    :param curve: a SE3 curve object, require operator (), min() and max() and rotation()
    :param dt: the discretization step
    :return: an array of shape (3, numPoints) and an array corresponding to the timeline
    """
    numPoints = round((curve.max() - curve.min()) / dt ) + 1
    res = np.zeros([4, numPoints])
    timeline = np.zeros(numPoints)
    t = curve.min()
    for i in range(numPoints):
        res[:,i] = Quaternion(curve.rotation(t)).coeffs()
        timeline[i] = t
        t += dt
        if t > curve.max():
            t = curve.max()
    return res, timeline

def discretizeSE3CurveToVec(curve,dt):
    """
    Discretize the given curve at the given dt
    return the result as an array (one column per discret point)
    In case where the time interval of the curve is not a multiple of dt, the last point is still included
    This mean that the timestep between the two last points may be less than dt
    :param curve: a SE3 curve object, require operator (), min() and max()
    :param dt: the discretization step
    :return: an array of shape (12, numPoints) and an array corresponding to the timeline
    """
    numPoints = round((curve.max() - curve.min()) / dt ) +1
    res = np.zeros([12, numPoints])
    timeline = np.zeros(numPoints)
    t = curve.min()
    for i in range(numPoints):
        res[:,i] = SE3toVec(curve.evaluateAsSE3(t))
        timeline[i] = t
        t += dt
        if t > curve.max():
            t = curve.max()
    return res, timeline

def constantSE3curve(placement, t_min, t_max = None):
    """
    Create a constant SE3_curve at the given placement for the given duration
    :param placement: the placement
    :param t_min: the initial time
    :param t_max: final time, if not provided the curve will have a duration of 0
    :return: the constant curve
    """
    if t_max is None:
        t_max = t_min
    rot = SO3Linear(placement.rotation, placement.rotation, t_min, t_max)
    trans = polynomial(placement.translation.reshape(-1,1), t_min, t_max)
    return SE3Curve(trans, rot)


def buildRectangularContactPoints(size, transform):
    """
    Build Array at the corners of the feet
    :param size: list of len 2 : size of the rectangle along x and y
    :param transform: an SE3 object: transform applied to all vectors
    :return: a 3x4 Array, with the 3D position of one contact point per columns
    """
    lxp = size[0] / 2. + transform.translation[0]  # foot length in positive x direction
    lxn = size[0] / 2. - transform.translation[0]  # foot length in negative x direction
    lyp = size[1] / 2. + transform.translation[1]  # foot length in positive y direction
    lyn = size[1] / 2. - transform.translation[1]  # foot length in negative y direction
    lz = transform.translation[2]  # foot sole height with respect to ankle joint
    contact_Point = np.ones((3, 4))
    contact_Point[0, :] = [-lxn, -lxn, lxp, lxp]
    contact_Point[1, :] = [-lyn, lyp, -lyn, lyp]
    contact_Point[2, :] = [lz] * 4
    return contact_Point

class DisplayContactSequenceRequirements():
    configurationValues = True

STONE_HEIGHT = 0.005
STONE_GROUP = "stepping_stones"
STONE_RF = STONE_GROUP + "/" + "RF"
STONE_LF = STONE_GROUP + "/" + "LF"
STONE_RH = STONE_GROUP + "/" + "RH"
STONE_LH = STONE_GROUP + "/" + "LH"

TRAJ_GROUP = "com_traj"

COM_GROUP = "com_groups"
COM_ = COM_GROUP + "/" + "P"


def SE3ToViewerConfig(placement):
    q = [0] * 7
    q[0:3] = placement.translation.tolist()
    r = Quaternion(placement.rotation)
    q[6] = r.w
    q[3:6] = r.coeffs().tolist()[0:3]
    return q

def displaySteppingStones(cs, gui, Robot, name="world"):
    gui.createGroup(STONE_GROUP)
    gui.createGroup(STONE_RF)
    gui.createGroup(STONE_LF)

    name_RF = STONE_RF + "/stone_"
    name_LF = STONE_LF + "/stone_"

    id_RF = 0
    id_LF = 0

    lfoot = conf.l_eeName
    rfoot = conf.r_eeName

    for phase in cs.contactPhases:
        if phase.isEffectorInContact(lfoot):
            gui.addBox(name_LF + str(id_LF), 0.2, 0.1, STONE_HEIGHT, [1, 0, 0, 1])
            gui.addToGroup(name_LF + str(id_LF), STONE_LF)
            gui.applyConfiguration(name_LF + str(id_LF), SE3ToViewerConfig(phase.contactPatch(lfoot).placement))

            id_LF += 1
        if phase.isEffectorInContact(rfoot):
            gui.addBox(name_RF + str(id_RF), 0.2, 0.1, STONE_HEIGHT, [0, 1, 0, 1])
            gui.addToGroup(name_RF + str(id_RF), STONE_RF)
            gui.applyConfiguration(name_RF + str(id_RF), SE3ToViewerConfig(phase.contactPatch(rfoot).placement))
            id_RF += 1

    gui.addToGroup(STONE_RF, STONE_GROUP)
    gui.addToGroup(STONE_LF, STONE_GROUP)
    gui.addToGroup(STONE_GROUP, name)
    gui.refresh()

def displayCOMPoints(cs, gui, name="world"):
    gui.createGroup(COM_GROUP)
    name_COM = COM_ + "/com_point_"
    id_COM = 0

    for pid,phase in enumerate(cs.contactPhases):
        if pid != 0:
            gui.addSphere(name_COM + str(id_COM), 0.01, [0, 0, 1, 1])
            gui.addToGroup(name_COM + str(id_COM), COM_GROUP)
            q = [0] * 7
            q[0:3] = phase.c_init
            q[6] = 1
            gui.applyConfiguration(name_COM+str(id_COM), q)

            id_COM += 1

    gui.addToGroup(COM_GROUP, name)
    gui.refresh()

def displayCOMTrajForPhase(phase, gui, name, name_group, color, dt):
    c = numpy2DToList(discretizeCurve(phase.c_t, dt)[0])
    gui.addCurve(name, c, color)
    gui.addToGroup(name, name_group)


def displayCOMTrajectory(cs, gui, sceneName, dt, colors=[0, 0, 0, 1], nameGroup="", linewidth=None):
    name_group = TRAJ_GROUP + nameGroup
    gui.createGroup(name_group)
    for pid,phase in enumerate(cs.contactPhases):
        if pid != 0:
            name = name_group + "/" + '%.2f' % phase.timeInitial + "-" + '%.2f' % phase.timeFinal
            color = colors[pid % len(colors)]
            displayCOMTrajForPhase(phase, gui, name, name_group, color, dt)
            if linewidth is not None:
                gui.setCurveLineWidth(name,linewidth)
    gui.addToGroup(name_group, sceneName)
    gui.refresh()

def displaySE3Traj(traj, gui, sceneName, name, color, time_interval, offset=SE3.Identity()):
    if name == None:
        name = "SE3_traj"
    rootName = name
    # add indices until the name is free
    node_list = gui.getNodeList()
    if node_list:
        i = 0
        while node_list.count(name) > 0:
            name = rootName + "_" + str(i)
            i += 1
        path = []
        dt = 0.01
        t = time_interval[0]
        while t <= time_interval[1]:
            m = traj.evaluateAsSE3(t)
            m = m.act(offset)
            path += [m.translation.tolist()]
            t += dt
        gui.addCurve(name, path, color)
        gui.addToGroup(name, sceneName)
        gui.refresh()

def displayEffectorTrajectories(cs, gui, Robot, suffixe = "", colorAlpha = 1):
    effectors = cs.getAllEffectorsInContact()
    for pid,phase in enumerate(cs.contactPhases):
        for eeName in effectors:
            if phase.effectorHaveAtrajectory(eeName):
                color = [1, 1, 0, 1]
                displaySE3Traj(phase.effectorTrajectory(eeName), gui, "world",
                                 eeName + "_traj_"+ suffixe + str(pid), color,
                                 [phase.timeInitial, phase.timeFinal])
