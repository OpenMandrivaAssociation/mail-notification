%define name mail-notification
%define version 4.0
%define rel 1
%define evo %(rpm -q evolution-devel --queryformat %%{VERSION})
%define fname %name-%version

Version: 	%{version}
Summary: 	New mail status tray icon
Name: 		%{name}
Release: 	%mkrel %rel
License: 	GPL
Group: 		Networking/Mail
Source: 	http://savannah.nongnu.org/download/mailnotify/%{fname}.tar.gz
Source1: 	http://savannah.nongnu.org/download/mailnotify/%{fname}.tar.gz.sig
URL: 		http://www.nongnu.org/mailnotify/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:  libeel-devel >= 2.6
BuildRequires:  libsoup-devel >= 2.2
BuildRequires:  libsasl-devel
BuildRequires:  openssl-devel
BuildRequires:	libgmime-devel
BuildRequires:  evolution-devel
BuildRequires:  evolution-data-server-devel >= 1.4
BuildRequires:  libgnomeprintui-devel
BuildRequires:  libnotify-devel
BuildRequires:  avahi-glib-devel avahi-client-devel
BuildRequires:  gob2
BuildRequires:  scrollkeeper
BuildRequires:  perl-XML-Parser
BuildRequires:  mono-devel
BuildRequires:  desktop-file-utils
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

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

%build
export LDFLAGS="-Wl,--export-dynamic"
%configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
rm -f %buildroot%_libdir/evolution/*/plugins/*a
%find_lang %name --with-gnome
mkdir -p %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}): \
 command="%{_bindir}/%{name} --display-main-window" \
 icon="%{name}.png" \
 longtitle="Get notified when new mail arrives" \
 needs="x11" \
 section="Internet/Mail" \
 title="Mail Notification" \
 startup_notify="yes" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Internet-Mail" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
ln -s %_datadir/icons/hicolor/48x48/apps/mail-notification.png %{buildroot}%{_liconsdir}/%{name}.png
ln -s %_datadir/icons/hicolor/32x32/apps/mail-notification.png %{buildroot}%{_iconsdir}/%{name}.png
ln -s %_datadir/icons/hicolor/16x16/apps/mail-notification.png %{buildroot}%{_miconsdir}/%{name}.png


%post 
%update_menus
%post_install_gconf_schemas mail-notification
%update_scrollkeeper
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas mail-notification

%postun
%clean_menus
%clean_scrollkeeper
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr (-,root,root)
%doc README COPYING INSTALL TODO 
%config(noreplace) %_sysconfdir/xdg/autostart/mail-notification.desktop
%_bindir/*
%_datadir/%name
%_datadir/applications/*
%dir %_datadir/omf/mail-notification/
%_datadir/omf/mail-notification/%name-C.omf
%_libdir/bonobo/servers/*
%_sysconfdir/gconf/schemas/mail-notification.schemas
%_datadir/icons/hicolor/*/apps/*
%_menudir/%name
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png

%files evolution
%defattr (-,root,root)
%doc COPYING
%_libdir/evolution/*/plugins/*

