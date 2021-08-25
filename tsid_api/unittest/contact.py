from tsid_ggory import ContactData, Phases
import sys, os
import pinocchio as pin
import example_robot_data
import tsid
import numpy as np

display = False
folder_path = os.getcwd() ## $Home/git/tsid_ggory/unittest something like that.
input_location = folder_path + '/../' + 'result/Darpa/'
input_name = '6LookAhead_Refined.p'
input_ = input_location + input_name
output_ = input_location + '6LookAhead_cs.xml'

robot = example_robot_data.load('talos')
cs_data_ = ContactData(input_, robot)
cs_ = cs_data_.createData()
cs_data_.save(output_)

if display:
    import gepetto.corbaserver
    import subprocess, time
    viewer = pin.visualize.GepettoVisualizer

    launched = subprocess.getstatusoutput("ps aux |grep 'gepetto-gui'|grep -v 'grep'|wc -l")
    if int(launched[1]) == 0:
        os.system('gepetto-gui &')
    time.sleep(1)
    viz = viewer(robot.model, robot.collision_model, robot.visual_model)
    viz.initViewer(loadModel=True)
    viz.displayCollisions(False)
    viz.displayVisuals(True)
    
    gui = viz.viewer.gui
    cameraTF = [4.388, -3.678, 2.83755, 0.4837, 0.1551, 0.1542, 0.84742]
    window_id = gui.getWindowID("python-pinocchio")
    gui.setCameraTransform(window_id, cameraTF)
    gui.setBackgroundColor1(window_id, [1, 1, 1, 1])
    gui.setBackgroundColor2(window_id, [1, 1, 1, 1])

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

            gui.addBox('world/box'+str(i), width, height, depth, [0.8, 0.8, 0.8, 1])
            gui.applyConfiguration('world/box'+str(i), center.tolist() + quat.tolist())
            gui.refresh()

    from tsid_ggory.util.util import displaySteppingStones, displayCOMPoints, displayCOMTrajectory
    displaySteppingStones(cs_, gui, robot)
    displayCOMPoints(cs_, gui)
    colors = [[0., 0., 1., 1.], [0., 1., 0., 1.]]
    displayCOMTrajectory(cs_, gui, "world", 0.01, colors, linewidth=5.0)

    viz.display(cs_data_.q_ref)
    

