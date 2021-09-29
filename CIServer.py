import os
import subprocess

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


run_simulator = subprocess.Popen(['./sim.x86_64'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True,
                         shell=True,
                         cwd="./simulatorbinary")


source = subprocess.run(['. ./devel/setup.sh'], 
                         stdout=subprocess.PIPE,
                         universal_newlines=True,
                         shell=True,
                         cwd="./temp/workspace/")

run_ROS = subprocess.Popen(['roslaunch', 'wolf_bringup', 'simulate_mission.launch'], 
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