from sde import SDE
import generators
import generator
import download

from pathlib import Path
import tempfile

def import_generator_groups(
    names: 'list[str]',
) -> 'list[dict[str, str | list[dict[str, str | function]]]]':
    generator_groups = []
    for name in names:
        if name == 'item-configurator-sqlite-accessor':
            generator_groups.append(generators.ItemConfiguratorSqliteAccessor)
        else:
            raise Exception(f'Unknown generator group: {name}')
    return generator_groups

def run(
    prev_checksum: str,
    generator_groups: 'list[str]',
    debug=False,
) -> 'str | None':
    generator_groups: 'list[dict[str, str | list[dict[str, str | function]]]]' = \
        import_generator_groups(generator_groups)

    http = download.http()
    new_checksum = download.checksum(http)
    
    if prev_checksum == new_checksum:
        print('Checksums match.')
        print('Done.')
        return None
    else:
        print('Checksums do not match.')
        dir_ = tempfile.mkdtemp()
        dir = Path(dir_)
        if debug:
            sde_dir = Path('.')
            sde_ = SDE(sde_dir)
        else:
            download.sde(http, dir)
            sde_ = SDE(dir)
        
        for generator_group in generator_groups:
            generator.generate_group(
                dir,
                sde_,
                generator_group,
                debug,
            )
        
        print('Done.')
        return new_checksum
