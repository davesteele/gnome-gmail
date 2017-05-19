#!/usr/bin/python

from distutils.core import setup, Command
from distutils.command.build import build
from distutils.command.clean import clean

import os
import sys
import shutil
import subprocess

podir = "./po"
pext = ".po"

langs = sorted([x[:-3] for x in os.listdir(podir) if x[-3:] == pext])


def modir(lang):
    return os.path.join("build/mo", lang)


def mkmo(lang):
    outpath = modir(lang)
    if os.path.exists(outpath):
        shutil.rmtree(outpath)
    os.makedirs(outpath)

    inpath = os.path.join(podir, lang + pext)
    cmd = "msgfmt %s -o %s/gnome-gmail.mo" % (inpath, outpath)

    subprocess.call(cmd, shell=True) and sys.exit(1)


def merge_i18n():

    cmd = "LC_ALL=C intltool-merge -u " +\
          "-c %s/.intltool-merge-cache " % podir +\
          podir
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
            args = " %s %s.in %s" % (flag, infile, infile)
            subprocess.call(cmd + args, shell=True) and sys.exit(1)


class my_build(build):
    def run(self, *args):
        build.run(self, *args)

        for lang in langs:
            mkmo(lang)

        merge_i18n()


def polist():
    dst_tmpl = "share/locale/%s/LC_MESSAGES/"
    polist = [(dst_tmpl % x, ["%s/gnome-gmail.mo" % modir(x)]) for x in langs]

    return polist


class my_build_i18n(Command):
    description = "Create/update po/pot translation files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating POT file")
        cmd = "cd po; intltool-update --pot --gettext-package=gnome-gmail"
        subprocess.call(cmd, shell=True)

        for lang in langs:
            print("Updating %s PO file" % lang)
            cmd = "cd po; intltool-update --dist \
                   --gettext-package=gnome-gmail %s >/dev/null 2>&1" % lang
            subprocess.call(cmd, shell=True)


class my_clean(clean):
    def run(self):
        clean.run(self)

        filelist = [x[:-3] for x in os.listdir('.') if x[-3:] == '.in']
        filelist += ['po/.intltool-merge-cache']
        filelist += ['gnomegmail.glade~', 'conftest.pyc']
        for infile in filelist:
            if os.path.exists(infile):
                os.unlink(infile)

        for dir in ['build/mo', 'build/scripts-2.7', 'build/scripts-3.4',
                    'build/scripts-3.5', '__pycache__', 'test/__pycache__']:
            if os.path.exists(dir):
                shutil.rmtree(dir)


class my_test(Command):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        self.pytest_args = []

    def finalize_options(self):
        pass

    def run(self):
        import pytest
        args = self.pytest_args
        if type(args) == str:
            args = args.split()
        errno = pytest.main(args)
        sys.exit(errno)

setup(
    name='gnome-gmail',
    version='2.4',
    description='support for Gmail as the preferred GNOME email application',
    author='David Steele',
    author_email='dsteele@gmail.com',
    url='https://davesteele.github.io/gnome-gmail/',
    scripts=['gnome-gmail'],
    requires=['gi', 'six'],
    data_files=[
        ('share/icons/hicolor/16x16/apps', ['icons/16x16/gnome-gmail.png']),
        ('share/icons/hicolor/24x24/apps', ['icons/24x24/gnome-gmail.png']),
        ('share/icons/hicolor/32x32/apps', ['icons/32x32/gnome-gmail.png']),
        ('share/icons/hicolor/48x48/apps', ['icons/48x48/gnome-gmail.png']),
        ('share/icons/hicolor/256x256/apps',
            ['icons/256x256/gnome-gmail.png']),
        ('share/applications', ['gnome-gmail.desktop']),
        ('share/gnome/autostart', ['gnome-gmail-startup.desktop']),
        ('share/gnome-gmail', ['gnomegmail.glade', 'gnomegmail.py']),
        ('share/appdata', ['gnome-gmail.appdata.xml']),
               ] + polist(),
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Email',
        'Topic :: Desktop Environment :: Gnome',
        'License :: OSI Approved :: " \
            "GNU General Public License v2 or later (GPLv2+)',
        'Intended Audience :: End Users/Desktop',
                ],
    cmdclass={
        'build_i18n': my_build_i18n,
        'clean': my_clean,
        'build': my_build,
        'test': my_test,
             },
     )
