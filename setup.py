#!/usr/bin/python

from distutils.core import setup, Command
from distutils.command.build import build
from distutils.command.clean import clean

import os
import shutil

podir = "po"
pos = [x for x in os.listdir(podir) if x[-3:] == ".po"]
langs = sorted([os.path.split(x)[-1][:-3] for x in pos])


def modir(lang):
    mobase = "build/mo"
    if not os.path.exists(mobase):
        os.mkdir(mobase)

    return os.path.join(mobase, lang)


def rmmo(lang):
    path = modir(lang)
    if os.path.exists(path):
        shutil.rmtree(path)


def mkmo(lang):
    rmmo(lang)

    outpath = modir(lang)
    os.mkdir(outpath)

    inpath = os.path.join(podir, lang + ".po")

    cmd = "msgfmt %s -o %s/gnome-gmail.mo" % (inpath, outpath)

    os.system(cmd)


def merge_i18n():
    cmd = "LC_ALL=C intltool-merge -u -c ./po/.intltool-merge-cache ./po "
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
        os.system(cmd)

        for lang in langs:
            print("Updating %s PO file" % lang)
            cmd = "cd po; intltool-update --dist \
                   --gettext-package=gnome-gmail %s >/dev/null 2>&1" % lang
            os.system(cmd)


class my_clean(clean):
    def run(self):
        clean.run(self)

        filelist = [x[:-3] for x in os.listdir('.') if x[-3:] == '.in']
        filelist += ['po/.intltool-merge-cache']
        filelist += ['gnomegmail.glade~']
        for infile in filelist:
            if os.path.exists(infile):
                os.unlink(infile)

        for dir in ['build/mo', 'build/scripts-2.7', 'build/scripts-3.4'
                    'build/scripts-3.5']:
            if os.path.exists(dir):
                shutil.rmtree(dir)


setup(
    name='gnome-gmail',
    version='1.9.3',
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
             },
     )
