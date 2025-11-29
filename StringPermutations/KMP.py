from collections import Counter

#string 2 is what we're looking for (P, pattern) (length m)
#string 1 is what we're looking in for string 2 (T, text) (length n)
def countPermStr(string1, string2) -> int:
    # check if either string is none
    if string1 is None or string2 is None:
        raise ValueError
    #check if string 2 is longer than string 1
    if len(string2) > len(string1):
        raise ValueError
    
    n = len(string1)
    m = len(string2)
    
    def _failureFunction() -> list:
        f = [0] * m #failure function array is length of pattern
        x = 1
        length = 0
        while x < m:
            if string2[x] == string2[length]:
                f[x] = j + 1
                x += 1
                length += 1
            elif length > 0:
                length = f[length - 1]
            else:
                f[x] = 0 #no match
                x += 1
        return f

    failure = _failureFunction()
    print(failure)
    i = 0
    j = 0
    result = 0

    while i < n:
        if string1[i] == string2[j]:
            if j == m - 1:
                result += 1
            else:
                i += 1
                j += 1
        else:
            if j > 0:
                j = failure[j - 1]
            else:
                i += 1
    return result

print(countPermStr("cbacab", "ab"))