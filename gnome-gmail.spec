Name: gnome-gmail
Version: 1.8.2
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
Requires: pygtk2-libglade

%description
This package makes Gmail a choice in the Gnome control panel for the default
mail handler. It opens in the default web browser.

Logout to complete the configuration.

%prep
%setup -q

%build
./configure --with-gconf-schema-file-dir=/etc/gconf/schemas
make

%install
rm -Rf %{buildroot}
make DESTDIR=%{buildroot} install
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    --add-category Network \
    --remove-category System \
    --remove-category ContactManagement \
    %{name}.desktop


%clean
rm -Rf %{buildroot}

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
%{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi


%postun
update-desktop-database &> /dev/null || :
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
%attr( 0755, root, root) /usr/share/icons/hicolor/256x256/apps/gnome-gmail.png
%attr( 0644, root, root) /usr/share/applications/gnome-gmail.desktop
%attr( 0644, root, root) /usr/share/gnome/autostart/setOOmailer.desktop
%attr( 0644, root, root) /usr/share/man/man1/gnome-gmail.1.gz
%attr( 0644, root, root) /usr/share/man/man1/setOOmailer.1.gz
%attr( 0644, root, root) /usr/share/locale/cs/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/da/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/de/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/el_GR/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/es/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/et/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/fa/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/fi/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/fr/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/hr/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/hu/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/hy/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/it/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ja/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ms/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/pl/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ps/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/pt/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ro/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ru/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/sv/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ta/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/ta_LK/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/tr/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/uk/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/vi/LC_MESSAGES/gnome-gmail.mo
%attr( 0644, root, root) /usr/share/locale/zh_CN/LC_MESSAGES/gnome-gmail.mo


%changelog

* Mon Oct 24 2011 David Steele <daves@users.sourceforge.net> - 1.8.2-1
- Added Dependencies needed by GNOME 3 (python-glade2 and python-gconf)
- Set as Default mailer on installation, using setOOmailer
- Fix postinstall crash on upgrade (LP: #878494)
- Lintian fixes
- Fix setOOmailer XML write failure
- Updates to 6 languages
- Determine Drafts folder, for attachments, using Google IMAP Extentions
- Remove dependency on libgnome2


* Mon Aug 29 2011 David Steele <daves@users.sourceforge.net> - 1.8.1-1
- Fix setting gnome-gmail as default mailer, using dconf

* Thu Aug 25 2011 David Steele <daves@users.sourceforge.net> - 1.8-1
- GNOME 3 compatibility (LP: #729357)
- Messages with attachments open directly, instead of the Drafts folder
- Fixed "Send Document as Email" in LibreOffice (LP: #774055)
- Added python-glade2 dependency for Oneiric (LP: #833355)
- Translation improvementsa(LP: #783005)
- Unity message indicator (LP: #773765)

* Tue Mar 29 2011 Michael R. Crusoe <michael.crusoe@gmail.com> - 1.7.3-1
- Switch to native package as debian/ is maintained upstream
- Add libgconf2-dev, autotools-dev, and dh-autoreconf to Build-Depends
- Migrate to simplified dh based debian/rules (these last two changes fixes a FTBFS)
- Include the non-Debian changelog in the package

* Mon Feb 21 2011 David Steele <daves@users.sourceforge.net> - 1.7.2-1
- Fix autotools bug in 1.7.1 (autoconf withoug debian libgconf2-dev installed)

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

