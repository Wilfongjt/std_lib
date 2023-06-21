import os
import time
import subprocess
from pathlib import Path
from os import listdir
from os.path import isfile, join
# import shutil

def prompt(msg, default, hardstop=True):
    rc = '{} [{}] : '.format(msg, default)
    rc = input(rc)
    if not rc:
        rc = default
    if rc in ['n','N','x','X','q','Q']:
        if hardstop:
            print('stopping...Stopped')
            exit(0)

    return rc


def file_age(folder, filename):
    x = os.stat('/bin')
    result = (time.time() - x.st_mtime)
    #print("The age of the given file is: ", result)
    return result
def folder_exists(folder):
    exists = os.path.isdir('{}'.format(folder))
    return exists


def file_exists(folder, filename):
    exists = os.path.isfile('{}/{}'.format(folder, filename))
    return exists


def get_env_value(KEY_NAME, default='TBD'):
    if KEY_NAME in os.environ:
        return os.environ[KEY_NAME]
    return default
def verify(prompts, prefix=None):
    # make sure values are ok
    if not prefix:
        for p in prompts:
            if prompts[p] in ['TBD']:
                return False
    else:
        for p in prompts:
            if prompts[p] in ['TBD']:
                if p.startswith(prefix):
                    return False
    return True
def createFolder(folder):
    # create all folders in a given path
    # No trailing / in folder
    #path = folder

    try:
        p=''
        for sub in folder.split('/'):
            if len(sub) > 0:
                p += '/{}'.format( sub )
                #print('check folder ', p)
                if not os.path.exists(p):
                    print('* creating folder ', p)
                    os.mkdir('{}/'.format(p))

    except OSError:
        path=None
        print("FAILURE: Creation of the directory %s failed" % path)

    return

def hasRemoteProject(url):
    # check if github repo exists
    result = subprocess.run(["git","ls-remote", "-h",url], capture_output=True, text=True)
    # 0 mean success
    #print('hasRemoteProject', result)
    if result.returncode == 0:
        return True
    return False

#def folder_exists(folder):
#    exists = os.path.isdir('{}'.format(folder))
#    return exists

def isCloned(project_folder):
    # expects the cur folder to be a project folder
    #print('cwd', os.getcwd())
    #print('isCloned', project_folder, end='')
    exists = os.path.isdir('{}/.git'.format(project_folder))
    #print(exists)
    return exists

def getCurrentBranch(project_folder):
    head_dir = Path("lib") / ".git" / "HEAD"
    #head_dir = Path(project_folder) / ".git" / "HEAD"

    #print('cwd', os.getcwd())
    #print('head_dir', head_dir)
    #head_dir = '../.git/HEAD'
    with head_dir.open("r") as f:
        content = f.read().splitlines()

    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]
    return ""

def getFolderNameList(path):
    # list of folders
    onlyfolders = []

    if len(listdir(path)) > 0:
        # onlyfolders = ['{}/{}'.format(path,f) for f in listdir(path) if not isfile(join(path, f))]
        onlyfolders = ['{}'.format(f) for f in listdir(path) if not isfile(join(path, f))]
        #if ext != None:
        #    onlyfolders = [f for f in onlyfolders if f.startswith(ext) or f.endswith(ext)]

    # return only folder names
    return [fn for fn in onlyfolders]
def getCurrentDirectory():
    return os.getcwd().replace('/_scripts','')
def getDevelopment():
    # look for Development folder
    #print(type(getCurrentDirectory()),getCurrentDirectory())
    pos = 1
    rc = getCurrentDirectory().split('/')
    idx = rc.index('Development')

    while idx + pos > len(rc):
        rc.append('TBD')

    rc = rc[0:idx + pos]
    #print('dev', '/'.join(rc))
    return rc[idx+pos-1]
def getOrganization():
    # get the organization folder
    pos = 2
    rc = getCurrentDirectory().split('/')
    idx = rc.index('Development')
    while idx + pos > len(rc):
        rc.append('TBD')
    rc = rc[0:idx+pos]

    #print('org', '/'.join(rc))
    return rc[idx+pos-1]

def getWorkspace():
    # get the workspace folder
    pos = 3
    rc = getCurrentDirectory().split('/')
    idx = rc.index('Development') #os.getcwd().split('/').index('Development')

    # pad with TBD
    while idx + pos > len(rc):
        rc.append('TBD')

    rc = rc[0:idx+pos]
    #print('ws', '/'.join(rc))
    return rc[idx+pos-1]
def getProject():
    # get the project folder
    pos = 4
    rc = getCurrentDirectory().split('/')
    idx = rc.index('Development') #os.getcwd().split('/').index('Development')

    # pad with TBD
    while idx + pos > len(rc):
        rc.append('TBD')

    rc = rc[0:idx+pos]
    #print('prj', '/'.join(rc))
    return rc[idx+pos-1]

def hasBranch(branch_name):
    # check if github repo exists
    result = subprocess.run(["git","branch"], capture_output=True, text=True)
    # 0 mean success
    #print('hasRemoteProject', result.stdout)
    if result.returncode == 0:
        if branch_name in result.stdout:
            return True
    return False
def getBranch():
    # get the project folder
    pos = 4
    rc = getCurrentDirectory().split('/')
    idx = rc.index('Development') #os.getcwd().split('/').index('Development')

    # pad with TBD
    while idx + pos > len(rc):
        rc.append('TBD')

    rc = rc[0:idx+pos]
    #print('getBranch', rc)

    head_dir = Path('/'.join(rc)) / ".git" / "HEAD"

    with head_dir.open("r") as f:
        content = f.read().splitlines()

    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]
    return ""

def getFileList(path, ext=None):
    onlyfiles=[]

    if len(listdir(path)) > 0:
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f) )]
        if ext != None:
            onlyfiles = [f for f in onlyfiles if f.startswith(ext) or f.endswith(ext)]

    #return onlyfiles
    return [fn for fn in onlyfiles if '.DS_Store' not in fn]


def main():

    assert ( getDevelopment() == 'Development')
    assert ( getOrganization() == 'lyttlebit')
    assert ( getWorkspace() == '00_tools')
    assert ( getProject() == 'py_workspace')

    assert ( hasBranch('main') )
    #assert ( hasBranch('00_init') )

if __name__ == "__main__":
    # execute as script
    main()
    
