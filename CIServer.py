#!/usr/bin/env python3
import os
import subprocess
from pyvirtualdisplay import Display

def shell_source(script, ccwd):
    """Sometime you want to emulate the action of "source" in bash,
    settings some environment variables. Here is a way to do it."""
    import subprocess, os
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, cwd=ccwd, shell=True, encoding='utf-8')
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)

'''create temporary directory'''
mkdir = subprocess.run(['mkdir', 'temp'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)

''' Copy Template workspace into Temp'''
copy = subprocess.run(['cp', '-r', 'templatews/', 'temp/workspace'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)

'''Clone git repo into workspace'''
clone = subprocess.run(['git', 'clone', 'https://github.com/ncsurobotics/seawolf8.git'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True, 
                         cwd="./temp/workspace/src")

'''Clone in the submodules of the repository git submodule update --init --recursive'''

submodule = subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True, 
                         cwd="./temp/workspace/src/seawolf8")

'''switch to the right branch'''
submodule = subprocess.run(['git', 'checkout', 'unity_sim'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True, 
                         cwd="./temp/workspace/src/seawolf8")

print("Download Finished")

'''Build the project'''

print("Building....")
make = subprocess.run(['catkin_make'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True,
                         shell=True,
                         cwd="./temp/workspace/")

if make.returncode != 0:
    print(make.stdout)
    print("Build Failed!!")
    quit(-1)

print("Build finished")


with Display(visible=False, size=(100, 60)) as disp:
    run_simulator = subprocess.Popen(["./sim.x86_64"], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True,
                         shell=True,
                         cwd="./simulatorbinary")

    shell_source("./devel/setup.sh", "./temp/workspace")

    run_ROS = subprocess.Popen(['roslaunch wolf_bringup simulate_mission.launch'], 
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            shell=True,
                            cwd="./temp/workspace/")


    while True:
        output = run_ROS.stdout.readline()
        print(output.strip())
        return_code = run_ROS.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in run_ROS.stdout.readlines():
                print(output.strip())
            break

    delete_temp = subprocess.run(['rm', '-rf', './temp'], 
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            shell=True)
