"""EERI 325 Signal Theory 2 - Interactive demos.

Runs as a normal Streamlit app (streamlit run app.py) and inside
stlite in the browser for hosting on GitHub Pages.
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ---------------------------------------------------------------- palette
NAVY = "#0E2A47"
TEAL = "#1B7898"
GOLD = "#C9962E"
LIGHT = "#E8F0F4"
RED = "#B4432F"

plt.rcParams.update(
    {
        "axes.edgecolor": NAVY,
        "axes.labelcolor": NAVY,
        "xtick.color": NAVY,
        "ytick.color": NAVY,
        "axes.titlecolor": NAVY,
        "font.size": 11,
        "axes.grid": True,
        "grid.color": "#D5DEE4",
        "grid.linewidth": 0.6,
        "figure.facecolor": "white",
    }
)

st.set_page_config(page_title="EERI 325 | Signal Theory 2 demos", layout="wide")


def stem(ax, n, v, color=TEAL, ms=7, alpha=1.0, label=None):
    ml, sl, bl = ax.stem(n, v, basefmt=" ")
    plt.setp(ml, color=color, markersize=ms, alpha=alpha, label=label)
    plt.setp(sl, color=color, linewidth=2, alpha=alpha)


def parse_seq(text, fallback):
    try:
        vals = [float(t) for t in text.replace(",", " ").split()]
        return np.array(vals) if len(vals) else fallback
    except ValueError:
        st.warning("Could not read that sequence, using the previous values.")
        return fallback


# ---------------------------------------------------------------- sidebar
st.sidebar.title("EERI 325")
st.sidebar.caption("Signal Theory 2 · Class 1 companions")
demo = st.sidebar.radio(
    "Choose a demo",
    ["1 · Sampling and aliasing", "2 · Time shift and reversal", "3 · Convolution: flip and slide"],
)
st.sidebar.markdown("---")

# ================================================================ demo 1
if demo.startswith("1"):
    st.title("Where sequences come from: sampling")
    st.markdown(
        "We sample a continuous sinusoid $x_a(t)=\\sin(2\\pi f_0 t)$ at even "
        "spacing $T$, so $x[n] = x_a(nT)$ and $F_s = 1/T$. "
        "Move the sliders and watch what the sequence can and cannot capture."
    )

    f0 = st.sidebar.slider("Signal frequency f₀ (Hz)", 1.0, 10.0, 2.0, 0.5)
    fs = st.sidebar.slider("Sampling frequency Fs (Hz)", 1.0, 40.0, 16.0, 0.5)
    show_recon = st.sidebar.checkbox("Show the sinusoid the samples imply", True)

    T = 1.0 / fs
    t = np.linspace(0, 2, 2000)
    xa = np.sin(2 * np.pi * f0 * t)
    n = np.arange(0, int(np.floor(2 * fs)) + 1)
    xn = np.sin(2 * np.pi * f0 * n * T)

    # apparent (aliased) frequency the samples actually represent
    fa = f0 - fs * np.round(f0 / fs)

    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(t, xa, color=NAVY, lw=1.8, label=r"$x_a(t)$")
    if show_recon and abs(fa - f0) > 1e-9:
        ax.plot(t, np.sin(2 * np.pi * fa * t), color=RED, lw=1.6, ls="--",
                label=f"implied sinusoid ({abs(fa):.2f} Hz)")
    stem(ax, n * T, xn, color=GOLD, ms=6)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("amplitude")
    ax.set_title(f"x[n] = x_a(nT),   T = {T:.3f} s")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.set_ylim(-1.25, 1.25)
    st.pyplot(fig)

    nyq = 2 * f0
    c1, c2, c3 = st.columns(3)
    c1.metric("Sampling period T", f"{T:.3f} s")
    c2.metric("Samples per signal period", f"{fs / f0:.2f}")
    c3.metric("Nyquist rate 2f₀", f"{nyq:.1f} Hz")

    if fs > nyq:
        st.success(
            f"Fs = {fs:.1f} Hz exceeds the Nyquist rate of {nyq:.1f} Hz. "
            "The samples uniquely represent the sinusoid."
        )
    elif np.isclose(fs, nyq):
        st.warning(
            "Fs is exactly the Nyquist rate. In theory this is the boundary case, "
            "in practice it is fragile: try it and watch the sample values."
        )
    else:
        st.error(
            f"Fs = {fs:.1f} Hz is below the Nyquist rate of {nyq:.1f} Hz. "
            f"The samples are indistinguishable from a {abs(fa):.2f} Hz sinusoid. "
            "This is aliasing: the dashed curve passes through every sample."
        )

    with st.expander("Try this in class"):
        st.markdown(
            "- Set f₀ = 2 Hz, then slide Fs down slowly from 16 Hz. "
            "At what Fs does the implied sinusoid first differ from the true one?\n"
            "- Set Fs = 6 Hz and f₀ = 5 Hz. What frequency do the samples suggest? "
            "Verify with $f_a = f_0 - F_s\\,\\mathrm{round}(f_0/F_s)$."
        )

# ================================================================ demo 2
elif demo.startswith("2"):
    st.title("Time shifting and time reversal")
    st.markdown(
        "Shifting: $y[n] = x[n-N]$, where $N>0$ delays and $N<0$ advances. "
        "Reversal (folding): $y[n] = x[-n]$ reflects about $n=0$. "
        "Folding is the first move in graphical convolution, so build the intuition here."
    )

    seq_text = st.sidebar.text_input("Sequence x[n] (starts at n = 0)", "1 2 3 2 1")
    x = parse_seq(seq_text, np.array([1, 2, 3, 2, 1.0]))
    N = st.sidebar.slider("Shift N", -6, 6, 0)
    fold = st.sidebar.checkbox("Time reverse first (fold about n = 0)")

    nx = np.arange(len(x))
    if fold:
        ny = -nx[::-1] + N
        y = x[::-1]
        formula = f"y[n] = x[-(n - {N})] = x[{N} - n]" if N else "y[n] = x[-n]"
    else:
        ny = nx + N
        y = x
        formula = f"y[n] = x[n - {N}]" if N else "y[n] = x[n]"

    lim = max(8, abs(N) + len(x))
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    stem(axes[0], nx, x, color=TEAL)
    axes[0].set_title("Original  x[n]")
    stem(axes[1], ny, y, color=GOLD)
    axes[1].set_title(formula)
    for ax in axes:
        ax.set_xlim(-lim, lim)
        ax.set_xlabel("n")
        ax.axvline(0, color=NAVY, lw=0.8, alpha=0.5)
    st.pyplot(fig)

    if N > 0:
        st.info(f"N = {N} > 0: the sequence is **delayed** (moves right).")
    elif N < 0:
        st.info(f"N = {N} < 0: the sequence is **advanced** (moves left).")
    if fold:
        st.info("Folding first, then shifting, gives x[N − n]: the reflection slides with N.")

    with st.expander("Try this in class"):
        st.markdown(
            "- Predict where the peak lands for N = 3 with folding on, then check.\n"
            "- Is x[n] = {1, 2, 3, 2, 1} even about its centre? "
            "What N makes the folded version line up with the original?"
        )

# ================================================================ demo 3
else:
    st.title("The convolution sum: flip and slide")
    st.latex(r"y[n] \;=\; x[n]*h[n] \;=\; \sum_k x[k]\,h[n-k]")
    st.markdown(
        "Flip $h$, slide it to position $n$, multiply the overlapping samples, and sum. "
        "Drag the slider for $n$ and watch $y[n]$ build up one sample at a time."
    )

    preset = st.sidebar.selectbox(
        "Sequences",
        ["Lecture example: x = {1,2,3}, h = {1,1,1}",
         "Smoothing: noisy step and 4-point average",
         "Custom"],
    )
    if preset.startswith("Lecture"):
        x = np.array([1.0, 2, 3])
        h = np.array([1.0, 1, 1])
    elif preset.startswith("Smoothing"):
        rng = np.random.default_rng(3)
        x = np.concatenate([np.zeros(4), np.ones(8)]) + rng.normal(0, 0.15, 12)
        h = np.ones(4) / 4
    else:
        x = parse_seq(st.sidebar.text_input("x[n] from n = 0", "1 2 3"), np.array([1.0, 2, 3]))
        h = parse_seq(st.sidebar.text_input("h[n] from n = 0", "1 1 1"), np.array([1.0, 1, 1]))

    y_full = np.convolve(x, h)
    ny_full = np.arange(len(y_full))
    n = st.sidebar.slider("Output index n", 0, len(y_full) - 1, 0)

    k = np.arange(len(x))
    kh_pos = n - np.arange(len(h))          # positions of h[n-k] on the k axis
    lo, hi = min(0, kh_pos.min()) - 1, max(len(x), kh_pos.max() + 1, len(y_full)) + 1

    fig, axes = plt.subplots(3, 1, figsize=(9, 7.2), sharex=True)
    stem(axes[0], k, x, color=TEAL)
    axes[0].set_title("x[k]")

    stem(axes[1], kh_pos, h, color=GOLD)
    axes[1].set_title(f"h[{n} − k]   (h flipped, slid to n = {n})")

    # overlap products
    terms = []
    for kk in k:
        j = n - kk
        if 0 <= j < len(h):
            axes[1].axvspan(kk - 0.18, kk + 0.18, color=RED, alpha=0.12)
            terms.append((kk, x[kk], h[j]))

    done_n = ny_full[: n + 1]
    stem(axes[2], done_n, y_full[: n + 1], color=NAVY, alpha=0.45)
    stem(axes[2], [n], [y_full[n]], color=RED, ms=9)
    axes[2].set_title("y[n] so far")
    axes[2].set_xlabel("n")
    for ax in axes:
        ax.set_xlim(lo, hi)
    fig.tight_layout()
    st.pyplot(fig)

    if terms:
        pieces = " + ".join(f"({xv:g})({hv:g})" for _, xv, hv in terms)
        st.markdown(f"**y[{n}]** = {pieces} = **{y_full[n]:g}**")
    else:
        st.markdown(f"No overlap at n = {n}, so y[{n}] = 0.")

    st.caption(
        f"Output length rule: length(y) = length(x) + length(h) − 1 "
        f"= {len(x)} + {len(h)} − 1 = **{len(y_full)}**."
    )

    with st.expander("Try this in class"):
        st.markdown(
            "- On the lecture example, predict y[2] before moving the slider, "
            "then check against the tabular method.\n"
            "- Switch to the smoothing preset. Why does the output ramp instead of jump? "
            "Relate the ramp length to length(h)."
        )

st.sidebar.markdown("---")
st.sidebar.caption("Dr S. A. Ngorima · North-West University, Potchefstroom")
