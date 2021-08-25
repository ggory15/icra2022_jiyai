import numpy as np
import pickle
from scipy.spatial.transform import Rotation

class LocoData:
    """
    Get refined data to use it on tsid
    """

    def __init__(self, input_location, output_location):
        self.output_location = output_location
        self.refineddata = []

        with open(input_location, 'rb') as f:
            data= pickle.load(f)

        self.rawdata = data["Trajectory_of_All_Rounds"]
        self.casadi_param = data["CasadiParameters"]
        self.lv1_index = data["VarIdx_of_All_Levels"]["Level1_Var_Index"]
        self.lv2_index = data["VarIdx_of_All_Levels"]["Level2_Var_Index"]
        self.terrain_flag = False

        #Get FootStep/Terrain Quaternions
        if "TerrainModel" in data:
            self.patches = data["TerrainModel"]
            self.quats = []

            for patch in self.patches:
                quat = self.getQuaternion(patch)
                self.quats.append(quat)
            if len(self.quats) < 2:
                self.terrain_flag = False
            else:
                self.terrain_flag = True

    def refine(self):
        casadiPrevParams = []
        TSID_Trajectories = []
        for roundIdx in range(len(self.rawdata)):
            traj = self.rawdata[roundIdx]
            casadiParams = self.casadi_param[roundIdx]
            if roundIdx > 0:
                casadiPrevParams = self.casadi_param[roundIdx - 1]

            #Get raw data
            x_traj = traj[self.lv1_index["x"][0]:self.lv1_index["x"][1]+1]
            y_traj = traj[self.lv1_index["y"][0]:self.lv1_index["y"][1]+1]
            z_traj = traj[self.lv1_index["z"][0]:self.lv1_index["z"][1]+1]
            xdot_traj = traj[self.lv1_index["xdot"][0]:self.lv1_index["xdot"][1]+1]
            ydot_traj = traj[self.lv1_index["ydot"][0]:self.lv1_index["ydot"][1]+1]
            zdot_traj = traj[self.lv1_index["zdot"][0]:self.lv1_index["zdot"][1]+1]

            Lx_traj = traj[self.lv1_index["Lx"][0]:self.lv1_index["Lx"][1]+1]
            Ly_traj = traj[self.lv1_index["Ly"][0]:self.lv1_index["Ly"][1]+1]
            Lz_traj = traj[self.lv1_index["Lz"][0]:self.lv1_index["Lz"][1]+1]
            Ldotx_traj = traj[self.lv1_index["Ldotx"][0]:self.lv1_index["Ldotx"][1]+1]
            Ldoty_traj = traj[self.lv1_index["Ldoty"][0]:self.lv1_index["Ldoty"][1]+1]
            Ldotz_traj = traj[self.lv1_index["Ldotz"][0]:self.lv1_index["Ldotz"][1]+1]

            px_res = traj[self.lv1_index["px"][0]:self.lv1_index["px"][1]+1]
            py_res = traj[self.lv1_index["py"][0]:self.lv1_index["py"][1]+1]
            pz_res = traj[self.lv1_index["pz"][0]:self.lv1_index["pz"][1]+1]

            Ts_res = traj[self.lv1_index["Ts"][0]:self.lv1_index["Ts"][1]+1]
            
            #get traj for each phase
            Phase1_TimeSeries = np.linspace(0,Ts_res[0],8)
            Phase2_TimeSeries = np.linspace(Ts_res[0],Ts_res[1],8)
            Phase3_TimeSeries = np.linspace(Ts_res[1],Ts_res[2],8)

            Phase1_x = x_traj[0:8]
            Phase2_x = x_traj[7:15]
            Phase3_x = x_traj[14:]

            Phase1_y = y_traj[0:8]
            Phase2_y = y_traj[7:15]
            Phase3_y = y_traj[14:]

            Phase1_z = z_traj[0:8]
            Phase2_z = z_traj[7:15]
            Phase3_z = z_traj[14:]

            Phase1_xdot = xdot_traj[0:8]
            Phase2_xdot = xdot_traj[7:15]
            Phase3_xdot = xdot_traj[14:]

            Phase1_ydot = ydot_traj[0:8]
            Phase2_ydot = ydot_traj[7:15]
            Phase3_ydot = ydot_traj[14:]

            Phase1_zdot = zdot_traj[0:8]
            Phase2_zdot = zdot_traj[7:15]
            Phase3_zdot = zdot_traj[14:]

            Phase1_Lx = Lx_traj[0:8]
            Phase2_Lx = Lx_traj[7:15]
            Phase3_Lx = Lx_traj[14:]

            Phase1_Ly = Ly_traj[0:8]
            Phase2_Ly = Ly_traj[7:15]
            Phase3_Ly = Ly_traj[14:]

            Phase1_Lz = Lz_traj[0:8]
            Phase2_Lz = Lz_traj[7:15]
            Phase3_Lz = Lz_traj[14:]

            Phase1_Ldotx = Ldotx_traj[0:8]
            Phase2_Ldotx = Ldotx_traj[7:15]
            Phase3_Ldotx = Ldotx_traj[14:]

            Phase1_Ldoty = Ldoty_traj[0:8]
            Phase2_Ldoty = Ldoty_traj[7:15]
            Phase3_Ldoty = Ldoty_traj[14:]

            Phase1_Ldotz = Ldotz_traj[0:8]
            Phase2_Ldotz = Ldotz_traj[7:15]
            Phase3_Ldotz = Ldotz_traj[14:]

            PLx_init = casadiParams[14]
            PLy_init = casadiParams[15]
            PLz_init = casadiParams[16]

            PRx_init = casadiParams[17]
            PRy_init = casadiParams[18]
            PRz_init = casadiParams[19]

            LeftSwingFlag = casadiParams[0]
            RightSwingFlag = casadiParams[1]
            
            TSIDTrajectory = {}
            #Init Double Phase
            TSIDTrajectory["InitDouble_TimeSeries"]=Phase1_TimeSeries
            TSIDTrajectory["InitDouble_x"]=Phase1_x
            TSIDTrajectory["InitDouble_y"]=Phase1_y
            TSIDTrajectory["InitDouble_z"]=Phase1_z
            TSIDTrajectory["InitDouble_Lx"]=Phase1_Lx
            TSIDTrajectory["InitDouble_Ly"]=Phase1_Ly
            TSIDTrajectory["InitDouble_Lz"]=Phase1_Lz
            TSIDTrajectory["InitDouble_xdot"]=Phase1_xdot
            TSIDTrajectory["InitDouble_ydot"]=Phase1_ydot
            TSIDTrajectory["InitDouble_zdot"]=Phase1_zdot
            TSIDTrajectory["InitDouble_Ldotx"]=Phase1_Ldotx
            TSIDTrajectory["InitDouble_Ldoty"]=Phase1_Ldoty
            TSIDTrajectory["InitDouble_Ldotz"]=Phase1_Ldotz

            #Swing Phase
            TSIDTrajectory["Swing_TimeSeries"]=Phase2_TimeSeries
            TSIDTrajectory["Swing_x"]=Phase2_x
            TSIDTrajectory["Swing_y"]=Phase2_y
            TSIDTrajectory["Swing_z"]=Phase2_z
            TSIDTrajectory["Swing_Lx"]=Phase2_Lx
            TSIDTrajectory["Swing_Ly"]=Phase2_Ly
            TSIDTrajectory["Swing_Lz"]=Phase2_Lz
            TSIDTrajectory["Swing_xdot"]=Phase2_xdot
            TSIDTrajectory["Swing_ydot"]=Phase2_ydot
            TSIDTrajectory["Swing_zdot"]=Phase2_zdot
            TSIDTrajectory["Swing_Ldotx"]=Phase2_Ldotx
            TSIDTrajectory["Swing_Ldoty"]=Phase2_Ldoty
            TSIDTrajectory["Swing_Ldotz"]=Phase2_Ldotz

            #DoubleSupport Phase
            TSIDTrajectory["DoubleSupport_TimeSeries"]=Phase3_TimeSeries
            TSIDTrajectory["DoubleSupport_x"]=Phase3_x
            TSIDTrajectory["DoubleSupport_y"]=Phase3_y
            TSIDTrajectory["DoubleSupport_z"]=Phase3_z
            TSIDTrajectory["DoubleSupport_Lx"]=Phase3_Lx
            TSIDTrajectory["DoubleSupport_Ly"]=Phase3_Ly
            TSIDTrajectory["DoubleSupport_Lz"]=Phase3_Lz
            TSIDTrajectory["DoubleSupport_xdot"]=Phase3_xdot
            TSIDTrajectory["DoubleSupport_ydot"]=Phase3_ydot
            TSIDTrajectory["DoubleSupport_zdot"]=Phase3_zdot
            TSIDTrajectory["DoubleSupport_Ldotx"]=Phase3_Ldotx
            TSIDTrajectory["DoubleSupport_Ldoty"]=Phase3_Ldoty
            TSIDTrajectory["DoubleSupport_Ldotz"]=Phase3_Ldotz

            #Contact config
            TSIDTrajectory["Init_PL"]=[PLx_init,PLy_init,PLz_init]            
            TSIDTrajectory["Init_PR"]=[PRx_init,PRy_init,PRz_init]            
            TSIDTrajectory["Landing_P"] = list(np.concatenate((px_res,py_res,pz_res),axis=None))
            TSIDTrajectory["LeftSwingFlag"]=LeftSwingFlag
            TSIDTrajectory["RightSwingFlag"]=RightSwingFlag

            if self.terrain_flag == False:
                TSIDTrajectory["Init_L_quat"]=np.array([0,0,0,1])
                TSIDTrajectory["Init_R_quat"]=np.array([0,0,0,1])
                TSIDTrajectory["Landing_quat"]=np.array([0,0,0,1])
            else:   
                if (roundIdx == 0) or (roundIdx > len(self.rawdata)-2):
                    TSIDTrajectory["Init_L_quat"]=np.array([0,0,0,1])
                    TSIDTrajectory["Init_R_quat"]=np.array([0,0,0,1])
                elif (roundIdx == 1):
                    if casadiPrevParams[0] == 1.0:
                        TSIDTrajectory["Init_L_quat"]= self.quats[roundIdx-1]
                        TSIDTrajectory["Init_R_quat"]=np.array([0,0,0,1])   
                    else:
                        TSIDTrajectory["Init_R_quat"]= self.quats[roundIdx-1]
                        TSIDTrajectory["Init_L_quat"]= np.array([0,0,0,1])  
                else:
                    if casadiPrevParams[0] == 1.0:
                        TSIDTrajectory["Init_L_quat"]= self.quats[roundIdx-1]
                        TSIDTrajectory["Init_R_quat"]= self.quats[roundIdx-2]
                    else:
                        TSIDTrajectory["Init_R_quat"]= self.quats[roundIdx-1]
                        TSIDTrajectory["Init_L_quat"]= self.quats[roundIdx-2]    

                if (roundIdx < len(self.rawdata) - 3):
                    TSIDTrajectory["Landing_quat"] = self.quats[roundIdx]
                else:
                    TSIDTrajectory["Landing_quat"] = self.quats[len(self.rawdata) -3]    

            print ("Phase #", roundIdx)
            print ("Init_R", TSIDTrajectory["Init_R_quat"])
            print ("Init_L", TSIDTrajectory["Init_L_quat"])
            print ("Landing_quat", TSIDTrajectory["Landing_quat"])
            print ("")
            TSID_Trajectories.append(TSIDTrajectory)

        TerrainData = {'width': [], 'height': [], 'quat': [], 'center': [], 'normal': []}
        if self.terrain_flag:
            no = len(self.patches)

            for i in range(no):
                TerrainData['width'].append(np.linalg.norm(self.patches[i][1] - self.patches[i][0])) 
                TerrainData['height'].append(np.linalg.norm(self.patches[i][2] - self.patches[i][1]))
                
                x = np.matrix(self.patches[i][0] - self.patches[i][1]).T
                y = np.matrix(self.patches[i][0] - self.patches[i][3]).T
                z = np.cross(x.T, y.T).T
            
                mat_tmp = np.matrix(np.zeros((3,3)))
                mat_tmp[:, 0] = x / np.linalg.norm(x)
                mat_tmp[:, 1] = y / np.linalg.norm(y)
                mat_tmp[:, 2] = z / np.linalg.norm(z)
                r = Rotation.from_matrix(mat_tmp)
                
                TerrainData['quat'].append(r.as_quat())
                TerrainData['normal'].append( z.T / np.linalg.norm(z.T))
                center = self.patches[i][0]  + self.patches[i][1] + self.patches[i][2] + self.patches[i][3]
                TerrainData['center'].append(center/ 4.0)    
        else:
            TerrainData = None

        DumpedResult = {"TSID_Trajectories": TSID_Trajectories, "TerrainData": TerrainData}
        pickle.dump(DumpedResult, open(self.output_location, "wb"))

    def getQuaternion(self, Patch):
        #Input Format
        #p2---------------------p1
        # |                      |
        # |                      |
        # |                      |
        #p3---------------------p4

        p1 = Patch[0]
        p2 = Patch[1]
        p3 = Patch[2]
        p4 = Patch[3]

        #Unrotated Terrain Norm and Tangents
        #TerrainTangentX = np.array([1,0,0])
        #TerrainTangentY = np.array([0,1,0])
        #TerrainNorm = np.array([0,0,1])

        #Case 1 all flat
        if p1[2] == p2[2] and p2[2] == p3[2] and p3[2] == p4[2] and p4[2] == p1[2]:
            #print("Flat Terrain, use the default set up of terrain tangent and norm")
            r = Rotation.from_euler('x', 0, degrees=False) 
            quat = r.as_quat()
        #Case 2, tilt arond Y axis
        elif p1[2] == p4[2] and p2[2] == p3[2] and (not p1[2]-p2[2] == 0) and (not p4[2]-p3[2]==0):
            #print("tilt arond Y axis")
            tiltAngle = np.arctan2(p2[2]-p1[2],p1[0]-p2[0])
            r = Rotation.from_euler('y', tiltAngle, degrees=False) 
            quat = r.as_quat()
            #TerrainTangentX = r.as_matrix()@TerrainTangentX
            #TerrainNorm = r.as_matrix()@TerrainNorm
        #Case 3, tilt around X axis    
        elif p1[2] == p2[2] and p3[2] == p4[2] and (not p2[2]-p3[2] == 0) and (not p1[2]-p4[2]==0):
            tiltAngle = np.arctan2(p1[2]-p4[2],p1[1]-p4[1])
            r = Rotation.from_euler('x', tiltAngle, degrees=False) 
            quat = r.as_quat()
            #TerrainTangentY = r.as_matrix()@TerrainTangentY
            #TerrainNorm = r.as_matrix()@TerrainNorm
            #print("tilt arond X axis")
        else:
            raise Exception("Un-defined Terrain Type")

        return quat
