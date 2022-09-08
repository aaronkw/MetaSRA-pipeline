from collections import Counter, defaultdict

def bag_dist_multiset_sav (str_a, str_b):
    count_a = Counter(str_a)
    count_b = Counter(str_b)

    a_minus_b = 0
    b_minus_a = 0
    for c in count_a:
        if c in count_b:
            if count_a[c] > count_b[c]:
                a_minus_b += count_a[c] - count_b[c]
        else:
            a_minus_b += count_a[c]

    for c in count_b:
        if c in count_a:
            if count_b[c] > count_a[c]:
                b_minus_a += count_b[c] - count_a[c]
        else:
            b_minus_a += count_b[c]

    if a_minus_b > b_minus_a:
        return a_minus_b
    else:
        return b_minus_a

def bag_dist_multiset (str_a, str_b):
    count = defaultdict(int)
    for s in str_a:
        count[s] += 1
    for s in str_b:
        count[s] -=1
    pos, neg = 0, 0
    for v in count.values():
        if v > 0:
           pos += v
        else:
           neg += v
    neg = -neg
    #tot = sum (count.values())
    #pos = sum ([c  for c in count.values() if c > 0])
    #neg = sum ([-c for c in count.values() if c < 0])
    #neg = pos - tot        # (-neg) + pos = total
    return pos if pos > neg else neg
        
        
