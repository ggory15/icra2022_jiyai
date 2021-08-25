#
# Copyright (c) 2020 CNRS
#
#
# This file is part of multicontact-locomotion-planning
# multicontact-locomotion-planning is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# hpp-core is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# hpp-core  If not, see
# <http://www.gnu.org/licenses/>.

CMAKE_MINIMUM_REQUIRED(VERSION 2.8)


SET(PROJECT_NAME tsid_api)
SET(PROJECT_DESCRIPTION "Wholebody motion planner for jiyai-traj")
SET(PROJECT_URL "https://github.com/ggory15")

INCLUDE(cmake/base.cmake)
INCLUDE(cmake/python.cmake)

COMPUTE_PROJECT_ARGS(PROJECT_ARGS LANGUAGES CXX)
PROJECT(${PROJECT_NAME} ${PROJECT_ARGS})

FINDPYTHON(3) 

ADD_REQUIRED_DEPENDENCY("eigenpy >= 2.0")

ADD_REQUIRED_DEPENDENCY("pinocchio >= 2.2")
ADD_REQUIRED_DEPENDENCY("multicontact-api >= 2.0")
ADD_REQUIRED_DEPENDENCY("tsid >= 1.2")

# INSTALL(DIRECTORY momentumopt_configs
#   DESTINATION "share/mlp")

ADD_SUBDIRECTORY(python)



