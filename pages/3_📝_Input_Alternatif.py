import numpy as np
import pandas as pd
import streamlit as st
from pairwise_comp import *

st.set_page_config(page_title="Input Alternatif", page_icon="📊", layout="wide")
st.title("Input Alternatif")
# ==== INPUT ALTERNATIF ====
# Retrieve or initialize the alter_input_str in session state
if 'alter_input_str' not in st.session_state:
    st.session_state.alter_input_str = "Pil1|Pil2|Pil3"

st.markdown('''**Alternatif** merupakan **solusi potensial** atau **pilihan yang sedang dievaluasi** dalam proses pengambilan keputusan.
            Setelah tujuan utama diidentifikasi dan kriteria untuk mengevaluasi alternatif tersebut ditetapkan, langkah berikutnya
            dalam AHP adalah mengidentifikasi dan menilai alternatif berdasarkan kriteria tersebut.
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
# Text input for altenatif
#st.caption('Tiap alternatif sebaiknya memiliki maksimal 5 karakter. Pisahkan tiap alternatif dengan "|"')

alter_input_str = st.text_input('Masukkan Alternatif yang Ingin Dipertimbangkan. Pisahkan tiap alternatif dengan "|"', value=st.session_state.alter_input_str)
st.session_state.alter_input_str = alter_input_str

alter_inputs = alter_input_str.split("|")
st.session_state.alter_inputs = alter_inputs

# Display alternatif inputs
amount_alter = len(alter_inputs)
tot = generate_sequence(amount_alter)
st.write('Banyak Alternatif: ', amount_alter, "|", 'Jenis Alternatif: ', str(alter_inputs))

status_check_box = st.session_state.status_check_box
kriteria_inputs = st.session_state.kriteria_inputs
alt_matrix = []
status_rasio_alter_list = []
for krit_idx, krit in enumerate(kriteria_inputs):
    st.subheader(f"Komparasi {krit}")
    st.write(f"Bandingkan Alternatif Berdasarkan Aspek {krit}!")

    if status_check_box[krit_idx] == True:
        col_check = st.columns(len(alter_inputs))
        check_options = {}

        for i in range(len(alter_inputs)):
            if f"check_{krit_idx}{i}" not in st.session_state:
                st.session_state[f"check_{krit_idx}{i}"] = None

        for i in range(len(alter_inputs)):
            with col_check[i]:
                check_options[i] = st.number_input(f"Masukkan Value {alter_inputs[i]}:", key=f"check_{krit_idx}{i}"+"a", value=0.00 if st.session_state[f"check_{krit_idx}{i}"] == None else st.session_state[f"check_{krit_idx}{i}"])
                st.session_state[f"check_{krit_idx}{i}"] = check_options.get(i)

        kuant_weights = check_options.values()
        sum_kuant_weights = sum(kuant_weights)
        try:
            kuant_weights = [ele/sum_kuant_weights for ele in kuant_weights]
        except ZeroDivisionError:
            kuant_weights = [0 for _ in kuant_weights]
        df_alter = pd.DataFrame({f'Alt Krit {krit}': alter_inputs,
                                'Bobot Prioritas': kuant_weights})
        alt_matrix.append(kuant_weights)
        st.session_state[f"df_alter_{krit_idx}"] = df_alter

    else:
        # Process pairwise comparison
        col1, col2 = st.columns([0.4, 0.6])
        pref_alter_inputs = []
        valpref_alter_inputs = []

        alter_options = {}
        for i in range(amount_alter):
            for j in range(i+1, amount_alter):
                alter_options[f"pref_alter_{krit_idx}{i}{j}"] = [alter_inputs[i], alter_inputs[j]]

        for pref_key in alter_options:
            if pref_key not in st.session_state:
                st.session_state[pref_key] = None

        for i in range(1, tot+1):
            valpref_key = f"valpref_alter_{krit_idx}{i}"
            if valpref_key not in st.session_state:
                st.session_state[valpref_key] = None

        for pref_key, options in alter_options.items():
            with col1:
                pref_input = st.radio("Mana yang lebih baik?", options, index=None if st.session_state[pref_key] is None else options.index(st.session_state[pref_key]), horizontal=True, key=pref_key+"a")
                st.session_state[pref_key] = pref_input
            pref_alter_inputs.append(pref_input)
        st.session_state.pref_alter_inputs = pref_alter_inputs

        for i in range(1, tot+1):
            valpref_key = f"valpref_alter_{krit_idx}{i}"
            with col2:
                valpref_input = st.radio("Seberapa lebih baik?", range(1,10), index=None if st.session_state[valpref_key] is None else st.session_state[valpref_key]-1, horizontal=True, key=valpref_key+"b")
                st.session_state[valpref_key] = valpref_input
            valpref_alter_inputs.append(valpref_input)
        st.session_state.valpref_alter_inputs = valpref_alter_inputs

        df_alter, status_rasio_alter = kalkulasi_matriks(f'Alt Krit {krit}', amount_alter, alter_inputs, pref_alter_inputs, valpref_alter_inputs)
        alt_matrix.append(df_alter['Bobot Prioritas'].to_list())
        status_rasio_alter_list.append(status_rasio_alter)
        st.session_state[f"df_alter_{krit_idx}"], st.session_state[f"status_rasio_alter_{krit_idx}"] = df_alter, status_rasio_alter

alt_matrix = np.array(alt_matrix).transpose()
krit_weight = st.session_state.df_krit["Bobot Prioritas"].to_list()
krit_weight = np.array(krit_weight).transpose()
alt_rank_vec = np.dot(alt_matrix, krit_weight)

df_rank = pd.DataFrame({'Alternatif': alter_inputs,
                        'Bobot Prioritas': alt_rank_vec})
st.session_state.df_rank = df_rank

if False in status_rasio_alter_list:
    st.session_state.status_rasio_alter = False
else:
    st.session_state.status_rasio_alter = True