import streamlit as st

default_T = 360
def about_and_settings():
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
        checkbox = st.checkbox("See more modelling details")
        if checkbox:
            image1_path = "figs/diagram.png"
            st.image(image1_path)
            st.markdown("""
| Event                                      | Flow between compartments | Rate                                              |
|--------------------------------------------|---------------------------|---------------------------------------------------|
| **Inoculation**   🌿                         | $S_A \\longrightarrow L_A$ | $\\beta^A *$ #infectious vectors feeding on $S^A$ |
|                                            | $S_B \\longrightarrow L_B$ | $\\beta^B *$ #infectious vectors feeding on $S^B$ |
| **Incubation (onset of plant infectiousness)**   🌿 | $L_A \\longrightarrow I_A$ | $\\gamma * L_A$                                   |
|                                            | $L_B \\longrightarrow I_B$ | $\\gamma * L_B$                                   |
| **Roguing**   🌿                             | $I_A \\longrightarrow S_A$ | $\\rho * I_A$                                     |
|                                            | $I_B \\longrightarrow S_B$ | $\\rho * I_B$                                     |
| **Aquisition**   🪰                          | $\\longrightarrow V^A$     | $\\alpha^A *$ #virus-free insects on $I_A$        |
|                                            | $\\longrightarrow V^B$     | $\\alpha^B *$ #virus-free insects on $I_B$        |
| **Recovery**    🪰                           | $V^A \\longrightarrow$     | $r * V^A$                                         |
|                                            | $V^B \\longrightarrow$     | $r * V^B$                                         |
| **Insect mortality**   🪰                    | $V^A \\longrightarrow$     | $\\omega * V^A$                                   |
|                                            | $V^B \\longrightarrow$     | $\\omega * V^B$                                   |
""")
    col1, col2, _ = st.columns([4, 11, 9])
    with col1:
        st.markdown("# Parameter settings")
    with col2:
        st.markdown("### Variety-wise epidemiological parameters")
        st.markdown("** _These settings entirely define the disease considered. After you configure this, you have to reselect the cultivars before going back to the simulation._")
        quick_menu_cols = st.columns(2)
        with quick_menu_cols[0]:
            disease_option_dic = {'- Default -': 0,'CMD': 1, 'CBSD': 2}
            selected_disease = st.selectbox("**Quick disease selection**", options=list(disease_option_dic.keys()))
            if disease_option_dic[selected_disease] == 1:
                st.session_state.alpha_susc = 0.27
                st.session_state.beta_susc = 132.21
                st.session_state.alpha_res = 0.09
                st.session_state.beta_res = 41.81
                st.session_state.r = 0.0
                st.session_state.yi_susc = 18.6
                st.session_state.yi_res = 15
                st.session_state.yi_tol = 24
            elif disease_option_dic[selected_disease] == 2:
                st.session_state.alpha_susc = 68.88
                st.session_state.beta_susc = 1.19
                st.session_state.alpha_res = 21.78
                st.session_state.beta_res = 0.38
                st.session_state.r = 28.08
                st.session_state.yi_susc = 3.1
                st.session_state.yi_res = 2.1
                st.session_state.yi_tol = 20.25

        epi_cols = st.columns(2)
        with epi_cols[0]:
            st.session_state.alpha_susc = st.number_input("**Acquisition** rate on **suceptible and tolerant**:", min_value=0.01, max_value=2500.0, value=st.session_state.alpha_susc, step=0.01, format="%.2f")
            st.session_state.beta_susc = st.number_input("**Inoculation** rate on **suceptible and tolerant**:", min_value=0.01, max_value=2500.0, value=st.session_state.beta_susc, step=0.01, format="%.2f")
        with epi_cols[1]:
            st.session_state.alpha_res = st.number_input("**Acquisition** rate on **resistant**:", min_value=0.01, max_value=2500.0, value=st.session_state.alpha_res, step=0.01, format="%.2f")
            st.session_state.beta_res = st.number_input("**Inoculation** rate on **resistant**:", min_value=0.01, max_value=2500.0, value=st.session_state.beta_res, step=0.01, format="%.2f")
        st.markdown("---")
        st.markdown("### Variety yields")
        
        yield_cols = st.columns(3)
        with yield_cols[0]:
            st.session_state.yh_susc = st.number_input("Yield of **susceptible** variety when **healthy**:", min_value=5.0, max_value=60.0, value=31.0, step=0.1, format="%.1f")
            st.session_state.yi_susc = st.number_input("Yield of **susceptible** variety when **infected**:", min_value=5.0, max_value=st.session_state.yh_susc, value=18.6, step=0.1, format="%.1f")
        with yield_cols[1]:
            st.session_state.yh_res = st.number_input("Yield of **resistant** variety when **healthy**:", min_value=5.0, max_value=60.0, value=25.0, step=0.1, format="%.1f")
            st.session_state.yi_res = st.number_input("Yield of **resistant** variety when **infected**:", min_value=5.0, max_value=st.session_state.yh_res, value=15.0, step=0.1, format="%.1f")
        with yield_cols[2]:
            st.session_state.yh_tol = st.number_input("Yield of **tolerant** variety when **healthy**:", min_value=5.0, max_value=60.0, value=25.0, step=0.1, format="%.1f")
            st.session_state.yi_tol = st.number_input("Yield of **tolerant** variety when **infected**:", min_value=5.0, max_value=st.session_state.yh_tol, value=24.0, step=0.1, format="%.1f")
        st.markdown("---")
        
        st.markdown("### Season duration")
        st.session_state.T = st.number_input("Season duration (days):", min_value=180, max_value=500, value=default_T, step=1)
        st.markdown("---")
        
        st.markdown("### Insect parameters ")
        st.session_state.sigma = st.number_input("Insect dispersal rate $\sigma$:", min_value=0.0, max_value=1.0, value=st.session_state.sigma, step=0.01, format="%.2f")
        st.session_state.omega = st.number_input("Insect mortality rate $\omega$:", min_value=0.0, max_value=1.0, value=st.session_state.omega, step=0.01, format="%.2f")
        st.session_state.r = st.number_input("Insect recovery rate $r$:", min_value=0.0, max_value=100.0, value=st.session_state.r, step=0.1, format="%.2f") 
        st.markdown("---")
        
        st.markdown("### Insect abundance setup")
        st.session_state.f_very_low = st.number_input("Insect abundance per plant in very low insect pressure:", min_value=0.0, max_value=1.0, value=st.session_state.f_very_low, step=0.1, format="%.2f")
        st.session_state.f_low = st.number_input("Insect abundance per plant in low insect pressure:", min_value=0.0, max_value=10.0, value=st.session_state.f_low, step=0.1, format="%.2f")
        st.session_state.f_medium = st.number_input("Insect abundance per plant in medium insect pressure:", min_value=0.0, max_value=20.0, value=st.session_state.f_medium, step=1.0, format="%.2f")
        st.session_state.f_high = st.number_input("Insect abundance per plant in high insect pressure:", min_value=0.0, max_value=100.0, value=st.session_state.f_high, step=1.0, format="%.2f")
    return st.session_state