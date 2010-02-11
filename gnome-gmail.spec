Name: gnome-gmail
Version: 1.5
Release: 1
Group: Applications/Communications
Vendor: David Steele
URL: http://sourceforge.net/projects/%{name}
License: GPLv2
Summary: Make Gmail an option for the default Gnome mail handler
Source: %{name}-%{version}.tgz
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: control-center
Requires: python
Requires: pygobject2

%description
This package makes Gmail a choice in the Gnome control panel for the default
mail handler. It opens in the default web browser.

%prep
%setup -q

%build

%install
rm -Rf %{buildroot}
make prefix=%{buildroot} install
#install -D gnome-gmail %{buildroot}/usr/bin/gnome-gmail
#install -D gnome-gmail.xml %{buildroot}/usr/share/gnome-control-center/default-apps/gnome-gmail.xml
#install -D gnomegmail.glade %{buildroot}/usr/lib/gnome-gmail/gnomegmail.glade

%clean
rm -Rf %{buildroot}

%post


%files
%doc README COPYING
%attr( 0755, root, root) /usr/bin/gnome-gmail
%attr( 0644, root, root) /usr/share/gnome-control-center/default-apps/gnome-gmail.xml
%attr( 0644, root, root) /usr/lib/gnome-gmail/gnomegmail.glade
%attr( 0755, root, root) /usr/share/icons/hicolor/16x16/apps/gmail.png
%attr( 0755, root, root) /usr/share/icons/hicolor/24x24/apps/gmail.png
%attr( 0755, root, root) /usr/share/icons/hicolor/32x32/apps/gmail.png
%attr( 0755, root, root) /usr/share/icons/hicolor/48x48/apps/gmail.png

%changelog
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

