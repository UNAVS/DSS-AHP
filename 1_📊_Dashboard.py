import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
base="light"
st.set_page_config(page_title="AHP Calculator", page_icon="📊", layout="wide")
cont1 = st.container()
cont2 = st.container(border=True)
cont1.title("EconSpace Product Launch Prioritize Recommendation Using AHP")
cont3 = st.container()
cont4 = st.container(border=True)
if 'status_kriteria' not in st.session_state:
    # cont2.markdown('''
    #             Apa itu Analytic Hierarchy Process?\n
    #             AHP merupakan suatu model pendukung keputusan yang dikembangkan oleh Thomas L. Saaty. Model pendukung keputusan ini akan menguraikan masalah multi faktor atau multi kriteria yang kompleks menjadi suatu hirarki, menurut Saaty (1993), hirarki didefinisikan sebagai suatu representasi dari sebuah permasalahan yang kompleks dalam suatu struktur multi-level dimana level pertama adalah tujuan, yang diikuti level faktor, kriteria, sub kriteria, dan seterusnya ke bawah hingga level terakhir dari alternatif. Dengan hirarki, suatu masalah yang kompleks dapat diuraikan ke dalam kelompok-kelompoknya yang kemudian diatur menjadi suatu bentuk hirarki sehingga permasalahan akan tampak lebih terstruktur dan sistematis  (Syaifullah, 2010).
    #             ''')
    cont2.markdown('''
                   Hai ***[EconSpace](https://economicspace.id/)***!👋 Dashboard ini hadir sebagai solusi mengambil
                   keputusan yang tepat untuk menentukan skala prioritas peluncuran produk kamu. Manajemen EconSpace dapat
                   menyesuaikan aspek bisnis yang penting untuk dipertimbangkan agar sesuai dengan ekspektasi yang telah
                   diproyeksikan dalam meluncurkan produk. Menarik bukan?🙌
                ''')
    cont3.header("⚙️Cara Kerja")
    cont3.markdown('''
                    - Tentukan **kriteria** yang akan **dipertimbangkan**
                    - **Isi** halaman input kriteria
                    - Tentukan **alternatif** yang akan **dipertimbangkan**
                    - **Isi** halaman input alternatif
                    - **Hasil** ditampilkan dalam **halaman dashboard** setelah pengisian telah selesai dilakukan
                   ''')
else:
    cont1.header("Cek Rasio Konsistensi")
    if st.session_state.status_rasio_krit == False:
        cont1.error("Nilai Rasio Konsisten Kriteria Belum Terpenuhi! Periksa Kembali Halaman Input Kriteria!")
    else:
        cont1.success("Nilai Rasio Konsistensi Kriteria Terpenuhi!")
    if st.session_state.status_rasio_alter == False:
        cont1.error("Nilai Rasio Konsisten Alternatif Belum Terpenuhi! Periksa Kembali Halaman Input Alternatif!")
    else:
        cont1.success("Nilai Rasio Konsistensi Alternatif Terpenuhi!")


cont3.header("📌Rekomendasi Prioritas Alternatif")
if 'df_rank' not in st.session_state:
    cont3.error("Silahkan Lakukan Input Kriteria dan Alternatif Terlebih Dahulu!")
else:
    df_rank = st.session_state.df_rank
    df_rank = df_rank.sort_values(by="Bobot Prioritas", ascending=False)
    bar_chart_rank = alt.Chart(df_rank).mark_bar().encode(x='Bobot Prioritas:Q', y='Alternatif:O', color=alt.Color('Alternatif').scale(scheme="category10"))
    cont3.altair_chart(bar_chart_rank, use_container_width=True)
    cont3.info(f'''
    Berdasarkan perhitungan AHP, anda direkomendasikan untuk mengambil alternatif: **:green[{df_rank["Alternatif"].to_list()[0].upper()}]**
    ''')

if 'df_krit' not in st.session_state:
    cont3.error("Silahkan Lakukan Input Kriteria Terlebih Dahulu!")
else:
    kriteria_inputs = st.session_state.kriteria_input_str.split("|")
    most_prior_alts = {}
    for i in range(len(kriteria_inputs)):
        curr_data = st.session_state[f"df_alter_{i}"]
        curr_data = curr_data.sort_values(by="Bobot Prioritas", ascending=False)
        if curr_data["Bobot Prioritas"].to_list().count(curr_data["Bobot Prioritas"].to_list()[0]) > 1:
            continue
        most_prior = curr_data[f'Alt Krit {kriteria_inputs[i]}'].to_list()[0]
        if most_prior not in most_prior_alts.keys():
            most_prior_alts[most_prior] = [kriteria_inputs[i]]
        else:
            most_prior_alts[most_prior] += [kriteria_inputs[i]]

    text_most_prior = ''
    for i in most_prior_alts:
        awal = f'Alternatif **:orange[{i}]** unggul pada Kriteria **:green[{", ".join(most_prior_alts.get(i))}]**.\n'
        text_most_prior += awal
    text_most_prior = text_most_prior[:-2]

    df_krit = st.session_state.df_krit
    df_krit = df_krit.sort_values(by="Bobot Prioritas", ascending=False)
    top2 = df_krit["Kriteria"].to_list()[:2]
    cont4 = st.container(border=True)
    cont4.write("Penjelasan:\n"+f"Kriteria yang memiliki peran yang paling besar dalam pemilihan alternatif adalah **:violet[{top2[0].upper()}]** dan **:violet[{top2[1].upper()}]**.\n"+text_most_prior)
    st.divider()
    st.header("Prioritas Kriteria")
    bar_chart = alt.Chart(df_krit).mark_bar().encode(y='Bobot Prioritas:Q', x='Kriteria:O', color=alt.Color('Bobot Prioritas').scale(scheme="yelloworangered", domain=[0,1]))
    st.altair_chart(bar_chart, use_container_width=True)

st.header("📌Detail Prioritas Tiap Kriteria")
if 'kriteria_inputs' not in st.session_state:
    st.error("Silahkan Lakukan Input Kriteria dan Alternatif Terlebih Dahulu!")
else:
    bar_chart_alts = {}
    for i in range(len(kriteria_inputs)):
        st.subheader(f"Detail Prioritas Kriteria {kriteria_inputs[i]}")
        bar_chart_alts[i] = alt.Chart(st.session_state[f"df_alter_{i}"]).mark_bar().encode(
            x=alt.X(f'Alt Krit {kriteria_inputs[i]}:N', title='Alternatif'),
            y=alt.Y('Bobot Prioritas:Q', title='Bobot Prioritas'), color=alt.Color('Bobot Prioritas').scale(scheme="yelloworangered", domain=[0,1]))
        st.altair_chart(bar_chart_alts[i], use_container_width=True)
