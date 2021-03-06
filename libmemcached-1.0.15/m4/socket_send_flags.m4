dnl Copyright (C) 2012 Data Differential LLC
dnl Copyright (C) 2011 Trond Norbye
dnl This file is free software; Trond Norbye
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.
dnl ---------------------------------------------------------------------------
dnl Macro: SOCKET_SEND_FLAGS
dnl ---------------------------------------------------------------------------

AC_DEFUN([SOCKET_SEND_FLAGS],[
  AC_CACHE_CHECK([for MSG_NOSIGNAL], [ac_cv_msg_nosignal], [
    AC_LANG_PUSH([C])
    AX_SAVE_FLAGS
    CFLAGS="$CFLAGS -I${srcdir}"

    AC_COMPILE_IFELSE([AC_LANG_PROGRAM([#include <netdb.h>], [ int flags= MSG_NOSIGNAL ])], [ac_cv_msg_nosignal="yes"])
    AC_LANG_POP
    AX_RESTORE_FLAGS
  ])

  AC_CACHE_CHECK([for MSG_DONTWAIT], [ac_cv_msg_dontwait], [
    AC_LANG_PUSH([C])
    AX_SAVE_FLAGS
    CFLAGS="$CFLAGS -I${srcdir}"

    AC_COMPILE_IFELSE([AC_LANG_PROGRAM([#include <netdb.h>], [ int flags= MSG_DONTWAIT ])], [ac_cv_msg_dontwait="yes"])
    AC_LANG_POP
    AX_RESTORE_FLAGS
  ])

  AC_CACHE_CHECK([for MSG_MORE], [ac_cv_msg_more], [
    AC_LANG_PUSH([C])
    AX_SAVE_FLAGS
    CFLAGS="$CFLAGS -I${srcdir}"

    AC_COMPILE_IFELSE([AC_LANG_PROGRAM([#include <netdb.h>], [ int flags= MSG_MORE ])], [ac_cv_msg_more="yes"])
    AC_LANG_POP
    AX_RESTORE_FLAGS
  ])

  AS_IF([test "x$ac_cv_msg_nosignal" = "xyes"],[ AC_DEFINE(HAVE_MSG_NOSIGNAL, 1, [Define to 1 if you have a MSG_NOSIGNAL])])
  AS_IF([test "x$ac_cv_msg_dontwait" = "xyes"],[ AC_DEFINE(HAVE_MSG_DONTWAIT, 1, [Define to 1 if you have a MSG_DONTWAIT])])
  AS_IF([test "x$ac_cv_msg_more" = "xyes"],[ AC_DEFINE(HAVE_MSG_MORE, 1, [Define to 1 if you have a MSG_MORE])])
])

dnl ---------------------------------------------------------------------------
dnl End Macro: SOCKET_SEND_FLAGS
dnl ---------------------------------------------------------------------------
