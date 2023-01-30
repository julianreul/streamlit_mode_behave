import streamlit as st
import pandas as pd
import numpy as np
import time
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('MO|DE.behave')
   
add_text = st.sidebar.text(
    "Author: Julian Reul \
    \nInstitution: IEK-3, Forschungszentrum Jülich GmbH\
    \nE-Mail: j.reul@fz-juelich.de\
    \nGitHub: https://github.com/julianreul/mode_behave"
    )

st.markdown("MO|DE.behave is an open-source Python package for discrete choice modeling.")
   
st.markdown("""
    Discrete choice theory is used for the analysis
    of individual and aggregate choice behavior.
    Mixed logit models are a special type of discrete choice model,
    which enable the identification of preference or consumer groups
    in an observed base population.
    Discrete choice models use survey data of
    observed or stated choice as an input.
    """)
    
st.markdown("""
    You can upload your survey data according to the described format  
    within the documentation-section to derive and analyse  
    choice preferences within the observed base population.
    """)
    
#uploading data from local directory
uploaded_file = st.file_uploader("Upload your survey data as .csv-files")

st.markdown("___")

PATH_HOME = os.path.dirname(__file__)
sep = os.path.sep


if uploaded_file is not None:

    try:
        dataframe = pd.read_csv(uploaded_file, sep=";")
    except:
        raise AttributeError("Data in wrong format: Check file-format (.csv) and separator (;)")
         
    #Check column names to derive attributes
    col_names = dataframe.columns.values
    col_names_reduced = []
    for c in col_names:
        c_red = c[:-4]
        if c_red in ["choice", "av"]:
            continue
        else:
            col_names_reduced.append(c_red)
        
    col_names_reduced = list(set(col_names_reduced))    

    with st.form(key='Selecting Columns'):
        k_temp = st.number_input(
            'How many preference/consumer groups do you want to analyze? (float values will be rounded to integers.)', 
            value=2
            )
        
        options = st.multiselect(
            'Which attributes do you want to consider as model parameters?',
            col_names_reduced
            )        
        
        submit_button = st.form_submit_button(label='Confirm selection')

    if submit_button:
        
        st.text("Model estimation starts...")
        
        import mode_behave_public as mb 
     
        choice_cols = [col for col in col_names if col.startswith("choice")]
        #number of choice alternatives
        alt_temp = max([int(c[7]) for c in choice_cols])+1
        #number of equal choice alternatives
        equal_alt_temp = max([int(c[9]) for c in choice_cols])+1
                
        #derive param_temp and declare all attributes and random and variable.
        param_fixed = []
        param_random = col_names_reduced
    
        param_temp = {'constant': 
                          {
                           'fixed':[],
                           'random':[]
                           },
                      'variable':
                          {
                           'fixed': [],
                           'random':[]
                           }
                      }
    
        param_temp['variable']['fixed'] = param_fixed
        param_temp['variable']['random'] = param_random    
            
        #Initialize model
        model = mb.Core(
            param=param_temp, 
            data_in=dataframe, 
            alt=alt_temp, 
            equal_alt=equal_alt_temp
            )
    
        #estimate MXL model
        start = time.time()
        #estimate mixed logit model
        
        model.estimate_mixed_logit(
            min_iter=10, 
            max_iter=1000,
            tol=0.01,
            space_method = 'abs_value',
            scale_space = 2,
            max_shares = 1000,
            bits_64=True,
            t_stats_out=False
            )
        end = time.time()
        delta = int(end-start)
        text_temp = 'Estimation of mixed model took: ' + str(delta) + ' seconds.'
        st.text(text_temp)
    
        #Evaluation of MNL- and MXL-model
        text_temp = "LL-Ratio of MNL-model: " + str(model.loglike_MNL()[0])
        st.text(text_temp)
        text_temp = "LL-Ratio of MXL-model: " + str(model.loglike_MXL())
        st.text(text_temp)
        
        save_fig_path_temp = PATH_HOME + sep + "data"
    
        k_temp = int(round(k_temp, 0))
        
        st.markdown("___")
        st.header("1. Visualize parameter space")
        
        #visualize the preferences distribution   
        fig_space = model.visualize_space(
            k=k_temp, 
            scale_individual=True, 
            cluster_method='kmeans', 
            external_points=np.array([model.initial_point]),
            bw_adjust=0.03,
            save_fig_path=save_fig_path_temp,
            return_figure=True
            )
        
        st.pyplot(fig_space)
        
        st.markdown("___")
        st.header("2. Visualize simulation for each cluster")
        
        fig_forecast = model.forecast(method='LC', 
                    k=k_temp,
                    cluster_method='kmeans',
                    name_scenario='clustering',
                    return_figure=True
                    )
        
        st.pyplot(fig_forecast)