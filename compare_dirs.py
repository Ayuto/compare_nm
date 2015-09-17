# =============================================================================
# >> IMPORTS
# =============================================================================
import argparse
import sys
import compare_nm

from path import Path


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def compare_dirs(old_dir, new_dir, output_dir, filter_name=None):
    old_dir = Path(old_dir)
    new_dir = Path(new_dir)
    output_dir = Path(output_dir)

    if not output_dir.exists():
        output_dir.mkdir()

    old_files = set(path.namebase for path in old_dir.files())
    new_files = set(path.namebase for path in new_dir.files())

    removed_files = old_files.difference(new_files)
    added_files = new_files.difference(old_files)
    shared_files = old_files.intersection(new_files)

    print 'Removed files:'
    for file_name in sorted(removed_files):
        print '\t', file_name

    print '\n' * 3

    print 'Added files:'
    for file_name in sorted(added_files):
        print '\t', file_name

    print '\n' * 3

    print 'Shared files:'
    for file_name in sorted(shared_files):
        print '\t', file_name
        added, removed = compare_nm.compare(
            old_dir / file_name + '.txt',
            new_dir / file_name + '.txt',
            filter_name
        )

        with open(output_dir / file_name + '.difference.txt', 'w') as f:
            f.write('Removed symbols:\n')
            for symbol in removed:
                f.write('\t{0}\n'.format(symbol))

            f.write('\n' * 3)

            f.write('Added symbols:\n')
            for symbol in added:
                f.write('\t{0}\n'.format(symbol))


# =============================================================================
# >> MAIN ROUTINE
# =============================================================================
def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('old_dir')
    parser.add_argument('new_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--filter')
    args = parser.parse_args(argv[1:])
    compare_dirs(args.old_dir, args.new_dir, args.output_dir, args.filter)

if __name__ == '__main__':
    main(sys.argv)