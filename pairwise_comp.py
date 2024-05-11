import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

def generate_sequence(n):
    sequence = []
    for i in range(1, n + 1):
        term = sum(range(1, i + 1))
        sequence.append(term)
    return sequence[-2]

# ==== KALKULASI KRITERIA ====
def kalkulasi_matriks(jenis_kalkulasi, amount_kriteria, kriteria_inputs, pref_kriteria_inputs, valpref_kriteria_inputs):
    ## ==== MATRIKS PREFERENSI ====
    start_index = 0
    tot = int((amount_kriteria*(amount_kriteria+1))/2)
    pref_krit_split = []
    valpref_krit_split = []

    for i in range(amount_kriteria-1, 0, -1):
        sublist1 = pref_kriteria_inputs[start_index:start_index + i]
        sublist2 = valpref_kriteria_inputs[start_index:start_index + i]
        pref_krit_split.append(sublist1)
        valpref_krit_split.append(sublist2)
        start_index += i

    matrix = np.zeros((amount_kriteria, amount_kriteria))
    np.fill_diagonal(matrix, 1)
    for row in range(len(matrix)-1):
        check_count = 0
        check_len = len(pref_krit_split[row])

        for ele in range(row+1, len(matrix)):
            if pref_krit_split[row][check_count] == kriteria_inputs[row]:
                matrix[row][ele] = valpref_krit_split[row][check_count]
            else:
                matrix[ele][row] = valpref_krit_split[row][check_count]
            check_count += 1
            if check_count == check_len: break

    for row in range(len(matrix)):
        for ele in range(len(matrix)):
            if matrix[row][ele] == 0:
                matrix[row][ele] = 1/matrix[ele][row]
    print(matrix)
    ## ==== KALKULASI BOBOT KRITERIA ====
    transposed_matrix = matrix.copy().transpose()
    for row in range(len(transposed_matrix)):
        row_sum = sum(transposed_matrix[row])
        for ele in range(len(transposed_matrix)):
            transposed_matrix[row][ele] = transposed_matrix[row][ele] / row_sum
    norm_matrix = transposed_matrix.copy().transpose()
    criteria_weight = [round(sum(row)/len(row), 3) for row in norm_matrix]

    ## ==== KALKULASI RASIO KONSISTENSI ====
    rand_idx_dict ={3: 0.58,
                    4: 0.9,
                    5: 1.12,
                    6: 1.24,
                    7: 1.32,
                    8: 1.41,
                    9: 1.45,
                    10: 1.49,
                    11: 1.51,
                    12: 1.48,
                    13: 1.56,
                    14: 1.57,
                    15: 1.58}

    matrix_x = np.dot(matrix, np.array(criteria_weight).transpose())
    lambda_max = sum([matrix_x[i]/criteria_weight[i] for i in range(len(criteria_weight))])/len(criteria_weight)
    cons_idx = (lambda_max-amount_kriteria)/(amount_kriteria-1)
    rand_idx = rand_idx_dict.get(amount_kriteria)
    cons_ratio = round(cons_idx/rand_idx, 3)

    ## ==== OUTPUT KRITERIA ====
    if cons_ratio <= 0.1:
        st.success("KALKULASI BERHASIL! RASIO KONSISTENSI TELAH TERPENUHI! CR: " + str(cons_ratio))
        status_rasio = True
    else:
        st.error("ERROR: RASIO KONSISTENSI TIDAK MEMENUHI! CR: " + str(cons_ratio))
        status_rasio = False
    df_krit = pd.DataFrame({jenis_kalkulasi: kriteria_inputs,
                            'Bobot Prioritas': criteria_weight})
    return df_krit, status_rasio
    # bar_chart = alt.Chart(df_krit).mark_bar().encode(y='Bobot Prioritas:Q', x='Kriteria:O')
    # st.altair_chart(bar_chart, use_container_width=True)

# def kalkulasi_kuant()
