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
from model import modelTrajectories, diseaseIncidence, finalDiseaseIncidence, cropYield, distinctCropYield, yieldOptimizer, displayOptimal, displayDiseaseDynamics
from usefulFunctions import resistanceCategory
import edit_var
from edit_var import edit_tab

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


# Set Plant parameters

#Default varieties selected in the cultivar editing tab (edit_var.py
st.session_state.setdefault("selected_first", (0, 1))  # First variety selected in the grid
st.session_state.setdefault("selected_second", (3, 6))  # Second variety selected in the grid
#Mixture distribution
st.session_state.setdefault("theta_A", 0.5)  # 50% of each variaty as default mixture

# Plant A parameters
st.session_state.setdefault("alpha_A", 0.0124)  # Acquisition rate
st.session_state.setdefault("beta_A", 6.9442)  # Inoculation rate
st.session_state.setdefault("yield_healthy_A", 40) # Average yield when healthy
st.session_state.setdefault("yield_diseased_A", 20) # Average yield when diseased
st.session_state.setdefault("gamma_A", 0.033)  # Latency speed
st.session_state.setdefault("d_A", 1.0)  # Detection probability
st.session_state.setdefault("category_A", "Susceptible")  # Resistance category

#st.markdown(st.session_state.alpha_A)
#st.markdown(st.session_state.alpha_B)

# Plant B parameters
st.session_state.setdefault("alpha_B", 0.0052)  # Acquisition rate
st.session_state.setdefault("beta_B", 3.5635)  # Inoculation rate
st.session_state.setdefault("yield_healthy_B", 35) # Average yield when healthy
st.session_state.setdefault("yield_diseased_B", 28) # Average yield when diseased
st.session_state.setdefault("gamma_B", 0.033)  # Latency speed
st.session_state.setdefault("d_B", 0.6571)  # Detection probability
st.session_state.setdefault("category_B", "Resistant")  # Resistance category


# Insect parameters
st.session_state.setdefault("sigma", 0.45) # Dispersal parameter
st.session_state.setdefault("omega", 0.19) # Mortality parameter
st.session_state.setdefault("r", 0.0)  # Recovering parameter

# Insect abundance parameters
st.session_state.setdefault("f_very_low", 0.1) # Insect abundance per plant in very low insect pressure
st.session_state.setdefault("f_low", 1.0) # Insect abundance per plant in low insect pressure
st.session_state.setdefault("f_medium", 5.0) # Insect abundance per plant in medium insect pressure
st.session_state.setdefault("f_high", 10.0) # Insect abundance per plant in high insect pressure
st.session_state.setdefault("f_very_high", 50.0) # Insect abundance per plant in  very high insect pressure

# Cassava growing parameters
st.session_state.setdefault("K", 10000) # Field density
st.session_state.setdefault("T", 270) # Season duration
st.session_state.setdefault("rho", 0.033) # Roguing rate
st.session_state.setdefault("roguing_compliance", 0) # Compliance to rogue
st.session_state.setdefault("absolute_roguing_rate", 0) # Equals to roguing compliance times roguing rate

# Selected pressure parameters
st.session_state.setdefault("f", st.session_state.f_very_low) # Insect abundance per plant


step = 0.01
                            

# Set Streamlit app title
# st.title("Cassava mixture")

def main():
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.markdown("### Mixture strategy")
        st.session_state.theta_A = st.slider("Percentage of cultivar A in the mixture (%):", min_value=0.0, max_value=100.0, value=st.session_state.theta_A*100, step=0.1)/100
    #with col3:
    #    st.session_state.K = st.slider("Field density (plants/ha):", min_value=8000, max_value=15000, value=st.session_state.K, step=500)
    with col3:
        st.markdown("### Insect and season details")
        subcol1, subcol2, subcol3 = st.columns([1,1,1])
        with subcol1:
            insect_pressure_option_dic = {'Very low': 0, 'Low': 1, 'Medium': 2, 'High': 3, 'Very high': 4}
            selected_pressure = st.selectbox("Plant-wise insect burden", options=list(insect_pressure_option_dic.keys()))
            if insect_pressure_option_dic[selected_pressure] == 0:
                st.session_state.f = st.session_state.f_very_low
            elif insect_pressure_option_dic[selected_pressure] == 1:
                st.session_state.f = st.session_state.f_low
            elif insect_pressure_option_dic[selected_pressure] == 2:
                st.session_state.f = st.session_state.f_medium
            elif insect_pressure_option_dic[selected_pressure] == 3:
                st.session_state.f = st.session_state.f_high
            elif insect_pressure_option_dic[selected_pressure] == 4:
                st.session_state.f = st.session_state.f_very_high
        with subcol2:
            st.session_state.T = st.number_input("Season duration (days):", min_value=180, max_value=500, value=st.session_state.T, step=1)
        with subcol3: 
            roguing_checkbox = st.checkbox("Roguing?")
            if roguing_checkbox:
                st.session_state.roguing_compliance = 1
                st.session_state.rho= 1/st.number_input("Days between roguing rounds", min_value=1, max_value=365, value=int(1/st.session_state.rho), step=1)
                st.session_state.absolute_roguing_rate = st.session_state.rho*st.session_state.roguing_compliance
            else:
                st.session_state.roguing_compliance = 0
                st.session_state.absolute_roguing_rate = 0
    st.markdown("<hr>", unsafe_allow_html=True)
        
    
    plotcol1, plotcol2, plotcol3 = st.columns([12,1,8])
    
    ##################################################################################################
    # plotting
    theta , _ = yieldOptimizer(st.session_state)
    with plotcol1:
        st.markdown("## Your Mixture")
        displayDiseaseDynamics(st.session_state.theta_A, st.session_state)    
    with plotcol3:
        st.markdown("## Optimal Mixture")
        displayOptimal(theta, st.session_state)
    
###################################################################################
if main_tab == "Select cultivars":
    edit_tab()
if main_tab == "Simulation":
    if st.session_state.selected_first == None or st.session_state.selected_second == None:
        st.markdown("## Select two cultivars in the nearby tab")
    else:
        main()
    

   # _, col1, col2, _ = st.columns([1, 5, 5, 1])
   # with col1:
   #     st.markdown("### Variety A")
   #     st.session_state.alpha_A= st.slider("Acquisition rate A", min_value=0.0, max_value=1.0, value=st.session_state.alpha_A, step=0.01)
   #     st.session_state.beta_A= st.slider("Inoculation rate A", min_value=0.0, max_value=1.0, value=st.session_state.beta_A, step=0.01)
   #     st.session_state.gamma_A= 1/st.slider("Latency duration A(days)", min_value=0, max_value=40, value=int(1/st.session_state.gamma_A), step=1)
   #     st.session_state.d_A= st.slider("Detection probability A", min_value=0.0, max_value=1.0, value=st.session_state.d_A, step=0.05)
   #     st.session_state.yield_healthy_A= st.slider("Yield when healthy A(ton/ha)", min_value=0, max_value=100, value=st.session_state.yield_healthy_A, step=1)
   #     st.session_state.yield_diseased_A= st.slider("Yield when infected A(ton/ha)", min_value=0, max_value=100, value=st.session_state.yield_diseased_A, step=1)
   # with col2:
   #     st.markdown("### Variety B")
   #     st.session_state.alpha_B= st.slider("Acquisition rate B", min_value=0.0, max_value=1.0, value=st.session_state.alpha_B, step=0.01)
   #     st.session_state.beta_B= st.slider("Inoculation rate B", min_value=0.0, max_value=1.0, value=st.session_state.beta_B, step=0.01)
   #     st.session_state.gamma_B= 1/st.slider("Latency duration B(days)", min_value=0, max_value=40, value=int(1/st.session_state.gamma_B), step=1)
   #     st.session_state.d_B= st.slider("Detection probability B", min_value=0.0, max_value=1.0, value=st.session_state.d_B, step=0.05)
   #     st.session_state.yield_healthy_B= st.slider("Yield when healthy B(ton/ha)", min_value=0, max_value=100, value=st.session_state.yield_healthy_B, step=1)
   #     st.session_state.yield_diseased_B= st.slider("Yield when infected B(ton/ha)", min_value=0, max_value=100, value=st.session_state.yield_diseased_B, step=1)
    
elif main_tab == "About & Parameters":
    col1, col2, _ = st.columns([3, 10, 8])
    with col1:
        st.markdown("# About")
    with col2:
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("- The model consider a mixture of two cassava cultivars named 'Cultivar A' and 'Cultivar B' ")
        st.markdown("- The plant cultivars can be selected in the 'Select cultivar' tab and they differ by their resistance status and yields")
        st.markdown("- We assume a constant plant-wise insect abundance in the locality")
        st.markdown("- We assume an initial disease inoculum of 1 plant on 10 000")
        st.markdown("- Insect are initially all virus-free")
    col1, col2, _ = st.columns([3, 10, 8])
    with col1:
        st.markdown("# Parameter settings")
    with col2:
        st.markdown("# ")
        st.markdown("### Insect parameters ")
        st.session_state.sigma = st.slider("Insect dispersal rate $\sigma$:", min_value=0.0, max_value=1.0, value=st.session_state.sigma, step=0.01)
        st.session_state.omega = st.slider("Insect mortality rate $\omega$:", min_value=0.0, max_value=1.0, value=st.session_state.omega, step=0.01)
        st.session_state.r = st.slider("Insect recovery rate $r$:", min_value=0.0, max_value=1.0, value=st.session_state.r, step=0.01)
        
        st.markdown("### Insect abundance setup")
        st.session_state.f_very_low = st.slider("Insect abundance per plant in very low insect pressure:", min_value=0.0, max_value=5.0, value=st.session_state.f_very_low, step=0.1)
        st.session_state.f_low = st.slider("Insect abundance per plant in low insect pressure:", min_value=0.0, max_value=10.0, value=st.session_state.f_low, step=0.1)
        st.session_state.f_medium = st.slider("Insect abundance per plant in medium insect pressure:", min_value=0.0, max_value=50.0, value=st.session_state.f_medium, step=1.0)
        st.session_state.f_high = st.slider("Insect abundance per plant in high insect pressure:", min_value=0.0, max_value=200.0, value=st.session_state.f_high, step=1.0)
        st.session_state.f_very_high = st.slider("Insect abundance per plant in  very high insect pressure:", min_value=0.0, max_value=500.0, value=st.session_state.f_very_high, step=1.0)