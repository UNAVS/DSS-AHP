import numpy as np
import pandas as pd
import streamlit as st
from pairwise_comp import *

st.set_page_config(page_title="Input Kriteria", page_icon="📊", layout="wide")
st.title("Input Kriteria")
# ==== INPUT KRITERIA ====
# Retrieve or initialize the kriteria_input_str in session state
if 'kriteria_input_str' not in st.session_state:
    st.session_state.kriteria_input_str = "A|B|C|D"
st.markdown('''**Kriteria** merupakan **faktor-faktor penting** yang **mempengaruhi pengambilan keputusan** dan digunakan untuk
            menilai pilihan yang tersedia dalam mencapai tujuan. Individu atau kelompok akan **menilai** seberapa penting
            masing-masing kriteria relatif terhadap yang lain dengan menggunakan perbandingan berpasangan.
            Ini membantu dalam **menentukan bobot atau prioritas relatif** dari setiap kriteria.
             \n Berikut interpretasi intensitas keputusan yang digunakan:
            ''')
df = pd.DataFrame(
    {
        "code_ik":["1","3","5","7","9","2, 4, 6, 8"],
        "ket":["Kedua elemen sama pentingnya","Elemen yang satu sedikit lebih penting daripada",
               "Elemen yang satu lebih penting daripada yang lainnya","Satu elemen jelas lebih mutlak penting daripada",
               "Satu elemen mutlak penting daripada elemen lainnya","Nilai-nilai antara dua nilai pertimbangan yang berdekatan"]
    }
)
st.dataframe(
    df,
    column_config={
        "code_ik":"Intensitas Keputusan",
        "ket":"Keterangan"
    },
    hide_index=True,
)
st.caption('⚠️ Jumlah kriteria maksimal yang disarankan adalah 9 kriteria untuk meminimalisir kompleksitas dan memaksimalkan konsistensi.')
# Text input for criteria
kriteria_input_str = st.text_input('Masukkan Kriteria yang Ingin Dipertimbangkan. Pisahkan tiap kriteria dengan "|"', value=st.session_state.kriteria_input_str)
st.session_state.kriteria_input_str = kriteria_input_str
kriteria_inputs = kriteria_input_str.split("|")
st.session_state.kriteria_inputs = kriteria_inputs

# Display kriteria inputs
amount_kriteria = len(kriteria_inputs)
tot = generate_sequence(amount_kriteria)
st.write('Banyak Kriteria: ', amount_kriteria, "|", 'Jenis Kriteria: ', str(kriteria_inputs))

st.caption("Centang Jika Kriteria Bersifat Kuantitatif!")
checks = st.columns(len(kriteria_inputs))
kuant_check_box = {}
status_check_box = []
for i in range(len(kriteria_inputs)):
    if f"keycheck_{i}" not in st.session_state:
        st.session_state[f"keycheck_{i}"] = None

for i in range(len(kriteria_inputs)):
    with checks[i]:
        kuant_check_box[i] = st.checkbox(kriteria_inputs[i], value=False if st.session_state[f"keycheck_{i}"] is None else st.session_state[f"keycheck_{i}"], key=f"check_{i}")
        st.session_state[f"keycheck_{i}"] = kuant_check_box.get(i)
        status_check_box.append(kuant_check_box.get(i))
st.session_state.status_check_box = status_check_box

st.divider()
# Process pairwise comparison
col1, col2 = st.columns([0.4, 0.6])
pref_kriteria_inputs = []
valpref_kriteria_inputs = []

krit_options = {}
for i in range(amount_kriteria):
    for j in range(i+1, amount_kriteria):
        krit_options[f"pref_krit_{i}{j}"] = [kriteria_inputs[i], kriteria_inputs[j]]

for pref_key in krit_options:
    if pref_key not in st.session_state:
        st.session_state[pref_key] = None

for i in range(1, tot+1):
    valpref_key = f"valpref_krit_{i}"
    if valpref_key not in st.session_state:
        st.session_state[valpref_key] = None

for pref_key, options in krit_options.items():
    with col1:
        pref_input = st.radio("Mana yang lebih penting?", options, index=None if st.session_state[pref_key] is None else options.index(st.session_state[pref_key]), horizontal=True, key=pref_key+"a")
        st.session_state[pref_key] = pref_input
    pref_kriteria_inputs.append(pref_input)
st.session_state.pref_kriteria_inputs = pref_kriteria_inputs

for i in range(1, tot+1):
    valpref_key = f"valpref_krit_{i}"
    with col2:
        valpref_input = st.radio("Seberapa lebih penting?", range(1,10), index=None if st.session_state[valpref_key] is None else st.session_state[valpref_key]-1, horizontal=True, key=valpref_key+"b")
        st.session_state[valpref_key] = valpref_input
    valpref_kriteria_inputs.append(valpref_input)
st.session_state.valpref_kriteria_inputs = valpref_kriteria_inputs

df_krit, status_rasio_krit = kalkulasi_matriks('Kriteria', amount_kriteria, kriteria_inputs, pref_kriteria_inputs, valpref_kriteria_inputs)
st.session_state.df_krit, st.session_state.status_rasio_krit = df_krit, status_rasio_krit

st.session_state.status_kriteria = True