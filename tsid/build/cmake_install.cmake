# Install script for directory: /home/ggory15/jiyai_git/icra2022_jiyai/tsid

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/include/tsid/config.hh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/include/tsid/deprecated.hh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/include/tsid/warning.hh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so.1.6.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so.1.6.0")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so.1.6.0"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/libtsid.so.1.6.0")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so.1.6.0" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so.1.6.0")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so.1.6.0"
         OLD_RPATH "/opt/openrobots/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so.1.6.0")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/libtsid.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so"
         OLD_RPATH "/opt/openrobots/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libtsid.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tsid" TYPE FILE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/tsid.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/config.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/deprecation.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/utils" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/utils/statistics.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/utils" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/utils/stop-watch.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/utils" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/utils/Stdafx.hh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/math" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/math/fwd.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/math" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/math/utils.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/math" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/math/constraint-base.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/math" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/math/constraint-equality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/math" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/math/constraint-inequality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/math" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/math/constraint-bound.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/fwd.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-base.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-motion.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-actuation.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-contact-force.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-com-equality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-se3-equality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-contact-force-equality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-cop-equality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-actuation-equality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-actuation-bounds.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-joint-bounds.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-joint-posture.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-joint-posVelAcc-bounds.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-capture-point-inequality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/tasks" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/tasks/task-angular-momentum-equality.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/contacts" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/contacts/fwd.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/contacts" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/contacts/contact-base.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/contacts" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/contacts/contact-6d.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/contacts" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/contacts/contact-point.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/trajectories" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/trajectories/fwd.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/trajectories" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/trajectories/trajectory-base.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/trajectories" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/trajectories/trajectory-se3.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/trajectories" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/trajectories/trajectory-euclidian.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/fwd.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/utils.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-output.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-base.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-factory.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-factory.hxx")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-qpoases.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-eiquadprog.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-eiquadprog-rt.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-eiquadprog-rt.hxx")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/solvers" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/solvers/solver-HQP-eiquadprog-fast.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/robots" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/robots/fwd.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/robots" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/robots/robot-wrapper.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/formulations" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/formulations/contact-level.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/formulations" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/formulations/inverse-dynamics-formulation-base.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/tsid/formulations" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ OWNER_WRITE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/include/tsid/formulations/inverse-dynamics-formulation-acc-force.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/tsid" TYPE FILE FILES
    "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/generated/tsidConfig.cmake"
    "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/generated/tsidConfigVersion.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/tsid/tsidTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/tsid/tsidTargets.cmake"
         "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/CMakeFiles/Export/lib/cmake/tsid/tsidTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/tsid/tsidTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/tsid/tsidTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/tsid" TYPE FILE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/CMakeFiles/Export/lib/cmake/tsid/tsidTargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^()$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/tsid" TYPE FILE FILES "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/CMakeFiles/Export/lib/cmake/tsid/tsidTargets-noconfig.cmake")
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/bindings/cmake_install.cmake")
  include("/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/tests/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/ggory15/jiyai_git/icra2022_jiyai/tsid/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
