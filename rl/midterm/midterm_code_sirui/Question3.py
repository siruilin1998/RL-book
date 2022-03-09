from dataclasses import dataclass
from typing import Tuple, Dict, Mapping, Sequence
from rl.markov_decision_process import FiniteMarkovDecisionProcess
from rl.policy import FiniteDeterministicPolicy
from rl.markov_process import FiniteMarkovProcess, FiniteMarkovRewardProcess
from rl.distribution import Categorical
from scipy.stats import poisson
import numpy as np

@dataclass(frozen = True)
class DiceState:
    on_table: Sequence[int]
    sum_in_hand: int
    ones_in_hand: int

#class DiceAction:
    #move_to_hand: Sequence[int]


class DiceStatehash:
    def __init__(self, on_table: Sequence[int], sum_in_hand: int, ones_in_hand: int):
        self.on_table = str(on_table)
        self.sum_in_hand = sum_in_hand
        self.ones_in_hand = ones_in_hand

    def __repr__(self):
        rep = '(Initial dices:' + self.on_table + 'sum of dices in hand:' + str(self.sum_in_hand) + 'ones in hand:' + str(self.ones_in_hand) + ')'
        return rep

    #def __hash__(self):
        #return hash((hash(self.on_table), self.sum_in_hand, self.ones_in_hand))

class DiceAction:
    num_of_ones: int
    num_of_large: int

StateActionMapping = Mapping[
    DiceState,
    Mapping[DiceAction, Categorical[Tuple[Tuple, int]]]
]

def DiceSpaceNK2(N: int, K: int):
    if N == 1: return [np.array([i]) for i in range(1,K+1)]
    else:
        output = []
        for elem in DiceSpaceNK2(N - 1, K):
            for j in range(1, K+1):
                output += [np.concatenate((np.array([j]), elem))]
        return output

def DiceSpaceNK(N: int, K: int) -> Mapping[int, Sequence[Sequence[int]]]:
    d: Dict[int, Sequence[Sequence[int]]] = {}
    for m in range(1, N + 1):
        d[m] = DiceSpaceNK2(m, K)
    return d

def maxelem(seq: Sequence[int], B: int) -> Sequence[int]:
    new = seq[np.argpartition(seq, -B)[-B:]]
    return sum(new)

#def ActionSpaceNK(N: int) -> Mapping[int, Sequence[Sequence[int]]]:
#    d: Dict[int, Sequence[Sequence[int]]] = {}
#    candidate = range(1, N + 1)
#    index: Mapping[int, Sequence[Sequence[int]]] = DiceSpaceNK(N, 2)
#    for m in range(1, N + 1):
#        Seqq: Sequence[Sequence[int]] = index[m]
#        s: Sequence[Sequence[int]] = []
#        for seq in Seqq:
#            if sum(seq) !=  len(seq):
#                arr = np.array([candidate[i] for i in range(m) if seq[i] == 2])
#                s += [arr]
#        d[m] = s
#    return d


def Countones(arr: Sequence[int]) -> int:
    count = 0
    for i in range(len(arr)):
        if (arr[i] == 1): count += 1
    return count

class DiceRollingGameMDP(FiniteMarkovDecisionProcess[DiceState, DiceAction]):

    def __init__(
            self,
            NumberOfDices: int,
            SizeOfDices: int,
            ThresholdOfOnes: int
    ):
        self.NumberOfDices: int = NumberOfDices
        self.SizeOfDices: int = SizeOfDices
        self.ThresholdOfOnes: int = ThresholdOfOnes
        self.DiceSpace: Mapping[int, Sequence[Sequence[int]]] = DiceSpaceNK(self.NumberOfDices, self.SizeOfDices)
        self.DiceSpace[0] = [np.array([-1])]
        #self.ActionSpace: Mapping[int, Sequence[Sequence[int]]] = ActionSpaceNK(self.NumberOfDices)

        super().__init__(self.get_action_transition_reward_map())



    def get_action_transition_reward_map(self) -> StateActionMapping:
        d: Dict[Tuple, Dict[DiceAction, Categorical[Tuple[Tuple,
                                                              int]]]] = {}

        for num in range(1, self.NumberOfDices + 1): #remaining number of dices on table
            for seq in self.DiceSpace[num]: #remaining dices on table
                for M in range(0, self.NumberOfDices - num + 1): #number of ones in hand
                    for S in range(M + (self.NumberOfDices - num - M)*2, M + (self.NumberOfDices - num - M) * self.SizeOfDices + 1): #sum of dices in hand
                        d1: Dict[Any, Categorical[Tuple[Tuple,
                                                              int]]] = {}
                        #state: DiceState = DiceState(seq, S, M)
                        A = Countones(seq)
                        B = num - A

                        for index_ones in range(A + 1):
                            for index_large in range(int (index_ones == 0), B + 1):
                                #action: DiceAction = DiceAction(index_ones, index_large)
                                largesum = maxelem(seq, index_large)

                                reward: int = 0
                                if M >= self.ThresholdOfOnes:  # function of reward based on present state and action
                                    reward = largesum + index_ones

                                elif M + index_ones < self.ThresholdOfOnes:
                                    reward = 0

                                else:
                                    reward = S + largesum + index_ones

                                Newsum: int = S + largesum + index_ones
                                Newones: int = M + index_ones
                                remainnum: int = num - (index_ones + index_large)

                                prob_dist: Dict[Tuple[Tuple, int], float] = \
                                    {((str(Newstate), Newsum, Newones), reward):
                                         0.1 for Newstate in self.DiceSpace[remainnum]}

                                d1[(index_ones, index_large)] = Categorical(prob_dist)

                        d[(str(seq), S, M)] = d1
        return d


if __name__ == '__main__':
    from pprint import pprint

    user_NumberOfDices = 6
    user_SizeOfDices = 4
    user_ThresholdOfOnes = 1

    user_gamma = 1.0

    diceroll_mdp: FiniteMarkovDecisionProcess[DiceStatehash, DiceAction] = \
        DiceRollingGameMDP(
           NumberOfDices = user_NumberOfDices,
           SizeOfDices = user_SizeOfDices,
           ThresholdOfOnes= user_ThresholdOfOnes
        )

    #print("MDP Transition Map")
    #print("------------------")
    #print(diceroll_mdp)

    from rl.dynamic_programming import value_iteration_result

    print("MDP Value Iteration Optimal Value Function and Optimal Policy")
    print("--------------")
    opt_vf_vi, opt_policy_vi = value_iteration_result(diceroll_mdp, gamma=user_gamma)
    pprint(opt_vf_vi)
    print(opt_policy_vi)


    print()
