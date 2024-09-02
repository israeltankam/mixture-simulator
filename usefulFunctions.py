def resistanceCategory(alpha, beta, gamma, d):
    if alpha == None:
        return "None"
    else:
        ab_thres = 0.0297
        gamma_thres = 1/30
        d_thres = 0.5
        if d <= d_thres:
            return "Tolerant"
        else:
            if alpha*beta >= ab_thres:
                if gamma > gamma_thres:
                    return "Highly susceptible"
                else:
                    return "Susceptible"
            else:
                if gamma >= gamma_thres:
                    return "Resistant"
                else:
                    return "Highly resistant"