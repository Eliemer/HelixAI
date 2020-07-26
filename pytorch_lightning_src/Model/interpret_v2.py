import torch
import torch.nn as nn
import torch.optim as optim
import time
import copy
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


residues = ['A', 'R', 'N', 'D', 'N', 'C', 'Q',
            'E', 'G', 'G', 'H', 'I', 'L', 'K',
            'M', 'F', 'P', 'S', 'T', 'W', 'Y',
            '?', 'V']

"""
This version of the pyTorch interpreter is for capstone purposes.
"""

#do the regressors
def prepare_ksegments(series,weights):
    '''
    '''
    N = len(series)
    #
    wgts = np.diag(weights)
    wsum = np.diag(weights*series)
    sqrs = np.diag(weights*series*series)

    dists = np.zeros((N,N))
    means = np.diag(series)

    for i in range(N):
        for j in range(N-i):
            r = i+j
            wgts[j,r] = wgts[j,r-1] + wgts[r,r]
            wsum[j,r] = wsum[j,r-1] + wsum[r,r]
            sqrs[j,r] = sqrs[j,r-1] + sqrs[r,r]
            means[j,r] = wsum[j,r] / wgts[j,r]
            dists[j,r] = sqrs[j,r] - means[j,r]*wsum[j,r]

    return dists, means

def regress_ksegments(series, weights, k):
    '''
    '''
    N = len(series)

    dists, means = prepare_ksegments(series, weights)

    k_seg_dist = np.zeros((k,N+1))
    k_seg_path = np.zeros((k,N))
    k_seg_dist[0,1:] = dists[0,:]

    k_seg_path[0,:] = 0
    for i in range(k):
        k_seg_path[i,:] = i

    for i in range(1,k):
        for j in range(i,N):
            choices = k_seg_dist[i-1, :j] + dists[:j, j]
            best_index = np.argmin(choices)
            best_val = np.min(choices)

            k_seg_path[i,j] = best_index
            k_seg_dist[i,j+1] = best_val

    reg = np.zeros(series.shape)
    rhs = len(reg)-1
    for i in reversed(range(k)):
        lhs = k_seg_path[i,rhs]
        reg[int(lhs):rhs] = means[int(lhs),rhs]
        rhs = int(lhs)

    return reg


class Interpreter():

    def __init__ (self, model=None, loss_fn=None,protein_type='Kinase'):
        self.model = model
        self.loss_fn = loss_fn
        self.protein_type = protein_type


    def interpret_test(self, dataset, epochs=1, batch_size=1):

        print('\t\t#### Testing ####')
        avgloss = float(0)
        total_right = float(0.0)
        total = float(0.0)
        start = time.time()
        attributions = {}
        losses = {}

        #Set the model to evaluation mode
        self.model.eval()

        for epoch in range(epochs):
            epoch_total = float(0.0)
            epoch_right = float(0.0)
            true_pos = 0.0
            true_negs = 0.0
            false_pos = 0.0
            false_negs = 0.0
            avgloss = 0.0
            i = 0
           
            for v,c,m,target in dataset:
            
                idx = dataset.dataset.indices[i]
                sample_id = dataset.dataset.dataset.input_df.iloc[idx][0].lower()+'_'+dataset.dataset.dataset.input_df.iloc[idx][1].lower()
                sample_class  =dataset.dataset.dataset.input_df.iloc[idx][2]
                i = i+1

                #if  sample_id not in active_list and  sample_id not in inactive_list : continue

                v_grad = torch.autograd.Variable(v,requires_grad=True).to(self.model.device).float()
                c_grad = torch.autograd.Variable(c,requires_grad=True).to(self.model.device).float()

                v = v.to(self.model.device).float()
                c = c.to(self.model.device).float()

               
                v_grad.retain_grad()
                c_grad.retain_grad()

                mask = m.to(self.model.device).float()
                target = target.to(self.model.device).long()

                y_pred = self.model(v_grad, c_grad, mask)
                y_argmax = torch.argmax(y_pred, dim=1)


                loss = self.loss_fn(y_pred, target)
                loss.backward()

                mask = torch.sum(mask[0],dim=-1)
                mask[mask<2] = 0
                mask[mask>0] = 1
                
                i_ = 0
               
                for t in range(len(mask)):
                    if (mask[t] == 1):
                        i_ = t
                        break
                
                start_res,point =  self.get_start_residue(sample_class)
                if point == 0:
                    point = len(v[0])
               

                ind = 0
                for j in range(len(v[0]-1)):
                    args = torch.argmax((v[0][j:j+3,:23]),dim=-1).tolist()
                    if args == start_res:
                        ind = j
                        break

                if ind > 0:
                    mask = torch.cat((mask[ind:],torch.zeros([ind]).to(self.model.device)),dim=0)
                    v[0] = torch.cat([v[0][ind:],torch.zeros([ind,v[0].shape[1]]).to(self.model.device)],dim=0)
                    c[0] = torch.cat([c[0][ind:],torch.zeros((ind,c[0].shape[1])).to(self.model.device)],dim=0)
                    temp = torch.zeros(m[0].shape)
                    temp[:temp.shape[0]-ind, :temp.shape[1]-ind]= m[0][ind:, ind:]
                    m[0] = temp

                seq = []
                for j in range(len(v[0])):
                    if torch.sum(v[0][j,:23])==0:
                        l = '-'
                    else:
                        ind_ = torch.argmax(v[0][j,:23])
                        l = residues[ind_]
                    seq.append(l)
               

                ind = ind - i_

             
                mask2 = torch.repeat_interleave(mask.unsqueeze(-1),29,dim = -1)
                mask =  torch.repeat_interleave(mask.unsqueeze(-1),3,dim = -1)


                
                v_attr =v_grad.grad[0] *v[0]* mask2
                c_attr = c_grad.grad[0] *c[0]* mask

                vc_all = torch.sum(torch.cat([v_attr*1000,c_attr*1000],dim=-1),dim=-1)
                vc_all = vc_all/torch.max(torch.abs(vc_all))

                #Pass Input*Gradient tensor to numpy array for plot purposes
                mask = mask.cpu().numpy()
                vc_all = vc_all.cpu().detach().numpy()

                mask = mask.astype(float)
                vc_all = vc_all.astype(float)
                attrib = np.array([ -(mask[:,0]-1), vc_all])



                if sample_class not in losses:
                    losses[sample_class] = []
                    losses[sample_class].append([sample_id, loss])
                else: losses[sample_class].append([sample_id, loss])


                attributions[sample_id] = [attrib,seq,ind,None]

                for x in range(y_argmax.size()[0]):
                    total = float(total) + 1
                    epoch_total = float(epoch_total) + 1
                    if y_argmax[x] == target[x]:
                        total_right = float(total_right) + 1
                        epoch_right = float(epoch_right) + 1


                avgloss = float(avgloss) + loss.item()


            return losses, attributions

    def generate_attributions(self, losses, attributions, output_path="./attributions", k_value=25):
        pdbs=[]
        all_= []
        
        for key in losses.keys():
            losses_ = np.array(losses[key])
            top_ = losses_[:,1].astype('float').argsort()[:150]
            top_  = losses_[top_[0:5]]
            
            for i, _ in enumerate(top_):
                y = []
                temp = 0
                curr_pdb = {}
                
                curr_pdb['pdb_class'] = str(key)
                curr_pdb['pdb_name'] = _[0].split('_')[0].upper()
                curr_pdb['pdb_chain'] = _[0].split('_')[1].upper()
                curr_pdb['pdb_loss']= ":{:1.4f}".format(float(_[1]))


                x = attributions[_[0]][0]
                x = x[:,0:160]
            
                y.append(x)
                temp = temp + 1

                temp_ = np.sum(np.concatenate(y,axis=0),axis=0)
                temp_ = regress_ksegments(temp_,np.ones(temp_.size),k_value)
                temp_ = temp_ / np.max(np.abs(temp_))
                y = [np.expand_dims(temp_,axis=0)] + y
                all_.append(temp_)
                pdbs.append(curr_pdb)
        data = []
        label = []
        offsets = []
        for key in attributions.keys():
            x = attributions[key][0].T
            data.append(x)
            label.append(key)
            offsets.append(attributions[key][2])

        data = np.array(data)
        label = np.array(label)
        offsets = np.array(offsets)
        all_ = np.array(all_)
        np.savez(output_path, data=data, labels=label, offsets=offsets,  all_=all_)
        return pdbs, output_path

            


    def get_start_residue(self,sample_class): 
        start_res = [0,0,0]
        point = 0
        if self.protein_type == 'Kinase':
            if sample_class == 0:
                #Active
                start_res = [0,0,0]
                point = 0
            else:
                #Inactive
                start_res = [0, 0, 0]
                point = 0
        elif self.protein_type =='RAS':
            start_res = [0,0,0] #14
            point = 0
        return start_res,point
