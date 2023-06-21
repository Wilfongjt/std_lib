import os
from _functions import createFolder, getFileList
from __text_file_helper import TextFileHelper
from __dev_env import DevEnv
from __doc_folders import DocFolders
from __doc_comments import DocComments

#print('cwd', os.getcwd())
print(DocComments(os.getcwd(), '/lib/install.py').toMarkdown())

#
### Install Process
#
def main():
    ## To use the tools, you must install them on your computer.
    ## 1. Clone py_workspace
    ##      * Navigate to the py_workspace clone folder
    ##      * From the command line: python3 install.py
    ##      * Install.py does the following:
    env_file = 'lib/.env'
    srcFolder = os.getcwd()
    dstFolder = '{}/Development/_tools'.format(os.path.expanduser('~'))
    dstLibFolder = '{}/lib'.format(dstFolder)
    dstScrptFolder = '{}/scripts'.format(dstFolder)

    ##1. Initialize Application Folders
    ##      * Create tools folder when folder is not found, eg ~/<USER>/Development/_tools
    ##      * Create bash script folder when folder is not found, eg ~/<USER>/Development/_tools/scripts
    createFolder(dstScrptFolder)
    #
    ##      * Create python library folder when folder is not found, eg ~/<USER>/Development/_tools/lib
    #
    createFolder(dstLibFolder)
    ##1. Initialize Environment
    #
    ##      * Create .env file when environment file is not found, ~/<USER>/Development/_tools/.env
    #
    src_folder = srcFolder
    dst_folder = dstFolder
    DevEnv(folder=dst_folder, filename=env_file).open()
    file_env = '        - {}'.format(env_file)

    #
    ##1. Install Bash Scripts
    #
    ##      * Copy Tool Scripts to when "_tools/" exists
    #
    src_folder = srcFolder
    dst_folder = dstFolder
    fileNames = getFileList(src_folder, ext='sh') # list of .sh files
    fileNames = [fn for fn in fileNames if fn != 'install.sh']
    tool_sh = ''
    for fn in fileNames:
        srcFn = fn
        dstFn = fn
        tool_sh += '        - {}\n'.format(fn)

        TextFileHelper(src_folder, srcFn) \
            .copyTo(dst_folder, dstFn)
    #
    ##      * Copy Project Scripts when "_tool/scripts" exists
    #
    src_folder = '{}/scripts'.format(srcFolder)
    dst_folder = '{}/scripts'.format(dstFolder)
    fileNames = getFileList(src_folder, ext='sh')
    script_sh = ''
    for fn in fileNames:
        srcFn = fn
        dstFn = fn
        script_sh += '          - {}\n'.format(fn)

        TextFileHelper(src_folder, srcFn) \
            .copyTo(dst_folder, dstFn)
    #
    ##1. Install Python Scripts
    #
    #
    ##      * Copy Python lib Scripts when "_tools/lib" folder exists
    #
    src_folder = '{}/lib'.format(srcFolder)
    dst_folder = '{}/lib'.format(dstFolder)
    fileNames = getFileList(src_folder, ext='py')
    lib_py=''
    for fn in fileNames:
        srcFn = fn
        dstFn = fn

        lib_py += '          - {}\n'.format(fn)
        #print('* copy {} to _tools/lib/{}'.format(srcFn, dstFn))

        TextFileHelper(src_folder, srcFn) \
            .copyTo(dst_folder, dstFn)


    print(DocFolders(dstFolder, title='Installation').toMarkdown())
    print('dstFolder',dstFolder)
if __name__ == "__main__":
    # execute as script
    main()