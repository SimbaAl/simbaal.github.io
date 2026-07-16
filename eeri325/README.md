# EERI 325 Signal Theory 2 — interactive demos

Three in-browser demos for Class 1 concepts: sampling and aliasing, time
shift and reversal, and the convolution flip-and-slide sum. Written as a
standard Streamlit app and hosted as static files via stlite, so it runs
on GitHub Pages with no server.

## Deploy to simbaal.github.io

1. In your `SimbaAl/simbaal.github.io` repository, create a folder, e.g. `eeri325`.
2. Copy `index.html` and `app.py` into that folder.
3. Commit and push. After the Pages build finishes, the demos live at:

   https://simbaal.github.io/eeri325/

4. Put that link (or a QR code of it) on your slides. First load takes
   10–20 seconds while the Python runtime downloads; it is cached afterwards.

## Run locally while developing

Normal Streamlit (instant reloads, best for editing):

    pip install -r requirements.txt
    streamlit run app.py

Test the exact GitHub Pages version (stlite fetches app.py over HTTP, so
opening index.html directly from the file system will not work):

    python -m http.server 8000
    # then open http://localhost:8000

## Editing

All content lives in `app.py`. The three demos are separated by clear
`demo 1/2/3` section markers. Colours at the top match the Class 1 deck
palette (navy, teal, gold). Adding a fourth demo for a later class means
adding one entry to the sidebar radio and one new section.
