import sys
from pathlib import Path
import pickle
from collections import Counter

import numpy as np

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

util_dir = Path.cwd().parent.joinpath('Utility')
sys.path.insert(1, str(util_dir))
from Database import *
from Information import *

class Stochastic:
    def __init__(self, dist, db_files, hitNumCut=20):
        self.dist = dist
        self.dbs = db_files
        self.hitNumCut = hitNumCut

        self.db_iter = iter(db_files)

        self.current_db = None
        self.session = None
        self.__update_db()

        self.ptcls = None
        self.ptcl_iter = None
        self.__make_ptcl_iter()

    def __connect_db(self):
        engine = create_engine('sqlite:///'+str(self.current_db))
        Session = sessionmaker(bind=engine) # session factory
        session = Session() # session object
        self.session = session

    def __update_db(self):
        self.current_db = next(self.db_iter)
        self.__connect_db()

    def __find_ptcls(self):
        ptcls = self.session.query(Particle).all()
        self.ptcls = ptcls

    def __make_ptcl_iter(self):
        self.__find_ptcls()
        self.ptcl_iter = iter(self.ptcls)

    def generate(self, mode='eval'):
        trackNum = int(self.dist.rvs(size=1))
        trackFoundNum = 0
        tracks = {}
        hits = {}

        while trackFoundNum < trackNum:
            try:
                ptcl = next(self.ptcl_iter)
            except:
                sys.stdout.write('\n')
                sys.stdout.flush()
                pinfo('Run out of particles')
                pinfo('Connecting to the next track database')
                self.__update_db()
                self.__make_ptcl_iter()
                ptcl = next(self.ptcl_iter)

            strawHit_qrl = self.session.query(StrawDigiMC).filter(StrawDigiMC.particle==ptcl.id)
            hitNum = strawHit_qrl.count()

            if (hitNum >= self.hitNumCut) and (ptcl.pdgId == 11):
                tracks[ptcl.id] = []
                track = tracks[ptcl.id]

                strawHits = strawHit_qrl.all()
                for hit in strawHits:
                    track.append(hit.id)
                    hits[hit.id] = (hit.x, hit.y, hit.z)

                pdgId = self.session.query(Particle.pdgId).filter(Particle.id==ptcl.id).one_or_none()[0]
                track.append(pdgId)
                trackFoundNum += 1
            else:
                continue
        if mode == 'eval':
            return hits, tracks
        else:
            return hits
