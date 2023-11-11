# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from autoeq.frequency_response import FrequencyResponse


def form_pairs(frs, refs):
    pairs = []
    for fr in frs:
        if fr.name in refs:
            pairs.append((fr.copy(), refs[fr.name]))
    return pairs


def init_plot(pairs, title):
    fig, axs = plt.subplots(1, 3)
    fig.set_size_inches(30, 8)
    fig.suptitle(title)
    description = 'Calibrated against reference measurements with headphones: '
    line_len = len(description)
    n_lines = 1
    for fr, _ in pairs:
        if line_len > 240:
            description += '\n'
            line_len = 0
            n_lines += 1
        description += f'{fr.name}, '
        line_len += len(fr.name) + 2
    description = description[:-2]
    fig.text(0.5, -0.05 * (n_lines / 3), description, ha='center')
    return fig, axs


def individual_errors(pairs, fig, ax):
    errors = []
    for fr, ref in pairs:
        fr.compensate(ref, min_mean_error=True)
        errors.append(fr.error)
        fr.raw = fr.error.copy()
        fr.error = []
        fr.target = []
        fr.plot(fig=fig, ax=ax, show_fig=False, raw_plot_kwargs={'color': 'C0', 'alpha': 0.3})
    ax.set_ylim([-15, 15])
    ax.set_title('Individual Errors')
    ax.legend(['Error'])
    return errors


def mean_std(errors, fig, ax):
    errors = np.vstack(errors)
    mean = np.mean(errors, axis=0)
    std = np.std(errors, axis=0)
    fr = FrequencyResponse(name='Mean and Standard Deviation')
    fr.raw = mean
    fr.smoothen(window_size=1/3, treble_window_size=1/3)
    fr.raw = fr.smoothed.copy()
    fr.smoothed = []
    fr.plot(fig=fig, ax=ax, show_fig=False, raw_plot_kwargs={'color': 'C0', 'label': 'Mean'})
    ax.fill_between(fr.frequency, mean - std, mean + std, facecolor='#c1dff5', label='STD')
    ax.set_ylim([-15, 15])
    ax.legend()
    return fr


def calibrate_target(mean, target, fig, ax):
    target.plot(
        fig=fig, ax=ax, show_fig=False,
        raw_plot_kwargs={'color': 'C0', 'label': target.name})
    target = target.copy()
    target.name = 'Calibrated target'
    target.raw += mean.raw
    target.plot(
        fig=fig, ax=ax, show_fig=False,
        raw_plot_kwargs={'color': 'C1', 'label': f'Calibrated target'})
    ax.legend()
    ax.set_title('Target')
    ax.set_ylim([-15, 15])
    return target


def calibrate(db, form, frs, refs, target):
    pairs = form_pairs(frs, refs)
    fig, axs = init_plot(pairs, f'{db} {form}')
    errors = individual_errors(pairs, fig, axs[0])
    mean = mean_std(errors, fig, axs[1])
    calibrated_target = calibrate_target(mean, target, fig, axs[2])
    return errors, mean, calibrated_target, fig
