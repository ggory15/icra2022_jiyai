from ndcurves import piecewise, polynomial, SE3Curve
from multicontact_api import ContactSequence
import multicontact_api

def setCOMtrajectoryFromPoints(phase, c, dc, ddc, timeline, overwriteInit = True, overwriteFinal = True):
    """
    Define the CoM position, velocity and acceleration trajectories as a linear interpolation between each points
    Also set the initial / final values for c, dc and ddc to match the ones in the trajectory
    :param phase:
    :param c:
    :param dc:
    :param ddc:
    :param timeline:
    :param overwrite: Default True : overwrite init/final values even if they exist
    :return:
    """
    phase.c_t = piecewise.FromPointsList(c,timeline.T)
    phase.dc_t = piecewise.FromPointsList(dc,timeline.T)
    phase.ddc_t = piecewise.FromPointsList(ddc,timeline.T)
    if overwriteInit:
        phase.c_init = c[:,0]
    if overwriteInit:
        phase.dc_init = dc[:,0]
    if overwriteInit:
        phase.ddc_init = ddc[:,0]
    if overwriteFinal:
        phase.c_final = c[:,-1]
    if overwriteFinal:
        phase.dc_final= dc[:,-1]
    if overwriteFinal:
        phase.ddc_final = ddc[:,-1]


def setAMtrajectoryFromPoints(phase, L, dL, timeline, overwriteInit = True, overwriteFinal = True):
    """
    Define the AM  value and it's time derivative trajectories as a linear interpolation between each points
    Also set the initial / final values for L and dL to match the ones in the trajectory
    :param phase:
    :param L:
    :param dL:
    :param timeline:
    :param overwrite: Default True : overwrite init/final values even if they exist
    :return:
    """
    phase.L_t = piecewise.FromPointsList(L,timeline.T)
    phase.dL_t = piecewise.FromPointsList(dL,timeline.T)
    if overwriteInit:
        phase.L_init = L[:,0]
    if overwriteInit:
        phase.dL_init = dL[:,0]
    if overwriteFinal:
        phase.L_final = L[:,-1]
    if overwriteFinal:
        phase.dL_final= dL[:,-1]

def connectPhaseTrajToInitialState(phase, duration):
    """
    Insert at the beginning of the trajectory of c, dc and ddc a quintic spline connecting phase.c_init, dc_init and ddc__init
    and L and dL with a trajectory at 0
    :param phase:
    :param duration:
    """
    if duration <= 0.:
        return
    if phase.c_t is None or phase.dc_t is None or phase.ddc_t is None:
        raise RuntimeError("connectPhaseTrajToFinalState can only be called with a phase with an initialized COM trajectory")
    if phase.L_t is None or phase.dL_t is None :
        raise RuntimeError("connectPhaseTrajToFinalState can only be called with a phase with an initialized AM trajectory")
    if not phase.c_init.any():
        raise RuntimeError("connectPhaseTrajToFinalState can only be called with a phase with an initialized c_final")
    t_final = phase.c_t.min()
    t_init = t_final - duration
    c_final = phase.c_t(t_final)
    dc_final = phase.dc_t(t_final)
    ddc_final = phase.ddc_t(t_final)
    L_final = phase.L_t(t_final)
    dL_final = phase.dL_t(t_final)
    com_t = polynomial( phase.c_init, phase.dc_init, phase.ddc_init,c_final, dc_final, ddc_final, t_init, t_final)
    L_t = polynomial(phase.L_init, phase.dL_init, L_final, dL_final, t_init, t_final)

    # insert this trajectories at the beginning of the phase :
    piecewise_c= piecewise(com_t)
    piecewise_c.append(phase.c_t)
    phase.c_t = piecewise_c
    piecewise_dc= piecewise(com_t.compute_derivate(1))
    piecewise_dc.append(phase.dc_t)
    phase.dc_t = piecewise_dc
    piecewise_ddc= piecewise(com_t.compute_derivate(2))
    piecewise_ddc.append(phase.ddc_t)
    phase.ddc_t = piecewise_ddc
    piecewise_L= piecewise(L_t)
    piecewise_L.append(phase.L_t)
    phase.L_t = piecewise_L
    piecewise_dL= piecewise(L_t.compute_derivate(1))
    piecewise_dL.append(phase.dL_t)
    phase.dL_t = piecewise_dL
    # set the new initial time
    phase.timeInitial = t_init

def connectPhaseTrajToFinalState(phase, duration = None):
    """
    Append to the trajectory of c, dc and ddc a quintic spline connecting phase.c_final, dc_final and ddc_final
    and L and dL with a trajectory at 0
    :param phase:
    :param duration:
    """
    if phase.c_t is None or phase.dc_t is None or phase.ddc_t is None:
        # initialise empty trajectories
        phase.c_t = piecewise()
        phase.dc_t = piecewise()
        phase.ddc_t = piecewise()
        # get the initial state from the phase :
        c_init = phase.c_init
        dc_init = phase.dc_init
        ddc_init = phase.ddc_init
        t_init = phase.timeInitial
    else:
        # get the initial state from the last points of the trajectories :
        t_init = phase.c_t.max()
        c_init = phase.c_t(t_init)
        dc_init = phase.dc_t(t_init)
        ddc_init = phase.ddc_t(t_init)
    if phase.L_t is None or phase.dL_t is None :
        # initialise empty trajectories
        phase.L_t = piecewise()
        phase.dL_t = piecewise()
        # get the initial state from the phase :
        L_init = phase.L_init
        dL_init = phase.dL_init
    else :
        L_init = phase.c_t(t_init)
        dL_init = phase.dL_t(t_init)
    if not phase.c_final.any():
        raise RuntimeError("connectPhaseTrajToFinalState can only be called with a phase with an initialized c_final")
    if duration is not None:
        t_final = t_init + duration
    else:
        t_final = phase.timeFinal
    com_t = polynomial(c_init, dc_init, ddc_init, phase.c_final, phase.dc_final, phase.ddc_final, t_init, t_final)
    L_t = polynomial(L_init, dL_init, phase.L_final, phase.dL_final, t_init, t_final)
    phase.c_t.append(com_t)
    phase.dc_t.append(com_t.compute_derivate(1))
    phase.ddc_t.append(com_t.compute_derivate(2))
    phase.L_t.append(L_t)
    phase.dL_t.append(L_t.compute_derivate(1))
    phase.timeFinal = t_final

def effectorPlacementFromPhaseConfig(phase, eeName, fullBody):
    if fullBody is None :
        raise RuntimeError("Cannot compute the effector placement from the configuration without initialized fullBody object.")
    if not phase.q_init.any():
        raise RuntimeError("Cannot compute the effector placement as the initial configuration is not initialized in the ContactPhase.")

    fullBody.setCurrentConfig(phase.q_init.tolist())
    return SE3FromConfig(fullBody.getJointPosition(eeName))
    
def generate_effector_trajectories_for_sequence(cfg, cs, generate_end_effector_traj, output_, fullBody = None):
    """
    Generate an effector trajectory for each effectors which are going to be in contact in the next phase
    :param cfg: an instance of the configuration class
    :param cs: the contact sequence
    :param generate_end_effector_traj: a pointer to the method used to generate an end effector trajectory for one phase
    :param fullBody: an instance of rbprm FullBody
    :return: a new contact sequence, containing the same data as the one given as input
    plus the effector trajectories for each swing phases
    """
    cs_res = ContactSequence(cs)
    effectors = cs_res.getAllEffectorsInContact()
    previous_phase = None
    for pid in range(cs_res.size()-1): # -1 as last phase never have effector trajectories
        phase = cs_res.contactPhases[pid]
        next_phase = cs_res.contactPhases[pid+1]
        if pid > 0 :
            previous_phase = cs_res.contactPhases[pid-1]

        for eeName in effectors:
            if not phase.isEffectorInContact(eeName) and next_phase.isEffectorInContact(eeName):
                # eeName will be in compute in the next phase, a trajectory should be added in the current phase
                placement_end = next_phase.contactPatch(eeName).placement
                time_interval = [phase.timeInitial, phase.timeFinal]
                if previous_phase is not None and previous_phase.isEffectorInContact(eeName):
                    placement_init = previous_phase.contactPatch(eeName).placement
                else:
                    placement_init = effectorPlacementFromPhaseConfig(phase,eeName,fullBody)
                # build the trajectory :
                traj = generate_end_effector_traj(cfg, time_interval,placement_init,placement_end)
                phase.addEffectorTrajectory(eeName,traj)
    cs_res.saveAsBinary(output_)

    return cs_res

def deleteAllTrajectories(cs):
    for phase in cs.contactPhases:
        deletePhaseWBtrajectories(phase)
        phase.c_t = None
        phase.dc_t = None
        phase.ddc_t = None
        phase.L_t = None
        phase.dL_t = None
        phase.root_t = None

def deletePhaseWBtrajectories(phase):
    phase.q_t = None
    phase.dq_t = None
    phase.ddq_t = None
    phase.tau_t = None

def updateContactPlacement(cs, pid_begin, eeName, placement, update_rotation):
    """
    Starting from cs.contactPhases[pid_begin] and going until eeName is in contact,
    the placement of eeName is modified with the given placement.
    Note that the wholebody configurations are not updated !
    :param cs: The ContactSequence to modify
    :param pid_begin: the Id of the first phase to modify
    :param eeName: the effector name
    :param placement: the new placement for eeName
    :param update_rotation: if True, update the placement, if False update only the translation
    """
    for pid in range(pid_begin, cs.size()):
        phase = cs.contactPhases[pid]
        if phase.isEffectorInContact(eeName):
            if update_rotation:
                phase.contactPatch(eeName).placement = placement
            else:
                new_placement = phase.contactPatch(eeName).placement
                new_placement.translation = placement.translation
                phase.contactPatch(eeName).placement = new_placement
        else:
            return

def setPreviousFinalValues(phase_prev, phase, cfg):
    """
    Set the final values and last points of the trajectory of phase_prev to the initial values of phase
    :param phase_prev:
    :param phase:
    :param cfg:
    :return:
    """
    if phase_prev is None:
        return
    setFinalFromInitialValues(phase_prev,phase)
    t = phase_prev.timeFinal
    phase_prev.q_t.append(phase_prev.q_final, t)
   

def setFinalFromInitialValues(previous_phase, next_phase):
    """
    Set c_final, dc_final, ddc_final, L_final, dL_final of previous_phase
    to the values of the 'init' in next_phase
    :param previous_phase:
    :param next_phase:
    :return:
    """
    previous_phase.c_final = next_phase.c_init
    previous_phase.dc_final = next_phase.dc_init
    previous_phase.ddc_final = next_phase.ddc_init
    previous_phase.L_final = next_phase.L_init
    previous_phase.dL_final = next_phase.dL_init
    previous_phase.q_final = next_phase.q_init
