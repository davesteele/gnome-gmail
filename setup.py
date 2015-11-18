#!/usr/bin/python2

import DistUtilsExtra.auto
import DistUtilsExtra.command
import distutils.command
import os
import shutil

import sys
if not sys.version_info[0] == 2:
    print "Sorry, Python 3 is not supported (yet)"
    sys.exit(1)

class my_build_i18n(DistUtilsExtra.command.build_i18n.build_i18n):
    def run(self):
        DistUtilsExtra.command.build_i18n.build_i18n.run(self)

        cmd = "LC_ALL=C /usr/bin/intltool-merge -u -c ./po/.intltool-merge-cache ./po "
        for infile in (x[:-3] for x in os.listdir('.') if x[-3:] == '.in'):
            print("Processing %s.in to %s" % (infile, infile))

            if 'desktop' in infile:
                flag = '-d'
            elif 'schema' in infile:
                flag = '-s'
            elif 'xml' in infile:
                flag = '-x'
            else:
                flag = ''

            if flag:
                os.system("%s %s %s.in %s" % (cmd, flag, infile, infile))

class my_clean(distutils.command.clean.clean):
    def run(self):
        distutils.command.clean.clean.run(self)

        filelist = [x[:-3] for x in os.listdir('.') if x[-3:] == '.in']
        filelist += ['po/.intltool-merge-cache']
        filelist += ['po/gnome-gmail.pot']
        filelist += ['gnomegmail.glade~']
        for infile in filelist:
            if os.path.exists(infile):
                os.unlink(infile)

        for dir in ['build/mo', 'build/scripts-2.7']:
            if os.path.exists(dir):
                shutil.rmtree(dir)


DistUtilsExtra.auto.setup(
      name='gnome-gmail',
      version='1.9.3',
      description='support for Gmail as the preferred email application in GNOME',
      author='David Steele',
      author_email='dsteele@gmail.com',
      url='https://davesteele.github.io/gnome-gmail/',
      scripts = ['gnome-gmail'],
      requires=['gi'],
      data_files=[
          ('/usr/share/icons/hicolor/16x16/apps', ['icons/16x16/gnome-gmail.png']),
          ('/usr/share/icons/hicolor/24x24/apps', ['icons/24x24/gnome-gmail.png']),
          ('/usr/share/icons/hicolor/32x32/apps', ['icons/32x32/gnome-gmail.png']),
          ('/usr/share/icons/hicolor/48x48/apps', ['icons/48x48/gnome-gmail.png']),
          ('/usr/share/icons/hicolor/256x256/apps', ['icons/256x256/gnome-gmail.png']),
          ('/usr/share/applications', ['gnome-gmail.desktop']),
          ('/usr/share/gnome/autostart', ['gnome-gmail-startup.desktop']),
          ('share/gnome-gmail', ['gnomegmail.glade', 'gnomegmail.py']),
                 ],
      classifiers=[
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2',
          'Topic :: Communications :: Email',
          'Topic :: Desktop Environment :: Gnome',
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Intended Audience :: End Users/Desktop',
                  ],
      cmdclass={
          'build_i18n': my_build_i18n,
          'clean': my_clean,
               },
     )

