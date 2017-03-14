import json
import click
import os

def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


with open('datapackage.json', 'r') as file:
    dp = json.load(file)


def gen_resource(directory_name, dataset_name):
    datafiles = [f for f in get_filepaths("./{}".format(directory_name)) if f.endswith(".csv")]
    return {"name": dataset_name, "data": datafiles}



def update(resource):
    with open('datapackage.json', 'r') as file:
        dp = json.load(file)
    if resource not in dp['resources']:
        dp['resources'].append(resource)
        with open('datapackage.json', 'w') as file:
            json.dump(dp, file, indent=4)


@click.group()
def main():
    """Update datapackage cli"""

@click.option('--dir', '-d', help="Directory relative to current directory to get file list from.")
@click.option('--name', '-n', help="Dataset name to list in the datapackage.json resource manfiest.")
@main.command()
def add(dir, name):
    """Update datapackage cli"""
    resource_list = gen_resource(dir, name)
    update(resource_list)

@click.option('--dir', '-d', help="Directory relative to current directory to get file list from.")
@main.command()
def add_all(dir):
    targets = [x[0] for x in os.walk(dir)][1:]
    for t in targets:
        name = t.split('/')[1]
        resource_list = gen_resource(t, name)
        update(resource_list)

if __name__ == "__main__":
    main()
