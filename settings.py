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
    col1, col2, _ = st.columns([3, 10, 8])
    with col1:
        st.markdown("# Parameter settings")
    with col2:
        st.markdown("### Variety yields")
        settings_cols = st.columns(3)
        with settings_cols[0]:
            st.session_state.yh_susc = st.slider("Yield of **susceptible** variety when **healthy**:", min_value=5.0, max_value=60.0, value=31.0, step=0.1)
            st.session_state.yi_susc = st.slider("Yield of **susceptible** variety when **infected**:", min_value=5.0, max_value=st.session_state.yh_susc, value=18.6, step=0.1)
        with settings_cols[1]:
            st.session_state.yh_res = st.slider("Yield of **resistant** variety when **healthy**:", min_value=5.0, max_value=60.0, value=25.0, step=0.1)
            st.session_state.yi_res = st.slider("Yield of **resistant** variety when **infected**:", min_value=5.0, max_value=st.session_state.yh_res, value=15.0, step=0.1)
        with settings_cols[2]:
            st.session_state.yh_tol = st.slider("Yield of **tolerant** variety when **healthy**:", min_value=5.0, max_value=60.0, value=31.0, step=0.1)
            st.session_state.yi_tol = st.slider("Yield of **tolerant** variety when **infected**:", min_value=5.0, max_value=st.session_state.yh_tol, value=27.9, step=0.1)
            
        st.markdown("### Season duration")
        st.session_state.T = st.number_input("Season duration (days):", min_value=180, max_value=500, value=default_T, step=1)
        
        st.markdown("### Insect parameters ")
        st.session_state.sigma = st.slider("Insect dispersal rate $\sigma$:", min_value=0.0, max_value=1.0, value=st.session_state.sigma, step=0.01)
        st.session_state.omega = st.slider("Insect mortality rate $\omega$:", min_value=0.0, max_value=1.0, value=st.session_state.omega, step=0.01)
        st.session_state.r = st.slider("Insect recovery rate $r$:", min_value=0.0, max_value=1.0, value=st.session_state.r, step=0.01)
        
        st.markdown("### Insect abundance setup")
        st.session_state.f_low = st.slider("Insect abundance per plant in low insect pressure:", min_value=0.0, max_value=10.0, value=st.session_state.f_low, step=0.1)
        st.session_state.f_medium = st.slider("Insect abundance per plant in medium insect pressure:", min_value=0.0, max_value=20.0, value=st.session_state.f_medium, step=1.0)
        st.session_state.f_high = st.slider("Insect abundance per plant in high insect pressure:", min_value=0.0, max_value=100.0, value=st.session_state.f_high, step=1.0)
    return st.session_state