# streamlit-diary

https://altair-viz.github.io/gallery/filled_step_chart.html


# to launch

python3 -m venv .venv

source .venv/bin/activate (ou .venv\Scripts\activate sur Windows)

pip install -r requirements.txt

pip install -U git+https://github.com/thoellrich/july.git@fix-mpl.cbook.MatplotlibDepreciationWarning

streamlit run app.py

(ou sur gcp : streamlit run app.py --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false)
