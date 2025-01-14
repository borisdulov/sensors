import streamlit as st
import random
import pandas as pd

def calculate_data(input_min, input_max, output_min, output_max, error_threshold):
    step_input = (input_max - input_min) / 5
    step_output = (output_max - output_min) / 5

    input_values = [input_min + i * step_input for i in range(6)]
    ideal_outputs = [output_min + i * step_output for i in range(6)]

    deviations = [random.uniform(-1, 1) for _ in range(12)]
    forward_values = [ideal_outputs[i] + deviations[i] for i in range(6)]
    backward_values = [ideal_outputs[i] + deviations[i + 6] for i in range(6)]

    forward_errors = [100 * abs(ideal_outputs[i] - forward_values[i]) / (output_max - output_min) for i in range(6)]
    backward_errors = [100 * abs(ideal_outputs[i] - backward_values[i]) / (output_max - output_min) for i in range(6)]

    data = [
        {
            "Input Value": input_values[i],
            "Ideal Output": ideal_outputs[i],
            "Forward Value": forward_values[i],
            "Backward Value": backward_values[i],
            "Forward Error (%)": forward_errors[i],
            "Backward Error (%)": backward_errors[i],
        }
        for i in range(6)
    ]

    total_errors = sum(1 for e in forward_errors + backward_errors if e > error_threshold)

    return pd.DataFrame(data), total_errors

def main():
    st.title("Sensor Configuration App")

    sensor_types = {
        "Термометр": {
            "default_input_min": -50,
            "default_input_max": 150,
            "default_output_min": 4,
            "default_output_max": 20,
        },
        "Манометр": {
            "default_input_min": 0,
            "default_input_max": 10,
            "default_output_min": 0,
            "default_output_max": 10,
        },
        "Датчик уровня": {
            "default_input_min": 0,
            "default_input_max": 100,
            "default_output_min": 0,
            "default_output_max": 20,
        },
    }

    sensor_type = st.selectbox("Тип датчика", list(sensor_types.keys()))

    if sensor_type:
        config = sensor_types[sensor_type]

        input_min = st.number_input("Мин. входное значение", value=config["default_input_min"], step=1)
        input_max = st.number_input("Макс. входное значение", value=config["default_input_max"], step=1)

        output_min = st.number_input("Мин. выходное значение", value=config["default_output_min"], step=1)
        output_max = st.number_input("Макс. выходное значение", value=config["default_output_max"], step=1)

        error_threshold = st.number_input("Погрешность (%)", value=5.0, step=0.1)

        if st.button("Создать"):
            if input_min >= input_max:
                st.error("Минимальное входное значение должно быть меньше максимального.")
            elif output_min >= output_max:
                st.error("Минимальное выходное значение должно быть меньше максимального.")
            else:
                data, total_errors = calculate_data(input_min, input_max, output_min, output_max, error_threshold)

                st.subheader("Таблица случайных отклонений значений")
                st.dataframe(data)

                if total_errors == 0:
                    st.success("Прибор соответствует заданной точности")
                else:
                    st.error("Прибор не соответствует заданной точности")

if __name__ == "__main__":
    main()
