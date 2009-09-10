prefix = 
package = gnome-gmail
version = 1.2
release = 1

arch = noarch

shortname = ${package}-${version}
fullyqualifiedname = ${shortname}-${release}

scriptfiles = gnome-gmail

tarfiles = Makefile ${package}.spec $(scriptfiles)\
	README COPYING gnome-gmail.xml

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
	${CP} ${tarfiles} ${shortname}
	${TAR} -czf ${shortname}.tgz ${shortname}

clean:
	${RM} *.tgz
	${RM} *.rpm
	${RM} -r ${shortname}
	${RM} *.1.gz
	${RM} -r doc
	${RM} debian/changelog
	-rm -rf debian
	${RM} *.deb

rpm: ${fullyqualifiedname}.${arch}.rpm ${fullyqualifiedname}.src.rpm

${fullyqualifiedname}.${arch}.rpm ${fullyqualifiedname}.src.rpm: ${shortname}.tgz 
	${RPMBUILD} ${shortname}.tgz
	${MV} ${arch}/${fullyqualifiedname}.${arch}.rpm .
	${RMDIR} ${arch}

debian/changelog: debian/changelog.in Makefile

deb:
	-rm -rf debian
	mkdir debian
	mkdir debian/DEBIAN
	cp control debian/DEBIAN
	install -d debian/usr/bin
	install gnome-gmail debian/usr/bin
	install -d debian/usr/share/gnome-control-center/default-apps
	install gnome-gmail.xml debian/usr/share/gnome-control-center/default-apps
	dpkg-deb --build debian
	mv debian.deb gnome-gmail_1.2-1_all.deb

