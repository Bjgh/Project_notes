#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Bradley Gram-Hansen
Time created:  15:25
Date created:  06/09/2017

License: MIT
'''
import torch
import numpy as np
from torch.autograd import Variable
import Distributions.distributions as dis
from core import VariableCast
class program():
    ''''This needs to be a function of all free variables.
         If I provide a map of all values and computes the log density
         and assigns values rather than samples.
         If I don't provide then it samples
         For any variable values provided in the map, they are assigned

         method
         def eval

         Needs to be a class '''
    def __init__(self):
    #     '''Generating code, returns  a map of variable names / symbols
    #      store all variables of interest / latent parameters in here.
    #       Strings -  A list of all the unique numbers of the para'''
    #     # self.params = [{'x' + Strings[i] : None} for i in range(len(Strings))]
        self.params  = {'x':None}

    def calc_grad(self, logjoint, parms):
        ''' Stores the gradients, grad, in a tensor, where each row corresponds to each the
            data from the Variable of the gradients '''
        grad = torch.autograd.grad([logjoint], [parms], grad_outputs=torch.ones(parms[0].data.size()))
        # note: Having grad_outputs set to the dimensions of the first element in the list, implies that we believe all
        # other values are the same size.
        # print(grad)
        if parms.size()[0] == 1:
            gradients = torch.Tensor(1,parms.size()[0])
        else:
            gradients = torch.Tensor(parms.size())

        for i in range(len(parms)):
            gradients[i,:] = grad[i][0].data.unsqueeze(0)  # ensures that each row of the grads represents a params grad
        return gradients

    def tensor_to_list(self,values):
        parms = []
        for value in values:
            if isinstance(value, Variable):
                temp = Variable(value.data, requires_grad=True)
                parms.append(temp)
            else:
                temp = VariableCast(value)
                temp = Variable(value.data, requires_grad=True)
                parms.append(value)
        return parms
class program_simple(program):
    def __init__(self):
        super().__init__()

    def generate(self):
        ''' Generates the initial state and returns the samples and logjoint evaluated at initial samples  '''

        ################## Start FOPPL input ##########
        logp = [] # empty list to store logps of each variable
        parms = []
        a = VariableCast(0.0)
        b = VariableCast(2.236)
        normal_object = dis.Normal(a, b)
        x = Variable(normal_object.sample().data, requires_grad = True)
        parms.append(x)

        std  = VariableCast(1.4142)
        obs2 = VariableCast(7.0)
        p_y_g_x    = dis.Normal(parms[0], std)

        # TO DO Ask Yuan, is it either possible to have once an '.logpdf' method is initiated can we do a
        # logp.append(<'variable upon which .logpdf method used'>)
        logp.append(normal_object.logpdf(parms))
        logp.append(p_y_g_x.logpdf(obs2))
        # TO DO We will need to su m all the logs here.
        # Do I have them stored in a dictionary with the value
        # or do we have a separate thing for the logs?
        ################# End FOPPL output ############

        # sum up all logs
        logp_x_y   = VariableCast(torch.zeros(1,1))
        for logprob in logp:
            logp_x_y = logp_x_y + logprob
        return logp_x_y, parms, VariableCast(self.calc_grad(logp_x_y,parms))
    def eval(self, values, grad= False, grad2= False):
        ''' Takes a map of variable names, to variable values . This will be continually called
            within the leapfrog step

        values      -       Type: python dict object
                            Size: len(self.params)
                            Description: dictionary of 'parameters of interest'
        grad        -       Type: bool
                            Size: -
                            Description: Flag to denote whether the gradients are needed or not
        '''
        logp = []  # empty list to store logps of each variable # In addition to foopl input
        parms = self.tensor_to_list(values)
        ################## Start FOPPL input ##########
        a = VariableCast(0.0)
        b = VariableCast(2.236)
        normal_object = dis.Normal(a, b)

        std  = VariableCast(1.4142)
        obs2 = VariableCast(7.0)
        # Need a better way of dealing with values. As ideally we have a dictionary (hash map)
        # then we say if values['x']
        p_y_g_x    = dis.Normal(parms[0], std)

        logp.append(normal_object.logpdf(parms[0]))
        logp.append(p_y_g_x.logpdf(obs2))

        ################# End FOPPL output ############
        logjoint = VariableCast(torch.zeros(1, 1))

        for logprob in logp:
            logjoint = logjoint + logprob
        # grad2 is a hack so that we can call this at the start
        if grad:
            gradients = self.calc_grad(logjoint, parms)
            return VariableCast(gradients)
        elif grad2:
            gradients = self.calc_grad(logjoint, parms)
            return logjoint, VariableCast(gradients)
        else:
            return logjoint, parms
    def free_vars(self):
        return self.params


class program_linear_reg(program):
    def __init__(self):
        super().__init__()

    def generate(self):
        logp   = []
        parms  = []
        c23582 = VariableCast(torch.Tensor([0.0]))
        c23583 = VariableCast(torch.Tensor([10.0]))
        normal_obj1 = dis.Normal(c23582, c23583)
        x23474 = Variable(normal_obj1.sample().data, requires_grad = True)  # sample
        parms.append(x23474)
        p23585 = normal_obj1.logpdf(x23474)  # prior
        logp.append(p23585)
        c23586 = VariableCast(torch.Tensor([0.0]))
        c23587 = VariableCast(torch.Tensor([10.0]))
        normal_obj2 = dis.Normal(c23586, c23587)
        x23471 = Variable(normal_obj2.sample().data, requires_grad = True)  # sample
        parms.append(x23471)
        p23589 = normal_obj2.logpdf(x23471)  # prior
        logp.append(p23589)
        c23590 = VariableCast(torch.Tensor([1.0]))
        # Do I cast this as a variable with requires_grad = True ???
        x23591 = x23471 * c23590 + x23474 # some problem on Variable, Variable.data

        # x23592 = Variable(x23591.data + x23474.data, requires_grad = True)

        c23593 = VariableCast(torch.Tensor([1.0]))
        normal_obj2 = dis.Normal(x23591, c23593)

        c23595 = VariableCast(torch.Tensor([2.1]))
        y23481 = c23595
        p23596 = normal_obj2.logpdf(y23481)  # obs, log likelihood
        logp.append(p23596)
        c23597 = VariableCast(torch.Tensor([2.0]))

        # This is highly likely to be the next variable
        x23598 = torch.mul(x23471, c23597) + x23474
        # x23599 = torch.add(x23598, x23474)
        c23600 = torch.Tensor([1.0])
        # x23601 = dis.Normal(x23599, c23600)

        normal_obj3 = dis.Normal(x23598, c23600)
        c23602 = torch.Tensor([3.9])
        y23502 = c23602
        p23603 = normal_obj3.logpdf(y23502)  # obs, log likelihood
        logp.append(p23603)
        c23604 = torch.Tensor([3.0])
        x23605 = Variable(torch.mul(x23471, c23604).data, requires_grad = True)
        x23606 = torch.add(x23605, x23474)
        c23607 = torch.Tensor([1.0])
        normal_obj4 = dis.Normal(x23606, c23607)
        c23609 = torch.Tensor([5.3])
        y23527 = c23609
        p23610 = normal_obj4.log_pdf(y23527)  # obs, log likelihood
        logp.append(p23610)
        p23611 = torch.add([p23585, p23589, p23596, p23603, p23610])
        # return E from the model
        # Do I want the gradients of x23471 and x23474? and nothing else.
        if grad:
            gradients = self.calc_grad(p23611, parms)
            return VariableCast(gradients)
        elif grad2:
            gradients = self.calc_grad(p23611, values)
            return p23611, VariableCast(gradients)
        else:
            return p23611, values

    def eval(self, values, grad=False, grad2=False):
        logp = []
        parms = []
        for value in values:
            if isinstance(value, Variable):
                temp = Variable(value.data, requires_grad = True)
                parms.append(temp)
            else:
                temp = VariableCast(value)
                temp = Variable(value.data, requires_grad = True)
                parms.append(value)
        c23582 = VariableCast(torch.Tensor([0.0]))
        c23583 = VariableCast(torch.Tensor([10.0]))
        normal_obj1 = dis.Normal(c23582, c23583)
        x23474 = parms[0] # sample
        parms.append(x23474)
        p23585 = normal_obj1.logpdf(x23474)  # prior
        logp.append(p23585)
        c23586 = VariableCast(torch.Tensor([0.0]))
        c23587 = VariableCast(torch.Tensor([10.0]))
        normal_obj2 = dis.Normal(c23586, c23587)
        x23471 = parms[1]  # sample
        parms.append(x23471)
        p23589 = normal_obj2.logpdf(x23471)  # prior
        logp.append(p23589)
        c23590 = VariableCast(torch.Tensor([1.0]))
        # Do I cast this as a variable with requires_grad = True ???
        x23591 = x23471 * c23590 + x23474  # some problem on Variable, Variable.data

        # x23592 = Variable(x23591.data + x23474.data, requires_grad = True)

        c23593 = VariableCast(torch.Tensor([1.0]))
        normal_obj2 = dis.Normal(x23591, c23593)

        c23595 = VariableCast(torch.Tensor([2.1]))
        y23481 = c23595
        p23596 = normal_obj2.logpdf(y23481)  # obs, log likelihood
        logp.append(p23596)
        c23597 = VariableCast(torch.Tensor([2.0]))

        # This is highly likely to be the next variable
        x23598 = torch.mul(x23471, c23597) + x23474
        # x23599 = torch.add(x23598, x23474)
        c23600 = torch.Tensor([1.0])
        # x23601 = dis.Normal(x23599, c23600)

        normal_obj3 = dis.Normal(x23598, c23600)
        c23602 = torch.Tensor([3.9])
        y23502 = c23602
        p23603 = normal_obj3.logpdf(y23502)  # obs, log likelihood
        logp.append(p23603)
        c23604 = torch.Tensor([3.0])
        x23605 = Variable(torch.mul(x23471, c23604).data, requires_grad=True)
        x23606 = torch.add(x23605, x23474)
        c23607 = torch.Tensor([1.0])
        normal_obj4 = dis.Normal(x23606, c23607)
        c23609 = torch.Tensor([5.3])
        y23527 = c23609
        p23610 = normal_obj4.log_pdf(y23527)  # obs, log likelihood
        logp.append(p23610)
        p23611 = torch.add([p23585, p23589, p23596, p23603, p23610])
        # return E from the model
        # Do I want the gradients of x23471 and x23474? and nothing else.
        if grad:
            gradients = self.calc_grad(p23611, parms)
            return VariableCast(gradients)
        elif grad2:
            gradients = self.calc_grad(p23611, values)
            return p23611, VariableCast(gradients)
        else:
            return p23611, values
class programif():
    ''''This needs to be a function of all free variables.
         If I provide a map of all vlues and computes the log density
         and assigns values rather than samples.
         If I don't provide then it samples
         For any variable values provided in the map, they are assigned

         method
         def eval

         Needs to be a class '''
    def __init__(self):
        '''Generating code, returns  a map of variable names / symbols '''
        self.params = {'x': None}

    def eval(self, values):
        ''' Takes a map of variable names, to variable values '''
        a = VariableCast(0.0)
        b = VariableCast(1)
        normal_object = Normal(a, b)
        if values['x'] is not None:
            x = Variable(values['x'], requires_grad=True)
        # else:
        #     x = normal_object.sample()
        #     x = Variable(x.data, requires_grad = True)
        if torch.gt(x,torch.zeros(x.size()))[0][0]:
        logp_x = normal_object.logpdf(x)
        std = VariableCast(1.73)
        p_y_g_x = Normal(x, std)
        obs2 = VariableCast(7.0)
        logp_y_g_x = p_y_g_x.logpdf(obs2)
        logp_x_y = Variable.add(logp_x, logp_y_g_x)
        return logp_x_y, {'x':x.data}
    def free_vars(self):
        return self.params