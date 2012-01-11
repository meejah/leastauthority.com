from StringIO import StringIO
from twisted.trial.unittest import TestCase

from lae_automation.monitor import check_server, check_servers
from lae_automation import monitor
from lae_automation import server
import __builtin__

class TestServerMonitoring(TestCase):
    PUBLICHOST = '0.0.0.0'
    PRIVHOST = '1.1.1.1'
    MONPRVKEYPATH = '/a/fake/path'
    STDOUT = StringIO()
    STDERR = StringIO()

    HOSTLIST = [(PUBLICHOST, PRIVHOST), (PUBLICHOST, PRIVHOST)]
    def test_checkserver_failonUID(self):
        PSLINES = """FAILID"""
        def call_run(remotecommand):
            self.failUnlessEqual(remotecommand, 'ps -fC tahoe')
            return PSLINES
        self.patch(monitor, 'run', call_run)
        def call_crun(remotecommand, **kwargs):
            self.failUnlessEqual(remotecommand, 'whoami')
            return 'monitor'
        self.patch(server, 'run', call_crun)

        def call_open(filehandle, mode='r'):
            self.failUnlessEqual(filehandle, '/a/fake/path')
        self.patch(__builtin__, 'open', call_open)
        check_server(self.PUBLICHOST, self.MONPRVKEYPATH, self.STDOUT, self.STDERR)


    def test_checkserver_failonargnum(self):
        PSLINES = """UID        PID  PPID  C STIME TTY          TIME CMD\ncustomer   555     1  0 05:20 ?        00:00:00 /usr/bin/python /home/customer/LAFS_source/support/bin/tahoe introducer\ncustomer   564     1  0 05:20 ?        00:00:00 /usr/bin/python /home/customer/LAFS_source/support/bin/tahoe restart storageserver"""
        def call_run(remotecommand):
            self.failUnlessEqual(remotecommand, 'ps -fC tahoe')
            return PSLINES
        self.patch(monitor, 'run', call_run)

        def call_crun(remotecommand, **kwargs):
            self.failUnlessEqual(remotecommand, 'whoami')
            return 'monitor'
        self.patch(server, 'run', call_crun)

        def call_open(filehandle, mode='r'):
            self.failUnlessEqual(filehandle, '/a/fake/path')
        self.patch(__builtin__, 'open', call_open)
        check_server(self.PUBLICHOST, self.MONPRVKEYPATH, self.STDOUT, self.STDERR)


    def test_checkserver_failonnodes(self):
        PSLINES = """UID        PID  PPID  C STIME TTY          TIME CMD\ncustomer   555     1  0 05:20 ?        00:00:00 /usr/bin/python /home/customer/LAFS_source/support/bin/tahoe restart introducer\ncustomer   564     1  0 05:20 ?        00:00:00 /usr/bin/python /home/customer/LAFS_source/support/bin/tahoe restart introducer"""
        def call_run(remotecommand):
            self.failUnlessEqual(remotecommand, 'ps -fC tahoe')
            return PSLINES
        self.patch(monitor, 'run', call_run)

        def call_crun(remotecommand, **kwargs):
            self.failUnlessEqual(remotecommand, 'whoami')
            return 'monitor'
        self.patch(server, 'run', call_crun)

        def call_open(filehandle, mode='r'):
            self.failUnlessEqual(filehandle, '/a/fake/path')
        self.patch(__builtin__, 'open', call_open)
        check_server(self.PUBLICHOST, self.MONPRVKEYPATH, self.STDOUT, self.STDERR)


    def test_checkserver_withps_success(self):
        PSLINES = """UID        PID  PPID  C STIME TTY          TIME CMD\ncustomer   555     1  0 05:20 ?        00:00:00 /usr/bin/python /home/customer/LAFS_source/support/bin/tahoe restart introducer\ncustomer   564     1  0 05:20 ?        00:00:00 /usr/bin/python /home/customer/LAFS_source/support/bin/tahoe restart storageserver"""
        def call_run(remotecommand):
            self.failUnlessEqual(remotecommand, 'ps -fC tahoe')
            return PSLINES
        self.patch(monitor, 'run', call_run)

        def call_crun(remotecommand, **kwargs):
            self.failUnlessEqual(remotecommand, 'whoami')
            return 'monitor'
        self.patch(server, 'run', call_crun)

        def call_open(filehandle, mode='r'):
            self.failUnlessEqual(filehandle, '/a/fake/path')
        self.patch(__builtin__, 'open', call_open)
        check_server(self.PUBLICHOST, self.MONPRVKEYPATH, self.STDOUT, self.STDERR)


    def test_checkserverS_true(self):
        def call_check_server(public_host, monitor_privkey_path, stdout, stderr):
            return True
        self.patch(monitor, 'check_server', call_check_server)
        result = check_servers(self.HOSTLIST, self.MONPRVKEYPATH, self.STDOUT, self.STDERR)
        self.failUnlessEqual(result, True)


    def test_checkserverS_false(self):
        def call_check_server(public_host, monitor_privkey_path, stdout, stderr):
            return False
        self.patch(monitor, 'check_server', call_check_server)
        result = check_servers(self.HOSTLIST, self.MONPRVKEYPATH, self.STDOUT, self.STDERR)
        self.failUnlessEqual(result, False)


    def test_comparetolocal_success(self):
        LOCPUBDNSNAME = 'ec2-0-0-0-0.c'
        LOCINSTANCEID = 'i-aaaaaaaa'
        LOCSTARTTIME  = '2012-00-00T00:00:00.000Z'
