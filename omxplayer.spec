%global commit_date     20181014
%global commit_long     7f3faf6cadac913013248de759462bcff92f0102
%global commit_short    %(c=%{commit_long}; echo ${c:0:7})
%global ffmpeg_rel      4.0.2
%global debug_package   %{nil}

# We don't want any bundled libs in these directories to generate Provides
%global __provides_exclude_from %{_libdir}/%{name}/.*\\.so
%global private_libs libavcodec|libavdevice|libavfilter|libavformat|libavutil|libswresample|libswscale
%global __requires_exclude ^(%{private_libs})\\.so

Name:       omxplayer
Version:    %{commit_date}
Release:    1.%{commit_short}%{dist}
Summary:    Raspberry Pi command line OMX player
Group:      Applications/Multimedia
License:    GPL-2.0+
URL:        https://github.com/popcornmix/%{name}
Source0:    %{url}/archive/%{commit_long}.tar.gz#/%{name}-%{commit_short}.tar.gz
Source1:    https://github.com/FFmpeg/FFmpeg/archive/n%{ffmpeg_rel}.tar.gz#/ffmpeg-%{ffmpeg_rel}.tar.gz
Source2:    %{name}.desktop
Patch1:     0001-Makefile.patch
Patch2:     0003-Makefile.ffmpeg.patch
Patch3:     0004-fix-libs-path.patch
Patch4:     0005-fix-font-paths.patch
Patch5:     0006-video-group-check.patch
ExclusiveArch:  armv7hl

BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  raspberrypi-vc-libs-devel
BuildRequires:  raspberrypi-vc-static
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libssh)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(smbclient)

Requires:   %{name}-libs
Requires:   fbset
Requires:   gnu-free-sans-fonts

Provides: bundled(libavcodec)
Provides: bundled(libavdevice)
Provides: bundled(libavfilter)
Provides: bundled(libavformat)
Provides: bundled(libavutil)
Provides: bundled(libswresample)
Provides: bundled(libswscale)


%description
OMXPlayer is a video player specifically made for the Raspberry Pi's GPU.
It relies on the OpenMAX hardware acceleration API, which is the Broadcom's
VideoCore officially supported API for GPU video/audio processing.


%package libs
Summary: Libraries used by %{name}
Group: System Environment/Libraries


%description libs
Libraries used by %{name}


%package desktop
Summary: OMXPlayer Desktop Entry specification file
Requires: lxterminal
Requires: libnotify


%description desktop
The freedesktop Desktop Entry specification file for OMXPlayer to integrate into
desktop environments.


%prep
%setup -n %{name}-%{commit_long}
mkdir ffmpeg && tar -xzf %{SOURCE1} -C ffmpeg --strip-components=1

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%if 0%{?fedora} > 28
# Disable ffmpeg libsmbclient support for now :-/
# ERROR: libsmbclient not found
# Refer: https://bugs.gentoo.org/666548
sed -i 's/enable-libsmbclient/disable-libsmbclient/' Makefile.ffmpeg
%endif


%build
%{make_build} -f Makefile.ffmpeg configure
%{make_build} -f Makefile.ffmpeg compile
%{make_install} -f Makefile.ffmpeg

# should we generate a version.h here first?
%{make_build} omxplayer.bin
%{make_build} omxplayer.1


%install
%{__install} -d %{buildroot}/%{_bindir}
%{__install} -p %{name} %{buildroot}/%{_bindir}
%{__install} -p %{name}.bin %{buildroot}/%{_bindir}

%{__install} -d %{buildroot}/%{_mandir}
%{__install} -p %{name}.1 %{buildroot}/%{_mandir}

%{__install} -d %{buildroot}/%{_libdir}/%{name}
%{__install} -p ffmpeg_compiled/usr/local/lib/*.so* %{buildroot}/%{_libdir}/%{name}/

%{__install} -d %{buildroot}/%{_datadir}/applications
%{__install} -p %{SOURCE2} %{buildroot}/%{_datadir}/applications
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc README.md
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{_mandir}/%{name}.1


%files libs
%license COPYING
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so*


%files desktop
%{_datadir}/applications/*.desktop


%changelog
* Sun Oct 14 2018 Vaughan Agrez <devel at agrez dot net> 20181014-1.7f3faf6
- Update to git commit: 7f3faf6cadac913013248de759462bcff92f0102
- Bump ffmpeg release to 4.0.2
- Refactor Makefile / Makefile.ffmpeg patches
- Drop makefile.include patch
- Disable generation of man file
- Fix BuildRequires

* Thu Apr 05 2018 Vaughan Agrez <devel at agrez dot net> 20170908-2.037c3c1
- Bump ffmpeg release to 3.3.6
- Add desktop file
- Add video group check (Patch 5)

* Thu Nov 23 2017 Vaughan Agrez <devel at agrez dot net> 20170908-1.037c3c1
- Update to git commit: 037c3c1eab2601dc1e8fb329c2290eb2380acb3c
- Bump ffmpeg release to 3.3.5
- Drop ffmpeg openssl build fixes (merged upstream)

* Tue Jul 25 2017 Vaughan Agrez <devel at agrez dot net> 20170330-3.061425a5
- Fix building against openssl >= 1.1.0 (Patches 5 & 6)
- Bump ffmpeg release to 3.1.9
- Exclude Requires/Provides for bundled libs
- Use %%{make_build} to build ffmpeg
- Drop %%post & %%postun sections

* Mon Apr 24 2017 Vaughan Agrez <devel at agrez dot net> 20170330-2.061425a5
- Add requires for fbset

* Thu Apr 20 2017 Vaughan Agrez <devel at agrez dot net> 20170330-1.061425a5
- Initial package
