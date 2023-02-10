# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 09:30:37 2023

@author: j.reul
"""
import os
import numpy as np

import mode_behave_public as mb

class Function:
    """
    This class provides the functionality within the Home.py
            
    """
    
    def __init__(self, data_in, alt, equal_alt, param, k, numeric_analysis, **kwargs):
                                            
        #Initialize model
        self.model = mb.Core(
            param=param, 
            data_in=data_in, 
            alt=alt, 
            equal_alt=equal_alt
            )

        #number of clusters to analyze
        self.k = int(round(k, 0))
        
        self.numeric = numeric_analysis
        
        self.PATH_HOME = os.path.dirname(__file__)
        self.sep = os.path.sep

        
    def estimate_model(self):

        if self.numeric:
            t_stats_out = True
        else:
            t_stats_out = False
            
        #estimate mixed logit model        
        self.model.estimate_mixed_logit(
            min_iter=10, 
            max_iter=1000,
            tol=0.01,
            space_method = 'abs_value',
            scale_space = 2,
            max_shares = 1000,
            bits_64=True,
            t_stats_out=t_stats_out
            )

    def get_likelihood(self):
        LL_MNL = self.model.loglike_MNL()[0]
        LL_MXL = self.model.loglike_MXL()
        
        return LL_MNL, LL_MXL


    def conduct_visual_analysis(self):
        save_fig_path_temp = self.PATH_HOME + self.sep + "data"
                
        #visualize the preferences distribution   
        fig_space = self.model.visualize_space(
            k=self.k, 
            scale_individual=True, 
            cluster_method='kmeans', 
            external_points=np.array([self.model.initial_point]),
            bw_adjust=0.03,
            save_fig_path=save_fig_path_temp,
            return_figure=True
            )
        
        fig_forecast = self.model.forecast(method='LC', 
                    k=self.k,
                    cluster_method='kmeans',
                    name_scenario='clustering',
                    return_figure=True
                    )
        
        return fig_space, fig_forecast
    
    def conduct_numeric_analysis(self):
        return self.model.initial_point, self.model.t_stats