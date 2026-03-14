import numpy as np
from scipy.integrate import solve_ivp
import streamlit as st
import plotly.graph_objects as go

# ===============================
# 1. PARAMETER TANGKI
# ===============================

class TankConfig:

    def __init__(self):

        # Dimensi tangki silinder
        self.radius = 1.0          # meter
        self.height = 3.0          # meter

        # Debit air
        self.inlet_flow = 0.05     # m3/s
        self.outlet_flow = 0.03    # m3/s

        # Kondisi awal
        self.initial_height = 0.5  # meter

        # Waktu simulasi
        self.simulation_time = 200 # detik


# ===============================
# 2. MODEL FISIKA
# ===============================

class TankModel:

    def __init__(self, config):
        self.config = config

    def tank_area(self):
        return np.pi * self.config.radius**2

    def dh_dt(self, t, h):

        A = self.tank_area()

        Qin = self.config.inlet_flow
        Qout = self.config.outlet_flow

        return (Qin - Qout) / A


# ===============================
# 3. SIMULASI
# ===============================

class TankSimulator:

    def __init__(self, config):

        self.config = config
        self.model = TankModel(config)

    def run(self):

        t_span = (0, self.config.simulation_time)
        t_eval = np.linspace(0, self.config.simulation_time, 500)

        sol = solve_ivp(
            self.model.dh_dt,
            t_span,
            [self.config.initial_height],
            t_eval=t_eval
        )

        return sol.t, sol.y[0]


# ===============================
# 4. VISUALISASI
# ===============================

def plot_height(time, height):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time,
        y=height,
        mode='lines',
        name='Ketinggian Air'
    ))

    fig.update_layout(
        title="Perubahan Ketinggian Air dalam Tangki",
        xaxis_title="Waktu (detik)",
        yaxis_title="Ketinggian Air (meter)",
        template="plotly_white"
    )

    return fig


# ===============================
# 5. STREAMLIT APP
# ===============================

def main():

    st.title("Simulasi Sistem Tangki Air")

    config = TankConfig()

    st.sidebar.header("Parameter")

    config.radius = st.sidebar.slider("Radius Tangki (m)",0.5,3.0,1.0)
    config.height = st.sidebar.slider("Tinggi Tangki (m)",1.0,5.0,3.0)

    config.inlet_flow = st.sidebar.slider("Debit Inlet (m3/s)",0.01,0.1,0.05)
    config.outlet_flow = st.sidebar.slider("Debit Outlet (m3/s)",0.01,0.1,0.03)

    config.initial_height = st.sidebar.slider("Ketinggian Awal (m)",0.0,config.height,0.5)

    config.simulation_time = st.sidebar.slider("Waktu Simulasi (s)",50,500,200)

    simulator = TankSimulator(config)

    time, height = simulator.run()

    st.subheader("Grafik Ketinggian Air")

    fig = plot_height(time, height)

    st.plotly_chart(fig)

    st.write("### Analisis")

    if config.inlet_flow > config.outlet_flow:
        st.success("Tangki akan terisi penuh")
    elif config.inlet_flow < config.outlet_flow:
        st.warning("Tangki akan kosong")
    else:
        st.info("Volume air stabil")


if __name__ == "__main__":
    main()