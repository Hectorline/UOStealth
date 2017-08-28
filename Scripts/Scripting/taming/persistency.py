__author__ = 'Will'
import pickle


def load_ignore_list():
    try:
        ignore_file = open("scripts\\ignore.txt", 'r')
        ignore_set = pickle.load(ignore_file)
        ignore_file.close()
        return ignore_set
    except Exception, e:
        return set()


def load_spots_list():
    try:
        spots_file = open("scripts\\spots.txt", 'r')
        spots_list = pickle.load(spots_file)
        spots_file.close()
        return spots_list
    except Exception, e:
        print e
        return []


def save_spots(spots_list):
    spots_file = open("scripts\\spots.txt", 'w')
    pickle.dump(spots_list, spots_file)
    spots_file.close()


def add_ignore(obj, ignore_set):
    print "ignoring {0}".format(obj)
    ignore_file = open("scripts\\ignore.txt", 'w')
    if len(ignore_set) == 0:
        for item in obj:
            ignore_set.add(item)
    else:
        ignore_set.add(obj)
    #print ignore_set
    pickle.dump(ignore_set, ignore_file)
    ignore_file.close()
