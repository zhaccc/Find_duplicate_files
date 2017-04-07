import os

def walk(dirname):
    """
    This function looks at directory content and
    makes a list out of files in that directory.
    """
    lst = []
    for root, dirs, files in os.walk(dirname):
        for name in files:
            path = os.path.join(root, name)
            
            lst.append(path)
            
    return lst
            
dirlist = walk('.')


def pipe(cmd):
    """
    Runs shell commands.
    """
    fp = os.popen(cmd)
    read_lines = fp.read()
    close_lines = fp.close()
    return read_lines, close_lines
    

def compute_checksum(file_list): 
    """
    Function has MD5sum command for creating checksum.
    I used some bash scripting to create a clean checksum
    without printing out the filename behind it.
    """
    cmd = "md5sum < " + file_list + "| awk '{print $1}'"
    return pipe(cmd)


def filter_search(sufix, dirlist):
    """
    Function makes a dictionary in which he adds a MD5 checksum
    on every file in that dirlist (files are filtered by their extension),
    than adds a checksum as a key and filename as a value.
    In case of the same checksum it adds aditional filename as value to 
    checksum key.
    """
    dictionary = {}
    for name in dirlist:
        if name.endswith(sufix):
            checksum = compute_checksum(name)
            
            if checksum in dictionary:
                dictionary[checksum].append(name)
            else:
                dictionary[checksum] = [name]
            
    return dictionary
            
checksum_files = filter_search('.txt', dirlist)

    
def print_duplicates(dictionary):
    """
    Function traverses the dictionary list and if there are more
    values than 1 in the dictionary under the same checksum key,
    it displays those files as duplicates.
    """
    for checksum, value in dictionary.iteritems():
        if len(value) > 1:
            print 'The following files have the same checksum:'
            for name in value:
                print name
                
if __name__ == '__main__':
    print_duplicates(checksum_files)
