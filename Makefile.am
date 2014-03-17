dist_bin_SCRIPTS = gnome-gmail setOOmailer

pkgsharedir = $(datarootdir)/gnome-gmail
dist_pkgshare_DATA = gnomegmail.glade
dist_pkgshare_SCRIPTS = evolution

schemadir = @GCONF_SCHEMA_FILE_DIR@
schema_in_files = gnome-gmail.schemas.in
schema_DATA = $(schema_in_files:.schemas.in=.schemas)
@INTLTOOL_SCHEMAS_RULE@

defaultappdir = $(datarootdir)/gnome-control-center/default-apps
defaultapp_in_files = gnome-gmail.xml.in
defaultapp_DATA = $(defaultapp_in_files:.xml.in=.xml)
@INTLTOOL_XML_RULE@

autostartdir = $(datarootdir)/gnome/autostart
autostart_in_files = setOOmailer.desktop.in
autostart_DATA = $(autostart_in_files:.desktop.in=.desktop)

desktopdir = $(datarootdir)/applications
desktop_in_files = gnome-gmail.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

iconbasedir = $(datarootdir)/icons/hicolor
icon16x16dir = $(iconbasedir)/16x16/apps
icon24x24dir = $(iconbasedir)/24x24/apps
icon32x32dir = $(iconbasedir)/32x32/apps
icon48x48dir = $(iconbasedir)/48x48/apps
icon256x256dir = $(iconbasedir)/256x256/apps

dist_icon16x16_DATA = icons/16x16/gnome-gmail.png
dist_icon24x24_DATA = icons/24x24/gnome-gmail.png
dist_icon32x32_DATA = icons/32x32/gnome-gmail.png
dist_icon48x48_DATA = icons/48x48/gnome-gmail.png
dist_icon256x256_DATA = icons/256x256/gnome-gmail.png

CLEANFILES = $(PACKAGE)_$(VERSION).orig.tar.gz \
   $(PACKAGE)_$(VERSION)_$(RELEASE)_all.deb \
   $(PACKAGE)_$(VERSION)_$(RELEASE).debian.tar.gz \
   $(PACKAGE)_$(VERSION)_$(RELEASE).dsc \
   setOOmailer.desktop \
   gnome-gmail.desktop \
   gnome-gmail.schemas \
   gnome-gmail.xml

DISTCLEANFILES = config.status config.log

clean-local: clean-local-deb
PHONY: clean-local-deb
clean-local-deb:
	-rm -f $(PACKAGE)_$(VERSION)-*_*.changes $(PACKAGE)_$(VERSION)-*_*.build
	-rm -f $(PACKAGE)_$(VERSION)-*_all.deb $(PACKAGE)_$(VERSION)-*.debian.tar.gz
	-rm -f $(PACKAGE)_$(VERSION)-*.dsc

distclean-local:
	-rm -rf $(PACKAGE)_$(VERSION) $(PACKAGE)-$(VERSION).tar.gz

PHONY: deb
deb: dist
	cp $(DIST_ARCHIVES) $(PACKAGE)_$(VERSION).orig.tar.gz
	tar -xzf $(PACKAGE)_$(VERSION).orig.tar.gz
	cp -r debian $(distdir)
	cd $(distdir) && ./configure
	cd $(distdir) && debuild

PHONY: sourceforge-release-deb
sourceforge-release-deb:
	rsync -e ssh $(PACKAGE)_$(VERSION)-*_all.deb $(PACKAGE)-$(VERSION).tar.gz daves,gnome-gmail@frs.sourceforge.net:/home/frs/project/g/gn/gnome-gmail/Version_$(VERSION)/

PHONY: rpm
rpm: dist
	rpmbuild -ba --clean --target noarch --define "_srcrpmdir ${PWD}" --define "_rpmdir ${PWD}" --define "_sourcedir ${PWD}" gnome-gmail.spec
	mv noarch/$(PACKAGE)-$(VERSION)-*.noarch.rpm .
	rm -rf noarch

PHONY: sourceforge-release-rpm
sourceforge-release-rpm:
	rsync -e ssh $(PACKAGE)-$(VERSION)-*.noarch.rpm $(PACKAGE)-$(VERSION)-*.src.rpm $(PACKAGE).spec daves,gnome-gmail@frs.sourceforge.net:/home/frs/project/g/gn/gnome-gmail/Version_$(VERSION)/


SUBDIRS = po

ACLOCAL_AMFLAGS = -I m4

EXTRA_DIST = config.rpath m4/ChangeLog gnome-gmail.desktop.in \
    setOOmailer.desktop.in gnome-gmail.schemas.in gnome-gmail.xml.in
