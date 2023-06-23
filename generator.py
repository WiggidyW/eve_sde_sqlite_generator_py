from pathlib import Path
import subprocess
import sqlite3
import shutil
import env
import os

def generate_group(
    dir: Path,
    sde,
    generator_group: 'dict[str, str | list[dict[str, str | function]]]',
    debug: bool,
):
    if debug:
        for generator in generator_group['generators']:
            destination = Path('.') /\
                'debug_out' /\
                generator_group["ref"] /\
                'db.sqlite'
            generate(
                dir,
                sde,
                destination,
                generator['initialize'],
                generator['insert'],
                debug=True,
            )
    
    else:
        git_url = env.get_or_panic(generator_group['ref'])
        repo_name = git_url.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        repo_path = dir / repo_name
        # clone the repo to dir
        subprocess.run(
            ['git', 'clone', git_url],
            cwd=dir,
        )

        # generate the database and move it to the repo
        for generator in generator_group['generators']:
            destination = f'{repo_path}/{generator["destination"]}'
            generate(
                dir,
                sde,
                destination,
                generator['initialize'],
                generator['insert'],
            )
            # add the database to git
            subprocess.run(
                ['git', 'add', destination],
                cwd=repo_path,
                check=True,
            )
            # commit the changes
            subprocess.run(
                ['git', 'commit', '-m', f'Update {generator["destination"]}'],
                cwd=repo_path,
                check=True,
            )

        # push the commits
        subprocess.run(['git', 'push'], cwd=repo_path, check=True)


def generate(
    dir: Path,
    sde,
    destination,
    initialize,
    insert,
    debug=False,
):
    # create the database
    conn = sqlite3.connect(dir / 'db.sqlite')
    c = conn.cursor()

    # initialize the database
    initialize(c, sde)
    conn.commit()

    # insert the data
    insert(c, sde)
    conn.commit()

    # close the connection
    conn.close()

    # move the file to the destination
    if debug:
        os.makedirs(destination.parent, exist_ok=True)
        shutil.move(dir / 'db.sqlite', destination)
    else:
        shutil.move(dir / 'db.sqlite', dir / Path(destination))
