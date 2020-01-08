#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
import subprocess
import os
def getBranchRegistry():
    if 'LABTAINER_DIR' in os.environ:
        registry_file = os.path.join(os.environ['LABTAINER_DIR'], 'config', 'registry.config')
    else:
        print('LABTAINER_DIR not defined, unable to find registry.config')
        exit(1)
    cmd = 'git rev-parse --abbrev-ref HEAD'
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    branch = None
    registry = None
    if len(output[1].strip()) > 0:
        ''' No git, assume use of test-registry '''
        labtainer_config_file = os.path.join(os.environ['LABTAINER_DIR'], 'config', 'labtainer.config')
        labtainer_config = ParseLabtainerConfig(labtainer_config_file)
        registry = labtainer_config.test_registry
    elif len(output[0].strip()) > 0:
        branch = output[0].decode('utf-8').strip()
        if os.path.isfile(registry_file):
            with open(registry_file) as fh:
                for line in fh:
                    parts = line.split()
                    if parts[0] == branch:
                        registry = 'testregistry:%s' % parts[1]
                        break
        else:
            print('No config/registry.config file %s' % registry_file)
            exit(1)
    else:
        print('No branch found')
        exit(1)

    return branch, registry

if __name__ == '__main__':
    branch, registry = getBranchRegistry()
    print(registry)
