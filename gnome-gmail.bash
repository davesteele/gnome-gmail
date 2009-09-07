#!/bin/sh

# gnome-gmail - a script that passes gnome mailto links to gmail in your browser
# Copyright (c) 2006 Matthew C Ruschmann <http://matthew.ruschmann.net>
# Version: 1.0

# Adapted from ymail - by David L Norris <dave@webaugur.com>
# http://webaugur.com/wares/files/ymail

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Ask GNOME for the web browser command.
BROWSER=`gconftool-2 --get '/desktop/gnome/url-handlers/http/command' | cut -f1 -d' ' `

# If no arguments just start gmail
if test -z "${*}"
  then
    ${BROWSER} "http://www.gmail.com"
    exit
fi

# Grab all command line parameters and strip mailto: if it exists.
TOMAIL=`echo "${*}" | sed -e 's/mailto://g'`
TOMAIL=`echo "$TOMAIL" | sed -e 's/?/\&/g'`
TOMAIL=`echo "$TOMAIL" | sed -e 's/&subject=/\&su=/g'`

# This is the URL Yahoo! Companion and Yahoo! Toolbar uses to send email:
TOURL="https://gmail.google.com/gmail?view=cm&cmid=0&fs=1&tearoff=1&to="

# Print out what we are about to do
echo ${BROWSER} "${TOURL}${TOMAIL}"

# Execute mail command
${BROWSER} "${TOURL}${TOMAIL}"

