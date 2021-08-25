import numpy as np
import pickle
from importlib import import_module
from .conf import conf_talos as conf
from multicontact_api import ContactPhase, ContactSequence, ContactPatch
from .util.util import SE3FromConfig, computeContactNormal, rootOrientationFromFeetPlacement
from .util.cs_util import setAMtrajectoryFromPoints, setCOMtrajectoryFromPoints, connectPhaseTrajToInitialState, connectPhaseTrajToFinalState
from .phase import Phases
import pinocchio as pin

class ContactData:
    """
    Get COM Traj to use it on tsid
    """
    def __init__(self, input_, robot):
        self.input_ = input_
        self.refined_data = []
        self.robot = robot
        self.model = robot.model
        self.data = robot.data
        self.q_ref = self.model.referenceConfigurations["half_sitting"]
        #self.q_ref[0] += 0.603 #shift CoM x

        with open(self.input_, 'rb') as f:
            while True:
                try:
                    data = pickle.load(f)
                except EOFError:
                    break
            self.refined_data.append(data)

        self.traj_data = self.refined_data[0]['TSID_Trajectories']
        self.terrain_data = self.refined_data[0]['TerrainData']

        self.createContactSequence()
        
        self.time_set = conf.time_set
        self.Mass = conf.MASS
        self.COM_SHIFT_Z = conf.COM_SHIFT_Z
        self.TIME_SHIFT_COM = conf.TIME_SHIFT_COM
        self.DURATION_CONNECT_GOAL = conf.DURATION_CONNECT_GOAL

        self.l_eeName = conf.l_eeName
        self.r_eeName = conf.r_eeName
        self.cs = []

    def save(self, output_):
        self.cs.saveAsXML(output_, "ContactPatch")
        
    def createData(self):
        self.createContactSequence()
        for i in range (self.raw_cs_size):
            if i%3 == 1 or i%3 == 2 or i == 0:
                self.cs.append(self.createContactPhase(self.robot, self.q_ref, self.raw_cs, i))
        self.createContactSequenceWithCurves()

        return self.cs

    def createContactSequence(self):
        self.raw_cs = Phases(self.traj_data)
        self.raw_cs_size = self.raw_cs.size * 3 -3

        self.cs = ContactSequence(0)

    def createContactPhase(self, fb, q, cs, index):
        phase = ContactPhase()
        phase.q_init = np.array(q)
        cs_size = cs.size * 3

        ## initial phase ##
        if index == 0 :
            phase.q_init = np.array(q)
            pin.forwardKinematics(self.model, self.data, phase.q_init)
            pin.updateFramePlacements(self.model, self.data)
            com = np.array(fb.com())

            phase.c_init = com.copy()
            phase.dc_init = np.zeros((3, 1))
            phase.ddc_init = np.zeros((3, 1))

            phase.c_final = cs.getCOMSeriesFromePhase(index+1)[:, 0]
            phase.dc_final = np.zeros((3, 1))# cs.getCOMdotSeriesFromePhase(index+1)[:, 0]
            phase.ddc_final = np.zeros((3, 1))

            phase.L_final = np.zeros((3,1))
            phase.dL_final = np.zeros((3,1))

            if self.time_set:
                phase.timeInitial = 0.
                phase.timeFinal = cs.p[index+1].time[0]

            patch = ContactPatch(self.data.oMf[self.model.getFrameId(self.l_eeName)]) 
            phase.addContact(self.l_eeName, patch)

            patch = ContactPatch(self.data.oMf[self.model.getFrameId(self.r_eeName)]) 
            phase.addContact(self.r_eeName, patch)

        if index%3 == 1:
            phase.c_init = cs.getCOMSeriesFromePhase(index)[:, 0]
            phase.dc_init = np.zeros((3, 1))# cs.getCOMdotSeriesFromePhase(index)[:, 0]
            phase.ddc_init = np.zeros((3, 1))

            phase.c_final = cs.getCOMSeriesFromePhase(index+1)[:, 0]
            phase.dc_final = np.zeros((3, 1)) #cs.getCOMdotSeriesFromePhase(index+1)[:, 0]
            phase.ddc_final = np.zeros((3, 1))

            phase.L_final = np.zeros((3,1))
            phase.dL_final = np.zeros((3,1))
            if self.time_set:
                phase.timeInitial = cs.p[index].time[0]
                phase.timeFinal = cs.p[index+1].time[0]

            if cs.p[index].ssp == 'Lf': #  Left support
                if index > 3:
                    placement = cs.p[index].oMf_Li
                    patch = ContactPatch(placement)
                else:
                    patch = ContactPatch(self.data.oMf[self.model.getFrameId(self.l_eeName)])  
                phase.addContact(self.l_eeName, patch)
            else:
                if index > 3:
                    placement = cs.p[index].oMf_Ri
                    patch = ContactPatch(placement)
                else:
                    patch = ContactPatch(self.data.oMf[self.model.getFrameId(self.r_eeName)]) 
                phase.addContact(self.r_eeName, patch)

        if index%3 == 2:
            phase.c_init = cs.getCOMSeriesFromePhase(index)[:, 0]
            phase.dc_init = np.zeros((3, 1))# cs.getCOMdotSeriesFromePhase(index)[:, 0]
            phase.ddc_init = np.zeros((3, 1))
            
            if self.time_set:
                phase.timeInitial = cs.p[index].time[0]

            if index < cs_size-1:
                phase.c_final = cs.getCOMSeriesFromePhase(index+2)[:, 0]
                phase.dc_final = np.zeros((3, 1)) #cs.getCOMdotSeriesFromePhase(index+2)[:, 0]
                phase.ddc_final = np.zeros((3, 1))
                phase.L_final = np.zeros((3,1))
                phase.dL_final = np.zeros((3,1))
                if self.time_set:
                    phase.timeFinal = cs.p[index+2].time[0]
            else: 
                phase.c_final = cs.getCOMSeriesFromePhase(index)[:, -1]
                phase.dc_final = np.zeros((3, 1))
                phase.ddc_final = np.zeros((3, 1))

                phase.L_final = np.zeros((3,1))
                phase.dL_final = np.zeros((3,1))
 
                if self.time_set:
                    phase.timeFinal = cs.p[index].time[-1]

            if cs.p[index-1].ssp == 'Lf': #  Left support
                if index > 3:
                    placement = cs.p[index].oMf_Li
                    patch = ContactPatch(placement)
                else:
                    patch = ContactPatch(self.data.oMf[self.model.getFrameId(self.l_eeName)]) 
                phase.addContact(self.l_eeName, patch)
                
                placement =  cs.p[index].oMf_Rf
                patch = ContactPatch(placement)
                phase.addContact(self.r_eeName, patch)
            else:
                placement = cs.p[index].oMf_Lf
                patch = ContactPatch(placement)
                phase.addContact(self.l_eeName, patch)

                if index > 3:
                    placement =  cs.p[index].oMf_Ri
                    patch = ContactPatch(placement)
                else:
                    patch = ContactPatch(self.data.oMf[self.model.getFrameId(self.r_eeName)])               
                phase.addContact(self.r_eeName, patch)

        return phase

    def createContactSequenceWithCurves(self):
        p_id = 0  # phase id in cs
        p0 = self.cs.contactPhases[0]
        c_init = self.raw_cs.getCOMSeriesFromePhase(0)[:, 0].reshape(3,1)
        p0.timeInitial = self.TIME_SHIFT_COM

        c_t = c_init.reshape(3, 1)
        dc_t = p0.dc_init.reshape(3, 1)
        ddc_t = p0.ddc_init.reshape(3, 1)
        L_t = p0.L_init.reshape(3, 1)
        dL_t = p0.dL_init.reshape(3, 1)
        times = np.array(self.TIME_SHIFT_COM)
        current_t = self.TIME_SHIFT_COM

        check_New = False
        dL_USE = False

        for i in range (self.raw_cs_size):
            if i == 0: # first phase
                k = len(self.raw_cs.p[i].time)
                for j in range (k): 
                    if j == 0:
                        dt = self.raw_cs.p[i].time[j+1]
                        ddc = self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1] / dt
                    elif j < k -1:
                        dt = self.raw_cs.p[i].time[j+1] - self.raw_cs.p[i].time[j]
                        ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1] -self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j])  / dt
                    else:
                        dt = self.raw_cs.p[i+1].time[0] - self.raw_cs.p[i].time[-1]
                        ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, 0] -self.raw_cs.getCOMdotSeriesFromePhase(i)[:, -1])  / dt

                    if j < k -1:
                        c = self.raw_cs.getCOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        dc = self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        L = self.raw_cs.getMOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        dL = self.raw_cs.getMOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                    else:
                        c = self.raw_cs.getCOMSeriesFromePhase(i+1)[:, 0].reshape(3, 1)
                        dc = self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, 0].reshape(3, 1)
                        L = self.raw_cs.getMOMSeriesFromePhase(i+1)[:, 0].reshape(3, 1)
                        dL = self.raw_cs.getMOMdotSeriesFromePhase(i+1)[:, 0].reshape(3, 1)

                    c_t = np.append(c_t, c.reshape(3,1), axis = 1)
                    dc_t = np.append(dc_t, dc.reshape(3,1), axis = 1)
                    ddc_t = np.append(ddc_t, ddc.reshape(3,1), axis = 1)
                    L_t = np.append(L_t, L.reshape(3,1), axis = 1)
                    if dL_USE:
                        dL_t = np.append(dL_t, dL.reshape(3,1), axis = 1)
                    else:
                        dL_t = np.append(dL_t, np.zeros((3,1)), axis = 1)
                    current_t += dt
                    times = np.append(times, current_t)
                
                check_New = True
            if i%3 == 1:
                k = len(self.raw_cs.p[i].time) 
                for j in range (k):
                    if j < k-1:
                        dt = self.raw_cs.p[i].time[j+1] - self.raw_cs.p[i].time[j]
                        ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1] -self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j])  / dt
                    else:
                        dt = self.raw_cs.p[i+1].time[0] - self.raw_cs.p[i].time[-1]
                        ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, 0] -self.raw_cs.getCOMdotSeriesFromePhase(i)[:,-1])  / dt

                    if j < k-1:
                        c = self.raw_cs.getCOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        dc = self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        L = self.raw_cs.getMOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        dL = self.raw_cs.getMOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                    else:
                        c = self.raw_cs.getCOMSeriesFromePhase(i+1)[:, 0].reshape(3, 1)
                        dc = self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, 0].reshape(3, 1)
                        L = self.raw_cs.getMOMSeriesFromePhase(i+1)[:, 0].reshape(3, 1)
                        dL = self.raw_cs.getMOMdotSeriesFromePhase(i+1)[:, 0].reshape(3, 1)

                    c_t = np.append(c_t, c.reshape(3,1), axis = 1)
                    dc_t = np.append(dc_t, dc.reshape(3,1), axis = 1)
                    ddc_t = np.append(ddc_t, ddc.reshape(3,1), axis = 1)
                    L_t = np.append(L_t, L.reshape(3,1), axis = 1)
                    if dL_USE:
                        dL_t = np.append(dL_t, dL.reshape(3,1), axis = 1)
                    else:
                        dL_t = np.append(dL_t, np.zeros((3,1)), axis = 1)
                    current_t += dt
                    times = np.append(times, current_t)
                    
                check_New = True
            if i%3 == 2:
                if i+1 is not self.raw_cs_size:
                    k = len(self.raw_cs.p[i].time) + len(self.raw_cs.p[i+1].time)
                    k1 = len(self.raw_cs.p[i].time)
                    k2 = len(self.raw_cs.p[i+1].time)
                    
                    for j in range (k):
                        if j < k1-1:
                            dt = self.raw_cs.p[i].time[j+1] - self.raw_cs.p[i].time[j]
                            ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1] -self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j])  / dt   
                        else:
                            if j == k1:
                                dt = self.raw_cs.p[i+1].time[j-k1] - self.raw_cs.p[i].time[-1]
                                ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, j-k1] -self.raw_cs.getCOMdotSeriesFromePhase(i)[:, -1])  / dt
                            elif j < k1 + k2:
                                dt = self.raw_cs.p[i+1].time[j-k1] - self.raw_cs.p[i+1].time[j-k1-1]
                                ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, j-k1] -self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, j-k1-1])  / dt
                            else:
                                dt = self.raw_cs.p[i+2].time[0] - self.raw_cs.p[i+1].time[j-k1]
                                ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i+2)[:, 0] -self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, j-k1])  / dt
                        if j < k1-1:
                            c = self.raw_cs.getCOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                            dc = self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                            L = self.raw_cs.getMOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                            dL = self.raw_cs.getMOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        elif j < k1 + k2 - 1:
                            c = self.raw_cs.getCOMSeriesFromePhase(i+1)[:, j-k1].reshape(3, 1)
                            dc = self.raw_cs.getCOMdotSeriesFromePhase(i+1)[:, j-k1].reshape(3, 1)
                            L = self.raw_cs.getMOMSeriesFromePhase(i+1)[:, j-k1].reshape(3, 1)
                            dL = self.raw_cs.getMOMdotSeriesFromePhase(i+1)[:, j-k1].reshape(3, 1)
                        else:
                            c = self.raw_cs.getCOMSeriesFromePhase(i+2)[:, 0].reshape(3, 1)
                            dc = self.raw_cs.getCOMdotSeriesFromePhase(i+2)[:, 0].reshape(3, 1)
                            L = self.raw_cs.getMOMSeriesFromePhase(i+2)[:, 0].reshape(3, 1)
                            dL = self.raw_cs.getMOMdotSeriesFromePhase(i+2)[:, 0].reshape(3, 1)

                        c_t = np.append(c_t, c.reshape(3,1), axis = 1)
                        dc_t = np.append(dc_t, dc.reshape(3,1), axis = 1)
                        ddc_t = np.append(ddc_t, ddc.reshape(3,1), axis = 1)
                        L_t = np.append(L_t, L.reshape(3,1), axis = 1)
                        if dL_USE:
                            dL_t = np.append(dL_t, dL.reshape(3,1), axis = 1)
                        else:
                            dL_t = np.append(dL_t, np.zeros((3,1)), axis = 1)
                        current_t += dt
                        times = np.append(times, current_t)
                        check_New = True
                else:
                    k = len(self.raw_cs.p[i].time) -1
                    for j in range (k):
                        dt = self.raw_cs.p[i].time[j+1] - self.raw_cs.p[i].time[j]
                        ddc = (self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1] - self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j] )/ dt

                        c = self.raw_cs.getCOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        dc = self.raw_cs.getCOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        L = self.raw_cs.getMOMSeriesFromePhase(i)[:, j+1].reshape(3, 1)
                        dL = self.raw_cs.getMOMdotSeriesFromePhase(i)[:, j+1].reshape(3, 1)
        
                        c_t = np.append(c_t, c.reshape(3,1), axis = 1)
                        dc_t = np.append(dc_t, dc.reshape(3,1), axis = 1)
                        ddc_t = np.append(ddc_t, ddc.reshape(3,1), axis = 1)
                        L_t = np.append(L_t, L.reshape(3,1), axis = 1)
                        dL_t = np.append(dL_t, dL.reshape(3,1), axis = 1)
                        current_t += dt
                        times = np.append(times, current_t)

            if (check_New and p_id < self.raw_cs_size - 1): 
                phase = self.cs.contactPhases[p_id]
                setCOMtrajectoryFromPoints(phase, c_t, dc_t, ddc_t, times, overwriteInit= (p_id > 0))
                setAMtrajectoryFromPoints(phase, L_t, dL_t, times, overwriteInit= (p_id > 0))
                # set final time :
                phase.timeFinal = times[-1]
                # Start new phase :
                p_id += 1
                phase = self.cs.contactPhases[p_id]

                # set initial time :
                phase.timeInitial = times[-1]
                # reset arrays of values to only the last point :
                c_t = c_t[:,-1].reshape(3,1)
                dc_t = dc_t[:,-1].reshape(3,1)
                ddc_t = ddc_t[:,-1].reshape(3,1)
                L_t = L_t[:,-1].reshape(3,1)
                dL_t = dL_t[:,-1].reshape(3,1)
                times = times[-1]
                check_New = False

        phase = self.cs.contactPhases[-1]
        setCOMtrajectoryFromPoints(phase, c_t, dc_t, ddc_t, times, overwriteFinal = not  (self.DURATION_CONNECT_GOAL > 0.))
        setAMtrajectoryFromPoints(phase, L_t, dL_t, times, overwriteFinal = not (self.DURATION_CONNECT_GOAL > 0.))
        phase.timeFinal = times[-1]
                
        if self.TIME_SHIFT_COM > 0:
            connectPhaseTrajToInitialState(self.cs.contactPhases[0], self.TIME_SHIFT_COM)
        if self.DURATION_CONNECT_GOAL > 0:
            connectPhaseTrajToFinalState(self.cs.contactPhases[-1], self.DURATION_CONNECT_GOAL)
    
    
        
