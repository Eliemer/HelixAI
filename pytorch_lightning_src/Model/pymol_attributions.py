from pymol import cmd, stored
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
cmap = cm.seismic
norm = Normalize(vmin=-1, vmax=1)

def zero_residues(sel1,offset=0,chains=0):
        """
        DESCRIPTION
        Renumbers the residues so that the first one is zero, or offset
        USAGE
        zero_residues selection [, offset [, chains ]]
        EXAMPLES
        zero_residues protName            # first residue is 0
        zero_residues protName, 5         # first residue is 5
        zero_residues protName, chains=1  # each chain starts at 0
        zero_residues *
        """
        offset = int(offset)

        # variable to store the offset
        stored.first = None
        # get the names of the proteins in the selection

        names = ['(model %s and (%s))' % (p, sel1)
                        for p in cmd.get_object_list('(' + sel1 + ')')]

        if int (chains):
                names = ['(%s and chain %s)' % (p, chain)
                                for p in names
                                for chain in cmd.get_chains(p)]

        # for each name shown
        for p in names:
                # get this offset
                ok = cmd.iterate("first %s and polymer and n. CA" % p,"stored.first=resv")
                # don't waste time if we don't have to
                if not ok or stored.first == offset:
                        continue;
                # reassign the residue numbers
                cmd.alter("%s" % p, "resi=str(int(resi)-%s)" % str(int(stored.first)-offset))
                # update pymol

        cmd.rebuild()

class StructureAttribution:
    def __init__(self,attribution_path,data_path,output_path):
        self.attribution_path = attribution_path
        self.data_path = data_path
        self.output_path = output_path

    def structure_attribution(self, pdb_id, flag=False):

        # Load Attribution
        data = np.load(self.attribution_path,allow_pickle=True)
        attributions = data['data']
        offsets = data['offsets']
        labels = data['labels']
        ind = np.where(labels == pdb_id)
        attribution = attributions[ind][0][:,-1]
        
        cmd.bg_color('white')
        cmd.load(self.data_path+pdb_id[:-2]+'.pdb')
        cmd.split_chains()
        for name in cmd.get_names('objects', 0, '(all)'):
            if not name.endswith(pdb_id[-1].upper()):
                cmd.delete(name)
            else: zero_residues(name)
        cmd.reset()

        cmd.color('white', pdb_id)
        for i, _ in enumerate(attribution):
            cmd.select('toBecolored', 'res ' + str(i+offsets[ind][0]))
            cmd.set_color('saliency'+str(i), list(cmap(norm(_)))[:3])
            cmd.color('saliency'+str(i), 'toBecolored')

        cmd.select('selected','chain '+pdb_id[-1].upper())
        #cmd.show('mesh', 'selected')
        cmd.deselect()
        cmd.save(self.output_path + pdb_id+'.pse')
        return self.output_path+pdb_id+'.pse'


#############################################################
# pdb_id = '4q9z_a'
# attributions_path = 'Output/Kinases/seed1/attributions.npz'
# data_path = 'pdb_extractor/Kinases/PDB/'

# cmd.reinitialize()
# cmd.bg_color('black')
# sA = StructureAttribution(attributions_path,data_path)
# sA.structure_attribution(pdb_id)