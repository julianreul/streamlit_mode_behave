import streamlit as st
import pandas as pd
import numpy as np

st.title('Documentation MO|DE.behave')

st.markdown("___")

st.header("Discrete Choice Modelling")

st.markdown("...some descriptions...")

st.markdown("___")

st.header("Correct Input Format")

st.markdown("Exemplary input data:")

df = pd.DataFrame(
   np.random.randn(10, 15),
   columns=[
       "choice_0_0",
       "choice_1_0",
       "choice_2_0",
       "av_0_0",
       "av_1_0",
       "av_2_0",
       "attr1_0_0",
       "attr1_1_0",
       "attr1_2_0",
       "attr2_0_0",
       "attr2_1_0",
       "attr2_2_0",
       "attr3_0_0",
       "attr3_1_0",
       "attr3_2_0",
       ]
   )

df["av_0_0"] = 1
df["av_1_0"] = 1
df["av_2_0"] = 1
df["choice_0_0"] = 1
df["choice_1_0"] = 0
df["choice_2_0"] = 0

st.table(df)

st.markdown(
    """
    - **Each row** represents a **single observation** from an observed- or stated-preference survey.
    - There are three **types of columns**:
        1. Choice-columns (choice_x_y), indicating, which choice alternative has been chosen in the respective observation.
        2. Availability-columns (av_x_y), indicating, if a choice alternative was available during the observation.
        3. Attribute-columns (attribute_name_x_y), indicating the value of the respective attribute of the choice option or the decision maker.
    - **Each column** has **two suffixes**:  
        1. The first suffix (_x) counts the choice alternative.
        2. The second suffix (_y) counts the number of equal choice alternatives.
        Exemplary choice options: 2 apples and 1 banana.
        This would result in the following choice- and av-columns:
        - choice_0_0 (first apple), choice_0_1 (second apple), choice_1_0 (first banana)
        - av_0_0 (first apple), av_0_1 (second apple), av_1_0 (first banana)
    - The values in **choice- and av-columns** are either 0 (not chosen/not available) or 1 (has been chosen/was available). 
    - The values in the **attribute-colums** either describe the choice options (e.g. color of an apple) or the decision-maker (e.g. age of the decision-maker).  
      An attribute which describes the decision-maker is equal across all choice options.
      Exemplary choice options: 2 apples and 1 banana.
      - e.g., columns for attribute age: age_0_0 = 28, age_0_1 = 28, age_1_0 = 28,
        Indicating, that the age of the decision-maker was 28 for all choice options, since it was the same person.
    - **Summary**: 
        - The input data should contain **three types of columns**: Choice-, availability-, and attribute-columns.
        - There should be **one row for each survey-observation**.
        - The input data should contain the following **number of choice- and availability columns**: no_choice_alternatives*max(no_equal_choice_alternatives)
        - The input data should contain the following **number of attribute-columns**: no_choice_alternatives*max(no_equal_choice_alternatives)*no_attributes
    """
    )
