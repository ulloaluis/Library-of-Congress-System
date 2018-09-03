#!/usr/bin/env python3

import random as r


class LC:
    """Library of Congress System for sorting books.

    This class represents a call ID for a book sorted under the Library of
    Congress System.

    Intended Usage (testing): Practice sorting multiple ID's based on the LC system.

    interactive_testing(list of id lists (each id list represents a level))
    -runs terminal-based test that allows you to practice sorting with respect
    the LC system
    -arguments passed can be either a list of LC lists, or a list of id string lists

    Notes:
    1. Class numbers do not begin with O, I, W, X, Y. The letter O is removes since
    it conflicts with another naming standard. I, W, X, Y are removed since they
    are not necessary for my purposes, though you may want to add these back in.

    2. String representations have a chance of being printed without a '.' separating
    cutter numbers. This is to help practice with book tags that may be formatted that way.

    Randomly Generated class numbers:
    3. The number of cutters, number of letters and size of whole number in class number,
    and related factors are all chosen randomly. See the class constants for percentages.

    Specified class numbers:
    4. format: LC('XXX0000.frac.cutter.cutter ...')
    -Could exclude class num fraction, variable amount of cutters, etc
    -Required:
        Class Number:
            -Must always have a class number
            -Starts with at least one letter (capital)
            -Has a whole number immediately after (fraction (.2, .131231, etc.) optional)
        Cutters (if used, must be formatted this way):
            -First character is a '.'
            -Second character is a letter
            -Rest must be some whole number (but by the LC system, this number is read as a decimal)
    Examples: LC('A4.23.B9.C13'), LC('A4'), LC('C3.2'), LC(A1.B235)
    """

    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    class_alpha_start = 'ABCDEFGHJKLMNPQRSTUVZ'  # removed: O, I, W, X, Y
    class_num_of_letter_groups = [1] * 20 + [2] * 10 + [3] * 2  # 62% 32% 6%
    class_whole_length = [1] * 20 + [2] * 10 + [3] * 5 + [4]

    num_of_cutters = [1] * 20 + [2] * 5 + [3] * 5  # 66% 17% 17%

    string_rep = [1] * 20 + [0] * 10

    def __init__(self, id=None):
        self._tracker = None  # will use to see how list has been moved around

        if not id:
            self._class_num_parts = self._rand_class_num()
            self._cutter_nums = self._rand_cutter_nums()

            self.class_num = ''.join(self._class_num_parts)
            self.cutter_nums = '.' + '.'.join(self._cutter_nums)

            self.id = self.class_num + self.cutter_nums

        else:  # parse the passed id
            self._class_num_parts = self._parse_class_num(id)
            self._cutter_nums = self._parse_cutter_nums(id)

            self.class_num = ''.join(self._class_num_parts)
            self.cutter_nums = '.' + '.'.join(self._cutter_nums)

            self.id = id

    def _parse_class_num(self, id):
        """Parses the class number in id.

        Returns same list that is returned when a class number is
        randomly created; contains letters, num, and optional frac.
        """
        res = []
        class_num = id.split('.')
        part_1 = class_num[0]
        for i, ch in enumerate(part_1):
            if ch.isdigit():  # start of digit portion of class_num
                res.append(part_1[:i])  # letters
                res.append(part_1[i:])  # digits
                break

        if len(class_num) > 1 and class_num[1][0].isdigit():  # part of class num (frac)
            res.append('.' + class_num[1])  # frac

        return res

    def _parse_cutter_nums(self, id):
        """Parses the cutter numbers in idself.

        Returns same list that is returned when cutter numbers are
        randomly created; contains cutter_nums without the '.'.
        """
        cutters = id.split('.')
        if len(cutters) > 1 and cutters[1][0].isdigit():  # frac part of class_num, remove
            cutters = cutters[1:]  # remove class_num
        return cutters[1:]  # removes fraction (if statement ran) or class_num

    def _rand_class_num(self):
        """Randomly creates the components for a class number.

        A class number begins with a one, two, or three-letter
        group, though 3 is extremely rare. This letter group is
        followed by a one, two, three, or four place whole number
        which may or may not have an attached decimal fractional part.
        """
        res = []
        letters = ''
        num_groups = r.choice(self.class_num_of_letter_groups)
        for i in range(num_groups):
            if i == 0:
                letters += r.choice(self.class_alpha_start)
            else:
                letters += r.choice(self.alpha)
        res.append(letters)

        whole_num_size = r.choice(self.class_whole_length)
        num = str(r.randint((whole_num_size - 1) * 10, whole_num_size * 10 - 1))
        res.append(num)

        if r.choice([True, False]):
            frac = '%.2f' % r.random()  # 0.0 - 1.0
            res.append(frac)

        return res

    def _rand_cutter_nums(self):
        """Randomly creates cutter numbers.

        A cutter number is an alphanumerical sequence. The numbers
        in the cutter are always decimal numbers.
        """
        num_cutters = r.choice(self.num_of_cutters)
        cutters = []
        for _ in range(num_cutters):
            cutter = r.choice(self.alpha)
            cutter += str(r.randint(1, 99))  # int represents decimal fraction
            cutters.append(cutter)

        return cutters

    def _parse_id(self, lcid):
        """Returns a dict with valuable data about id.

        Largest Possible Format: XXX0000.00.X00.X00.X00 ... (X alpha, 0 num)
        """
        res = {'class_num': {}, 'cutter_nums': {}}
        class_num_parts = lcid._class_num_parts  # letters, num, ~frac
        res['class_num']['letter-length'] = len(class_num_parts)
        res['class_num']['letters'] = class_num_parts[0]
        res['class_num']['num'] = class_num_parts[1]
        if len(class_num_parts) > 2:
            res['class_num']['frac'] = class_num_parts[2][1:]  # remove '.'

        cutter_nums = lcid._cutter_nums
        res['cutter_nums']['len'] = len(cutter_nums)
        for i, cutter_num in enumerate(cutter_nums):
            res['cutter_nums'][i] = {}
            res['cutter_nums'][i]['letter'] = cutter_num[0]
            res['cutter_nums'][i]['decimal'] = cutter_num[1:]

        return res

    def _enforce_frac(self, frac):
        """If frac was .3 or .4, will be compared as 30 or 40.
        Precondition: frac is either 1 or 2 digits long
        """
        return int(frac) / (pow(10, len(str(frac))))

    def __eq__(self, other):
        return self.id == other.id

    def _cutter_logic(self, my_comp, other_comp):
        for i in range(max(my_comp['cutter_nums']['len'], other_comp['cutter_nums']['len'])):
            my_cutter = my_comp['cutter_nums'].get(i)
            ot_cutter = other_comp['cutter_nums'].get(i)
            if (my_cutter is None and ot_cutter is None) or (my_cutter is None):
                return True
            elif ot_cutter is None:
                return False
            else:
                # compare letter then decimal
                if my_cutter['letter'] == ot_cutter['letter']:
                    # all cutters are decimals, enforce 00 like with fractions
                    # want .5 to be 50 not 5
                    my_dec = self._enforce_frac(my_cutter['decimal'])
                    ot_dec = self._enforce_frac(ot_cutter['decimal'])

                    if my_dec == ot_dec:
                        continue
                    else:
                        return my_dec < ot_dec  # .3594 < .36
                else:
                    return my_cutter['letter'] < ot_cutter['letter']
        return False  # finished for loop, all was equal, not less than

    def __lt__(self, other):
        """Define how to sort one id versus another.

        Start lexicographically. If num of letters for one is smaller than
        the other, then the smaller one goes first. If alphabetically the same,
        start looking at numbers as a whole. It's 3am, this code is prob spaghetti.
        """
        my_comp = self._parse_id(self)
        other_comp = self._parse_id(other)

        my_letters, other_letters = my_comp['class_num']['letters'], other_comp['class_num']['letters']
        if my_letters == other_letters:
            my_class_num, ot_class_num = int(my_comp['class_num']['num']), int(other_comp['class_num']['num'])
            if my_class_num == ot_class_num:
                if 'frac' in my_comp['class_num'] and 'frac' in other_comp['class_num']:  # both have fractions
                    # enforce fractions to 2 decimals (format 00 so .5 is 50 not 5)
                    my_frac = self._enforce_frac(my_comp['class_num']['frac'])
                    ot_frac = self._enforce_frac(other_comp['class_num']['frac'])
                    if my_frac == ot_frac:
                        return self._cutter_logic(my_comp, other_comp)
                    else:
                        return my_frac < ot_frac  # .3594 < .36
                elif 'frac' not in my_comp['class_num'] and 'frac' not in other_comp['class_num']:  # both not fractions
                    return self._cutter_logic(my_comp, other_comp)
                else:  # in one or the other
                    return True if 'frac' in other_comp['class_num'] else False
            else:
                return my_class_num < ot_class_num  # not equal, compare class nums

        else:
            return my_letters < other_letters  # not equal, compare letters lexicographically

    def __repr__(self):
        """Alternate print form that shows class type, lists print with this."""
        return str(self)

    def __str__(self):
        """Alternates between with '.' and without. """
        if r.choice(self.string_rep):  # 66% chance to print with '.'
            return self.id
        else:  # 33% chance to print without '.'
            # class number fraction stays
            i = self.id.find('.')  # first occurrence of '.' = maybe fraction
            if self.id[i + 1].isdigit():  # is fraction
                return self.id[:i + 1] + self.id[i + 1:].replace('.', '')
            # not a fraction, starts with char, is cutter
            return self.id.replace('.', '')


def sort_and_display(ids, num_ids):
    fixed = sorted(ids)
    print(fixed)
    print(''.join([str(lc.tracker) + '->' for lc in fixed])[:-2])
    print('-' * num_ids + '-' * 2 * (num_ids - 1))


def test_1():
    """See two ID's being compared"""
    x = LC()
    y = LC()
    print(str(x) + '  versus  ' + str(y))
    print(str(x) + ' < ' + str(y) + '  ?  ')
    print(str(x < y))


def test_2():
    """Generate a list of id's and watch them be sorted"""
    num_ids = 5
    ids = []
    for i in range(num_ids):
        x = LC()
        x.tracker = i + 1  # no 0 based indexing
        ids.append(x)
    print(ids)

    sort_and_display(ids, num_ids)


def test_3(*args):
    """Test pre-written ids."""
    num_ids = len(args)
    ids = []
    for i, id in enumerate(args):
        id.tracker = i + 1
        ids.append(id)
    print(ids)
    sort_and_display(ids, num_ids)


def interactive_testing(*args):
    """args represents lists of lists of ids, each used for a test.

    User can enter a list of LCs or a list of their internal ids.
    """
    print("There are %d tests." % len(args))
    print("I will display X amount of IDs. Consider the IDs to be labeled 1 to X in order of left to right.")
    print("Order the IDs based on the LC system.")
    print("Example input: 1->3->2 (in ascending order)\n")

    if isinstance(args[0][0], str):  # if strings were passed, turn into LCs
        args = [[LC(id) for id in test] for test in args]

    quit = False
    for i, test in enumerate(args):  # play each level logic
        num_ids = len(test)
        for j, id in enumerate(test):
            id.tracker = j + 1
        print("Here are some ids. There are %d to sort. Enter 'stop' at anytime to exit." % len(test))
        print(test)

        user = input('What is your answer (N->M->..->X) or stop? ')
        fixed = sorted(test)
        answer = ''.join([str(lc.tracker) + '->' for lc in fixed])[:-2]
        while True:  # user guess logic
            if user == 'stop':
                quit = True
                break

            if user == answer:
                print('You got it!')
                print(fixed)
                print(answer)
                print('-' * num_ids + '-' * 2 * (num_ids - 1))
                print()
                break
            else:
                user = input('Not quite! Remember N->M->..->X or stop. Try again: ')

        # end messages
        if quit:
            print('\nThanks for playing! Here are all the test answers:')
            for testA in args:
                for k, lc in enumerate(testA):
                    lc.tracker = k + 1
                print(testA)
                sort_and_display(testA, len(testA))
            break

        if i == len(args) - 1:
            print('Out of levels! Thanks for playing.')


if __name__ == '__main__':
    # print(LC('A123.B2.C399999') < LC('A123.B2.C4'))  # True
    # test_3(LC('PT87.13.G8'), LC('LD83.I8'), LC('LD83.H8'),
    #  LC('LD83.Z8'), LC('PT87.13.G81'), LC('PT87.13.G815'),
    #  LC('PT87.13.G82'), LC('Z853.2.G8'), LC('Z853.2.H3'),
    #  LC('Z853.2.H316'), LC('Z853.2.R2'))
    #
    # test_3(LC('Q1.S5'), LC('PB2.S5'), LC('PA298.S5'),
    #  LC('PA5.S5'), LC('P433.S5'))
    #
    # test_3(LC('H433.P29'),
    #  LC('H432.2.P29'), LC('H432.15.P29'), LC('H432.1.P29'),
    #  LC('H432.P29'))
    #
    # test_3(LC('H8192.A4'), LC('H820.A4'),
    #  LC('H82.1.A4'), LC('H82.A4'), LC('H9.A4'))
    #
    # interactive_testing([LC('Q1.S5'), LC('PB2.S5'), LC('PA298.S5'),
    # LC('PA5.S5'), LC('P433.S5')], [LC('H433.P29'),
    # LC('H432.2.P29'), LC('H432.15.P29'), LC('H432.1.P29'),
    # LC('H432.P29')], [LC('H8192.A4'), LC('H820.A4'),
    # LC('H82.1.A4'), LC('H82.A4'), LC('H9.A4')])

    interactive_testing(['JC29.B1', 'JC29.A1', 'JC29.B3', 'JC29.B25', 'JC29.B35942', 'JC29.B4'],
                        ['PR192.4.B3.N4', 'PR192.4.B3', 'PR192.4.B35', 'PR192.4.B4.S3', 'PR192.4.B4.R682',
                         'PR192.5.B5', 'PR192.4.B4.S3.M8', 'PR192.5.C1'])
