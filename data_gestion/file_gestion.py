#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import join
from sage.all import Set


def read_pref_approval(count, pref):
    """
    Reads the line and returns the preferences
    :param count: number of voters having this preference
    :param pref: list of candidates voters approve or not
    :type count: int
    :type pref: str
    :return: preference formated to fit to our needs
    :rtype: list
    """
    # temp is the preference for a set of people :
    # the number of people having this preference, a strict order of preferences
    # If indifferent between candidates, a Set (from sagemath) of them is added to the list of preferences
    temp = [count, []]
    pref = [i.strip() for i in pref.split(",")]
    i = 0
    while i < len(pref):
        p = pref[i]
        if p[0] != '{' or i == 0:
            p = p.strip('{}')
            if len(p) > 0:
                temp[1].append(int(p))
        else:
            indiff = []
            p = p[1:]
            while p[-1] != '}':
                indiff.append(int(p))
                i += 1
                p = pref[i]
            p = p.strip('{}')
            if p:
                indiff.append(int(p))
            temp[1].append(Set(indiff))
        i += 1
    return [temp]


def read_strict_pref(count, pref):
    """
    Reads the line and returns the preferences
    :param count: number of voters having this preference
    :param pref: ranking of candidates for these voters
    :type count: int
    :type pref: str
    :return: preference formated to fit to our needs
    :rtype: list
    """
    # temp is the preference for a set of people :
    # the number of people having this preference, a strict order of preferences
    # If indifferent between candidates, a Set (from sagemath) of them is added to the list of preferences
    if '{' in pref:
        approved = list(map(int, pref[:pref.index("{")].rstrip(",").split(",")))
        disapproved = list(map(int, pref[pref.index("{") + 1:pref.index("}")].split(",")))
    else:
        approved = list(map(int, pref.split(",")))
        disapproved = []
    res = []

    for i in range(len(approved)):
        temp = [count, approved[:i+1] + [Set(approved[i+1:] + disapproved)]]
        res.append(temp)

    return res


def read_file(filename, strict=False):
    """
    Reads the file and returns data content
    :param filename: absolute or relative path to the file
    :param strict: True if the file depicts strict preferences, False otherwise
    :type filename: str
    :raise ValueError: if file doesn't exist or wrong file format
    :return: map with all data from the file
    """

    # Opening file
    try:
        fp = open(filename, "r")
    except:
        raise ValueError("ERROR: File doesn't exist")

    file_error_message = "ERROR: Wrong file format"
    # Candidates related data
    try:
        nb_candidates = int(fp.readline())
    except:
        raise ValueError(file_error_message)
    # Map of candidates
    try:
        candidates = {}
        for _ in range(nb_candidates):
            line = fp.readline().split(",")
            candidates[int(line[0].strip())] = line[1].strip()
    except:
        raise ValueError(file_error_message)

    # Number of voters, Sum of Vote Count, Number of Unique Orders
    try:
        nb_voters, sum_vote_count, nb_unique_orders = [int(i.strip()) for i in fp.readline().split(",")]
    except:
        raise ValueError(file_error_message)

    # Lists of preferences
    # try:
    prefs = []
    total_count = 0
    for _ in range(nb_unique_orders):
        line = fp.readline()
        count = int(line[:line.index(",")])
        total_count += count
        pref = line[line.index(",") + 1:]
        if strict:
            temp = read_strict_pref(count, pref)
        else:
            temp = read_pref_approval(count, pref)
        prefs.extend(temp)
    # except:
    #     raise ValueError(file_error_message)

    test = fp.readline()
    if test:
        sys.exit(file_error_message)

    if total_count != sum_vote_count:
        sys.exit("ERROR: Vote numbers don't match")

    # Closing file
    fp.close()

    # Just making sure the preferences are sorted by decreasing order of number of voters
    prefs.sort(key=lambda x: x[0], reverse=True)

    return {"nb_candidates": nb_candidates,
            "candidates": candidates,
            "nb_voters": nb_voters,
            "sum_vote_count": sum_vote_count,
            "nb_unique_orders": nb_unique_orders,
            "preferences": prefs}


def read_directory(dirname):
    """
    Reads the files in the directory and returns concatenation of the data contents
    :param dirname: absolute or relative path to the directory
    :type dirname: str
    :raise ValueError: if wrong directory, empty directory, or wrong file format
    :return: map with all data from the files
    """
    try:
        files = [join(dirname, i) for i in listdir(dirname) if i[-4:] == ".toc"]
    except:
        raise ValueError("No such directory")
    if not files:
        raise ValueError("No .toc files detected")

    structure = read_file(files[0])

    unique_orders = [pref[1] for pref in structure["preferences"]]

    for f in files[1:]:
        temp_struct = read_file(f)
        structure["nb_voters"] += temp_struct["nb_voters"]
        structure["sum_vote_count"] += temp_struct["sum_vote_count"]
        for pref in temp_struct["preferences"]:
            if pref[1] in unique_orders:
                i = unique_orders.index(pref[1])
                structure["preferences"][i][0] += pref[0]
            else:
                structure["preferences"].append(pref)
                structure["nb_unique_orders"] += 1
                unique_orders.append(pref[1])

    structure["preferences"].sort(key=lambda x: x[0], reverse=True)
    return structure


def remove_unwanted_candidates_from_structure_and_preferences(structure, unwanted_candidates):
    """
    Removes unwanted candidates from the structure, including in the preferences
    :param structure: structure we want to remove the candidates from
    :param unwanted_candidates: list of IDs of unwanted candidates
    :type unwanted_candidates: list
    :return: the new structure without the unwanted candidates
    """
    new_structure = {"nb_candidates": structure["nb_candidates"] - len(unwanted_candidates), "candidates": {},
                     "nb_voters": structure["nb_voters"], "sum_vote_count": structure["sum_vote_count"],
                     "preferences": []}

    # Modifying the candidates set and creating a conversion table to make the preferences transformation easier
    i = 1
    conversion_table = {}
    for candidate in structure["candidates"].keys():
        if candidate not in unwanted_candidates:
            new_structure["candidates"][i] = structure["candidates"][candidate]
            conversion_table[candidate] = i
            i += 1

    # Adding preferences after deleting unwanted_candidates
    unique_orders = []
    for nb_votes, pref in structure["preferences"]:
        # cleaning the list of preferences from its unwanted candidates
        temp = [conversion_table[i] for i in pref if i not in unwanted_candidates and isinstance(i, int)]
        if not isinstance(pref[-1], int):
            temp.append(Set([conversion_table[i] for i in pref[-1] if i not in unwanted_candidates]))
        # adding of the list of preferences to the structure
        if temp in unique_orders:
            new_structure["preferences"][unique_orders.index(temp)][0] += nb_votes
        else:
            new_structure["preferences"].append([nb_votes, temp])
            unique_orders.append(temp)

    new_structure["nb_unique_orders"] = len(unique_orders)

    return new_structure


def remove_unwanted_candidates(structure, unwanted_candidates):
    """
    Removes unwanted candidates from the structure
    :param structure: structure we want to remove the candidates from
    :param unwanted_candidates: list of IDs of unwanted candidates
    :type unwanted_candidates: list
    :return: the new structure without the unwanted candidates
    """
    new_structure = {"nb_candidates": structure["nb_candidates"] - len(unwanted_candidates), "candidates": {},
                     "nb_voters": structure["nb_voters"], "sum_vote_count": structure["sum_vote_count"],
                     "preferences": []}

    # Modifying the candidates set and creating a conversion table to make the preferences transformation easier
    i = 1
    conversion_table = {}
    for candidate in structure["candidates"].keys():
        if candidate not in unwanted_candidates:
            new_structure["candidates"][i] = structure["candidates"][candidate]
            conversion_table[candidate] = i
            i += 1

    # Adding preferences after deleting unwanted_candidates
    unique_orders = []
    for nb_votes, pref in structure["preferences"]:
        # cleaning the list of preferences from its unwanted candidates
        temp = [conversion_table[i] for i in pref if i not in unwanted_candidates and isinstance(i, int)]
        if not isinstance(pref[-1], int):
            temp.append(Set([conversion_table[i] for i in pref[-1] if i not in unwanted_candidates]))
        # adding of the list of preferences to the structure
        if temp in unique_orders:
            new_structure["preferences"][unique_orders.index(temp)][0] += nb_votes
        else:
            new_structure["preferences"].append([nb_votes, temp])
            unique_orders.append(temp)

    new_structure["nb_unique_orders"] = len(unique_orders)

    return new_structure


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("This program takes one and only one argument")
    f = sys.argv[1]
    structure = read_file(f, strict=True)
    for c in structure["candidates"].items():
        print(c)
    for j in structure["preferences"]:
        print(j)
