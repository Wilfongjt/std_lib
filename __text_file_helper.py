import os
import shutil
from _functions import file_exists

class TextFileHelper():
    def __init__(self, srcFolder, srcName):
        self.folder = srcFolder
        self.filename = srcName

    def exists(self):
        #print('folder', self.folder, '  filename', self.filename)
        return file_exists(self.folder, self.filename)

    def deleteWhenFound(self, delfolder=None, delfilename=None):
        folder = self.folder
        filename = self.filename
        if delfilename:
            filename = delfilename
        if delfolder:
            folder = delfolder

        # delete when exists
        if file_exists(folder, filename):
            os.remove("{}/{}".format(folder, filename))
        return self

    def copyTo(self, dstfolder, dstfilename):
        # fail when srcfolder and srcfilename equal dstfolder and dstfilename
        # copy source file when source file exists
        # remove destination file when destination file exists
        #
        if dstfolder == self.folder and dstfilename == self.filename:
            raise Exception('failed copy... source and destination are the same.')
        if file_exists(self.folder, self.filename):
            self.deleteWhenFound(dstfolder, dstfilename)
            shutil.copy2('{}/{}'.format(self.folder, self.filename),
                         '{}/{}'.format(dstfolder, dstfilename))
        return self

def main():
    from _functions import createFolder
    filename = 'README.md'
    srcfolder = os.getcwd()
    dstfolder = '{}/temp'.format(os.getcwd())

    createFolder(dstfolder)
    actual = TextFileHelper( srcfolder, filename)
    assert( actual )
    assert( actual.exists() )
    assert( actual.copyTo(dstfolder, filename) )
    assert( TextFileHelper( dstfolder, filename).exists() )
    assert( TextFileHelper( dstfolder, filename).deleteWhenFound() )
    assert( not TextFileHelper( dstfolder, filename).exists() )

if __name__ == "__main__":
    # execute as script
    main()

