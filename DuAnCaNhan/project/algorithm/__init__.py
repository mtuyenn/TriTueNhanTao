from .uninformed_search.bfs import bfs1, bfs2
from .uninformed_search.dfs import dfs1, dfs2
from .uninformed_search.ids import ids_normal, ids2_optimize
from .uninformed_search.ucs import ucs
from .informed_search.greedy import Greedy_Search
from .informed_search.a_star import A_star
from .informed_search.ida_star import IDA_start
from .hill_climbing import Simple_Hill_Climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, random_restart_hill_climbing, simulated_annealing
from .hill_climbing import local_beam_search
from .sreach_in_complex_environments.unobservable_search import unobservable_search
from .sreach_in_complex_environments.partialobservation_search import partialobservation_search
from .sreach_in_complex_environments.and_or_graph_search import and_or_graph_search_generator
from .CSP.backtracking import HCM_REGIONS, MAP_COLORS, backtracking_map_coloring
from .CSP.forward_checking import forward_checking_map_coloring
from .CSP.ac3 import ac3_map_coloring
from .CSP.min_conflicts import min_conflicts_map_coloring
from .adversarial_search.minimax import create_board as create_caro_board, winner as caro_winner, minimax_decision
from .adversarial_search.alpha_beta import alpha_beta_decision
from .adversarial_search.expectimax import expectimax_decision
