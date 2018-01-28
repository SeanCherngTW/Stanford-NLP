import sys
import os
import re
import pprint

email_normal_pat = '(\w+\.?;?\w+) ?@ ?(\w+\.?;?\w+).(com|COM|edu|EDU)'
email_char_pat = '(\w+) ?@ ?(\w+) ?stanford edu'
email_char2_pat = '(\w+) WHERE stanford DOM edu'
email_script_pat = 'obfuscate\(\'(\w+).(com|COM|edu|EDU)\',\'(\w+)'
email_follow_pat = '(\w+\.?\w+) \(followed by \"@(\w+\.?\w+).(com|COM|edu|EDU)'

tel_1_pat = '\(\d{3}\) ?\d{3}-\d{4}'
tel_2_pat = '\d{3}-\d{3}-\d{4}'
tel_3_pat = '\+1 \d{3} \d{3}[- ]\d{4}'

"""
email_normal_pat:
account@stanford.edu
account @ stanford.edu
account.account@stanford.edu
account@cs.stanford.edu
account@stanford.EDU
"""

"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""


def email_str_preprocess(s):
    replace_at_pat = '(&#x40;?| at )'
    replace_dot_pat = '( do?t )'
    replace_quote_pat = '(&ldquo;|&rdquo;)'
    s = re.sub(replace_at_pat, '@', s)
    s = re.sub(replace_dot_pat, '.', s)
    s = re.sub(replace_quote_pat, '"', s)
    return s.replace('-', '').replace('&lt;', '<')


def process_email(name, f, res):
    for line in f:
        line = email_str_preprocess(line)
        email_normal = re.findall(email_normal_pat, line)
        email_script = re.findall(email_script_pat, line)
        email_follow = re.findall(email_follow_pat, line)
        email_char = re.findall(email_char_pat, line)
        email_char2 = re.findall(email_char2_pat, line)
        for e in email_normal:
            if e[0] == 'Server' or e[0] == 'Talk' or e[0] == 'funding':
                break
            email = '%s@%s.%s' % e
            res.append((name, 'e', email.lower().replace(';', '.')))
        for e in email_script:
            email = '%s@%s.%s' % (e[2], e[0], e[1])
            res.append((name, 'e', email.lower().replace(';', '.')))
        for e in email_follow:
            email = '%s@%s.%s' % e
            res.append((name, 'e', email.lower().replace(';', '.')))
        for e in email_char:
            email = '%s@%s.stanford.edu' % e
            res.append((name, 'e', email.lower()))
        for e in email_char2:
            email = '%s@stanford.edu' % e
            res.append((name, 'e', email.lower()))
    return res


def process_tel(name, f, res):
    for line in f:
        tel_1 = re.findall(tel_1_pat, line)
        tel_2 = re.findall(tel_2_pat, line)
        tel_3 = re.findall(tel_3_pat, line)
        for p in tel_1:
            s = p.replace(' ', '').split(')')
            left = s[0]
            right = s[1].split('-')

            final_tel = '%s-%s-%s' % (left[1:], right[0], right[1])
            res.append((name, 'p', final_tel))

        for p in tel_2:
            res.append((name, 'p', p))

        for p in tel_3:
            s = p.split(' ')
            if '-' not in p:
                final_tel = '%s-%s-%s' % (s[1], s[2], s[3])
            else:
                left = s[1]
                right = s[2]
                right = right.split('-')
                final_tel = '%s-%s-%s' % (left, right[0], right[1])
            res.append((name, 'p', final_tel))
    return res


def process_file(name, f1, f2):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    res = process_tel(name, f1, res)
    res = process_email(name, f2, res)
    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""


def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path, fname)
        f1 = open(path, 'r', encoding='ISO-8859-1')
        f2 = open(path, 'r', encoding='ISO-8859-1')
        f_guesses = process_file(fname, f1, f2)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""


def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path, 'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""


def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    # print 'Guesses (%d): ' % len(guess_set)
    # pp.pprint(guess_set)
    # print 'Gold (%d): ' % len(gold_set)
    # pp.pprint(gold_set)
    print('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print('Summary: tp=%d, fp=%d, fn=%d' % (len(tp), len(fp), len(fn)))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""


def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list = get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) == 1):
        main('../data/dev', '../data/devGOLD')
    elif (len(sys.argv) == 3):
        main(sys.argv[1], sys.argv[2])
    else:
        print('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
