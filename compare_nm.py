# =============================================================================
# >> IMPORTS
# =============================================================================
import argparse
import sys


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_symbols(file_path, filter_name=None):
    """Return a set that contains symbols parsed from the given file that was
    created by using the 'nm' command.

    @param <file_path>:
    A string that defines the path of the file that contains the symbols.

    @param <filter_name>:
    A case-insensitive string that will be used to filter the result. If None,
    no filtering will be done.
    """
    symbols = set()
    with open(file_path) as f:
        for line in f:
            symbol = line.rstrip().split(None, 2)[-1]
            if (filter_name is not None
                    and filter_name.lower() not in symbol.lower()):
                continue

            symbols.add(symbol)

    return symbols

def compare(old_file, new_file, filter_name=None):
    """Compare two files which contain symbols and return a tuple that
    contains two list (added symbols and removed symbols).

    See get_symbols() for more information about the parameters.
    """
    old_symbols = get_symbols(old_file, filter_name)
    new_symbols = get_symbols(new_file, filter_name)

    return(sorted(old_symbols.difference(new_symbols)),
        sorted(new_symbols.difference(old_symbols)))

def print_compare(old_file, new_file, filter_name=None):
    """Same as compare(), but prints the difference."""
    added, removed = compare(old_file, new_file, filter_name)

    print 'Removed symbols:'
    for symbol in removed:
        print '\t', symbol

    print '\n' * 3

    print 'Added symbols:'
    for symbol in added:
        print '\t', symbol


# =============================================================================
# >> MAIN ROUTINE
# =============================================================================
def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('old_file')
    parser.add_argument('new_file')
    parser.add_argument('--filter')
    args = parser.parse_args(argv[1:])
    print_compare(args.old_file, args.new_file, args.filter)

if __name__ == '__main__':
    main(sys.argv)