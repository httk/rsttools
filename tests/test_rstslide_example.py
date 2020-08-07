#!/usr/bin/env python
#
# Copyright 2019 Rickard Armiento
#
# This file is part of a Python candidate reference implementation of
# the optimade API [https://www.optimade.org/]
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, unittest, subprocess, argparse

top = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

def run(command,args=[]):
    args = list(args)
    popen = subprocess.Popen([command] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return popen.communicate()

class TestRstslideExample(unittest.TestCase):

    def execute(self, command, *args):
        print("RUN:",command)
        out,err = run(command,args)
        self.assertTrue(len(err.strip())==0, msg=err)

    def test_rstslide_example(self):
        cwd = os.getcwd()
        os.chdir(os.path.join(top,'docs','rstslide'))
        self.execute(os.path.join(top,'bin','py.rstslide'),'presentation.rst')
        os.chdir(cwd)

#############################################################################


if __name__ == '__main__':

    ap = argparse.ArgumentParser(description="Test rstslide examples")
    args, leftovers = ap.parse_known_args()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestRstslideExample)
    unittest.TextTestRunner(verbosity=2).run(suite)


