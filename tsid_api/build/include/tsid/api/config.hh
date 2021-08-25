/* 
 * This file has been automatically generated by the jrl-cmakemodules.
 * Please see https://github.com/jrl-umi3218/jrl-cmakemodules/blob/master/config.hh.cmake for details.
*/

#ifndef TSID_API_CONFIG_HH
# define TSID_API_CONFIG_HH

// Package version (header).
# define TSID_API_VERSION_UNKNOWN_TAG 0 // Used to mention that the current version is unknown.
# define TSID_API_VERSION "UNKNOWN-dirty"
# define TSID_API_MAJOR_VERSION TSID_API_VERSION_UNKNOWN_TAG
# define TSID_API_MINOR_VERSION TSID_API_VERSION_UNKNOWN_TAG
# define TSID_API_PATCH_VERSION TSID_API_VERSION_UNKNOWN_TAG

#define TSID_API_VERSION_AT_LEAST(major, minor, patch) (TSID_API_MAJOR_VERSION>major || (TSID_API_MAJOR_VERSION>=major && \
                                                             (TSID_API_MINOR_VERSION>minor || (TSID_API_MINOR_VERSION>=minor && \
                                                                                                     TSID_API_PATCH_VERSION>=patch))))

#define TSID_API_VERSION_AT_MOST(major, minor, patch) (TSID_API_MAJOR_VERSION<major || (TSID_API_MAJOR_VERSION<=major && \
                                                            (TSID_API_MINOR_VERSION<minor || (TSID_API_MINOR_VERSION<=minor && \
                                                                                                     TSID_API_PATCH_VERSION<=patch))))

// Handle portable symbol export.
// Defining manually which symbol should be exported is required
// under Windows whether MinGW or MSVC is used.
//
// The headers then have to be able to work in two different modes:
// - dllexport when one is building the library,
// - dllimport for clients using the library.
//
// On Linux, set the visibility accordingly. If C++ symbol visibility
// is handled by the compiler, see: http://gcc.gnu.org/wiki/Visibility
# if defined _WIN32 || defined __CYGWIN__
// On Microsoft Windows, use dllimport and dllexport to tag symbols.
#  define TSID_API_DLLIMPORT __declspec(dllimport)
#  define TSID_API_DLLEXPORT __declspec(dllexport)
#  define TSID_API_DLLLOCAL
# else
// On Linux, for GCC >= 4, tag symbols using GCC extension.
#  if __GNUC__ >= 4
#   define TSID_API_DLLIMPORT __attribute__ ((visibility("default")))
#   define TSID_API_DLLEXPORT __attribute__ ((visibility("default")))
#   define TSID_API_DLLLOCAL  __attribute__ ((visibility("hidden")))
#  else
// Otherwise (GCC < 4 or another compiler is used), export everything.
#   define TSID_API_DLLIMPORT
#   define TSID_API_DLLEXPORT
#   define TSID_API_DLLLOCAL
#  endif // __GNUC__ >= 4
# endif // defined _WIN32 || defined __CYGWIN__

# ifdef TSID_API_STATIC
// If one is using the library statically, get rid of
// extra information.
#  define TSID_API_DLLAPI
#  define TSID_API_LOCAL
# else
// Depending on whether one is building or using the
// library define DLLAPI to import or export.
#  ifdef tsid_api_EXPORTS
#   define TSID_API_DLLAPI TSID_API_DLLEXPORT
#  else
#   define TSID_API_DLLAPI TSID_API_DLLIMPORT
#  endif // TSID_API_EXPORTS
#  define TSID_API_LOCAL TSID_API_DLLLOCAL
# endif // TSID_API_STATIC
#endif //! TSID_API_CONFIG_HH
