import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
from scipy.optimize import basinhopping
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go

def modelTrajectories(theta, session_state):
    # Importing parameters
    f = session_state.f 
    K = session_state.K
    T = session_state.T
    rho = session_state.absolute_roguing_rate
    sigma = session_state.sigma
    omega = session_state.omega
    r = session_state.r
    alpha_A = session_state.alpha_A
    alpha_B = session_state.alpha_B
    beta_A = session_state.beta_A
    beta_B = session_state.beta_B
    gamma_A = session_state.gamma_A
    gamma_B = session_state.gamma_B
    # Initial values
    lA_0 = 0
    iA_0 = theta/K
    lB_0 = 0
    iB_0 = (1-theta)/K
    F = f * K
    VA_0 = 0 #0.1 * F/2 # Initially, 10% of vectors are infected
    VB_0 = VA_0
    
    # Define the ODE system
    def ode_system(t, y):
        lA, iA, lB, iB, VA, VB = y
        psi = 1/(sigma + omega + r)
        dlAdt = (psi*sigma/K)*beta_A*(theta - lA - iA)*(VA + VB) - gamma_A*lA
        diAdt = gamma_A * lA - rho*iA
        dlBdt = (psi*sigma/K)*beta_B*(1 - theta - lB - iB)*(VA + VB) - gamma_B*lB
        diBdt = gamma_B * lB - rho*iB
        dVAdt = alpha_A*(iA*F - psi*(sigma*iA*(VA+VB) + (omega+r)*VA)) - (omega + r)*VA
        dVBdt = alpha_B*(iB*F - psi*(sigma*iB*(VA+VB) + (omega+r)*VB)) - (omega + r)*VB
        return [dlAdt, diAdt, dlBdt, diBdt, dVAdt, dVBdt]
    
    # Solve the ODE
    sol = solve_ivp(ode_system, [0, T], [lA_0, iA_0, lB_0, iB_0, VA_0, VB_0], t_eval=np.linspace(0, T, 100))
    
    return sol

def diseaseIncidence(theta, session_state):
    sol = modelTrajectories(theta, session_state)
    
    # Get the solution
    t_values = sol.t
    disease_incidence  = sol.y[1] + sol.y[3]

    return t_values, disease_incidence

def finalDiseaseIncidence(theta, session_state):
    t_values, disease_incidence = diseaseIncidence(theta)
    return disease_incidence[-1]

def cropYield(theta, session_state):
    sol = modelTrajectories(theta, session_state)
    
    # Get the solution
    t_values = sol.t
    lA_values, iA_values, lB_values, iB_values, VA_values, VB_values = sol.y
    lA = lA_values[-1]
    iA = iA_values[-1]
    sA = theta - (lA + iA)
    lB = lB_values[-1]
    iB = iB_values[-1]
    sB = (1-theta) - (lB + iB)
    
    # Calculate yield per hectare
    y = session_state.yield_healthy_A*(sA+lA) + session_state.yield_infected_A*iA + session_state.yield_healthy_B*(sB+lB) + session_state.yield_infected_B*iB
    return y
def distinctCropYield(theta, session_state):
    sol = modelTrajectories(theta,session_state)
    
    # Get the solution
    t_values = sol.t
    lA_values, iA_values, lB_values, iB_values, VA_values, VB_values = sol.y
    lA = lA_values[-1]
    iA = iA_values[-1]
    sA = theta - (lA + iA)
    lB = lB_values[-1]
    iB = iB_values[-1]
    sB = (1-theta) - (lB + iB)
    
    # Calculate yield per hectare
    yA = session_state.yield_healthy_A*(sA+lA) + session_state.yield_infected_A*iA 
    yB = session_state.yield_healthy_B*(sB+lB) + session_state.yield_infected_B*iB
    return yA, yB

#def yieldOptimizer(session_state):
    # Define bounds for theta
#    theta_bounds = (0, 1)
    # Define the negative function function
#    def neg_cropYield(theta):
#        return -cropYield(theta, session_state)

    # Minimize the negative function function
#    result = minimize_scalar(neg_cropYield, bounds=theta_bounds, method='bounded')
#    return result.x, -result.fun
def yieldOptimizer(session_state):
    bounds = [(0, 1)]  # Bounds for theta
    def neg_cropYield(theta):
        return -cropYield(theta[0], session_state)

    result = basinhopping(neg_cropYield, [0.5], niter=400, stepsize=0.5, minimizer_kwargs={"bounds": bounds})
    return result.x[0], -result.fun

def plotYieldVsTheta(session_state):
    # Define the range for theta
    theta_values = np.linspace(0, 1, 100)
    
    # Calculate cropYield for each theta
    yield_values = [cropYield(theta, session_state) for theta in theta_values]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjusted width to 60% of A4 paper width
    ax.plot(theta_values, yield_values, label='cropYield(theta)', color='black', linewidth=3)
    ax.set_xlabel('Proportion of Cultivar A', fontsize=18)
    ax.set_ylabel('Total Yield', fontsize=18)
    ax.set_title('Total yield vs Distribution of Cultivar A', fontsize=18)
    #ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    
def plotYieldVsThetaInteractive(session_state):
    # Define the range for theta
    theta_values = np.linspace(0, 1, 100)
    category_A = session_state.category_A
    
    # Calculate cropYield for each theta
    yield_values = [cropYield(theta, session_state) for theta in theta_values]
    
    # Create the interactive plot using Plotly
    fig = go.Figure()

    # Add the line plot with hover information
    fig.add_trace(go.Scatter(
        x=theta_values*100,
        y=yield_values,
        mode='lines',
        line=dict(color='black', width=3),
        hovertemplate='Proportion of Cultivar A: <b>%{x:.2f} %</b><br />Total Yield: <b>%{y:.2f} ton/ha</b><extra></extra>', # Tooltip format
        hoverlabel=dict(
            font=dict(size=16)  # Increase tooltip font size
        )
    ))

    # Set plot layout with axis labels and title
    fig.update_layout(
        title=dict(
            text=f'Total Yield vs Proportion of {category_A} Cultivar A',
            xanchor='center',  # Center the title
            x=0.5,  # Horizontal center
            font=dict(size=18)  # Font size of the title
        ),
        xaxis_title=dict(
            text=f'Proportion of {category_A} Cultivar A (%)',
            font=dict(size=18, color='black') # Increase xlabel size
        ),
        yaxis_title=dict(
            text='Total Yield (ton/ha)',
            font=dict(size=18, color='black')  # Increase ylabel size
        ),
        xaxis=dict(
            tickfont=dict(size=18, color='black'),
            showline=True,  # Display the x-axis line
            linecolor='black',  # Color of the x-axis line
            mirror=True,  # Mirror the axis line on both sides
            gridcolor='lightgray',
        ),
        yaxis=dict(
            tickfont=dict(size=18, color='black'),
            showline=True,  # Display the y-axis line
            linecolor='black',  # Color of the y-axis line
            mirror=True,  # Mirror the axis line on both sides
            gridcolor='lightgray',
        ),
        width=600,
        height=420,
    )

    # Display the interactive plot inside Streamlit
    st.plotly_chart(fig)

def displayOptimal(theta, session_state):
# Calculate the values
    percentageA = theta * 100
    percentageB = (1 - theta) * 100
    yieldA, yieldB = distinctCropYield(theta, session_state)
    category_A = session_state.category_A
    category_B = session_state.category_B
    total_yield = yieldA + yieldB

    # Plotting
    sizes = [theta, (1-theta)]

    fig, ax = plt.subplots(figsize=(9.6, 5), subplot_kw=dict(aspect="equal"))  # Adjusted width to 60% of A4 paper width

    wedges, texts, autotexts = ax.pie(sizes, labels=['', ''], autopct='%1.1f%%', startangle=140, explode=(0.1, 0), shadow=True)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    tooltips = [r'$\bf{Cultivar \ A}$' + f'\n({category_A})' + f'\n{percentageA:.2f} %\nyield = {yieldA:.2f}' + ' ton/ha',
                r'$\bf{Cultivar \ B}$' + f'\n({category_B})' + f'\n{percentageB:.2f} %\nyield = {yieldB:.2f}' + ' ton/ha']

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(tooltips[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, fontsize=10, color='black', **kw)

    # Add boxed message for total yield on the right
    ax.text(1.2, 0, f'Total Yield = {total_yield:.2f}' + ' ton/ha', fontsize=12, color='black', ha='left', va='center', bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.5'))

    # Display the plot in Streamlit
    st.pyplot(fig)

def displayDiseaseDynamics(theta, session_state):
    sol = modelTrajectories(theta, session_state)
    yieldA, yieldB = distinctCropYield(theta, session_state)
    total_yield = yieldA + yieldB
    category_A = session_state.category_A
    category_B = session_state.category_B
    
    # Access the solution
    t_values = sol.t
    lA_values, iA_values, lB_values, iB_values, VA_values, VB_values = sol.y

    # Plot the solutions
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # First subplot
    axes[0].plot(t_values, iA_values+iB_values, label='All infected plants', color='black', linewidth=3)
    axes[0].plot(t_values, iA_values, label=f'Infected {category_A}')
    axes[0].plot(t_values, iB_values, label=f'Infected {category_B}')
    axes[0].set_xlabel('Time', fontsize=18)
    axes[0].set_ylabel('Proportions', fontsize=18)
    axes[0].set_title('Disease Dynamics Over Time', fontsize=18)
    axes[0].legend()
    axes[0].grid(True)
    axes[0].text(10, max(np.max(iA_values),np.max(iB_values))/2, f'{category_A} Cultivar Yield = {yieldA:.2f}' + ' ton/ha \n' + f'{category_B} Cultivar Yield = {yieldB:.2f}' + ' ton/ha \n' + f'Total Yield = {total_yield:.2f}' + ' ton/ha', fontsize=12, color='black', ha='left', va='center', bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.5'))
    # Second subplot
    axes[1].plot(t_values, VA_values, label=f'Acquired on {category_A} plants')
    axes[1].plot(t_values, VB_values, label=f'Acquired on {category_B} plants')
    axes[1].set_xlabel('Time', fontsize=18)
    axes[1].set_ylabel('Populations', fontsize=18)
    axes[1].set_title('Infected Insect Dynamics Over Time', fontsize=18)
    axes[1].legend()
    axes[1].grid(True)

    fig.tight_layout()

    # Display the figure in Streamlit
    st.pyplot(fig)
