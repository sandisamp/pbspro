#!/bin/bash -x


PBS_VERSION=$(cat pbspro.spec | grep " pbs_version " | sed 's/.* //')
PBS_DIR=$(pwd)/../

create_file()
{
# substituting variables because pbs spec file contains similar strings, sed command fails
 	first=$1
 	second=$2
	third=$3
# adding shebang for shell scripts	
	echo "#!/bin/bash" > $third
	echo "RPM_INSTALL_PREFIX=/opt/pbs" >> $third	
	echo "export RPM_INSTALL_PREFIX" >> $third
# Moving pbs_* files from etc to /opt/pbs/etc/ in postinst
	if [ $third == *.postinst ]
	then
		echo "mkdir \${RPM_INSTALL_PREFIX}/etc" >> $third
		echo "mv /etc/pbs_* \${RPM_INSTALL_PREFIX}/etc" >> $third 
	fi

	eval "sed -n '/$first/,/$second/p' pbspro.spec | tee -a $third"	
	eval "sed -i '$ d' $third"
	eval "sed -i 's/$first/#xxx/' $third"

# replacing macros with values as they are not recognizable in shell script	
	eval "sed -i 's/%{pbs_prefix}/\/opt\/pbs/' $third"
	eval "sed -i 's/%{version}/${PBS_VERSION}/' $third"
	eval "sed -i 's/%{pbs_home}/\/var\/spool\/pbs/' $third"
	eval "sed -i 's/%{pbs_dbuser}/postgres/' $third"
	eval "sed -i 's/%endif/#xxx/' $third"
	eval "sed -i 's/%if %{defined have_systemd}/#xxx/' $third"
}

# Rname current directory to pbspro-(version_no)
mv  ${PBS_DIR}/pbspro ${PBS_DIR}/pbspro-${PBS_VERSION}
./autogen.sh
#./configure --prefix=/opt/pbs --libexecdir=/opt/pbs/libexec

# creating debian folder templates
dh_make --single --yes --createorig

# creating debian scripts
create_file "%post %{pbs_server}" "%post %{pbs_execution}" pbspro-server.postinst
create_file "%postun %{pbs_server}" "%postun %{pbs_execution}" pbspro-server.postrm
create_file "%preun %{pbs_server}" "%preun %{pbs_execution}" pbspro-server.prerm

create_file "%post %{pbs_execution}" "%post %{pbs_client}" pbspro-execution.postinst
create_file "%postun %{pbs_execution}" "%postun %{pbs_client}" pbspro-execution.postrm
create_file "%preun %{pbs_execution}" "%preun %{pbs_client}" pbspro-execution.prerm

create_file "%post %{pbs_client}" "%preun %{pbs_server}" pbspro-client.postinst
create_file "%postun %{pbs_client}" "%files %{pbs_server}" pbspro-client.postrm
create_file "%preun %{pbs_client}" "%postun %{pbs_server}" pbspro-client.prerm

# adding configuration rules in debian/rules file
echo "override_dh_auto_configure:
	dh_auto_configure -- prefix=/opt/pbs -- libexecdir=/opt/pbs/libexec" >> debian/rules

# moving scripts to debian folder
mv *.postinst debian/
mv *.prerm debian/
mv *.postrm debian/

# Creating debian control file
echo "Source: pbspro
Section: unknown
Priority: optional
Maintainer: PBSPro
Build-Depends: debhelper (>=9),autotools-dev
Homepage: https://www.pbspro.org/

Package: pbspro-server
Architecture: any
Depends: \${shlibs:Depends}, \${misc:Depends}
Conflicts: pbspro-execution, pbspro-client, pbspro-client-ohpc, pbspro-execution-ohpc, pbspro-server-ohpc, pbs, pbs-mom, pbs-cmds
Description: PBS Professional® is a fast, powerful workload manager and
 job scheduler designed to improve productivity, optimize
 utilization & efficiency, and simplify administration for
 HPC clusters, clouds and supercomputers.
 .
 This package is intended for a server host. It includes all
 PBS Professional components.

Package: pbspro-execution
Architecture: any
Depends: \${shlibs:Depends}, \${misc:Depends}
Conflicts: pbspro-server, pbspro-client, pbspro-client-ohpc, pbspro-execution-ohpc, pbspro-server-ohpc, pbs, pbs-mom, pbs-cmds
Description: PBS Professional® is a fast, powerful workload manager and
 job scheduler designed to improve productivity, optimize
 utilization & efficiency, and simplify administration for
 HPC clusters, clouds and supercomputers.
 .
 This package is intended for an execution host. It does not
 include the scheduler, server, or communication agent. It
 does include the PBS Professional user commands.>

Package: pbspro-client
Architecture: any
Depends: \${shlibs:Depends}, \${misc:Depends}
Conflicts: pbspro-server, pbspro-execution, pbspro-client-ohpc, pbspro-execution-ohpc, pbspro-server-ohpc, pbs, pbs-mom, pbs-cmds
Description: PBS Professional® is a fast, powerful workload manager and
 job scheduler designed to improve productivity, optimize
 utilization & efficiency, and simplify administration for
 HPC clusters, clouds and supercomputers.
 .
 This package is intended for a client host and provides
 the PBS Professional user commands." > debian/control


# building the package
dpkg-buildpackage -d -b -us -uc


find debian/tmp/ -type f > pbspro-server.install
cp pbspro-server.install debian/
sed -n '/%files %{pbs_execution}/,/%files %{pbs_client}/p' pbspro.spec | grep "exclude %{.*}" | tee tmp
while read -r line
do
    name="$line"
    find $name >> tmp2
done < "tmp"

while read -r line
do
    name="$line"
    list=`eval "echo $name | sed 's:.*/::'"`
    eval "sed -i '/$list/d' pbspro-server.install"
done < "tmp2"
mv pbspro-server.install pbspro-execution.install
mv pbspro-execution.install debian/

rm tmp
rm tmp2
#sed -i '/pbs_cgroups.CF/d' pbspro-server.install

find debian/tmp/ -type f > pbspro-server.install

sed -n '/%files %{pbs_client}/,/%exclude %{_unitdir}\/pbs.service/p' pbspro.spec | grep "exclude %{.*}" | tee tmp
while read -r line
do
    name="$line"
    find $name >> tmp2
done < "tmp"

while read -r line
do
    name="$line"
    list=`eval "echo $name | sed 's:.*/::'"`
    eval "sed -i '/$list/d' pbspro-server.install"
done < "tmp2"
mv pbspro-server.install pbspro-client.install
mv pbspro-client.install debian/

rm tmp
rm tmp2

dpkg-buildpackage -d -b -us -uc

