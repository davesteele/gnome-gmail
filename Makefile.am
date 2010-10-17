dist_bin_SCRIPTS = gnome-gmail setOOmailer

dist_man1_MANS = gnome-gmail.1 setOOmailer.1

pkgsharedir = $(datarootdir)/gnome-gmail
dist_pkgshare_DATA = gnomegmail.glade
dist_pkgshare_SCRIPTS = evolution

schemadir = @GCONF_SCHEMA_FILE_DIR@
dist_schema_DATA = gnome-gmail.schemas

defaultappdir = $(datarootdir)/gnome-control-center/default-apps
dist_defaultapp_DATA = gnome-gmail.xml

autostartdir = $(datarootdir)/gnome/autostart
dist_autostart_DATA = setOOmailer.desktop

desktopdir = $(datarootdir)/applications
dist_desktop_DATA = gnome-gmail.desktop

iconbasedir = $(datarootdir)/icons/hicolor
icon16x16dir = $(iconbasedir)/16x16/apps
icon24x24dir = $(iconbasedir)/24x24/apps
icon32x32dir = $(iconbasedir)/32x32/apps
icon48x48dir = $(iconbasedir)/48x48/apps

dist_icon16x16_DATA = icons/16x16/gnome-gmail.png
dist_icon24x24_DATA = icons/24x24/gnome-gmail.png
dist_icon32x32_DATA = icons/32x32/gnome-gmail.png
dist_icon48x48_DATA = icons/48x48/gnome-gmail.png

CLEANFILES = $(PACKAGE)_$(VERSION).orig.tar.gz \
   $(PACKAGE)_$(VERSION)_$(RELEASE)_all.deb \
   $(PACKAGE)_$(VERSION)_$(RELEASE).debian.tar.gz \
   $(PACKAGE)_$(VERSION)_$(RELEASE).dsc

DISTCLEANFILES = config.status config.log

clean-local: clean-local-deb
PHONY: clean-local-deb
clean-local-deb:
	-rm -f $(PACKAGE)_$(VERSION)-*_*.changes $(PACKAGE)_$(VERSION)-*_*.build
	-rm -f $(PACKAGE)_$(VERSION)-*_all.deb $(PACKAGE)_$(VERSION)-*.debian.tar.gz
	-rm -f $(PACKAGE)_$(VERSION)-*.dsc

distclean-local:
	-rm -rf $(PACKAGE)_$(VERSION) $(PACKAGE)-$(VERSION).tar.gz

deb: dist
	cp $(DIST_ARCHIVES) $(PACKAGE)_$(VERSION).orig.tar.gz
	tar -xzf $(PACKAGE)_$(VERSION).orig.tar.gz
	cp -r debian $(distdir)
	cd $(distdir) && ./configure
	cd $(distdir) && debuild

SUBDIRS = po

ACLOCAL_AMFLAGS = -I m4

EXTRA_DIST = config.rpath m4/ChangeLog
