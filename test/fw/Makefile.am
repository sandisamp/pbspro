#
# Copyright (C) 1994-2018 Altair Engineering, Inc.
# For more information, contact Altair at www.altair.com.
#
# This file is part of the PBS Professional ("PBS Pro") software.
#
# Open Source License Information:
#
# PBS Pro is free software. You can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PBS Pro is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Commercial License Information:
#
# For a copy of the commercial license terms and conditions,
# go to: (http://www.pbspro.com/UserArea/agreement.html)
# or contact the Altair Legal Department.
#
# Altair’s dual-license business model allows companies, individuals, and
# organizations to create proprietary derivative works of PBS Pro and
# distribute them - whether embedded or bundled with other software -
# under a commercial license agreement.
#
# Use of Altair’s trademarks, including but not limited to "PBS™",
# "PBS Professional®", and "PBS Pro™" and Altair’s logos is subject to Altair's
# trademark licensing policies.
#

ptlmoduledir = $(exec_prefix)/unsupported/fw/ptl
ptlbindir = $(exec_prefix)/unsupported/fw/bin

ptl_moduledir = /opt/ptl/ptl
ptl_bindir = /opt/ptl/bin
ptl_prefixdir = /opt/ptl
ptl_docdir = /opt/ptl/doc


dist_ptl_bin_DATA= \
	bin/pbs_as \
	bin/pbs_benchpress \
	bin/pbs_config \
	bin/pbs_cov \
	bin/pbs_loganalyzer \
	bin/pbs_py_spawn \
	bin/pbs_snapshot \
	bin/pbs_stat \
	bin/pbs_swigify

ptl_modulelibdir = $(ptl_moduledir)/lib

dist_ptl_doc_DATA = \
	doc/caveats.rst \
	doc/commands.rst \
	doc/howtotest.rst \
	doc/index.rst  \
	doc/install.rst \
	doc/intro.rst  \
	doc/make.bat \
	doc/ptl.rst \
	doc/tutorial.rst \
	doc/Makefile

dist_ptl_doc_PYTHON = \
	doc/conf.py

dist_ptl_prefix_PYTHON = \
	setup.py

dist_ptl_modulelib_PYTHON = \
	ptl/lib/pbs_api_to_cli.py \
	ptl/lib/pbs_ifl_mock.py \
	ptl/lib/pbs_testlib.py \
	ptl/lib/__init__.py

ptl_moduleutilsdir = $(ptl_moduledir)/utils

dist_ptl_moduleutils_PYTHON = \
	ptl/utils/pbs_procutils.py \
	ptl/utils/pbs_dshutils.py \
	ptl/utils/pbs_covutils.py \
	ptl/utils/pbs_cliutils.py \
	ptl/utils/pbs_logutils.py \
	ptl/utils/pbs_testsuite.py \
	ptl/utils/pbs_fileutils.py \
	ptl/utils/pbs_anonutils.py \
	ptl/utils/pbs_snaputils.py \
	ptl/utils/__init__.py

ptl_moduleutilspluginsdir = $(ptl_moduleutilsdir)/plugins
dist_ptl_moduleutilsplugins_PYTHON = \
	ptl/utils/plugins/ptl_test_tags.py \
	ptl/utils/plugins/ptl_test_loader.py \
	ptl/utils/plugins/ptl_test_db.py \
	ptl/utils/plugins/ptl_test_info.py \
	ptl/utils/plugins/ptl_test_runner.py \
	ptl/utils/plugins/ptl_test_data.py \
	ptl/utils/plugins/__init__.py

dist_ptlbin_SCRIPTS = \
	bin/pbs_stat \
	bin/pbs_loganalyzer \
	bin/pbs_snapshot

dist_ptlmodule_PYTHON = ptl/__init__.py
dist_ptl_module_PYTHON = ptl/__init__.py

ptlmodulelibdir = $(ptlmoduledir)/lib

dist_ptlmodulelib_PYTHON = \
	ptl/lib/pbs_api_to_cli.py \
	ptl/lib/pbs_ifl_mock.py \
	ptl/lib/pbs_testlib.py \
	ptl/lib/__init__.py

ptlmoduleutilsdir = $(ptlmoduledir)/utils

dist_ptlmoduleutils_PYTHON = \
	ptl/utils/pbs_procutils.py \
	ptl/utils/pbs_dshutils.py \
	ptl/utils/pbs_covutils.py \
	ptl/utils/pbs_cliutils.py \
	ptl/utils/pbs_logutils.py \
	ptl/utils/pbs_testsuite.py \
	ptl/utils/pbs_fileutils.py \
	ptl/utils/pbs_anonutils.py \
	ptl/utils/pbs_snaputils.py \
	ptl/utils/__init__.py

ptlmoduleutilspluginsdir = $(ptlmoduleutilsdir)/plugins

dist_ptlmoduleutilsplugins_PYTHON = \
	ptl/utils/plugins/ptl_test_tags.py \
	ptl/utils/plugins/ptl_test_loader.py \
	ptl/utils/plugins/ptl_test_db.py \
	ptl/utils/plugins/ptl_test_info.py \
	ptl/utils/plugins/ptl_test_runner.py \
	ptl/utils/plugins/ptl_test_data.py \
	ptl/utils/plugins/__init__.py

install-data-hook:
	cd $(DESTDIR)$(ptlbindir) && \
	mv pbs_stat pbs_stat.py && \
	mv pbs_loganalyzer pbs_loganalyzer.py && \
	mv pbs_snapshot pbs_snapshot.py

install-data-hook:
	cd $(DESTDIR)$(ptl_bindir) && \
	rm -f pbs_stat.py && \
	rm -f pbs_loganalyzer.py && \
	rm -f pbs_snapshot.py && \
	rm -f pbs_as.py && \
	rm -f pbs_benchpress.py && \
	rm -f pbs_config.py && \
	rm -f pbs_cov.py && \
	rm -f pbs_py_spawn.py && \
	rm -f pbs_swigify.py

uninstall-hook:
	cd $(DESTDIR)$(ptlbindir) && \
	rm -f pbs_stat.py pbs_loganalyzer.py pbs_snapshot.py

uninstall-hook:
	cd $(DESTDIR)$(ptl_bindir) && \
	rm -f pbs_as.py pbs_config.py pbs_loganalyzer.py pbs_snapshot.py pbs_swigify.py pbs_benchpress.py pbs_cov.py pbs_py_spawn.py pbs_stat.py
