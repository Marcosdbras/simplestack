#!/bin/sh
### BEGIN INIT INFO
# Provides:          /usr/sbin/simplestack
# Required-Start:    $remote_fs $network $syslog
# Required-Stop:
# X-Stop-After:      sendsigs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: simplestack hypervisor control layer
# Description:       simplestack hypervisor control layer
### END INIT INFO

# Based on default init from Francisco Freire <francisco.freire@locaweb.com.br>

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="python simplestack service"
NAME=simplestack

SIMPLESTACK=simplestack
SIMPLESTACK_BIN=/usr/sbin/simplestack
SIMPLESTACK_OPTIONS=""
SIMPLESTACK_PIDFILE=/var/run/simplestack/simplestack.pid

SCRIPTNAME=/etc/init.d/$NAME

# Exit if the package is not installed
[ -x "$SIMPLESTACK_BIN" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Define LSB log_* functions.
. /lib/lsb/init-functions

create_xconsole() {
    XCONSOLE=/dev/xconsole
    if [ "$(uname -s)" = "GNU/kFreeBSD" ]; then
        XCONSOLE=/var/run/xconsole
        ln -sf $XCONSOLE /dev/xconsole
    fi
    if [ ! -e $XCONSOLE ]; then
        mknod -m 640 $XCONSOLE p
        chown root:adm $XCONSOLE
        [ -x /sbin/restorecon ] && /sbin/restorecon $XCONSOLE
    fi
}

case "$1" in
    start)
        log_daemon_msg "Starting $DESC" "$SIMPLESTACK"
        create_xconsole
        $SIMPLESTACK_BIN -a start
        case "$?" in
            0) sendsigs_omit
               log_end_msg 0 ;;
            1) log_progress_msg "already started"
               log_end_msg 0 ;;
            *) log_end_msg 1 ;;
        esac
    ;;
    stop)
        log_daemon_msg "Stopping $DESC" "$SIMPLESTACK"
        $SIMPLESTACK_BIN -a stop
        case "$?" in
            0) log_end_msg 0 ;;
            1) log_progress_msg "already stopped"
               log_end_msg 0 ;;
            *) log_end_msg 1 ;;
        esac
    ;;
    restart)
        $0 stop
        $0 start
    ;;
    status)
         $SIMPLESTACK_BIN -a status
    ;;
    *)
        echo "Usage: $SCRIPTNAME {start|stop|restart|status}"
        exit 1
    ;;
esac

:
