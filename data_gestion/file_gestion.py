# -*- coding: utf-8 -*-
import sys


def read_file(filename):
    """
    Reads the file and returns data content
    :param filename: absolute or relative path to the file
    :return:
    """

    # Opening file
    fp = open(filename, "r")

    file_error_message = "ERROR: Wrong file format"
    # Candidates related data
    try:
        nb_candidates = int(fp.readline())
    except:
        sys.exit(file_error_message)
    # Map of candidates
    try:
        candidates = {}
        for _ in range(nb_candidates):
            line = fp.readline().split(",")
            candidates[int(line[0].strip())] = line[1].strip()
    except:
        sys.exit(file_error_message)

    # Number of voters, Sum of Vote Count, Number of Unique Orders
    try:
        nb_voters, sum_vote_count, nb_unique_orders = [int(i.strip()) for i in fp.readline().split(",")]
    except:
        sys.exit(file_error_message)

    # Lists of preferences
    try:
        prefs = []
        total_count = 0
        for _ in range(nb_unique_orders):
            line = [i.strip() for i in fp.readline().split(",")]
            count = int(line[0])
            total_count += count
            pref = line[1:]

            # temp is the preference for a set of people :
            # the number of people having this preference, a strict order of preferences
            # If indifferent between candidates, a list of them is in the list of preferences
            temp = (count, [])
            i = 0
            while i < len(pref):
                p = pref[i]
                if p[0] != '{':
                    temp[1].append(int(p))
                else:
                    indiff = []
                    p = p[1:]
                    while p[-1] != '}':
                        indiff.append(int(p))
                        i += 1
                        p = pref[i]
                    indiff.append(int(p[:-1]))
                    temp[1].append(indiff)
                i += 1

            prefs.append(temp)
    except:
        sys.exit(file_error_message)

    test = fp.readline()
    if test:
        sys.exit(file_error_message)

    if total_count != sum_vote_count:
        sys.exit("ERROR: Vote numbers don't match")

    # Closing file
    fp.close()

    return candidates, prefs


if __name__ == '__main__':
    filename = sys.argv[1]
    candidates, prefs = read_file(filename)
    print(candidates)
    print(prefs)