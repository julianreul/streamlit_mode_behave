import streamlit as st
import pandas as pd
import numpy as np
import os

from functionality import Function

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

    choice_cols = [col for col in col_names if col.startswith("choice")]
    #number of choice alternatives
    alt_temp = max([int(c[7]) for c in choice_cols])+1
    #number of equal choice alternatives
    equal_alt_temp = max([int(c[9]) for c in choice_cols])+1

    with st.form(key='Selecting Columns'):
        k_temp = st.number_input(
            'How many preference/consumer groups do you want to analyze? (float values will be rounded to integers.)', 
            value=2
            )
        
        options = st.multiselect(
            'Which attributes do you want to consider as model parameters?',
            col_names_reduced
            )        
        
        st.markdown("Which type of analysis do you want to conduct?")
        
        visual_analysis = st.checkbox("Visual analysis")
        numeric_analysis = st.checkbox("Numeric analysis")
        
        submit_button = st.form_submit_button(label='Confirm selection')

    if submit_button:
        
        st.text("Model estimation starts...")
        
        #derive param_temp and declare all attributes and random and variable.
        param_fixed = []
        param_random = options

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

        
        function_ = Function(
            dataframe, 
            alt_temp, 
            equal_alt_temp, 
            param_temp, 
            k_temp, 
            numeric_analysis
            )
        
        function_.estimate_model()
        
        LL_MNL, LL_MXL = function_.get_likelihood()
    
        #Evaluation of MNL- and MXL-model
        text_temp = "LL-Ratio of MNL-model: " + str(LL_MNL)
        st.text(text_temp)
        text_temp = "LL-Ratio of MXL-model: " + str(LL_MXL)
        st.text(text_temp)
        
        #NUMERIC ANALYSIS
        if numeric_analysis:
            initial_point, t_stats = function_.conduct_numeric_analysis()
            #WORK ON THE CODE BELOW: 1) Provide a human-readable table with results. 2) Implement a download button for this table.
            st.write(initial_point)       
        
        #VISUAL ANALYSIS
        if visual_analysis:
            
            st.markdown("___")
            st.header("1. Visualize parameter space")

            fig_space, fig_forecast = function_.conduct_visual_analysis()
            
            st.pyplot(fig_space)
            
            st.markdown("___")
            st.header("2. Visualize simulation for each cluster")
            
            st.pyplot(fig_forecast)

