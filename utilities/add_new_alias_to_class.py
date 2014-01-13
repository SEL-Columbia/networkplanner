import sys, os
import csv, re

# Prevents this script from failing when output is piped
# to another process
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

if __name__ == '__main__':

    if (len(sys.argv) < 2):
        sys.stderr.write("example usage:  python add_new_alias_to_class.py class_alias_file\n")
        sys.exit()

    # setup model
    class_alias_file = sys.argv[1]

    csv_file = open(class_alias_file, 'r')
    csv_reader = csv.DictReader(csv_file)

    # Iterate over all csv rows, prepending short_section+"_"+short_option
    # to the list of aliases
    for row in csv_reader:
        
        clazz = row['class'].rpartition(".")[-1]
        short_section = row['short_section']
        short_option = row['short_option']
        added_alias = short_section + "_" + short_option
        class_file_name = row['file']
        # tmp_class_file = class_file.replace(".py", ".py_tmp")

        data = []
        with open(class_file_name, 'r') as class_file:
            # read a list of lines into data
            data = class_file.readlines()
            class_file.close()
            
        cur_line = 0
        while (cur_line < len(data) and (not re.search("^class[ ]+" + clazz, data[cur_line]))):
            cur_line += 1
            
        print "Found class %s at line %s:  %s" % (clazz, cur_line, data[cur_line])

        # presumably we've found the line starting the class def
        while (cur_line < len(data) and (not re.search("aliases[ ]*=", data[cur_line]))):
            cur_line += 1

        print "Found alias %s at line %s:  %s" % (clazz, cur_line, data[cur_line])

        if cur_line >= len(data):
            print "No alias found for class %s" % clazz
            continue

        # now we've found the alias line
        # replace the alias def with one that prepends short_section_short_option
        cur_alias_def = data[cur_line]

        p = re.compile(r"\[([^\]]*)]")

        new_alias_def = p.sub("['" + added_alias + "', \\1]", cur_alias_def)
        data[cur_line] = new_alias_def


        # and write everything back
        with open(class_file_name, 'w') as new_class_file:
            new_class_file.writelines( data )
            new_class_file.close()

