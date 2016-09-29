import re
import collections
import data
from Utils.utils import Utils

class protect_check():

    # ==================================================================================================================
    # UTILS
    # ==================================================================================================================
    def __run_otool(self, query, grep=None):
        """Run otool against a specific architecture."""
        cmd = '{bin} {query} {app}'.format(bin=data.DEVICE_TOOLS['OTOOL'],
                                              query=query,
                                              app=data.metadata['binary_path'])
        if grep: cmd = '%s | grep -Ei "%s"' % (cmd, grep)
        out = Utils.cmd_block(self.client, cmd).split("\n")
        return out

    def __check_flag(self, line, flagname, flag):
        """Extract result of the test."""
        tst = filter(lambda el: re.search(flag, el), line)
        res = True if tst and len(tst) > 0 else False
        self.tests[flagname] = res

    # ==================================================================================================================
    # CHECKS
    # ==================================================================================================================
    def _check_cryptid(self):
        out = self.__run_otool('-l', grep='cryptid')
        self.__check_flag(out, "Encrypted", "cryptid(\s)+1")

    def _check_pie(self):
        out = self.__run_otool('-hv')
        self.__check_flag(out, "PIE", "PIE")

    def _check_arc(self):
        out = self.__run_otool('-IV', grep='(\(architecture|objc_release)')
        self.__check_flag(out, "ARC", "_objc_release")

    def _check_stack_canaries(self):
        out = self.__run_otool('-IV', grep='(\(architecture|___stack_chk_(fail|guard))')
        self.__check_flag(out, "Stack Canaries", "___stack_chk_")

    # ==================================================================================================================
    # RUN
    # ==================================================================================================================
    def check(self):
        self.client = data.client
        for arch in data.metadata['architectures']:
            self.tests = collections.defaultdict(dict)
            # Checks
            self._check_cryptid()
            self._check_pie()
            self._check_arc()
            self._check_stack_canaries()
            # Print Output
            # self.printer.notify(arch)
            # for name, val in self.tests.items():
            #     if val:
            #         self.printer.notify('\t{:>20}: {}{:<30}{}'.format(name, Colors.G, 'OK', Colors.N))
            #     else:
            #         self.printer.error('\t{:>20}: {}{:<30}{}'.format(name, Colors.R, 'NO', Colors.N))

            print arch
            for name, val in self.tests.items():
                if val:
                    print name, "OK"
                else:
                    print name, "NO"
