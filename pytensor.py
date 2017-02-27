#!/usr/bin/env python

"""
Created on 2017-2-19

@author: Charl
"""
import re
import os
import datetime


def clean_dpkg():
    os.system("sudo apt-get remove --purge libcudnn5* libgie* -y")
    os.system("rm -rf cuda gie_samples *.tgz *.log ")
def install_dpkg(work_path, cuda, osenv):
    os.chdir(work_path)
    #match = re.compile(r"^lib[\w\d.-]*\+cuda"+cuda+r"[\w\d]+\.deb$")
    match = re.compile(r'nv-gie-repo-ubuntu'+osenv+r'[\w\d-]*?cuda'+cuda+r'[\w\d\.-]*?amd64.deb')
    allfiles = os.listdir("./")
    filenames = []
    #filenames.sort()
    for name in allfiles:
        #print name
        regex =  match.search(name)
        if regex != None:
             filenames.append(regex.group())
    for name in filenames:
        print "************",name,"*************"
        os.system("sudo dpkg -i "+ name)
    os.system("sudo apt-get update")
    os.system("sudo apt-get install libgie2 libgie-dev -y")
def test_samples(cuda):
    name = "sample.sh"
    if os.path.exists(name):
        os.system("bash " + name + " " + cuda + " 2>&1 | tee full_samples_cuda"+ cuda + ".log")
    else:
        print "file not exist!!"
def test_gie(cuda):
    giematch = re.compile(r"^gieTest-"+cuda+r"[\w\d.-]+\.tgz$")
    allfiles = os.listdir("./")
    for name in allfiles:
        regex =  giematch.search(name)
        if regex != None:
            filename=regex.group()
    os.system("tar -xvf " + filename)
    if os.path.exists("cuda"):
        name="test_.sh"
        os.system("bash " + name + " "+ cuda + " 2>&1 | tee full_gieTest_cuda"+ cuda + ".log")

def save_result(ose, cuda):
    nowtime = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    save_path = r"result/"+nowtime+"_"+ose+'.04_cuda'+ cuda
    os.system("mkdir -p " + save_path)
    os.system("mv *.log" + save_path)

if __name__ == '__main__':
    res = os.popen("lsb_release -a | grep -E ' ([0-9.]+) '").read()
    osenv = re.search(".*?(\d{2})(\.\d{2}.\d)",res).group(1)
    if osenv=="14":
        cudas=["7.5","8.0"]
    else:
        cudas=["8.0"]
    #cudas=["7.5"]
    #clean_dpkg()
    for cuda in cudas:
        homepath = os.getcwd()
        #The path of the gie packages
        giepath = homepath+"/ubuntu"+osenv+".04"+"/cuda"+cuda+"/"
        #os.chdir(giepath)
        #copy the test.tgz to homepath
        #os.system("cp *.tgz ../../")
        #os.chdir(homepath)
        #os.system("cp " + giepath + "*.tgz ./")
        #install libcudnn
        #install_dpkg(homepath+"/cudnn",cuda)
        #insatll libgie
        install_dpkg(giepath, cuda, osenv)
        os.chdir(homepath)
        test_samples(cuda)
        #test_gie(cuda)
        save_result(osenv, cuda)
        clean_dpkg()


