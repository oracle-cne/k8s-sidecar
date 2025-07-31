{{{$version := printf "%s.%s.%s" .major .minor .patch}}}
%global debug_package     %{nil}
%{!?registry: %global registry container-registry.oracle.com/olcne}

%global _name	    k8s-sidecar
%global _buildhost  build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:           %{_name}-container-image
Version:        {{{ $version }}}
Release:        1%{?dist}
Summary:        This is a docker container intended to run inside a kubernetes cluster to collect config maps with a specified label and store the included files in a local folder.
License:        MIT
Vendor:		    Oracle America
Group:          System/Management
Url:            https://github.com/kiwigrid/k8s-sidecar
Source:         %{name}-%{version}.tar.bz2

%description
This is a docker container intended to run inside a kubernetes cluster to collect config maps with a specified label and store the included files in an local folder.
It can also send an HTTP request to a specified URL after a configmap change. The main target is to be run as a sidecar container to supply an application with information from the cluster.
The contained Python script is working from Kubernetes API 1.10.

%prep
%setup -n %{name}-%{version}

%build
%global rpm_name %{_name}-%{version}-%{release}.%{_build_arch}
dnf clean expire-cache
yumdownloader --destdir=${PWD}/rpms %{rpm_name}

%global docker_tag %{registry}/%{_name}:v%{version}
%global dockerfile Dockerfile
docker build --pull --build-arg https_proxy=${https_proxy} \
	-t %{docker_tag} -f ./olm/builds/%{dockerfile} .
docker build --pull \
      --build-arg http_proxy=${https_proxy} \
      --build-arg https_proxy=${https_proxy} \
      -t %{docker_tag} -f ./olm/builds/%{dockerfile} .
docker save -o %{_name}.tar %{docker_tag}

%install
%__install -D -m 644 %{_name}.tar %{buildroot}/usr/local/share/olcne/%{_name}.tar

%files
%license LICENSE
/usr/local/share/olcne/%{_name}.tar

%clean

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Added Oracle Specific Build Files for k8s-sidecar-container-image
