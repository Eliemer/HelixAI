import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class Flatten(nn.Module):
    '''
    Layer flattens all dimensions of a tensor except for the first

    Params:
        x - Tensor of arbitrary shape

    Returns:
        x - Tensor of shape (BATCH, reduce_sum(features))
    '''

    def __init__(self):
        super().__init__()

    def forward(self, x):
        x = x.view(x.size()[0], -1)
        return x

class AdjacencyMatrix(nn.Module):
    '''
    Layer returns Tensor placeholders for graph convolutional networks.

    Params:
        c - Rank 3 tensor defining coordinates of nodes in n-euclidean space; BATCHxNxC
        m - Rank 3 tensor mask to apply from missing residues to adjacency matrix 'a'; BATCHxNxN
    Returns:
        a - Rank 4 tensor containing L2 distances between nodes concatenated with Cosine distances
        between nodes according to tensor c; BATCHx2xNxN
    '''
    def __init__(self):
        super(AdjacencyMatrix, self).__init__()

    def forward(self, c, m=None):

        a_l2 = L2PDist()(c)
        a_cos = CosinePDist(m)(c)
        a = [a_l2.unsqueeze(1), a_cos.unsqueeze(1)]

        return torch.cat(a, dim=1)

class L2PDist(nn.Module):
    '''
    Calculate L2 pairwise distance between coordinates

    Params:
        c - Rank 3 tensor defining coordinates of nodes in n-euclidean namespace

    Returns:
        a - Rank 3 tensor defining pairwise adjacency matrix of nodes.
    '''
    def __init__(self):
        super(L2PDist, self).__init__()

    def forward(self, c):
        l2 = torch.sum(c*c, 2)
        l2 = l2.view(-1,1,l2.size()[-1])
        a = l2 - 2* torch.matmul(c, c.permute(0,2,1)) + l2.permute(0,2,1)
        a = torch.abs(a)

        return a

class CosinePDist(nn.Module):
    '''
    Layer calculates cosine pairwise distances between coordinates in tensor c.

    Params:
        c - Rank 3 tensor defining coordinates of nodes in n-euclidean space.
    Returns:
        a - Rank 3 tensor defining cosine pairwise adjacency matrix of nodes.

    '''
    def __init__(self, mask=None):
        super(CosinePDist, self).__init__()
        self.mask = mask

    def forward(self, c):
        normalized = F.normalize(c, p=2, dim=-1)
        normalized_trans =  normalized.permute(0,2,1)
        prod = torch.matmul(normalized,normalized_trans)
        a = (1 - prod)/2.0
        if self.mask is not None:
            a = 1 - a
            a = torch.mul(a,self.mask)
        else:
            a = torch.add(-a,1)
        return a

class GraphKernels(nn.Module):
    '''
    Layer defines tensor layer which learns a graph kernel in order to normalize
    pairwise euclidean distances found in tensor a, according to node features in
    tensor v. The final set of normalized adjacency tensors a_prime have values
    ranging from [0,1].

    Params:
        v - Rank 3 tensor defining the node features; BATCHxNxF
        a - Rank 3 tensor defining L2 distances between nodes according to tensor c; BATCHxNxN
        nb_kernels - int; number of learned kernels

    Returns:
        a_prime - Rank 4 tensor of normalized adjacency tensors; BATCHxNxN

    '''
    def __init__(self, nb_kernels=1, batch_size=1, nb_features=1, nb_nodes=1, kernel_limit=100.0, training=None):
        super(GraphKernels, self).__init__()
        self.nb_kernels = nb_kernels
        self.kernel_limit = kernel_limit
        self.training = training
        self.batch_size = batch_size
        self.nb_features = nb_features
        self.nb_nodes = nb_nodes

        self.norm = nn.BatchNorm1d(nb_nodes)

        self.w = torch.empty(self.nb_features, self.nb_kernels * 2)
        nn.init.normal_(self.w, mean=0.0, std=np.sqrt(2/((self.nb_nodes * self.nb_features) + (self.nb_nodes * self.nb_kernels))))
        #
        # self.w = self.w.unsqueeze(0)
        # self.w = self.w.repeat(self.batch_size, 1, 1)

        self.w = nn.Parameter(self.w)

    def forward(self, v, a, mask=None):
        a_prime = []
        y = torch.matmul(v, self.w)

        for weight in torch.split(y, 2, dim=-1):
            c_1, c_2 = torch.split(weight, 1, dim=-1)
            c_2 = c_2.permute([0,2,1])
            c = c_1 + c_2
            c = self.norm(c)
            c.sigmoid_() # in-place sigmoid
            c = (c * int(self.kernel_limit)) + 0.00001
            a_ = torch.exp(-((a * a) / (2 * c * c)))

            if mask is not None:
                a_ = a_ * mask
            a_ = a_.unsqueeze(1)

            a_prime.append(a_)

        a_prime = torch.cat(a_prime, dim=1)
        return a_prime

class GraphConv(nn.Module):
    '''
    Layer defines basic graph convolution operation using inputs V and A. First,
    features between nodes are progated through the graph according to adjacency matrix set
    A. Next, new features are mapped according to fully connected layer to produce
    node feature tensor V'.

    It's important to note that this implemenation of graph convolutions does not
    parameterize each edge in the graph, rather a single weight is shared between all edges
    of any given node. Parameterizing all edges at the moment requires the generation
    of seperate adjacency matricies for each edge independently which is severly inefficient
    due to sparsity. This problem is currently being researched.That being said, single-weight
    graph convolutions still preform reasonably well using euclidean pairwise distance representations.

    Update: Graph Kernel parameterization prior to graph convolution provides substantial improvement over
    single-weight convolution.

    Params:
        v - Rank 3 tensor defining node features.
        a - Rank 3 tensor defining pairwise adjacency matrix of nodes.
        nb_filters - int32; number of features in V'
        activation - Layer defining activation of graph convolution

    Returns:
        v_prime - Rank 3 tensor defining node features for V'

    '''
    def __init__(self, nb_filters=1, nb_nodes=1, nb_features=1, support=1, batch_size=1, activation=nn.ReLU(), training=None):
        super(GraphConv, self).__init__()
        self.nb_filters = nb_filters
        self.activation = activation
        self.batch_size = batch_size
        self.nb_features = nb_features
        self.nb_nodes = nb_nodes
        self.support = support +1

        self.norm = nn.BatchNorm1d(nb_nodes)

        self.w = torch.empty(self.nb_features * self.support, self.nb_filters)
        nn.init.normal_(self.w, mean=0.0, std=np.sqrt(2/((self.support * self.nb_features) + self.nb_filters)))

        self.w = nn.Parameter(self.w)

        self.b = torch.zeros([self.nb_filters], dtype=torch.float32)
        self.b = nn.Parameter(self.b)

    def forward(self, v, a):
        v = v.unsqueeze(1)
        v_ = (torch.matmul(a, v)/self.nb_nodes)
        v_ = v_.view(a.size()[0], a.size()[-1], -1)
        # print(v.size(), v_.size(), a.size(), self.w.size())
        v_prime = torch.matmul(v_, self.w) + self.b


        v_prime = self.norm(v_prime)

        v_prime = self.activation(v_prime)
        return v_prime

class AverageSeqGraphPool(nn.Module):
    '''
    Method preforms sequence based average pooling on graph structure.
    V and C are assumed to be in sequential order.

    Params:
        v - Rank 3 tensor defining the node features; BATCHxNxF
        c - Rank 3 tensor defining coordinates of nodes in n-euclidean space; BATCHxNxC
        kernelsize - int32; pool window size along sequence.

    Returns:
        v_prime - Rank 3 tensor defining the node features for pooled V; BATCHx(N/pool_size)xF
        c_prime - Rank 3 tensor defining coordinates of nodes in n-euclidean space for pooled C; BATCHx(N/pool_size)xC
        a_prime - Rank 3 tensor defining L2 distances between nodes according to tensor c; BATCHx(N/pool_size)
    '''
    def __init__(self, pool_size=3):
        super(AverageSeqGraphPool, self).__init__()
        self.pool_size = pool_size

        self.l2pdist = L2PDist()
        self.cosdist = CosinePDist()

    def forward(self,v,c):
        # #Average Pool v and C
        # print(v.size(), c.size())
        v = v.permute(0,2,1)
        c = c.permute(0,2,1)
        # print(v.size(), c.size())

        v_prime = F.avg_pool1d(v, self.pool_size, self.pool_size)
        c_prime = F.avg_pool1d(c, self.pool_size, self.pool_size)

        # print(v_prime.size(), c_prime.size())
        v_prime = v_prime.permute(0,2,1)
        c_prime = c_prime.permute(0,2,1)
        # print(v_prime.size(), c_prime.size())

        l2dist = self.l2pdist(c_prime).unsqueeze(1)
        cosDist = self.cosdist(c_prime).unsqueeze(1)

        # print(l2dist.size(), cosDist.size())
        # l2dist = l2dist.permute(0,1,3,2) # its a 4d tensor
        # cosDist = cosDist.permute(0,1,3,2)
        # Generatin a new A
        a_prime = torch.cat([l2dist, cosDist], dim=1)
        # print(v_prime.size(), c_prime.size(), a_prime.size())
        return v_prime, c_prime , a_prime

class Attention(nn.Module):

    def __init__(self, nb_nodes=1, nb_features=1, batch_size=1):
        super(Attention, self).__init__()
        self.nb_nodes = nb_nodes
        self.nb_features = nb_features
        self.batch_size = batch_size

        # print(nb_nodes, nb_features)
        self.u = torch.empty(self.nb_features, self.nb_nodes)
        nn.init.xavier_uniform_(self.u)
        #
        # self.u.unsqueeze(0)
        # self.u.repeat(self.batch_size, 1, 1)
        self.u = nn.Parameter(self.u)

    def forward(self, v):

        temp = torch.sqrt(torch.as_tensor(self.nb_features, dtype=torch.float32))
        # print(v.size(), self.u.size())
        x = torch.matmul(v, self.u)
        x = x.permute(0,2,1)
        x = x / temp

        node_atten = F.softmax(x, dim=-1)

        v_prime = torch.matmul(node_atten, v)

        return v_prime
