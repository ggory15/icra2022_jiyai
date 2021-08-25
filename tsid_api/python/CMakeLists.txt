
SET(${PROJECT_NAME}_PYTHON_FILES
    __init__.py
    loco_data.py
    contact_data.py
    interpolation.py
    phase.py
    tsid_wb.py
    )

SET(${PROJECT_NAME}_CONF_FILES
    __init__.py
    conf_talos.py
    )

SET(${PROJECT_NAME}_UTIL_FILES
    __init__.py
    util.py
    cs_util.py
    simulator.py
    )

SET(${PROJECT_NAME}_TRAJ_FILES
    __init__.py
    bezier_predef.py
    limb_rrt.py
    limb_rrt_optimized.py
    )   

    
# Install python files : 
FOREACH(file ${${PROJECT_NAME}_PYTHON_FILES})
  PYTHON_INSTALL_ON_SITE("tsid_api" ${file})
ENDFOREACH(file ${${PROJECT_NAME}_PYTHON_FILES})

FOREACH(file ${${PROJECT_NAME}_CONF_FILES})
  PYTHON_INSTALL_ON_SITE("tsid_api/conf" ${file})
ENDFOREACH(file ${${PROJECT_NAME}_CONF_FILES})

FOREACH(file ${${PROJECT_NAME}_UTIL_FILES})
  PYTHON_INSTALL_ON_SITE("tsid_api/util" ${file})
ENDFOREACH(file ${${PROJECT_NAME}_UTIL_FILES})

FOREACH(file ${${PROJECT_NAME}_TRAJ_FILES})
  PYTHON_INSTALL_ON_SITE("tsid_api/trajectories" ${file})
ENDFOREACH(file ${${PROJECT_NAME}_TRAJ_FILES})
