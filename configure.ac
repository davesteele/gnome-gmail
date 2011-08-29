#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.65])
AC_INIT([gnome-gmail], [1.8.1], [https://sourceforge.net/tracker/?group_id=277145&atid=1176979])
AM_INIT_AUTOMAKE
AC_COPYRIGHT([Copyright 2010 David Steele <daves@users.sourceforge.net>])

GNOME_COMMON_INIT

AC_PROG_INTLTOOL([0.23])
GETTEXT_PACKAGE=gnome-gmail
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE")

ALL_LINGUAS="es"
AM_GLIB_GNU_GETTEXT

gnomegmaillocaledir='${prefix}/$(DATADIRNAME}/locale'
AC_SUBST(gnomegmaillocaledir)

AM_GCONF_SOURCE_2
AC_PATH_PROG(GCONFTOOL,gconftool-2)

AC_PREFIX_DEFAULT([/usr])

# Checks for programs.
AC_PROG_INSTALL
AC_PROG_MAKE_SET

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES([Makefile po/Makefile.in])
AC_OUTPUT
