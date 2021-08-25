#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "tsid::tsid" for configuration ""
set_property(TARGET tsid::tsid APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(tsid::tsid PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libtsid.so.1.6.0"
  IMPORTED_SONAME_NOCONFIG "libtsid.so.1.6.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS tsid::tsid )
list(APPEND _IMPORT_CHECK_FILES_FOR_tsid::tsid "${_IMPORT_PREFIX}/lib/libtsid.so.1.6.0" )

# Import target "tsid::tsid_pywrap" for configuration ""
set_property(TARGET tsid::tsid_pywrap APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(tsid::tsid_pywrap PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/python3/dist-packages/tsid/libtsid_pywrap.so"
  IMPORTED_SONAME_NOCONFIG "libtsid_pywrap.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS tsid::tsid_pywrap )
list(APPEND _IMPORT_CHECK_FILES_FOR_tsid::tsid_pywrap "${_IMPORT_PREFIX}/lib/python3/dist-packages/tsid/libtsid_pywrap.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
