import os
from _functions import prompt, get_env_value, verify,createFolder,\
                hasRemoteProject,isCloned,getCurrentBranch, getFileList, hasBranch

from __dev_env import DevEnv
from __text_file_helper import TextFileHelper
from __doc_comments import DocComments

#print('cwd', os.getcwd())
print(DocComments(os.getcwd(), '/lib/git.branch.py').toMarkdown())

def getParameterPrompts():
    return {
        'WS_ORGANIZATION': prompt('WS_ORGANIZATION', get_env_value('WS_ORGANIZATION')),
        'WS_WORKSPACE': prompt('WS_WORKSPACE', get_env_value('WS_WORKSPACE')),
        'GH_USER': prompt('GH_USER', get_env_value('GH_USER')),
        'GH_PROJECT': prompt('GH_PROJECT',get_env_value('GH_PROJECT')),
        'GH_BRANCH': prompt('GH_BRANCH', get_env_value('GH_BRANCH')),
    }

def main():
    ### Branch Process

    ##1. Initialize Environment
    ##      * Create default environment file When .env not found
    ##      * Open enviroment file When found in <SOURCE> folder

    print('starting folder', os.getcwd())
    devEnv = DevEnv(filename='lib/.env').open()
    #
    ##      * Impute the Develpment folder name (aka <DEVELOPMENT>), eg ~/Development/
    #
    devfolder = '{}/Development'.format(os.path.expanduser('~'))
    #
    ##      * Impute the Application folder name (aka <APP>), eg ~/Development/_tools
    #
    srcFolder = '{}/Development/_tools'.format(os.path.expanduser('~'))
    #
    ##1. Collect and Define Inputs
    #
    ##      * Confirm and Update Inputs with User
    #
    prompts = getParameterPrompts()
    #
    ##      * Impute WS_WORKSPACE URI eg ~/Development/<WS_ORGANIZATION>/<WS_WORKSPACE>
    #
    folder = '{}/{}/{}'.format(devfolder, prompts['WS_ORGANIZATION'], prompts['WS_WORKSPACE'])
    print('* check for workspace folder {} '.format(folder))
    #
    ##      * Impute remote repo URL eg https://github.com/<GH_USER>/<GH_PROJECT>.git
    #
    url = 'https://github.com/{}/{}.git'.format(prompts['GH_USER'], prompts['GH_PROJECT'])
    print('* checking for project repo', url)

    #
    ##1. Validate Inputs
    #

    #
    ##      * Stop When workspace ('WS_') settings are invalid
    #
    if not verify(prompts, prefix='WS_'): #
        print(prompts)
        print('Stop...Invalid WS value found')
        exit(0)

    #
    ##      * Stop When GitHub ('GH_') settings are invalid
    #
    if not verify(prompts, prefix='GH_'):  #
        print(prompts)
        print('Stop...Invalid GH value found')
        exit(0)

    #
    ##      * Stop When remote repo is not found
    #
    if not hasRemoteProject(url):
        print('Stop...Repo doenst exist')
        exit(0)
    #
    ##1. Setup for Develpment
    #
    #
    ##      * Create Workspace folder When folder doesnt exist
    #
    createFolder(folder)

    #
    ##      * Load settings into environment variables
    #
    devEnv.upsert(prompts)
    #
    ##      * Save environment to .env file in py_workspace folder
    #
    print('* save .env')
    devEnv.save()
    #
    # Start moving files...Switch to workspace folder
    #
    print('* switch to workspace ', folder)
    os.chdir(folder)
    #
    ##      * Clone the repository (aka Project) When repository is not cloned
    #
    folder = '{}/{}'.format(folder, prompts['GH_PROJECT'])
    if not isCloned(folder):
        print('* cloning...', end='')
        command = 'git clone {}'.format(url)
        os.system(command)
    else:
        print('* skipping...clone. "{}" is already cloned.'.format(prompts['GH_PROJECT']))
    #
    # Switch to project/repo folder
    #
    os.chdir(folder)
    print('* switch to project/repo', folder)
    #
    ##      * CHECKOUT branch ... get ready for development
    #
    if getCurrentBranch(folder) != prompts['GH_BRANCH']:
        command = 'git checkout -b {}'.format(prompts['GH_BRANCH'])
        print('* command', command, end='')
        os.system(command)
        #print('')
    else:
        print('* skipping...checkout. "{}" is already checked out.'.format(prompts['GH_BRANCH']))

    #
    ##1. Install Utility Scripts
    ##      * Create scripts folder in repository clone eg <PROJECT>/scripts
    #
    scriptsfolder = '{}/scripts'.format(folder)
    createFolder(scriptsfolder)

    #
    ##      * Copy _tools/scripts/*.sh to <PROJECT>/scripts
    #
    file_names = getFileList('{}/scripts'.format(srcFolder),'sh')

    for fn in file_names:
        print('fn', fn)
        TextFileHelper('{}/scripts'.format(srcFolder), fn).copyTo(scriptsfolder, fn)

    #
    # # Copy bk.sh to repo/scripts
    #
    #TextFileHelper('{}/{}'.format(srcFolder), 'bk.sh').copyTo(scriptsfolder, 'bk.sh')

    print('\n* confirm current branch', getCurrentBranch(folder))
    print('* update environment')

    #
    ##      * Save environment to <PROJECT>/scripts
    #
    #wsEnv = DevEnv(folder=scriptsfolder, filename='{}.env'.format(prompts['GH_PROJECT'])).open().save()
    wsEnv = DevEnv(folder=scriptsfolder, filename='lib/.env').open().save()


if __name__ == "__main__":
    # execute as script
    main()