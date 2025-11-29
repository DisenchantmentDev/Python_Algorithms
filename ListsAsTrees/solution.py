def findKey(k, t):
    #recursive helper function. Within findKey for scope
    def _recursiveFindKey(i):
        if i >= len(t) or t[i] is None:
            raise LookupError("not in tree")

        try:
            if t[i] == k:
                return i
            elif k< t[i]:
                return _recursiveFindKey((i*2) + 1)
            else:
                return _recursiveFindKey((i*2) + 2)
        except TypeError:
            raise Exception("tree error")

    if k is None:
        raise ValueError("null key")
    
    if t is None:
        raise ValueError("no tree")
    
    if not t:
        raise LookupError("not in tree")
    
    return _recursiveFindKey(0)

def addKey(k,t):
    def _recursiveAddKey(i):
        #if i is an index greater than what's allocated, expand with None
        #rather inefficient but in the immortal words of Michael Reeves:
        #"Python can do anything, just badly"
        while i >= len(t):
            t.append(None)

        #if the index we have found is None, insert there
        try:
            if out[i] is None:
                out[i] = k
                return
            elif out[i] == k:
                return
            elif k < out[i]:
                return _recursiveAddKey((i*2) + 1)
            else:
                return _recursiveAddKey((i*2) + 2)
        except TypeError:
            raise Exception("tree error")

    out = t.copy() #copy of t since modifying original tree causes issues

    if k is None:
        raise ValueError("null key")
    
    if t is None:
        raise ValueError("no tree")
    
    if not t:
        return [k]
    
    _recursiveAddKey(0)
    
    #clean the tree of None values
    while out and out[-1] is None:
        out.pop()
    
    return out
    
def deleteKey(k, t):
    #helper function to find min index of subtree starting at i
    #used later in deleteNode for handling deletion of node w/ two children
    def _minIndex(i): 
        while (i*2) + 1 < len(out) and out[(i*2) + 1] is not None:
            i = (i*2) + 1
        return i
    
    #you know the drill at this point
    def _recursiveDeleteNode(i):
        lc = (i*2) + 1
        rc = (i*2) + 2

        #check to see what our children are; make decisions based on that
        has_left = lc < len(out) and out[lc] is not None
        has_right = rc < len(out) and out[rc] is not None

        #no child? delete
        if not (has_left and has_right):
            out[i] = None
        #only left child? swap with left child and delete left
        elif has_left and not has_right:
            out[i] = out[lc]
            out[lc] = None
        #only right child? swap with right child and delete right
        elif has_right and not has_left:
            out[i] = out[rc]
            out[rc] = None
        else: #two children? recursively delete the min index of the right subtree
            min_index = _minIndex(rc)
            out[i] = out[min_index]
            _recursiveDeleteNode(min_index)

    out = t.copy()

    if k is None:
        raise ValueError("null key")
    
    if t is None:
        raise ValueError("no tree")
    
    #no tree, no key to delete
    if not t:
        raise LookupError("not in tree")

    #actually find the key first
    try:
        i = findKey(k, t)
    except LookupError:
        raise LookupError("not in tree")
    
    _recursiveDeleteNode(i)