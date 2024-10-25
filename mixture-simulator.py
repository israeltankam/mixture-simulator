#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import hydralit_components as hc
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from model import modelTrajectories, diseaseIncidence, finalDiseaseIncidence, cropYield, distinctCropYield, yieldOptimizer, displayOptimal, displayDiseaseDynamics, plotYieldVsTheta, plotYieldVsThetaInteractive
from usefulFunctions import resistanceCategory
import edit_var
from edit_var import edit_tab
from settings import about_and_settings

# Set page layout to centered and responsive
# st.set_page_config(layout="wide")
st.set_page_config(layout='wide',initial_sidebar_state='collapsed')


# specify the primary menu definition
menu_data = [
    {'icon': "far fa-chart-bar", 'label':"Simulation"},#no tooltip message
    {'icon': "fas fa-seedling", 'label':"Select cultivars"},
    {'icon': "fas fa-tachometer-alt", 'label':"About & Parameters"},
]

over_theme = {'txc_inactive': '#FFFFFF', 'menu_background':'#85929E'}
st.markdown("## Cassava Mixture simulator")
main_tab= hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    #home_name='Introduction',
    #login_name='Logout',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

# Set default parameters
default_rho = 0.033
default_T = 360
default_theta = 1.0
# Set Plant parameters

st.session_state.setdefault("alpha_susc", 0.27)
st.session_state.setdefault("beta_susc", 132.21)
st.session_state.setdefault("alpha_res", 0.09)
st.session_state.setdefault("beta_res", 41.81)

#Default varieties selected in the cultivar editing tab (edit_var.py
if 'selected_first' not in st.session_state:
    st.session_state.setdefault("selected_first", 0)  # First variety selected in the grid
if 'selected_second' not in st.session_state:
    st.session_state.setdefault("selected_second", 1)  # Second variety selected in the grid
#Mixture distribution
st.session_state.setdefault("theta_A", default_theta)  # 50% of each variaty as default mixture

# Plant A parameters
#Susceptible 
if 'alpha_A' not in st.session_state:
    st.session_state.setdefault("alpha_A", st.session_state.alpha_susc)
if 'beta_A' not in st.session_state:
    st.session_state.setdefault("beta_A", st.session_state.beta_susc)
if 'yield_healthy_A' not in st.session_state:
    st.session_state.setdefault("yield_healthy_A", 31.0)
if 'yield_infected_A' not in st.session_state:
    st.session_state.setdefault("yield_infected_A", 18.6)
if 'gamma_A' not in st.session_state:
    st.session_state.setdefault("gamma_A", 0.071)
if 'category_A' not in st.session_state:
    st.session_state.setdefault("category_A", "Susceptible")
    



#st.markdown(st.session_state.alpha_A)
#st.markdown(st.session_state.alpha_B)

# Plant B parameters
if 'alpha_B' not in st.session_state:
    st.session_state.setdefault("alpha_B", st.session_state.alpha_res)
if 'beta_B' not in st.session_state:
    st.session_state.setdefault("beta_B", st.session_state.beta_res)
if 'yield_healthy_B' not in st.session_state:
    st.session_state.setdefault("yield_healthy_B", 25.0)
if 'yield_infected_B' not in st.session_state:
    st.session_state.setdefault("yield_infected_B", 15.0)
if 'gamma_B' not in st.session_state:
    st.session_state.setdefault("gamma_B", 0.071)
if 'category_B' not in st.session_state:
    st.session_state.setdefault("category_B", "Resistant")


# Insect parameters
st.session_state.setdefault("sigma", 0.45) # Dispersal parameter
st.session_state.setdefault("omega", 0.19) # Mortality parameter
st.session_state.setdefault("r", 0.0)  # Recovering parameter

# Insect abundance parameters
st.session_state.setdefault("f_very_low", 0.1) # Insect abundance per plant in low insect pressure
st.session_state.setdefault("f_low", 1.0) # Insect abundance per plant in low insect pressure
st.session_state.setdefault("f_medium", 5.0) # Insect abundance per plant in medium insect pressure
st.session_state.setdefault("f_high", 10.0) # Insect abundance per plant in high insect pressure

# Cassava growing parameters
st.session_state.setdefault("K", 10000) # Field density
if 'T' not in st.session_state:
    st.session_state.setdefault("T", default_T) # Season duration
if 'rho' not in st.session_state:
    st.session_state.setdefault("rho", default_rho) # Roguing rate
st.session_state.setdefault("roguing_compliance", 0) # Compliance to rogue
st.session_state.setdefault("absolute_roguing_rate", 0) # Equals to roguing compliance times roguing rate

# Selected pressure parameters
st.session_state.setdefault("f", st.session_state.f_very_low) # Insect abundance per plant


step = 0.01
                            

# Set Streamlit app title
# st.title("Cassava mixture")

def main():
    col1, col2, col3, col4 = st.columns([3, 3, 3, 4])
    with col1:
        st.markdown("### Mixture strategy")
        st.session_state.theta_A = st.slider(f"""Percentage of {st.session_state.category_A} Cultivar in the mixture (%):""", min_value=0.0, max_value=100.0, value=default_theta*100, step=0.1)/100
    with col2:
        if st.session_state.theta_A == 0.0:
            st.markdown(f"""### <br />""", unsafe_allow_html=True)
            st.markdown(f"""##### (Monoculture: {st.session_state.category_B})""")
        if st.session_state.theta_A == 1.0:
            st.markdown(f"""### <br />""", unsafe_allow_html=True)
            st.markdown(f"""##### (Monoculture: {st.session_state.category_A})""")
    with col4:
        st.markdown("### Insect and roguing details")
        subcol1, subcol2 = st.columns([1,1])
        with subcol1:
            insect_pressure_option_dic = {'Very low': 0,'Low': 1, 'Medium': 2, 'High': 3}
            selected_pressure = st.selectbox("Plant-wise insect burden", options=list(insect_pressure_option_dic.keys()))
            if insect_pressure_option_dic[selected_pressure] == 0:
                st.session_state.f = st.session_state.f_very_low
            elif insect_pressure_option_dic[selected_pressure] == 1:
                st.session_state.f = st.session_state.f_low
            elif insect_pressure_option_dic[selected_pressure] == 2:
                st.session_state.f = st.session_state.f_medium
            elif insect_pressure_option_dic[selected_pressure] == 3:
                st.session_state.f = st.session_state.f_high   
        with subcol2: 
            roguing_checkbox = st.checkbox("Roguing?")
            if roguing_checkbox:
                st.session_state.roguing_compliance = 1
                st.session_state.rho= 1/st.number_input("Days between roguing rounds", min_value=1, max_value=365, value=int(1/default_rho), step=1)
                st.session_state.absolute_roguing_rate = st.session_state.rho*st.session_state.roguing_compliance
            else:
                st.session_state.roguing_compliance = 0
                st.session_state.absolute_roguing_rate = 0
    st.markdown("<hr>", unsafe_allow_html=True)
        
    
    plotcol1, plotcol2, plotcol3 = st.columns([12,1,8])
    
    ##################################################################################################
    # plotting
    with plotcol1:
        st.markdown("## Your Mixture")
        displayDiseaseDynamics(st.session_state.theta_A, st.session_state)  
    #with plotcol3:
        #st.markdown("## Total yield vs Mixture")
        #plotYieldVsThetaInteractive(st.session_state)
        
    find_optimal_checkbox = st.checkbox("### Find the Optimal")
    if find_optimal_checkbox:
        theta , _ = yieldOptimizer(st.session_state)
        st.markdown("## Optimal Mixture")
        optcol1, optcol2 = st.columns([2,3])
        with optcol1:
            displayOptimal(theta, st.session_state)
        with optcol2:
            displayDiseaseDynamics(theta, st.session_state)
          
###################################################################################
if main_tab == "Select cultivars":
    st.session_state = edit_tab()
if main_tab == "Simulation":
    if st.session_state.selected_first == None or st.session_state.selected_second == None:
        st.markdown("## Select two cultivars in the nearby tab")
    else:
        main()
    
elif main_tab == "About & Parameters":
    st.session_state = about_and_settings()
    