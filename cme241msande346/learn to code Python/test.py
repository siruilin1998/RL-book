import numpy as np
from rl.distribution import Categorical
from rl.function_approx import Tabular
from rl.monte_carlo import mc_prediction

# Construct testing process
from rl.chapter2.simple_inventory_mrp import InventoryState
from rl.chapter2.simple_inventory_mrp import SimpleInventoryMRPFinite
from rl.markov_process import FiniteMarkovRewardProcess

plt.plot(x_vals, y_vals)
plt.grid()
plt.xticks([0.0] + event_times)
plt.xlabel(”Event Timings”, fontsize=15)
plt.ylabel(”Memory Funtion Values”, fontsize=15)
plt.title(”Memory Function (Frequency and Recency)”, fontsize=25)
plt.show()

if __name__ == "__main__":
    user_capacity = 2
    user_poisson_lambda = 1.0
    user_holding_cost = 1.0
    user_stockout_cost = 10.0
    user_gamma = 0.9
    si_mrp = SimpleInventoryMRPFinite(
        capacity=user_capacity,
        poisson_lambda=user_poisson_lambda,
        holding_cost=user_holding_cost,
        stockout_cost=user_stockout_cost
    )
    Test_Process = FiniteMarkovRewardProcess(
        si_mrp.get_transition_reward_map()
    )

    # test using code in the BOOK
    num_traces = 10
    Initial_InventoryState = InventoryState(0, 0)
    traces = np.vstack(
        [Test_Process.reward_traces(Categorical({Initial_InventoryState: 1.0})) for _ in range(num_traces)])

    approx0 = Tabular()
    *updates, final_result_mc = list(mc_prediction(traces, approx0, 0.9))
    print(final_result_mc.values_map)

