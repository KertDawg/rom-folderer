
AC_INIT([rom-folderer], [0.1], [kertishenderson@gmail.com])
AC_CONFIG_AUX_DIR([build])
AC_CONFIG_FILES([Makefile])
AC_CHECK_PROG(PYINSTALLER_CHECK,pyinstaller,yes)
AS_IF([test x"$PYINSTALLER_CHECK" != x"yes"], [AC_MSG_ERROR([pyinstaller is not in the current path.])])
AC_CHECK_TOOL(PYINSTALLER,pyinstaller)
AM_INIT_AUTOMAKE([foreign])

AC_OUTPUT

