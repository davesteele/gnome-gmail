prefix = 
package = gnome-gmail
version = 1.6
release = 1

arch = noarch

DISTRO := $(lsb_release -i | cut -d: -f2 | sed s/'^\t'//)

shortname = ${package}-${version}
fullyqualifiedname = ${shortname}-${release}

scriptfiles = gnome-gmail

iconsizes = 16x16 24x24 32x32 48x48
iconbasedir = ${prefix}/usr/share/icons/hicolor
iconclass = apps

tarfiles = Makefile ${package}.spec $(scriptfiles)\
	README COPYING gnome-gmail.xml gnomegmail.glade test \
	gnome-gmail.schemas gnome-gmail.desktop 50_gnome-gmail \
	${foreach i, ${iconsizes}, icons/gmail-${i}.png } \
	setOOmailer setOOmailer.desktop evolution \
	debian/changelog \
	debian/compat \
	debian/control \
	debian/copyright \
	debian/docs \
	debian/postinst \
	debian/rules \
	debian/watch

bindir = ${prefix}/usr/bin
xmldir = ${prefix}/usr/share/gnome-control-center/default-apps
libdir = ${prefix}/usr/lib/gnome-gmail
ifeq (${DISTRO},Ubuntu)
   schemadir = ${prefix}/usr/share/gconf/schemas
else
   schemadir = ${prefix}/etc/gconf/schemas
endif
gconfdefdir = ${prefix}/usr/share/gconf/defaults
desktopdir = ${prefix}/usr/share/applications
autostartdir = ${prefix}/usr/share/gnome/autostart

signopt := $(shell rpmbuild --showrc | grep -v "{" | grep "gpg_name" )
signopt := $(if $(signopt), --sign, )

RM := /bin/rm -f 
MKDIR := /bin/mkdir
CP := /bin/cp -r
TAR := /bin/tar --exclude ".*"
SED := /bin/sed
RPMBUILD := /usr/bin/rpmbuild -ta --clean ${signopt} --target ${arch} --define "_srcrpmdir ${PWD}" --define "_rpmdir ${PWD}" 
ECHO := /bin/echo
GZIP := /bin/gzip -c
GROFF := /usr/bin/groff
PS2PDF := /usr/bin/ps2pdf
RMDIR := /bin/rmdir
MV := /bin/mv

PKGRPMFLAGS=--define "_topdir ${PWD}" --define "_specdir ${PWD}" --define "_sourcedir ${PWD}/dist" --define "_srcrpmdir ${PWD}" --define "_rpmdir ${PWD}"

all: 
	@${ECHO} "valid targets - tar rpm clean"

tar: ${shortname}.tgz

${shortname}.tgz: ${tarfiles} 
	-${RM} -r ${shortname}
	${MKDIR} ${shortname}
	${CP} --parents ${tarfiles} ${shortname}
	${TAR} -czf ${shortname}.tgz ${shortname}

clean:
	${RM} *.tgz
	${RM} *.rpm
	${RM} -r ${shortname}
	${RM} *.1.gz
	${RM} -r doc
	${RM} *.deb *.orig.tar.gz *.diff.gz *.dsc *.changes *.build


rpm: ${fullyqualifiedname}.${arch}.rpm ${fullyqualifiedname}.src.rpm

${fullyqualifiedname}.${arch}.rpm ${fullyqualifiedname}.src.rpm: ${shortname}.tgz 
	${RPMBUILD} ${shortname}.tgz
	${MV} ${arch}/${fullyqualifiedname}.${arch}.rpm .
	${RMDIR} ${arch}

installdirs = ${bindir} ${xmldir} ${libdir} ${iconbasedir} ${schemadir} \
	${gconfdefdir} ${desktopdir} ${autostartdir} \
	${foreach i, ${iconsizes}, ${iconbasedir}/${i}/${iconclass}}

install:
	install -d ${installdirs}
	install gnome-gmail ${bindir}
	install setOOmailer ${bindir}
	install gnome-gmail.xml ${xmldir}
	install gnomegmail.glade ${libdir}
	install gnome-gmail.schemas ${schemadir}
	install gnome-gmail.desktop ${desktopdir}
	install evolution ${libdir}
	install setOOmailer.desktop ${autostartdir}
	#install 50_gnome-gmail ${gconfdefdir}
	${foreach i, ${iconsizes}, install -m 0644 icons/gmail-${i}.png ${iconbasedir}/${i}/${iconclass}/gmail.png; }
	if [ -f ${iconbasedir}/icon-theme.cache ]; \
		then \
			gtk-update-icon-cache -f ${iconbasedir}; \
	fi

