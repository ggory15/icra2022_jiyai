# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Produce verbose output by default.
VERBOSE = 1

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build

# Utility rule file for dist_tarxz.

# Include the progress variables for this target.
include CMakeFiles/dist_tarxz.dir/progress.make

CMakeFiles/dist_tarxz:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating tar.xz tarball and its signature..."
	/usr/bin/tar -cJf tsid_api-UNKNOWN-dirty.tar.xz tsid_api-UNKNOWN-dirty/ && /usr/bin/gpg --detach-sign --armor -o /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build/tsid_api-UNKNOWN-dirty.tar.xz.sig /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build/tsid_api-UNKNOWN-dirty.tar.xz

dist_tarxz: CMakeFiles/dist_tarxz
dist_tarxz: CMakeFiles/dist_tarxz.dir/build.make

.PHONY : dist_tarxz

# Rule to build all files generated by this target.
CMakeFiles/dist_tarxz.dir/build: dist_tarxz

.PHONY : CMakeFiles/dist_tarxz.dir/build

CMakeFiles/dist_tarxz.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/dist_tarxz.dir/cmake_clean.cmake
.PHONY : CMakeFiles/dist_tarxz.dir/clean

CMakeFiles/dist_tarxz.dir/depend:
	cd /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build /home/ggory15/jiyai_git/icra2022_jiyai/tsid_api/build/CMakeFiles/dist_tarxz.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/dist_tarxz.dir/depend
