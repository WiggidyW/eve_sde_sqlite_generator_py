import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class SolarSystemStaticData:
    def __init__(self, dir):
        self.paths = list((dir / 'fsd' / 'universe')\
            .rglob("solarsystem.staticdata"))
        self.index = 0
        self.region_ids = {}
        self.constellation_ids = {}

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.paths):
            raise StopIteration
        f = open(self.paths[self.index])
        yml = yaml.load(f, Loader)
        f.close()
        self.index += 1

        # constellation_id_path = self.paths[self.index].parent.parent / 'constellation.staticdata'
        # if constellation_id_path not in self.constellation_ids:
        #     f = open(constellation_id_path)
        #     constellation_yml = yaml.load(f, Loader)
        #     f.close()
        #     self.constellation_ids[constellation_id_path] = constellation_yml['constellationID']
        # yml['constellationID'] = self.constellation_ids[constellation_id_path]

        region_id_path = self.paths[self.index].parent.parent.parent / 'region.staticdata'
        if region_id_path not in self.region_ids:
            f = open(region_id_path)
            region_yml = yaml.load(f, Loader)
            f.close()
            self.region_ids[region_id_path] = region_yml['regionID']
        yml['regionID'] = self.region_ids[region_id_path]

        return yml

class SDE:
    def __init__(self, dir):
        self.dir = dir / 'sde'
        self._solar_systems = None
        self._type_ids = None
        self._group_ids = None
        self._category_ids = None
        self._type_materials = None
        self._market_groups = None
        self._blueprints = None
        self._type_dogma = None

    def solar_systems(self):
        if self._solar_systems is None:
            self._solar_systems = SolarSystemStaticData(self.dir)
        return self._solar_systems
    
    def type_ids(self):
        if self._type_ids is None:
            with open(
                self.dir / 'fsd' / 'typeIDs.yaml',
                'r',
                encoding='utf8',
            ) as f:
                self._type_ids = yaml.load(f, Loader)
        return self._type_ids
    
    def group_ids(self):
        if self._group_ids is None:
            with open(
                self.dir / 'fsd' / 'groupIDs.yaml',
                'r',
                encoding='utf8',
            ) as f:
                self._group_ids = yaml.load(f, Loader)
        return self._group_ids
    
    def category_ids(self):
        if self._category_ids is None:
            with open(
                self.dir / 'fsd' / 'categoryIDs.yaml',
                'r',
                encoding='utf8',
            ) as f:
                self._category_ids = yaml.load(f, Loader)
        return self._category_ids
    
    def type_materials(self):
        if self._type_materials is None:
            with open(
                self.dir / 'fsd' / 'typeMaterials.yaml',
                'r',
                encoding='utf8',
            ) as f:
                self._type_materials = yaml.load(f, Loader)
        return self._type_materials
    
    def market_groups(self):
        if self._market_groups is None:
            with open(
                self.dir / 'fsd' / 'marketGroups.yaml',
                'r',
                encoding='utf8',
            ) as f:
                self._market_groups = yaml.load(f, Loader)
        return self._market_groups
    
    def blueprints(self):
        if self._blueprints is None:
            with open(
                self.dir / 'fsd' / 'blueprints.yaml',
                'r',
            ) as f:
                self._blueprints = yaml.load(f, Loader)
        return self._blueprints
    
    def type_dogma(self):
        if self._type_dogma is None:
            with open(
                self.dir / 'fsd' / 'typeDogma.yaml',
                'r',
            ) as f:
                self._type_dogma = yaml.load(f, Loader)
        return self._type_dogma
