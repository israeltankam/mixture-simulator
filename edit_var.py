import streamlit as st

def edit_tab():
    if 'yh_susc' not in st.session_state:
        st.session_state.yh_susc = 31.0
    if 'yi_susc' not in st.session_state:
        st.session_state.yi_susc = 18.6
    if 'yh_res' not in st.session_state:
        st.session_state.yh_res = 25.0
    if 'yi_res' not in st.session_state:
        st.session_state.yi_res = 15.0
    if 'yh_tol' not in st.session_state:
        st.session_state.yh_tol = 25.0
    if 'yi_tol' not in st.session_state:
        st.session_state.yi_tol = 24.0

    # Define the data
    data = [
            {"type": "Susceptible", "alpha": st.session_state.alpha_susc, "beta": st.session_state.beta_susc, "yield_healthy": st.session_state.yh_susc, "yield_infected": st.session_state.yi_susc},
            {"type": "Resistant", "alpha": st.session_state.alpha_res, "beta": st.session_state.beta_res, "yield_healthy": st.session_state.yh_res, "yield_infected": st.session_state.yi_res},
            #{"type": "Resistant high yield", "alpha": 0.0124, "beta": 1.9442, "yield_healthy": 40, "yield_infected": 30},
            {"type": "Tolerant", "alpha": st.session_state.alpha_susc, "beta": st.session_state.beta_susc, "yield_healthy": st.session_state.yh_tol, "yield_infected": st.session_state.yi_tol},
            {"type": "Buffer", "alpha": 0.0, "beta": 0.0, "yield_healthy": 0.0, "yield_infected": 0.0},
    ]
    # Initialize session state variables if they don't exist
    if 'selected_first' not in st.session_state:
        st.session_state.selected_first = None
    if 'selected_second' not in st.session_state:
        st.session_state.selected_second = None

    if 'alpha_A' not in st.session_state:
        st.session_state.alpha_A = None
    if 'beta_A' not in st.session_state:
        st.session_state.beta_A = None
    if 'yield_healthy_A' not in st.session_state:
        st.session_state.yield_healthy_A = None
    if 'yield_infected_A' not in st.session_state:
        st.session_state.yield_infected_A = None
    if 'category_A' not in st.session_state:
        st.session_state.category_A = None
    if 'alpha_B' not in st.session_state:
        st.session_state.alpha_B = None
    if 'beta_B' not in st.session_state:
        st.session_state.beta_B = None
    if 'yield_healthy_B' not in st.session_state:
        st.session_state.yield_healthy_B = None
    if 'yield_infected_B' not in st.session_state:
        st.session_state.yield_infected_B = None
    if 'category_B' not in st.session_state:
        st.session_state.category_B = None
    _,col,_ = st.columns([1, 3, 1])
    with col:
        st.markdown("** _Click on two cultivar buttons to select them for the mixture. The selected cultivar cards will be displayed below, with 'Cultivar A' corresponding to the first button clicked and 'Cultivar B' to the second._")
    # Display the grid
    cols = st.columns(4) # +1 if I add a new variety
    for j in range(4):
        cell = data[j]
        type_initial = cell['type']
        btn_text = f"{type_initial}, Yield Healthy = {cell['yield_healthy']}, Yield Infected = {cell['yield_infected']}"
        
        # Determine if the button should be highlighted
        is_selected_first = (st.session_state.selected_first == j)
        is_selected_second = (st.session_state.selected_second == j)
        
        # Add emoji based on selection state
        #if is_selected_first or is_selected_second:
        #    btn_text += ' ⭐'
        
        # Use a unique key for each button
        key = f"button_{j}"
        
        # Render the button
        if cols[j].button(btn_text, key=key):
            if st.session_state.selected_first is None and st.session_state.selected_second is None:
                # Set the first button
                st.session_state.selected_first = j
                st.session_state.alpha_A = cell['alpha']
                st.session_state.beta_A = cell['beta']
                st.session_state.yield_healthy_A = cell['yield_healthy']
                st.session_state.yield_infected_A = cell['yield_infected']
                st.session_state.category_A = cell['type']
            elif st.session_state.selected_second is None and j != st.session_state.selected_first:
                # Set the second button
                st.session_state.selected_second = j
                st.session_state.alpha_B = cell['alpha']
                st.session_state.beta_B = cell['beta']
                st.session_state.yield_healthy_B = cell['yield_healthy']
                st.session_state.yield_infected_B = cell['yield_infected']
                st.session_state.category_B = cell['type']
            else:
                # Reset selection if a third button is clicked
                st.session_state.selected_first = j
                st.session_state.selected_second = None
                st.session_state.alpha_A = cell['alpha']
                st.session_state.beta_A = cell['beta']
                st.session_state.yield_healthy_A = cell['yield_healthy']
                st.session_state.yield_infected_A = cell['yield_infected']
                st.session_state.category_A = cell['type']
                st.session_state.alpha_B = None
                st.session_state.beta_B = None
                st.session_state.yield_healthy_B = None
                st.session_state.yield_infected_B = None
                st.session_state.category_B = None

    varcol1, varcol2, varcol3 = st.columns([1, 1, 4])
    with varcol1:
        if st.session_state.selected_first is not None:
            st.markdown(f"""
            <pre>
        <b>Cultivar A</b> <span style="background-color: #f4d46e;">({st.session_state.selected_first + 1})<span>
        <div style="border: 1px solid black; padding: 10px; margin-top: 5px;">
        <b>{data[st.session_state.selected_first]['type']} </b>
        <br />
        <b>Yield Healthy:</b> {st.session_state.yield_healthy_A} t/ha
        <br />
        <b>Yield Infected:</b> {st.session_state.yield_infected_A} t/ha
        <br />
        <b>Model parameters:</b> acquisition = {st.session_state.alpha_A}, inoculation = {st.session_state.beta_A}
            </pre>
        </div>
            """, unsafe_allow_html=True)
    with varcol2:
        if st.session_state.selected_second is not None:
            st.markdown(f"""
            <pre>
        <b>Cultivar B</b> <span style="background-color: #f4d46e;">({st.session_state.selected_second + 1}) </span>
        <div style="border: 1px solid black; padding: 10px; margin-top: 5px;">
        <b>{data[st.session_state.selected_second]['type']} </b>
        <br />
        <b>Yield Healthy:</b> {st.session_state.yield_healthy_B} t/ha
        <br />
        <b>Yield Infected:</b> {st.session_state.yield_infected_B} t/ha
        <br />
        <b>Model parameters:</b> acquisition = {st.session_state.alpha_B}, inoculation = {st.session_state.beta_B}
            </pre>
        </div>
            """, unsafe_allow_html=True)
    
    return st.session_state
