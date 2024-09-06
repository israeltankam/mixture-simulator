import streamlit as st

# Define the data
data = [
    # Line 1
    [
        {"type": "Susceptible", "alpha": 0.0141, "beta": 7.0991, "d": 1.0000, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Susceptible", "alpha": 0.0124, "beta": 6.9442, "d": 1.0000, "yield_healthy": 40, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0143, "beta": 5.1064, "d": 1.0000, "yield_healthy": 40, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0092, "beta": 6.4704, "d": 1.0000, "yield_healthy": 40, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0095, "beta": 4.8070, "d": 1.0000, "yield_healthy": 34, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0081, "beta": 3.9568, "d": 1.0000, "yield_healthy": 40, "yield_diseased": 20},
        {"type": "Resistant", "alpha": 0.0055, "beta": 3.3491, "d": 1.0000, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Resistant", "alpha": 0.0037, "beta": 1.3430, "d": 1.0000, "yield_healthy": 33, "yield_diseased": 25}
    ],
    # Line 2
    [
        {"type": "Susceptible", "alpha": 0.0153, "beta": 6.5349, "d": 0.8857, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0152, "beta": 5.6766, "d": 0.8857, "yield_healthy": 40, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0131, "beta": 5.5624, "d": 0.8857, "yield_healthy": 40, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0082, "beta": 7.2224, "d": 0.8857, "yield_healthy": 34, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0121, "beta": 3.7714, "d": 0.8857, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Susceptible", "alpha": 0.0074, "beta": 4.3595, "d": 0.8857, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Resistant", "alpha": 0.0058, "beta": 3.1923, "d": 0.8857, "yield_healthy": 35, "yield_diseased": 30},
        {"type": "Resistant", "alpha": 0.0037, "beta": 1.3438, "d": 0.8857, "yield_healthy": 32, "yield_diseased": 15}
    ],
    # Line 3
    [
        {"type": "Susceptible", "alpha": 0.0114, "beta": 8.7961, "d": 0.7714, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0123, "beta": 7.0291, "d": 0.7714, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Susceptible", "alpha": 0.0099, "beta": 7.3833, "d": 0.7714, "yield_healthy": 34, "yield_diseased": 28},
        {"type": "Susceptible", "alpha": 0.0101, "beta": 5.8586, "d": 0.7714, "yield_healthy": 40, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0067, "beta": 6.7727, "d": 0.7714, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0080, "beta": 3.9991, "d": 0.7714, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Resistant", "alpha": 0.0065, "beta": 2.8745, "d": 0.7714, "yield_healthy": 40, "yield_diseased": 25},
        {"type": "Resistant", "alpha": 0.0035, "beta": 1.4408, "d": 0.7714, "yield_healthy": 40, "yield_diseased": 15}
    ],
    # Line 4
    [
        {"type": "Susceptible", "alpha": 0.0161, "beta": 6.1935, "d": 0.6571, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Susceptible", "alpha": 0.0110, "beta": 7.8794, "d": 0.6571, "yield_healthy": 34, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0123, "beta": 5.9388, "d": 0.6571, "yield_healthy": 34, "yield_diseased": 28},
        {"type": "Susceptible", "alpha": 0.0107, "beta": 5.5356, "d": 0.6571, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0089, "beta": 5.1175, "d": 0.6571, "yield_healthy": 34, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0095, "beta": 3.3674, "d": 0.6571, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Resistant", "alpha": 0.0052, "beta": 3.5635, "d": 0.6571, "yield_healthy": 35, "yield_diseased": 28},
        {"type": "Resistant", "alpha": 0.0026, "beta": 1.8944, "d": 0.6571, "yield_healthy": 34, "yield_diseased": 30}
    ],
    # Line 5
    [
        {"type": "Susceptible", "alpha": 0.0151, "beta": 6.6416, "d": 0.5429, "yield_healthy": 34, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0150, "beta": 5.7656, "d": 0.5429, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0120, "beta": 6.0763, "d": 0.5429, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Susceptible", "alpha": 0.0136, "beta": 4.3645, "d": 0.5429, "yield_healthy": 34, "yield_diseased": 30},
        {"type": "Susceptible", "alpha": 0.0090, "beta": 5.0950, "d": 0.5429, "yield_healthy": 34, "yield_diseased": 20},
        {"type": "Susceptible", "alpha": 0.0073, "beta": 4.4229, "d": 0.5429, "yield_healthy": 34, "yield_diseased": 28},
        {"type": "Resistant", "alpha": 0.0052, "beta": 3.5464, "d": 0.5429, "yield_healthy": 34, "yield_diseased": 15},
        {"type": "Resistant", "alpha": 0.0032, "beta": 1.5824, "d": 0.5429, "yield_healthy": 40, "yield_diseased": 28}
    ],
    # Line 6
    [
        {"type": "Tolerant", "alpha": 0.0154, "beta": 6.4777, "d": 0.4286, "yield_healthy": 33, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0124, "beta": 6.9796, "d": 0.4286, "yield_healthy": 40, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0142, "beta": 5.1224, "d": 0.4286, "yield_healthy": 40, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0101, "beta": 5.8793, "d": 0.4286, "yield_healthy": 33, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0088, "beta": 5.2202, "d": 0.4286, "yield_healthy": 33, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0097, "beta": 3.2988, "d": 0.4286, "yield_healthy": 33, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0053, "beta": 3.4846, "d": 0.4286, "yield_healthy": 40, "yield_diseased": 30},
        {"type": "Tolerant", "alpha": 0.0029, "beta": 1.7161, "d": 0.4286, "yield_healthy": 40, "yield_diseased": 30}
    ],
    # Line 7
    [
        {"type": "Tolerant", "alpha": 0.0120, "beta": 8.3299, "d": 0.3143, "yield_healthy": 33, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0139, "beta": 6.2115, "d": 0.3143, "yield_healthy": 33, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0114, "beta": 6.4163, "d": 0.3143, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0114, "beta": 5.2181, "d": 0.3143, "yield_healthy": 33, "yield_diseased": 30},
        {"type": "Tolerant", "alpha": 0.0128, "beta": 3.5730, "d": 0.3143, "yield_healthy": 33, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0088, "beta": 3.6380, "d": 0.3143, "yield_healthy": 33, "yield_diseased": 20},
        {"type": "Tolerant", "alpha": 0.0069, "beta": 2.6830, "d": 0.3143, "yield_healthy": 32, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0026, "beta": 1.9163, "d": 0.3143, "yield_healthy": 40, "yield_diseased": 25}
    ],
    # Line 8
    [
        {"type": "Tolerant", "alpha": 0.0154, "beta": 6.4746, "d": 0.2000, "yield_healthy": 33, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0139, "beta": 6.2201, "d": 0.2000, "yield_healthy": 40, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0157, "beta": 4.6528, "d": 0.2000, "yield_healthy": 33, "yield_diseased": 30},
        {"type": "Tolerant", "alpha": 0.0128, "beta": 4.6141, "d": 0.2000, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0081, "beta": 5.6571, "d": 0.2000, "yield_healthy": 40, "yield_diseased": 25},
        {"type": "Tolerant", "alpha": 0.0072, "beta": 4.4686, "d": 0.2000, "yield_healthy": 40, "yield_diseased": 28},
        {"type": "Tolerant", "alpha": 0.0059, "beta": 3.1738, "d": 0.2000, "yield_healthy": 40, "yield_diseased": 20},
        {"type": "Tolerant", "alpha": 0.0031, "beta": 1.6319, "d": 0.2000, "yield_healthy": 40, "yield_diseased": 30}
    ]
]

def edit_tab():
    # Initialize session state variables if they don't exist
    if 'selected_first' not in st.session_state:
        # Default to (1,2) if not set
        st.session_state.selected_first = (0, 1)
        # Set default values for Variety A
        cell = data[1][2]
        st.session_state.alpha_A = cell['alpha']
        st.session_state.beta_A = cell['beta']
        st.session_state.d_A = cell['d']
        st.session_state.yield_healthy_A = cell['yield_healthy']
        st.session_state.yield_diseased_A = cell['yield_diseased']
        st.session_state.category_A = cell['type']
    if 'selected_second' not in st.session_state:
        # Default to (5,7) if not set
        st.session_state.selected_second = (3, 6)
        # Set default values for Variety B
        cell = data[5][7]
        st.session_state.alpha_B = cell['alpha']
        st.session_state.beta_B = cell['beta']
        st.session_state.d_B = cell['d']
        st.session_state.yield_healthy_B = cell['yield_healthy']
        st.session_state.yield_diseased_B = cell['yield_diseased']
        st.session_state.category_B = cell['type']
    if 'alpha_A' not in st.session_state:
        st.session_state.alpha_A = None
    if 'beta_A' not in st.session_state:
        st.session_state.beta_A = None
    if 'd_A' not in st.session_state:
        st.session_state.d_A = None
    if 'yield_healthy_A' not in st.session_state:
        st.session_state.yield_healthy_A = None
    if 'yield_diseased_A' not in st.session_state:
        st.session_state.yield_diseased_A = None
    if 'alpha_B' not in st.session_state:
        st.session_state.alpha_B = None
    if 'beta_B' not in st.session_state:
        st.session_state.beta_B = None
    if 'd_B' not in st.session_state:
        st.session_state.d_B = None
    if 'yield_healthy_B' not in st.session_state:
        st.session_state.yield_healthy_B = None
    if 'yield_diseased_B' not in st.session_state:
        st.session_state.yield_diseased_B = None
    if 'yield_category_A' not in st.session_state:
        st.session_state.yield_category_A = None
    if 'yield_category_B' not in st.session_state:
        st.session_state.yield_category_B = None

    st.markdown("* Sus = Susceptible, Res = Resistant, Tol = Tolerant, YH = Yield when Healthy, YD = Yield when diseased")
    st.markdown("$\downarrow$ Increasing tolerance $\qquad$ Increasing resistance $\longrightarrow$")
    # Display the grid
    for i in range(8):
        cols = st.columns(8)
        for j in range(8):
            cell = data[i][j]
            # Truncate the type to its first letter
            type_initial = cell['type'][0:3]
            btn_text = f"--{type_initial}-- YH = {cell['yield_healthy']}, YD = {cell['yield_diseased']}"
            
            # Determine if the button should be highlighted
            is_selected_first = (st.session_state.selected_first == (i, j))
            is_selected_second = (st.session_state.selected_second == (i, j))
            
            # Add emoji based on selection state
            if is_selected_first or is_selected_second:
                btn_text += ' ⭐'
            
            # Use a unique key for each button
            key = f"button_{i}_{j}"
            
            # Render the button
            if cols[j].button(btn_text, key=key):
                if st.session_state.selected_first is None:
                    # Set the first button
                    st.session_state.selected_first = (i, j)
                    st.session_state.alpha_A = cell['alpha']
                    st.session_state.beta_A = cell['beta']
                    st.session_state.d_A = cell['d']
                    st.session_state.yield_healthy_A = cell['yield_healthy']
                    st.session_state.yield_diseased_A = cell['yield_diseased']
                    st.session_state.category_A = cell['type']
                elif st.session_state.selected_second is None and (i, j) != st.session_state.selected_first:
                    # Set the second button
                    st.session_state.selected_second = (i, j)
                    st.session_state.alpha_B = cell['alpha']
                    st.session_state.beta_B = cell['beta']
                    st.session_state.d_B = cell['d']
                    st.session_state.yield_healthy_B = cell['yield_healthy']
                    st.session_state.yield_diseased_B = cell['yield_diseased']
                    st.session_state.category_B = cell['type']
                else:
                    # Reset selection if a third button is clicked
                    st.session_state.selected_first = None
                    st.session_state.selected_second = None
                    st.session_state.alpha_A = None
                    st.session_state.beta_A = None
                    st.session_state.d_A = None
                    st.session_state.yield_healthy_A = None
                    st.session_state.yield_diseased_A = None
                    st.session_state.alpha_B = None
                    st.session_state.beta_B = None
                    st.session_state.d_B = None
                    st.session_state.yield_healthy_B = None
                    st.session_state.yield_diseased_B = None
    varcol1, varcol2, varcol3 = st.columns([1, 1, 4])
    with varcol1:
        if st.session_state.selected_first:
            st.markdown(f"""
            <pre>
        <b>Cultivar A</b> <span style="background-color: #f4d46e;">({st.session_state.selected_first[0] + 1}, {st.session_state.selected_first[1] + 1})<span>
        <div style="border: 1px solid black; padding: 10px; margin-top: 5px;">
        <b>{data[st.session_state.selected_first[0]][st.session_state.selected_first[1]]['type']} </b>
        <br />
        <b>Infection detectability:</b> {100*st.session_state.d_A:.2f}%, 
        <br />
        <b>Yield Healthy:</b> {st.session_state.yield_healthy_A} t/ha
        <br />
        <b>Yield Diseased:</b> {st.session_state.yield_diseased_A} t/ha
        <br />
        <b>Model parameters:</b> acquisition = {st.session_state.alpha_A}, inoculation = {st.session_state.beta_A}
            </pre>
        </div>
            """, unsafe_allow_html=True)
    with varcol2:
        if st.session_state.selected_second:
            st.markdown(f"""
            <pre>
        <b>Cultivar B</b> <span style="background-color: #f4d46e;">({st.session_state.selected_second[0] + 1}, {st.session_state.selected_second[1] + 1}) </span>
        <div style="border: 1px solid black; padding: 10px; margin-top: 5px;">
        <b>{data[st.session_state.selected_second[0]][st.session_state.selected_second[1]]['type']} </b>
        <br />
        <b>Infection detectability:</b> {100*st.session_state.d_B:.2f}%, 
        <br />
        <b>Yield Healthy:</b> {st.session_state.yield_healthy_B} t/ha
        <br />
        <b>Yield Diseased:</b> {st.session_state.yield_diseased_B} t/ha
        <br />
        <b>Model parameters:</b> acquisition = {st.session_state.alpha_B}, inoculation = {st.session_state.beta_B}
            </pre>
        </div>
            """, unsafe_allow_html=True)

    return(st.session_state)

