from collections import Counter

#string 1 = text (T)
#string 2 = pattern (P)
def countPermStr(string1, string2):
    # check if either string is none
    if not string1 or not string2:
        raise ValueError
    #check if string 2 is longer than string 1
    if len(string2) > len(string1):
        raise ValueError
    
    out = 0
    p_counter = Counter(string2)
    m = len(string2)
    n = len(string1)
    check_counter = Counter(string1[:m])

    if p_counter == check_counter:
        out += 1

    for i in range(m, n):
        check_counter[string1[i]] += 1
        check_counter[string1[i-m]] -= 1
        if check_counter[string1[i-m]] == 0:
            del check_counter[string1[i-m]]
        
        if check_counter == p_counter:
            out += 1

    return out

print(countPermStr("cbacab", "ab"))