%global commit_date     20170330
%global commit_long     061425a5eabf6e9ee43229911c073a863d144038
%global commit_short    %(c=%{commit_long}; echo ${c:0:7})
%global ffmpeg_rel      3.1.7
%global debug_package   %{nil}

Name:       omxplayer
Version:    %{commit_date}
Release:    2.%{commit_short}%{dist}
Summary:    Raspberry Pi command line OMX player
Group:      Applications/Multimedia
License:    GPL-2.0+
URL:        https://github.com/popcornmix/%{name}
Source0:    https://github.com/popcornmix/%{name}/archive/%{commit_long}.tar.gz#/%{name}-%{commit_short}.tar.gz
Source1:    https://github.com/FFmpeg/FFmpeg/archive/n%{ffmpeg_rel}.tar.gz#/ffmpeg-%{ffmpeg_rel}.tar.gz
Patch0:     0001-Makefile.patch
Patch1:     0002-Makefile.include.patch
Patch2:     0003-Makefile.ffmpeg.patch
Patch3:     0004-fix-libs-path.patch
Patch4:     0005-fix-font-paths.patch
ExclusiveArch:  armv7hl

BuildRequires:  boost-devel
BuildRequires:  raspberrypi-vc-static
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(bcm_host)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libssh)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(smbclient)

Requires:   %{name}-libs
Requires:   fbset
Requires:   gnu-free-sans-fonts



%description
Omxplayer is a video player specifically made for the Raspberry Pi's GPU. It relies on the OpenMAX hardware acceleration API, which is the Broadcom's VideoCore officially supported API for GPU video/audio processing.


%package libs
Summary: Libraries used by %{name}
Group: System Environment/Libraries


%description libs
Libraries used by %{name}


%prep
%autosetup -n %{name}-%{commit_long}

mkdir ffmpeg
tar -xzf %{SOURCE1} -C ffmpeg --strip-components=1

%build
make -f Makefile.ffmpeg CFLAGS="%{optflags}" configure
make -f Makefile.ffmpeg compile
make -f Makefile.ffmpeg install

# should we generate a version.h here first?
%{make_build} omxplayer.bin
%{make_build} omxplayer.1


%install
rm -rf $RPM_BUILD_ROOT

%{__install} -d %{buildroot}/%{_bindir}
%{__install} -p %{name} %{buildroot}/%{_bindir}
%{__install} -p %{name}.bin %{buildroot}/%{_bindir}

%{__install} -d %{buildroot}/%{_mandir}
%{__install} -p %{name}.1 %{buildroot}/%{_mandir}

%{__install} -d %{buildroot}/%{_libdir}/%{name}
%{__install} -p ffmpeg_compiled/usr/local/lib/*.so* %{buildroot}/%{_libdir}/%{name}/



%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%license COPYING
%doc README.md
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{_mandir}/%{name}.1


%files libs
%license COPYING
%{_libdir}/%{name}/*.so*


%changelog
* Mon Apr 24 2017 Vaughan Agrez <devel at agrez dot net> 20170330-2.061425a5
- Add requires for fbset

* Thu Apr 20 2017 Vaughan Agrez <devel at agrez dot net> 20170330-1.061425a5
- Initial package
