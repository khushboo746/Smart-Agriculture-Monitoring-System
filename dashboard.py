
import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_autorefresh import st_autorefresh
from cassandra.cluster import Cluster
from cassandra.io.asyncorereactor import AsyncoreConnection
from datetime import datetime, timezone


# -------------------------------
# 1. Page configuration
# -------------------------------

st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Smart Agriculture Monitoring System")
st.caption("Real-time agricultural sensor monitoring using Kafka and Cassandra")
st_autorefresh(interval=5000, key="dashboard_refresh")

st.divider()


# -------------------------------
# 2. Connect to Cassandra
# -------------------------------

@st.cache_resource
def connect_cassandra():

    cluster = Cluster(
        ["127.0.0.1"],
        connection_class=AsyncoreConnection
    )

    session = cluster.connect("agriculture")

    return session


# -------------------------------
# 3. Fetch sensor data
# -------------------------------

def get_sensor_data():

    session = connect_cassandra()

    today = datetime.now(timezone.utc).date()

    query = """
        SELECT farm_id, reading_date, event_time,
               sensor_id, soil_moisture,
               temperature, humidity, status
        FROM sensor_readings
        WHERE farm_id = %s AND reading_date = %s
    """

    rows = session.execute(query, ("FARM001", today))

    data = [row._asdict() for row in rows]

    return pd.DataFrame(data)


# -------------------------------
# 4. Refresh button
# -------------------------------

if st.button("🔄 Refresh Dashboard"):
    st.rerun()


# -------------------------------
# 5. Display dashboard
# -------------------------------

try:

    df = get_sensor_data()

    if df.empty:

        st.warning(
            "No sensor data found for today. "
            "Please start producer.py and consumer.py."
        )

    else:

        df["event_time"] = pd.to_datetime(df["event_time"])

        df = df.sort_values("event_time")

        latest = df.iloc[-1]

        st.subheader("📊 Latest Sensor Readings")

        # Display metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Soil Moisture",
            f"{latest['soil_moisture']:.2f} %"
        )

        col2.metric(
            "Temperature",
            f"{latest['temperature']:.2f} °C"
        )

        col3.metric(
            "Air Humidity",
            f"{latest['humidity']:.2f} %"
        )

        st.divider()

        # Status alert
        st.subheader("🚨 Farm Condition")

        if latest["status"] == "Dry Soil":

            st.error("⚠️ Alert: Soil moisture is low. Irrigation may be required.")

        elif latest["status"] == "High Temperature":

            st.warning("⚠️ Alert: Temperature is high. Monitor crop conditions.")

        else:

            st.success("✅ Farm conditions are currently normal.")

        st.caption(
            f"Last reading: {latest['event_time']} | "
            f"Sensor: {latest['sensor_id']}"
        )

        st.divider()

        # Soil moisture chart
        st.subheader("💧 Soil Moisture History")

        fig1 = px.line(
            df,
            x="event_time",
            y="soil_moisture",
            title="Soil Moisture Over Time",
            markers=True
        )

        fig1.update_layout(
            xaxis_title="Time",
            yaxis_title="Soil Moisture (%)"
        )

        st.plotly_chart(fig1, use_container_width=True)

        # Temperature chart
        st.subheader("🌡️ Temperature History")

        fig2 = px.line(
            df,
            x="event_time",
            y="temperature",
            title="Temperature Over Time",
            markers=True
        )

        fig2.update_layout(
            xaxis_title="Time",
            yaxis_title="Temperature (°C)"
        )

        st.plotly_chart(fig2, use_container_width=True)

        # Humidity chart
        st.subheader("☁️ Humidity History")

        fig3 = px.line(
            df,
            x="event_time",
            y="humidity",
            title="Air Humidity Over Time",
            markers=True
        )

        fig3.update_layout(
            xaxis_title="Time",
            yaxis_title="Humidity (%)"
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        # Historical readings
        st.subheader("📋 Sensor Data History")

        display_df = df.sort_values(
            "event_time",
            ascending=False
        )

        st.dataframe(
            display_df,
            use_container_width=True
        )

        # Download CSV
        csv = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Sensor Data (CSV)",
            data=csv,
            file_name="agriculture_sensor_data.csv",
            mime="text/csv"
        )

        st.caption(f"Total sensor readings: {len(df)}")


except Exception as e:

    st.error(f"Dashboard error: {e}")

    st.info(
        "Check that Cassandra is running and "
        "the Python 3.10 environment is activated."
    )
