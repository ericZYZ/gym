from math import sinh, cosh, acosh

# Hyperparameters used by AC model and reinforcement learning model.
# Hyperparameter names taken from paper, or as close to name as made sense in context.
t = 5                  # discrete time between each execution in minutes
risk_aversion = 0.01   # increase for higher risk aversion
eta = 2

# gets the full Almgren-Chriss volume trajectory
def ACVolTrajectory(no_of_execs: int,
                    volume: int,
                    sigma: float):
    # if no volatility liquidate evenly across trading horizon
    if sigma == 0:
        return [volume / float(no_of_execs) for _ in range(no_of_execs)]
    else:
        # calculates model specific parameters
        k_hat_sq = (risk_aversion * sigma ** 2) / eta
        k = acosh(t ** 2 * k_hat_sq / 2 + 1) / t

        # calculates time specific parameters
        const = 2 * sinh(0.5 * k * t) / sinh(k * no_of_execs * t)

        # calculates trade list proportions and thus calculates volume trajectory
        trade_list_prop = [const * cosh(k * t * (no_of_execs - (j + 0.5)))
                           for j in range(no_of_execs)]

        trade_list = [int(volume * v) for v in trade_list_prop[:-1]]
        trade_list = trade_list + [volume - sum(trade_list)]
        return trade_list