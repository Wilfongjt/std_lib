import os
import subprocess
import webbrowser
from _functions import prompt, get_env_value, verify,\
                hasRemoteProject, getCurrentBranch, folder_exists,\
                getDevelopment,getOrganization,getWorkspace,getProject, \
                getBranch, hasBranch
from __doc_comments import DocComments
#print('A folder', os.getcwd())
#print('home folder', os.path.expanduser('~'))
tool_install_sfolder = '{}/Development/_tools/lib'.format(os.path.expanduser('~'))
print(DocComments(tool_install_sfolder, 'git.rebase.py').toMarkdown())

def getParameterPrompts():
    return {
        'WS_ORGANIZATION': prompt('WS_ORGANIZATION', getOrganization()),
        'WS_WORKSPACE': prompt('WS_WORKSPACE', getWorkspace()),
        'GH_USER': prompt('GH_USER', get_env_value('GH_USER')),
        'GH_PROJECT': prompt('GH_PROJECT',getProject()),
        'GH_BRANCH': prompt('GH_BRANCH', getBranch()),
        'GH_MESSAGE': prompt('GH_MESSAGE', get_env_value('GH_MESSAGE'))
    }

def main():
    ## Rebase Process

    ##1. Initialize Environment

    print('Development', getDevelopment())
    print('Organization', getOrganization())
    print('Workspace', getWorkspace())
    print('Project', getProject())
    print('Branch', getBranch())
    #
    # only run from the <PROJECT-SCRIPTS> folder eg <DEVELOPEMENT>/<ORGANIZATION>/<WORKSPACE>/<PROJECT>/scripts
    #
    ##      * Ensure git.rebase is running from the scripts folder, ie current folder ends with "scripts"
    #

    if not os.getcwd().endswith('scripts'): # development runs from /lib
        print('Stopping... Will not run from repo folder.')
        print('            Not a project/repo scripts folder.')
        print('            Install to _tools and run from git.rebase.sh. {}'.format(os.getcwd()))
        exit(0)
    #
    ##1. Collect and Define Inputs
    #
    ##      * Confirm and Update Inputs with User
    #
    prompts = getParameterPrompts()
    #
    ##      * Impute the Develpment folder name (aka <DEVELOPMENT>), eg ~/Development/
    #
    devfolder = '{}/Development'.format(os.path.expanduser('~'))
    #
    ##      * Impute remote repo URL eg https://github.com/<GH_USER>/<GH_PROJECT>.git
    #
    url = 'https://github.com/{}/{}.git'.format(prompts['GH_USER'], prompts['GH_PROJECT'])

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

    print('Development', getDevelopment())
    print('Organization', getOrganization())
    print('Workspace', getWorkspace())
    print('Project', getProject())
    #exit(0)
    #
    ##      * Stop when Development folder in not found, eg ~/Development
    #
    folder = devfolder
    print('* checking folder {} '.format(folder), end='')
    if not folder_exists(folder):
        print('stopping...development not found')
        exit(0)
    print('ok')
    #
    # Switch to development folder
    #
    os.chdir(folder)
    #
    ##      * Stop when Organization fold is not found, eg ~/Development/<WS_ORGANIZATION>
    #
    folder = '{}/{}'.format(folder,prompts['WS_ORGANIZATION'])
    print('* checking folder {} '.format(folder), end='')
    if not folder_exists(folder):
        print('stopping...organization not found')
        exit(0)
    print('ok')
    #
    # Switch to organization folder
    #
    os.chdir(folder)
    #
    ##      * Stop when Workspace folder is not found, eg ~/Development/<WS_ORGANIZATION>/<WS_WORKSPACE>
    #
    folder = '{}/{}'.format(folder,prompts['WS_WORKSPACE'])
    print('* checking folder {} '.format(folder), end='')
    if not folder_exists(folder):
        print('stopping...workspace not found')
        exit(0)
    print('ok')
    #
    ##      * Stop when Project folder is not found, eg ~/Development/<WS_ORGANIZATION>/<WS_WORKSPACE>/<GH_PROJECT>
    #
    folder = '{}/{}'.format(folder,prompts['GH_PROJECT'])
    print('* checking folder {} '.format(folder), end='')
    if not folder_exists(folder):
        print('stopping...project/repo not found')
        exit(0)
    #print('ok')
    #print('* checking for project repo', url, end='')
    #
    ##      * Stop when remote repo is not found
    #
    if not hasRemoteProject(url):
        print('Stop...Repo doesnt exist')
        exit(0)
    print(' ok')
    #
    # Switch to repo folder
    #
    os.chdir(folder)
    print('* Switch to ', folder)
    #
    ##      * Stop when branch does not exist
    #
    if not hasBranch(prompts['GH_BRANCH']):
        print('stopping...Branch "{}" not found'.format(prompts['GH_BRANCH']))
        exit(0)
    #
    ##      * Stop when branch is equal to "main"
    #
    if getBranch() == 'TBD':
        print('stopping...Bad branch')
        exit(0)
    #
    ##      * Stop when branch is equal to "TBD"
    #
    if getBranch() == 'main':
        print('stopping...Cannot rebase the "main" branch')
        exit(0)
    #
    ##      * Stop when current branch is "main"
    #
    if getCurrentBranch(folder) == 'main':
        print('stopping... commit to "main" branch not allowed!')
        exit(0)
    #
    ##      * Stop when current branch is 'TBD'
    #
    if getCurrentBranch(folder) == 'TBD':
        print('stopping... branch not found {} how about {}'.format(prompts['GH_BRANCH'], getCurrentBranch(folder)))
        exit(0)

    #if getCurrentBranch(folder) != prompts['GH_BRANCH']:
    #    print('stopping... branch not found {} how about {}'.format(prompts['GH_BRANCH'], getCurrentBranch(folder)))
    #    exit(0)

    print('* current branch', getCurrentBranch(folder))
    ##1. Run Git
    ##      *  Checkout branch
    command = 'git checkout {}'.format(prompts['GH_BRANCH'])
    os.system(command)
    ##      * Add files to git
    os.system('git add .')
    ##      * Commit with <MESSAGE>
    command = 'git commit -m {}'.format(prompts['GH_MESSAGE'])
    os.system(command)
    ##      * Checkout main branch
    os.system('git checkout main')
    ##      * Pull origin main
    os.system('git pull origin main')
    ##      * Checkout branch
    command = 'git checkout {}'.format(prompts['GH_BRANCH'])
    os.system(command)
    # feedback
    os.system('git branch')
    ##      * Rebase repo
    command = 'git rebase {}'.format(prompts['GH_BRANCH'])
    os.system(command)
    ##      * Push to origin
    if prompt('PUSH?', 'N') not in ['N','n']:
        command = 'git push origin {}'.format(prompts['GH_BRANCH'])
        os.system(command)

    #print('* update environment')
    #devEnv.upsert(prompts)
    #print('* save .env')
    #devEnv.save()
    ##* Open Repo on GitHub
    print('open browser')
    #command = 'open -a safari "https://github.com/{}/{}"'.format(prompts['GH_USER'], prompts['GH_PROJECT'])
    #os.system(command)
    url = "https://github.com/{}/{}".format(prompts['GH_USER'], prompts['GH_PROJECT'])
    command =['open', '-a', 'safari', url]
    #subprocess.Popen(command)

    os.system('git status')
    print('done')

    # the webbrowser blocks the funtioning of the command window while the browser is open
    webbrowser.get('safari').open(url, new=2)

if __name__ == "__main__":
    # execute as script
    main()
