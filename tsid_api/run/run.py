import cmd, sys, os
import numpy as np
import copy
from tsid_api import LocoData, ContactData, Phases
from tsid_api.tsid_wb import *
import pinocchio as pin
import example_robot_data
import gepetto.corbaserver
import subprocess, time
from multicontact_api import ContactSequence
from tsid_api.conf import conf_talos as cfg
from tsid_api.util.util import displaySteppingStones, displayCOMPoints, displayCOMTrajectory, displayEffectorTrajectories
from tsid_api.util.simulator import display_wb
from pinocchio.visualize import GepettoVisualizer

class CMDShell(cmd.Cmd):
    intro = "Welcome to the tsid shell by ggory15.\nType help or ? to list commands.\n"
    prompt = "(script) "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.display = False
        self.robot = example_robot_data.load('talos')
        self.viz =[]

        launched = subprocess.getstatusoutput("ps aux |grep 'gepetto-gui'|grep -v 'grep'|wc -l")
        if int(launched[1]) == 0:
            self.display = False
        else:
            self.do_viewer(1)

        folder_path = os.getcwd() ## $Home/git/tsid_ggory/unittest something like that.
        self.input_location = folder_path + '/../' + 'data/' 
        self.output_location = folder_path + '/../'+ 'result/'
        self.input_name = '/test/sanghyun/darpa_2steps'        
        
        self.refined_output_ = []
        nargs = len(sys.argv)
        if nargs == 1:
            print ('Target Data:', self.input_name)
        elif nargs == 2:
            self.input_name = sys.argv[1]
            print ('Target Data:', self.input_name)
        else:
            print ('Wrong input, running the default data')

    def do_refine(self, arg):
        'Refine Raw data (from Jiyai)'
        input_ = self.input_location + self.input_name + '.p'
        self.refined_output_ = self.output_location + self.input_name + '_refined.p'
        Refined = LocoData(input_, self.refined_output_)
        Refined.refine() ## auto-save to output_location

    def do_contactsequence(self, arg):
        if (self.refined_output_ != []):
            cs_data_ = ContactData(self.refined_output_, self.robot)
        else:
            cs_data_ = ContactData(self.output_location + self.input_name + '_refined.p', self.robot)
        self.cs_ = cs_data_.createData()
        self.cs_output_ = self.output_location + self.input_name + '_cs.xml'
        cs_data_.save(self.cs_output_)

        if (self.display):
            terrain_ = cs_data_.terrain_data

            if terrain_ is not None:
                data_size = len(terrain_['width'])
                depth = 0.05
                for i in range(data_size):
                    width = terrain_['width'][i]
                    height = terrain_['height'][i]
                    center = terrain_['center'][i] -depth * terrain_['normal'][i].reshape(3)/2.0

                    if i == 0: 
                        width = terrain_['width'][i] / 2.0
                        height = terrain_['height'][i] * 1.5
                        center = terrain_['center'][i] + np.array([width, 0, 0]) / 2.0 - depth * terrain_['normal'][i].reshape(3)/2.0      

                    if i == data_size - 1:
                        width = terrain_['width'][i] / 50.0
                        height = terrain_['height'][i] * 1.5
                        center = terrain_['center'][i] - np.array([terrain_['width'][i], 0, 0]) / 2.0 + np.array([width, 0, 0]) / 2.0 - depth * terrain_['normal'][i].reshape(3)/2.0 

                    quat = terrain_['quat'][i]

                    self.gui.addBox('world/box'+str(i), width, height, depth, [0.8, 0.8, 0.8, 1])
                    self.gui.applyConfiguration('world/box'+str(i), center.tolist() + quat.tolist())
                    self.gui.refresh()

            
            displaySteppingStones(self.cs_, self.gui, self.robot)
            displayCOMPoints(self.cs_, self.gui)
            colors = [[0., 0., 1., 1.], [0., 1., 0., 1.]]
            displayCOMTrajectory(self.cs_, self.gui, "world", 0.01, colors, linewidth=5.0)
            self.viz.display(cs_data_.q_ref)

    def do_ee_traj(self, arg):
        from tsid_api.trajectories import bezier_predef
        self.ref_output_ = self.output_location + self.input_name + '_ref'

        cs = ContactSequence()
        cs.loadFromXML(self.output_location + self.input_name + '_cs.xml', "ContactSequence")
        cs_ref = bezier_predef.generate_effector_trajectories_for_sequence_bezier(cfg, cs, self.ref_output_)

        if (self.display):
            displayEffectorTrajectories(cs_ref, self.gui, self.robot, "_ref", 0.6)

    def do_tsid(self, arg):
        cs_ref = ContactSequence()
        cs_ref.loadFromBinary(self.output_location + self.input_name + '_ref') 
        cs_wb = generate_wholebody_tsid(cfg, cs_ref, self.robot, self.viz)
        cs_wb.saveAsBinary(self.output_location + self.input_name + '_wb')
        
    def do_display(self, arg):
        if not self.display:
            self.do_viewer(arg)
            self.do_contactsequence(arg)
        cs_wb = ContactSequence()
        cs_wb.loadFromBinary(self.output_location + self.input_name + '_wb')
        q_t = cs_wb.concatenateQtrajectories()
        display_wb(self.viz, q_t)

    def do_viewer(self, arg):
        self.display =True

        viewer = pin.visualize.GepettoVisualizer

        launched = subprocess.getstatusoutput("ps aux |grep 'gepetto-gui'|grep -v 'grep'|wc -l")
        if int(launched[1]) == 0:
            self.gepetto_viewer = subprocess.Popen("gepetto-gui", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        time.sleep(1)
        self.viz = viewer(self.robot.model, self.robot.collision_model, self.robot.visual_model)
        self.viz.initViewer(loadModel=True)
        self.viz.displayCollisions(False)
        self.viz.displayVisuals(True)
        
        self.gui = self.viz.viewer.gui
        cameraTF = [4.388, -3.678, 2.83755, 0.4837, 0.1551, 0.1542, 0.84742]
        window_id = self.gui.getWindowID("python-pinocchio")
        self.gui.setCameraTransform(window_id, cameraTF)
        self.gui.setBackgroundColor1(window_id, [1, 1, 1, 1])
        self.gui.setBackgroundColor2(window_id, [1, 1, 1, 1])

    def do_quit(self, arg):
        'Quit the tsid console'
        import signal
        if (self.display):
            os.killpg(os.getpgid(self.gepetto_viewer.pid), signal.SIGTERM)
        
        return True

    def do_autogen(self, arg):
        self.do_refine(arg)
        self.do_contactsequence(arg)
        self.do_ee_traj(arg)
        self.do_tsid(arg)

if __name__ == '__main__':
    CMDShell().cmdloop()
