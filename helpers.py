
def filemap(fname, func: callable=str, sep='\n'):
    with open(fname, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))

