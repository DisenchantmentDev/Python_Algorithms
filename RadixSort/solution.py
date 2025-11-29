import math


def radix_base(values_to_sort, base):

    def _digitSort(pos):
        n = len(values_to_sort)
        # output array; we're just resorting the original list so same length
        out = [0] * n
        # counts how many of each digit in specified place exist
        count = [0] * base

        # loop over each element: look at specified place and count it
        for i in values_to_sort:
            if i < 0:
                raise ValueError("invalid list element")
            digit = (i // (base ** pos)) % base
            count[digit] += 1

        # convert counts to positions
        # add previous count to current such that each has unique starting index
        for i in range(1, base):
            count[i] += count[i - 1]

        # actually sort based on digit; go backwards for stability
        for i in range(n - 1, -1, -1):
            digit = (values_to_sort[i] // (base ** pos)) % base
            out[count[digit] - 1] = values_to_sort[i]
            count[digit] -= 1

        return out

    # check for empty or None list
    if not values_to_sort or values_to_sort is None:
        raise ValueError("invalid arguments")

    # count digits in longest number; that's how many times we do sorts
    max_digits = int(math.log(max(values_to_sort), base)) + 1

    for position in range(max_digits):
        values_to_sort = _digitSort(position)

    return values_to_sort
