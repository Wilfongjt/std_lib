import os
from pprint import pprint

class DocComments(list):
    ## Given a folder and filename, Open and read the comment line in the file.
    def __init__(self, folder, filename):

        self.folder = folder
        self.filename = filename

        ## Open and Load a given file on request.
        print('folder', self.folder)
        print('filename', self.filename)
        with open('{}/{}'.format(self.folder, self.filename)) as f:

            lines = f.read()
            lines = lines.split('\n')

            for ln in lines:
                ln = ln.strip()
                if ln.startswith('class'):
                    ##* process line when line starts with "class"
                    self.append('## {}'.format(ln.replace(':','')))
                else:
                    if ln.startswith('##'):
                        ##* process line when line is double comment... eg "##"
                        self.append(ln)
    #
    ## Convert comments to markdown on request
    #
    def toMarkdown(self):
        markdown = []
        for ln in self:
            if '1.' in ln:
                ##* markdown is bold when "1. " is found

                ln = ln.replace('1. ','1. __')
                ln = '{}__'.format(ln)

            if ' on request' in ln:
                ##* markdown is bold when "on request" is found
                if markdown[len(markdown)-1].startswith('*'):
                    markdown.append(' ')
                markdown.append('__{}__ '.format(ln[2:]))
                #markdown.append('__{}__ '.format(ln[2:].strip()))
                #markdown.append('__{}__ '.format(ln.replace('##','').strip()))
                markdown.append(' ')
            elif ' when ' in ln:
                ##* markdown is list item when "when" is found
                markdown.append('{}'.format(ln[2:]))
                #                markdown.append('{}'.format(ln.replace('##','')))

            elif ln.startswith('## class'):
                ##* markdown is H1 when "# class" is found
                markdown.append('# {}'.format(ln[2:]))
                # markdown.append('# {}'.format(ln.replace('##','')))
                markdown.append(' ')
            else:
                ##* markdown is normal when line is # unknown
                markdown.append('{}'.format(ln.replace('##','')))
                #markdown.append('{}'.format(ln.replace('##','').strip()))

                markdown.append(' ')
        return '\n'.join(markdown)

def main():
    actual = DocComments(os.getcwd(), 'doc_comments.py')
    pprint(actual)
    assert (actual)
    print(actual.toMarkdown())

if __name__ == "__main__":
    # execute as script
    main()
