import sys

def winnow(windowSize, hashes):
    """
    Obtains fingerprints from the list 'hashes' using windows of size 'windowSize'.
    'hashes' should be a list of tuples in the format (index, hash)
    Returns the fingerprints in a list of tuples of the format (index, hash)
    """

    window = []
    # initialize window buffer
    for i in range(0, windowSize):
        window.append((i, sys.maxsize))
    
    right = 0 # window's rightmost index
    minHash = 0 # index of the minimum hash

    fingerPrints = []

    # iterate over all hash values in 'hashes'
    for i in range(0, len(hashes)):
        
        right = (right + 1) % windowSize # shift window
        window[right] = hashes[i] # add new hash to window

        # min hash is already at rightmost index, need to find new min hash
        if minHash == right:
            # iterate through window to find index of rightmost minimum hash
            # this iteration looks weird because we're iterating through a circular buffer
            j = (right - 1) % windowSize
            while j != right:
                if window[j][1] < window[minHash][1]:
                    minHash = j
                j = (j - 1 + windowSize) % windowSize
            # fingerprint the min hash
            fingerPrints.append(window[minHash])
        # otherwise, check if newest hash is less than previous min hash
        else:
            if window[right][1] <= window[minHash][1]:
                # newest hash is new min, fingerprint it
                minHash = right
                fingerPrints.append(window[minHash])

    return fingerPrints