%define name mail-notification
%define version 5.4

%define evo %(rpm -q evolution-devel --queryformat %%{VERSION})
%define fname %name-%version

Version: 	%{version}
Summary: 	New mail status tray icon
Name: 		%{name}
Release: 	%mkrel 12
License: 	GPLv3+ and GFDL+
Group: 		Networking/Mail
Source: 	http://savannah.nongnu.org/download/mailnotify/%{fname}.tar.bz2
Source1: 	http://savannah.nongnu.org/download/mailnotify/%{fname}.tar.bz2.sig
#gw from Fedora, port to Evolution 2.29 API
#gw patch generated C sources
Patch: mail-notification-5.4-evo2.29.patch
Patch1: mail-notification-5.4-gmime.patch
# gw from Fedora, SASL off-by-one error
Patch2:	mail-notification-5.4-sasl_encode64.patch
# (fc) 5.4-12mdv fix missing icons
Patch3: mail-notification-5.4-missing-icons.patch
URL: 		http://www.nongnu.org/mailnotify/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  libsasl-devel
BuildRequires:  openssl-devel
BuildRequires:	libgmime-devel
BuildRequires:  evolution-devel
#gw with the patch1 we need e-d-s 2.23
BuildRequires:  evolution-data-server-devel >= 2.23
BuildRequires:  libgnomeui2-devel
BuildRequires:  libgnomeprintui-devel
BuildRequires:  libnotify-devel
BuildRequires:  avahi-glib-devel avahi-client-devel
BuildRequires:  gob2
BuildRequires:  scrollkeeper
BuildRequires:  perl-XML-Parser
BuildRequires:  mono-devel
BuildRequires:  desktop-file-utils
#gw aclocal called:
BuildRequires:  intltool
BuildRequires:  libglade2-devel
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Suggests: fetchyahoo

%description
Mail Notification is a status icon (aka tray icon) that informs you if 
you have new mail. It works with system trays implementing the 
freedesktop.org System Tray Specification, such as the GNOME Panel 
Notification Area, the Xfce Notification Area, and the KDE System Tray. 
Mail Notification features include multiple mailbox support, mbox, MH, 
Maildir, Sylpheed, POP3, IMAP, and Gmail support, SASL and APOP 
authentication support, SSL support, automatic detection of mailbox 
format, automatic notification, and HIG 2.0 compliance.

%package evolution
Group: 		Networking/Mail
Requires: %name = %version
Requires: evolution >= %evo
Summary: New mail status tray icon for Evolution

%description evolution
Mail Notification is a status icon (aka tray icon) that informs you if 
you have new mail. It works with system trays implementing the 
freedesktop.org System Tray Specification, such as the GNOME Panel 
Notification Area, the Xfce Notification Area, and the KDE System Tray. 

Install this if you use Evolution.

%prep

%setup -q -n %fname
%patch -b .evo2.23
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .missing_icons

# Drop #line statements in C sources generated bu .gob,
# for the proper debuginfo package
pushd build/src
for f in *.c *.h
do
sed -i '/^#line / d' $f
done
popd 

touch build/src/mn-evolution-server.gob.stamp

%build
#gw link error in evolution plugin
%define _disable_ld_no_undefined 1
./jb configure prefix=%_prefix sysconfdir=%_sysconfdir gconf-schemas-dir=%_sysconfdir/gconf/schemas cflags="%optflags" ldflags="%ldflags -Wl,--export-dynamic" destdir=%buildroot
./jb build 

%install
rm -rf $RPM_BUILD_ROOT %name.lang

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 ./jb install
rm -f %buildroot%_libdir/evolution/*/plugins/*a
%find_lang %name --with-gnome
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Internet-Mail" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
ln -s %_datadir/icons/hicolor/48x48/apps/mail-notification.png %{buildroot}%{_liconsdir}/%{name}.png
ln -s %_datadir/icons/hicolor/32x32/apps/mail-notification.png %{buildroot}%{_iconsdir}/%{name}.png
ln -s %_datadir/icons/hicolor/16x16/apps/mail-notification.png %{buildroot}%{_miconsdir}/%{name}.png


%if %mdkversion < 200900
%post 
%update_menus
%post_install_gconf_schemas mail-notification
%update_scrollkeeper
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas mail-notification

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%clean_icon_cache hicolor
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr (-,root,root)
%doc README COPYING TODO 
%config(noreplace) %_sysconfdir/xdg/autostart/mail-notification.desktop
%_bindir/*
%_datadir/%name
%_datadir/applications/*
%dir %_datadir/omf/mail-notification/
%_datadir/omf/mail-notification/%name-C.omf
%_sysconfdir/gconf/schemas/mail-notification.schemas
%_datadir/icons/hicolor/*/apps/*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png

%files evolution
%defattr (-,root,root)
%doc COPYING
%_libdir/evolution/*/plugins/*

