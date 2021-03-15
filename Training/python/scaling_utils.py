import awkward as ak
import numpy as np

import time
import gc
import json
import collections

def Phi_mpi_pi(array_phi):
    array_phi = ak.where(array_phi <= np.pi, array_phi, array_phi - 2*np.pi)
    array_phi = ak.where(array_phi >= -np.pi, array_phi, array_phi + 2*np.pi)
    assert ak.sum(array_phi > np.pi) + ak.sum(array_phi < -np.pi) == 0
    return array_phi

def dR(deta, dphi):
    return np.sqrt(deta**2 + Phi_mpi_pi(dphi)**2)

def dR_signal_cone(pt_tau, min_pt, min_radius, opening_coef):
    return np.maximum(opening_coef/np.maximum(pt_tau, min_pt), min_radius)

def nested_dict():
    return collections.defaultdict(nested_dict)

def init_dictionaries(features_dict, cone_selection_dict, n_files):
    sums, sums2, counts, scaling_params = nested_dict(), nested_dict(), nested_dict(), nested_dict()
    for var_type in features_dict.keys():
        for var_dict in features_dict[var_type]:
            (var, (_, _, scaling_type, *lim_params)), = var_dict.items()
            if scaling_type == 'no_scaling':
                scaling_params[var_type][var] = {"mean": 0, "std": 1, "lim_min": "-inf", "lim_max": "inf"}
            elif scaling_type == 'linear':
                assert len(lim_params) == 2 and lim_params[0] <= lim_params[1]
                scaling_params[var_type][var] = {"mean": (lim_params[0]+lim_params[1])/2, "std": (lim_params[1]-lim_params[0])/2., "lim_min": -1., "lim_max": 1.} # NB: parameters for [-1, 1] clamping in DataLoader downstream
            elif scaling_type == 'normal':
                for cone_type in cone_selection_dict[var_type]['cone_types']:
                    if cone_type is not None:
                        sums[var_type][var][cone_type] = np.zeros(n_files, dtype='float64')
                        sums2[var_type][var][cone_type] = np.zeros(n_files, dtype='float64')
                        counts[var_type][var][cone_type] = np.zeros(n_files, dtype='int64')
                    else:
                        sums[var_type][var] = np.zeros(n_files, dtype='float64')
                        sums2[var_type][var] = np.zeros(n_files, dtype='float64')
                        counts[var_type][var] = np.zeros(n_files, dtype='int64')
            else:
                raise ValueError(f"in variable {var}: scaling_type should be either no_scaling, or linear, or normal")
    return sums, sums2, counts, scaling_params

def compute_mean(sums, counts, aggregate=True, *file_range):
    if aggregate:
        if file_range:
            assert len(file_range) == 2 and file_range[0] <= file_range[1]
            return sums[file_range[0]:file_range[1]].sum()/counts[file_range[0]:file_range[1]].sum()
        else:
            return sums.sum()/counts.sum()
    else:
        return sums/counts

def compute_std(sums, sums2, counts, aggregate=True, *file_range):
    if aggregate:
        if file_range:
            assert len(file_range) == 2 and file_range[0] <= file_range[1]
            average2 = sums2[file_range[0]:file_range[1]].sum()/counts[file_range[0]:file_range[1]].sum()
            average = sums[file_range[0]:file_range[1]].sum()/counts[file_range[0]:file_range[1]].sum()
            return np.sqrt(average2 - average**2)
        else:
            return np.sqrt(sums2.sum()/counts.sum() - (sums.sum()/counts.sum())**2)
    else:
        return np.sqrt(sums2/counts - (sums/counts)**2)

def fill_aggregators(var_array, tau_eta_array, tau_phi_array, constituent_eta_array, constituent_phi_array,
                     var, var_type, file_i, cone_type, dR_tau_signal_cone, dR_tau_outer_cone,
                     sums, sums2, counts, fill_scaling_params=False, scaling_params=None, lim_params=None):
    if cone_type == None:
        sums[var_type][var][file_i] += ak.sum(var_array)
        sums2[var_type][var][file_i] += ak.sum(var_array**2)
        counts[var_type][var][file_i] += ak.count(var_array)
        if fill_scaling_params:
            mean = compute_mean(sums[var_type][var], counts[var_type][var], aggregate=True)
            std = compute_std(sums[var_type][var], sums2[var_type][var], counts[var_type][var], aggregate=True)
            if lim_params:
                assert len(lim_params) == 2 and lim_params[0] <= lim_params[1]
                scaling_params[var_type][var] = {'mean': mean, 'std': std, "lim_min": lim_params[0], "lim_max": lim_params[1]}
            else:
                scaling_params[var_type][var] = {'mean': mean, 'std': std, "lim_min": "-inf", "lim_max": "inf"}
    elif cone_type == 'inner' or cone_type == 'outer':
        before_dR = time.time()
        constituent_dR = dR(tau_eta_array - constituent_eta_array, tau_phi_array - constituent_phi_array)
        after_dR = time.time()
        if cone_type == 'inner':
            cone_mask = constituent_dR <= dR_tau_signal_cone
        elif cone_type == 'outer':
            cone_mask = (constituent_dR > dR_tau_signal_cone) & (constituent_dR < dR_tau_outer_cone)
        after_cone_mask = time.time()
        sums[var_type][var][cone_type][file_i] += ak.sum(var_array[cone_mask])
        sums2[var_type][var][cone_type][file_i] += ak.sum(var_array[cone_mask]**2)
        counts[var_type][var][cone_type][file_i] += ak.count(var_array[cone_mask])
        after_agg = time.time()
        if fill_scaling_params:
            mean = compute_mean(sums[var_type][var][cone_type], counts[var_type][var][cone_type], aggregate=True)
            std = compute_std(sums[var_type][var][cone_type], sums2[var_type][var][cone_type], counts[var_type][var][cone_type], aggregate=True)
            if lim_params:
                assert len(lim_params) == 2 and lim_params[0] <= lim_params[1]
                scaling_params[var_type][var][cone_type] = {'mean': mean, 'std': std, "lim_min": lim_params[0], "lim_max": lim_params[1]}
            else:
                scaling_params[var_type][var][cone_type] = {'mean': mean, 'std': std, "lim_min": "-inf", "lim_max": "inf"} # if no clamping range specified, default to [-inf, inf]
        # print('fill_aggregators timing: ', round(after_dR-before_dR, 2), round(after_cone_mask-after_dR, 2), round(after_agg-after_cone_mask, 2))
    else:
        raise ValueError(f'cone_type for {var_type} should be either inner, or outer')

def dump_to_json(dict_map):
    for fout_name, dict in dict_map.items():
        with open(f'{fout_name}.json', 'w') as fout:
            json.dump(dict, fout)
