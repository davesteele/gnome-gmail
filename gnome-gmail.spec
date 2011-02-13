Name: gnome-gmail
Version: 1.7.1
Release: 1
Group: Applications/Communications
Vendor: David Steele
URL: http://sourceforge.net/projects/%{name}
License: GPLv2
Summary: Make Gmail an option for the default Gnome mail handler
Source: %{name}-%{version}.tar.gz
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: control-center
Requires: python >= 2.6
Requires: pygobject2
Requires: gconf-editor
Requires: gnome-python2-gnomekeyring

%description
This package makes Gmail a choice in the Gnome control panel for the default
mail handler. It opens in the default web browser.

%prep
%setup -q

%build
./configure --with-gconf-schema-file-dir=/etc/gconf/schemas
make

%install
rm -Rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -Rf %{buildroot}

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
%{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi




%files
%doc README COPYING
%attr( 0644, root, root) /etc/gconf/schemas/gnome-gmail.schemas
%attr( 0755, root, root) /usr/bin/gnome-gmail
%attr( 0755, root, root) /usr/bin/setOOmailer
%attr( 0644, root, root) /usr/share/gnome-control-center/default-apps/gnome-gmail.xml
%attr( 0644, root, root) /usr/share/gnome-gmail/gnomegmail.glade
%attr( 0755, root, root) /usr/share/gnome-gmail/evolution
%attr( 0755, root, root) /usr/share/icons/hicolor/16x16/apps/gnome-gmail.png
%attr( 0755, root, root) /usr/share/icons/hicolor/24x24/apps/gnome-gmail.png
%attr( 0755, root, root) /usr/share/icons/hicolor/32x32/apps/gnome-gmail.png
%attr( 0755, root, root) /usr/share/icons/hicolor/48x48/apps/gnome-gmail.png
%attr( 0644, root, root) /usr/share/applications/gnome-gmail.desktop
%attr( 0644, root, root) /usr/share/gnome/autostart/setOOmailer.desktop
%attr( 0644, root, root) /usr/share/man/man1/gnome-gmail.1.gz
%attr( 0644, root, root) /usr/share/man/man1/setOOmailer.1.gz
%attr( 0644, root, root) /usr/share/locale/da/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/de/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/es/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/fi/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/fr/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/it/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ja/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/pl/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/pt/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ro/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ru/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/sv/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ta/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ta_LK/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/tr/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/vi/LC_MESSAGES/gnome-gmail.mo


%changelog
* Sat Feb 12 2011 David Steele <daves@users.sourceforge.net> - 1.7.1-1
- Translations - de, es, fr, it, ja, pl, ro, ru, ta, tr, vi
- Manage the preferred mail setting from within the application (for Fedora 15)
- Now configures LibreOffice (and newer OpenOffice) for GNOME emailer use
- Attached files are identified by name instead of path

* Mon Oct 18 2010 David Steele <daves@users.sourceforge.net> - 1.7-1
- Internationalization support
- Automake support

* Fri Sep 17 2010 David Steele <daves@users.sourceforge.net> - 1.6-1
- Support for Open Office Send -> Document as Email
- Small bug fixes
- pylint cleanup
- Ubuntu packaging

* Tue Apr 05 2010 David Steele <daves@users.sourceforge.net> - 1.5.1-1
- Add python version restriction to package

* Sun Mar 06 2010 David Steele <daves@users.sourceforge.net> - 1.5-1
- Google Apps support
- GMail icon added for the task bar

* Sun Jan 17 2010 Dave Steele <daves@users.sourceforge.net> - 1.4-1
- Support for Nautilus - Send files via GMail
- Added mailto test cases - improved mailto handling

* Wed Nov 04 2009 Dave Steele <daves@users.sourceforge.net> - 1.3-1
- Web page updated with resources for mailto: test and Send Link bookmarklet
- Fixes to broken 1.2 RPM install
- Better mailto: argument handling
- Fixed to launch web browser instead of "HTML handler"

* Wed Sep 09 2009 Dave Steele <daves@users.sourceforge.net> - 1.2-1
- Better gmail URL

* Mon Sep 07 2009 Dave Steele <daves@users.sourceforge.net> - 1.1-1
- initial package release

