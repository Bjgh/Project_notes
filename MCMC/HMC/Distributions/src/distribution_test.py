# from DistributionClass.agnostic_tensor import *
import numpy as np
from torch.autograd import Variable
import torch
from HMC.Distributions.src import distributions as dis

mean = torch.rand(3).unsqueeze(-1).t()
std  = torch.rand(3).unsqueeze(-1).t()
## testing Normal
def true_grad_normal(sample, mean, std, diff):
    if diff == 'sample':
        return torch.sign(sample - mean) / std
    elif diff == 'mean':
        return -torch.sign(sample - mean) / std
    else:
        return -2/std + torch.div(torch.abs(sample- mean), std**2)

def testing_normal(mean, std):
    mean       = Variable(mean, requires_grad = True)
    std        = Variable(std, requires_grad=True)
    normal_obj = dis.Normal(mean, std)
    sample     = normal_obj.sample(num_samples = mean.size()[1])
    sample     = Variable(sample.data, requires_grad = True)
    normal_logpdf = normal_obj.logpdf(sample)

    diff_logpdf  = torch.autograd.grad([normal_logpdf], [sample], grad_outputs=torch.ones(sample.size()), retain_graph=True)[0]
    diff_logpdf2 = torch.autograd.grad([normal_logpdf], [mean], grad_outputs=torch.ones(mean.size()), retain_graph=True)[0]
    diff_logpdf3 = torch.autograd.grad([normal_logpdf], [std], grad_outputs=torch.ones(std.size()), retain_graph=True)[0]

    print(diff_logpdf)
    print(diff_logpdf2)
    print(diff_logpdf3)


def true_grad_laplace(sample, loc, scale, diff):
    if diff == 'location':
        return torch.sign(sample - loc) / scale
    elif diff == 'sample':
        return -torch.sign(sample - loc) / scale
    else:
        return -2/scale + torch.div(torch.abs(sample- loc), scale**2)


## testing Laplace
def testing_laplace(mean, std):
    '''Test the derivatives of the logpdf w.r.t the 'sample'
     'location (mean)'  and 'scale' (std)
     input
     -----
     mean - Type: Torch.tensors or np.arrays [1, .., N]
     std  - Type: Torch.tensors or np.arrays [1, .., N]
     '''
    location = Variable(mean, requires_grad = True)
    scale    = Variable(std, requires_grad = True)
    laplace_obj     = dis.Laplace(location, scale)
    sample          = Variable(laplace_obj.sample().data, requires_grad = True)
    laplace_logpdf  = laplace_obj.logpdf(sample)
    # Spits out the gradient as a tuple, so [0] takes the variable object from the tuple
    # containing the gradients
    diff_logpdf     = torch.autograd.grad([laplace_logpdf], [sample], grad_outputs= torch.ones(sample.size()), retain_graph= True)[0]
    diff_logpdf2    = torch.autograd.grad([laplace_logpdf], [location],grad_outputs= torch.ones(location.size()), retain_graph = True)[0]
    diff_logpdf3    = torch.autograd.grad([laplace_logpdf], [scale], grad_outputs= torch.ones(scale.size()), retain_graph = True)[0]
    # Pytorch gradients
    print('Printing autograd gradients: ')
    print(diff_logpdf)
    print(diff_logpdf2)
    print(diff_logpdf3)
    # True gradients
    print()
    print('Printing true gradients ')
    print('grad_sample',true_grad_laplace(sample,location,scale,diff = 'sample').data)
    print('grad_location',true_grad_laplace(sample,location,scale,diff = 'location').data)
    print('grad_scale', true_grad_laplace(sample, location, scale, diff = 'scale').data)

# Testing categorical
def testing_categorical()
# Testing normal
#testing_normal(mean,std)
# Testing laplacian
# testing_laplace(mean,std)
# Testing categorical

# Testing Bernoulli
