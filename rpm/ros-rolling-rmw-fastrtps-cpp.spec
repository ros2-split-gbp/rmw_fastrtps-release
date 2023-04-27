%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-rmw-fastrtps-cpp
Version:        7.2.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS rmw_fastrtps_cpp package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       %{name}-runtime%{?_isa?} = %{version}-%{release}
Requires:       ros-rolling-ament-cmake-devel
Requires:       ros-rolling-fastcdr-devel
Requires:       ros-rolling-fastrtps-devel
Requires:       ros-rolling-fastrtps-cmake-module-devel
Requires:       ros-rolling-rcutils-devel
Requires:       ros-rolling-rmw-devel
Requires:       ros-rolling-rmw-dds-common-devel
Requires:       ros-rolling-rmw-fastrtps-shared-cpp-devel
Requires:       ros-rolling-rosidl-dynamic-typesupport-devel
Requires:       ros-rolling-rosidl-runtime-c-devel
Requires:       ros-rolling-rosidl-runtime-cpp-devel
Requires:       ros-rolling-rosidl-typesupport-fastrtps-c-devel
Requires:       ros-rolling-rosidl-typesupport-fastrtps-cpp-devel
Requires:       ros-rolling-tracetools-devel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       ros-rolling-rmw-implementation-packages(member)

%description
Implement the ROS middleware interface using eProsima FastRTPS static code
generation in C++.

%package runtime
Summary:        Runtime-only files for rmw_fastrtps_cpp package
Requires:       ros-rolling-rcpputils-runtime
Requires:       ros-rolling-rcutils-runtime
Requires:       ros-rolling-rmw-runtime
Requires:       ros-rolling-rmw-fastrtps-shared-cpp-runtime
Requires:       ros-rolling-rosidl-dynamic-typesupport-runtime
Requires:       ros-rolling-tracetools-runtime
Requires:       ros-rolling-ros-workspace-runtime
BuildRequires:  ros-rolling-ament-cmake-ros-devel
BuildRequires:  ros-rolling-fastcdr-devel
BuildRequires:  ros-rolling-fastrtps-devel
BuildRequires:  ros-rolling-fastrtps-cmake-module-devel
BuildRequires:  ros-rolling-rcpputils-devel
BuildRequires:  ros-rolling-rcutils-devel
BuildRequires:  ros-rolling-rmw-devel
BuildRequires:  ros-rolling-rmw-dds-common-devel
BuildRequires:  ros-rolling-rmw-fastrtps-shared-cpp-devel
BuildRequires:  ros-rolling-rosidl-dynamic-typesupport-devel
BuildRequires:  ros-rolling-rosidl-runtime-c-devel
BuildRequires:  ros-rolling-rosidl-runtime-cpp-devel
BuildRequires:  ros-rolling-rosidl-typesupport-fastrtps-c-devel
BuildRequires:  ros-rolling-rosidl-typesupport-fastrtps-cpp-devel
BuildRequires:  ros-rolling-tracetools-devel
BuildRequires:  ros-rolling-ros-workspace-devel

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-cmake-gtest-devel
BuildRequires:  ros-rolling-ament-lint-auto-devel
BuildRequires:  ros-rolling-ament-lint-common-devel
BuildRequires:  ros-rolling-osrf-testing-tools-cpp-devel
BuildRequires:  ros-rolling-test-msgs-devel
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-rolling-rmw-implementation-packages(all)
%endif

%description runtime
Runtime-only files for rmw_fastrtps_cpp package

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

for f in \
    /opt/ros/rolling/include/ \
    /opt/ros/rolling/share/ament_index/resource_index/packages/ \
    /opt/ros/rolling/share/rmw_fastrtps_cpp/cmake/ \
    /opt/ros/rolling/share/rmw_fastrtps_cpp/package.dsv \
    /opt/ros/rolling/share/rmw_fastrtps_cpp/package.xml \
; do
    if [ -e %{buildroot}$f ]; then echo $f; fi
done > devel_files

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files -f devel_files

%files runtime
/opt/ros/rolling
%exclude /opt/ros/rolling/include/
%exclude /opt/ros/rolling/share/ament_index/resource_index/packages/
%exclude /opt/ros/rolling/share/rmw_fastrtps_cpp/cmake
%exclude /opt/ros/rolling/share/rmw_fastrtps_cpp/package.dsv
%exclude /opt/ros/rolling/share/rmw_fastrtps_cpp/package.xml

%changelog
* Thu Apr 27 2023 Geoffrey Biggs <geoff@openrobotics.org> - 7.2.0-1
- Autogenerated by Bloom

* Wed Apr 12 2023 Geoffrey Biggs <geoff@openrobotics.org> - 7.1.1-1
- Autogenerated by Bloom

* Wed Apr 12 2023 Geoffrey Biggs <geoff@openrobotics.org> - 7.1.0-1
- Autogenerated by Bloom

* Tue Mar 21 2023 Geoffrey Biggs <geoff@openrobotics.org> - 7.0.0-2
- Autogenerated by Bloom

