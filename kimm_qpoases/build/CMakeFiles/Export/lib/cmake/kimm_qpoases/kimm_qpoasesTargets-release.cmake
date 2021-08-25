#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "kimm_qpoases::kimm_qpoases" for configuration "Release"
set_property(TARGET kimm_qpoases::kimm_qpoases APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(kimm_qpoases::kimm_qpoases PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libkimm_qpoases.so.1.0.0"
  IMPORTED_SONAME_RELEASE "libkimm_qpoases.so.1.0.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS kimm_qpoases::kimm_qpoases )
list(APPEND _IMPORT_CHECK_FILES_FOR_kimm_qpoases::kimm_qpoases "${_IMPORT_PREFIX}/lib/libkimm_qpoases.so.1.0.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
