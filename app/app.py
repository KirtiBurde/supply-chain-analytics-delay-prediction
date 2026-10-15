import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Supply Chain Risk Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROFESSIONAL THEME
# ============================================================

NAVY = "#102A43"
DARK_NAVY = "#0B1F33"
TEAL = "#008F95"
ORANGE = "#F59E0B"
RED = "#DC3545"
GREEN = "#16A34A"
BACKGROUND = "#F4F7FB"
WHITE = "#FFFFFF"
TEXT = "#243447"
MUTED = "#64748B"

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #F4F7FB;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #102A43 0%,
            #0B1F33 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #102A43;
        font-weight: 700;
    }

    /* General text */
    .stApp p {
        line-height: 1.6;
    }

    /* Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(
            90deg,
            #008F95,
            #087E8B
        );
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.4rem;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover {
        background: #006D73;
        color: white;
    }

    /* Metric containers */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 14px rgba(16, 42, 67, 0.05);
    }

    div[data-testid="stMetricValue"] {
        color: #102A43;
        font-weight: 700;
    }

    /* Inputs */
    div[data-baseweb="select"] > div {
        border-radius: 9px;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 9px;
    }

    /* Horizontal divider */
    hr {
        border-color: #E2E8F0;
    }

    /* Custom cards */
    .hero-card {
        background: linear-gradient(
            120deg,
            #102A43 0%,
            #164E63 65%,
            #008F95 100%
        );
        padding: 38px;
        border-radius: 18px;
        color: white;
        margin-bottom: 26px;
        box-shadow: 0 8px 25px rgba(16, 42, 67, 0.12);
    }

    .hero-card h1 {
        color: white;
        margin-bottom: 12px;
        font-size: 2.2rem;
    }

    .hero-card p {
        color: #E2F3F4;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .section-heading {
        font-size: 1.4rem;
        font-weight: 700;
        color: #102A43;
        margin-top: 18px;
        margin-bottom: 18px;
    }

    .feature-card {
        background: white;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        min-height: 175px;
        box-shadow: 0 4px 12px rgba(16, 42, 67, 0.04);
        margin-bottom: 14px;
    }

    .feature-card h3 {
        font-size: 1.12rem;
        margin-bottom: 10px;
    }

    .feature-card p {
        color: #64748B;
        font-size: 0.94rem;
    }

    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 26px;
        margin-top: 12px;
        box-shadow: 0 4px 14px rgba(16, 42, 67, 0.05);
    }

    .result-card h2 {
        margin: 8px 0;
    }

    .result-card p {
        color: #64748B;
        margin-bottom: 4px;
    }

    .risk-low {
        border-left: 6px solid #16A34A;
    }

    .risk-medium {
        border-left: 6px solid #F59E0B;
    }

    .risk-high {
        border-left: 6px solid #DC3545;
    }

    .workflow-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        min-height: 135px;
        margin-bottom: 10px;
    }

    .workflow-card h3 {
        font-size: 1rem;
        margin-bottom: 8px;
    }

    .workflow-card p {
        color: #64748B;
        font-size: 0.88rem;
    }

    .footer {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        padding: 20px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. LOAD TRAINED MODEL
# ============================================================

@st.cache_resource
def load_model():

    model_path = (
        Path(__file__).resolve().parent
        / "delay_prediction_model.pkl"
    )

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    return joblib.load(model_path)


try:
    model = load_model()

except Exception as e:
    st.error("Unable to load the trained machine learning model.")
    st.exception(e)
    st.stop()


# ============================================================
# 4. MODEL FEATURES
# ============================================================

FEATURES = [
    "Delivery_Partner",
    "Package_Type",
    "Vehicle_Type",
    "Delivery_Mode",
    "Region",
    "Weather_Condition",
    "Distance_km",
    "Package_weight_kg"
]

CATEGORIES = {

    "Delivery_Partner": [
        "Amazon Logistics",
        "Blue Dart",
        "Delhivery",
        "Dhl",
        "Ecom Express",
        "Ekart",
        "Fedex",
        "Shadowfax",
        "Xpressbees"
    ],

    "Package_Type": [
        "Automobile Parts",
        "Clothing",
        "Cosmetics",
        "Documents",
        "Electronics",
        "Fragile Items",
        "Furniture",
        "Groceries",
        "Pharmacy"
    ],

    "Vehicle_Type": [
        "Bike",
        "Ev Bike",
        "Ev Van",
        "Scooter",
        "Truck",
        "Van"
    ],

    "Delivery_Mode": [
        "Express",
        "Same Day",
        "Standard",
        "Two Day"
    ],

    "Region": [
        "Central",
        "East",
        "North",
        "South",
        "West"
    ],

    "Weather_Condition": [
        "Clear",
        "Cold",
        "Foggy",
        "Hot",
        "Rainy",
        "Stormy"
    ]
}

NUMERIC_RANGES = {
    "Distance_km": (3.60, 297.10),
    "Package_weight_kg": (0.67, 49.52)
}


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def get_risk_level(probability):

    if probability < 0.40:
        return "Low Risk"

    elif probability < 0.70:
        return "Medium Risk"

    return "High Risk"


def get_risk_color(risk):

    if risk == "Low Risk":
        return GREEN

    elif risk == "Medium Risk":
        return ORANGE

    return RED


def get_risk_css(risk):

    if risk == "Low Risk":
        return "risk-low"

    elif risk == "Medium Risk":
        return "risk-medium"

    return "risk-high"


def predict_deliveries(data):

    input_data = data[FEATURES].copy()

    predictions = model.predict(input_data)

    probabilities = model.predict_proba(input_data)

    class_labels = list(model.classes_)

    delayed_index = class_labels.index(1)

    delay_probabilities = probabilities[:, delayed_index]

    results = data.copy()

    results["Predicted_Delay"] = predictions.astype(int)

    results["Delay_Status"] = np.where(
        predictions == 1,
        "Delayed",
        "On Time"
    )

    results["Delay_Probability"] = delay_probabilities

    results["Delay_Risk_Percentage"] = (
        delay_probabilities * 100
    ).round(2)

    results["Risk_Category"] = [
        get_risk_level(p)
        for p in delay_probabilities
    ]

    return results


def validate_bulk_data(data):

    if data.empty:
        return "The uploaded CSV contains no delivery records."

    missing_columns = [
        col for col in FEATURES
        if col not in data.columns
    ]

    if missing_columns:
        return (
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    if data[FEATURES].isnull().any().any():
        return (
            "Missing values detected in required columns. "
            "Please complete all delivery details."
        )

    for column, allowed_values in CATEGORIES.items():

        invalid_values = data.loc[
            ~data[column].isin(allowed_values),
            column
        ].unique()

        if len(invalid_values) > 0:
            return (
                f"Invalid values in {column}: "
                f"{list(invalid_values)}"
            )

    for column, (minimum, maximum) in NUMERIC_RANGES.items():

        converted = pd.to_numeric(
            data[column],
            errors="coerce"
        )

        if converted.isnull().any():
            return (
                f"{column} contains invalid numeric values."
            )

        if (
            (converted < minimum)
            | (converted > maximum)
        ).any():

            return (
                f"{column} must be between "
                f"{minimum} and {maximum}."
            )

        data[column] = converted

    return None


def get_recommendation(risk):

    if risk == "Low Risk":
        return (
            "The model estimates a relatively low delay risk. "
            "Continue routine shipment monitoring."
        )

    elif risk == "Medium Risk":
        return (
            "The model estimates moderate delay risk. "
            "Consider reviewing shipment progress, "
            "weather conditions, and delivery schedules."
        )

    return (
        "The model estimates elevated delay risk. "
        "Consider prioritizing shipment monitoring, "
        "reviewing delivery arrangements, and "
        "preparing contingency actions."
    )


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 15px 0 25px 0;">
            <h2 style="color:white;">
                🚚 Supply Chain
            </h2>
            <p style="color:#A8DADC;">
                Risk Intelligence Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "Single Delivery Prediction",
            "Bulk Delivery Prediction",
            "Model Information"
        ]
    )

    st.divider()

    st.caption("AI-Powered Logistics Analytics")

    st.caption("Machine Learning • Risk Assessment")

    st.caption("Portfolio Application")


# ============================================================
# 7. HOME PAGE
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero-card">
            <h1>AI-Powered Supply Chain Analytics</h1>
            <p>
                Delivery Risk Intelligence & Predictive Analytics
            </p>
            <br>
            <p>
                Transform shipment information into actionable
                delivery risk insights using machine learning.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Platform Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Model Input Features",
            "8",
            help="Six categorical and two numerical features"
        )

    with col2:
        st.metric(
            "Prediction Classes",
            "2",
            help="On Time and Delayed"
        )

    with col3:
        st.metric(
            "Risk Categories",
            "3",
            help="Low, Medium and High"
        )

    st.markdown(
        '<div class="section-heading">Platform Capabilities</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🚚 Single Delivery Prediction</h3>
                <p>
                    Evaluate an individual shipment using
                    delivery details and operational conditions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📊 Bulk Delivery Analytics</h3>
                <p>
                    Upload multiple shipments, generate
                    predictions, and download analytical results.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>⚠️ Risk Intelligence</h3>
                <p>
                    Classify estimated delivery risk into
                    low, medium, and high-risk categories.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-heading">How the Platform Works</div>',
        unsafe_allow_html=True
    )

    step1, step2, step3, step4 = st.columns(4)

    steps = [
        (
            "1. Enter Details",
            "Provide shipment and delivery information."
        ),
        (
            "2. ML Processing",
            "The trained model analyzes input features."
        ),
        (
            "3. Risk Prediction",
            "Generate delay probability and predicted status."
        ),
        (
            "4. Decision Support",
            "Review risk level and suggested monitoring actions."
        )
    ]

    for column, (title, description) in zip(
        [step1, step2, step3, step4],
        steps
    ):

        with column:

            st.markdown(
                f"""
                <div class="workflow-card">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.info(
        "Use the sidebar to start a single delivery prediction "
        "or analyze multiple shipments."
    )


# ============================================================
# 8. SINGLE DELIVERY PREDICTION
# ============================================================

elif page == "Single Delivery Prediction":

    st.title("🚚 Single Delivery Risk Prediction")

    st.caption(
        "Enter shipment information to estimate delivery "
        "delay probability using the trained ML model."
    )

    st.markdown(
        '<div class="section-heading">Shipment Details</div>',
        unsafe_allow_html=True
    )

    with st.form("single_prediction_form"):

        col1, col2 = st.columns(2, gap="large")

        with col1:

            delivery_partner = st.selectbox(
                "Delivery Partner",
                CATEGORIES["Delivery_Partner"]
            )

            package_type = st.selectbox(
                "Package Type",
                CATEGORIES["Package_Type"]
            )

            vehicle_type = st.selectbox(
                "Vehicle Type",
                CATEGORIES["Vehicle_Type"]
            )

            delivery_mode = st.selectbox(
                "Delivery Mode",
                CATEGORIES["Delivery_Mode"]
            )

        with col2:

            region = st.selectbox(
                "Region",
                CATEGORIES["Region"]
            )

            weather_condition = st.selectbox(
                "Weather Condition",
                CATEGORIES["Weather_Condition"]
            )

            distance = st.number_input(
                "Distance (km)",
                min_value=3.60,
                max_value=297.10,
                value=50.0,
                step=1.0
            )

            package_weight = st.number_input(
                "Package Weight (kg)",
                min_value=0.67,
                max_value=49.52,
                value=5.0,
                step=0.5
            )

        submitted = st.form_submit_button(
            "🔍 Analyze Delivery Risk",
            type="primary",
            use_container_width=True
        )

    if submitted:

        input_data = pd.DataFrame(
            [[
                delivery_partner,
                package_type,
                vehicle_type,
                delivery_mode,
                region,
                weather_condition,
                distance,
                package_weight
            ]],
            columns=FEATURES
        )

        try:

            result = predict_deliveries(input_data)

            prediction = int(
                result["Predicted_Delay"].iloc[0]
            )

            probability = float(
                result["Delay_Probability"].iloc[0]
            )

            risk = result["Risk_Category"].iloc[0]

            risk_color = get_risk_color(risk)

            risk_css = get_risk_css(risk)

            status = (
                "DELAYED"
                if prediction == 1
                else "ON TIME"
            )

            st.divider()

            st.markdown(
                '<div class="section-heading">Prediction Results</div>',
                unsafe_allow_html=True
            )

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.markdown(
                    f"""
                    <div class="result-card {risk_css}">
                        <p>Predicted Delivery Status</p>
                        <h2>{status}</h2>
                        <p>Machine Learning Classification</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with result_col2:

                st.markdown(
                    f"""
                    <div class="result-card {risk_css}">
                        <p>Estimated Delay Probability</p>
                        <h2>{probability * 100:.2f}%</h2>
                        <p style="color:{risk_color};">
                            {risk}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")

            st.subheader("Delivery Risk Indicator")

            st.progress(
                probability,
                text=f"Estimated Delay Risk: {probability * 100:.2f}%"
            )

            st.subheader("Risk Assessment")

            if risk == "Low Risk":
                st.success(f"🟢 {risk}")

            elif risk == "Medium Risk":
                st.warning(f"🟠 {risk}")

            else:
                st.error(f"🔴 {risk}")

            st.subheader("Operational Recommendation")

            st.info(get_recommendation(risk))

            st.caption(
                "Predictions are statistical estimates, not "
                "guaranteed delivery outcomes. Risk thresholds "
                "are defined by the application."
            )

        except Exception as e:

            st.error("Unable to generate the prediction.")
            st.exception(e)


# ============================================================
# 9. BULK DELIVERY PREDICTION
# ============================================================

elif page == "Bulk Delivery Prediction":

    st.title("📊 Bulk Delivery Risk Analytics")

    st.caption(
        "Upload shipment records to generate delivery "
        "predictions and analyze overall risk distribution."
    )

    st.markdown(
        '<div class="section-heading">Bulk Prediction Workflow</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    workflow = [
        (
            "Step 1",
            "Download the CSV template."
        ),
        (
            "Step 2",
            "Add your shipment records."
        ),
        (
            "Step 3",
            "Upload and analyze deliveries."
        )
    ]

    for column, (title, description) in zip(
        [col1, col2, col3],
        workflow
    ):

        with column:

            st.markdown(
                f"""
                <div class="workflow-card">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("Download Input Template")

    template = pd.DataFrame(
        [
            [
                "Blue Dart",
                "Electronics",
                "Truck",
                "Standard",
                "North",
                "Rainy",
                200.0,
                15.0
            ]
        ],
        columns=FEATURES
    )

    st.download_button(
        label="⬇️ Download CSV Template",
        data=template.to_csv(index=False),
        file_name="delivery_prediction_template.csv",
        mime="text/csv"
    )

    with st.expander("View Required Input Columns"):

        feature_table = pd.DataFrame({
            "Feature": FEATURES,
            "Data Type": [
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Numerical",
                "Numerical"
            ]
        })

        st.dataframe(
            feature_table,
            hide_index=True,
            use_container_width=True
        )

        st.caption(
            "Column names and categorical values must match "
            "the model's expected input format."
        )

    st.divider()

    st.subheader("Upload Delivery Data")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV containing the eight required features."
    )

    if uploaded_file is not None:

        try:

            data = pd.read_csv(uploaded_file)

            error = validate_bulk_data(data)

            if error:

                st.error(error)

            else:

                st.success(
                    "CSV uploaded and validated successfully."
                )

                st.subheader("Uploaded Data Preview")

                st.dataframe(
                    data.head(10),
                    use_container_width=True
                )

                if st.button(
                    "🚀 Generate Bulk Predictions",
                    type="primary"
                ):

                    results = predict_deliveries(data)

                    total = len(results)

                    delayed = int(
                        (results["Predicted_Delay"] == 1).sum()
                    )

                    on_time = total - delayed

                    delay_rate = (
                        delayed / total * 100
                        if total > 0
                        else 0
                    )

                    st.divider()

                    st.subheader("Prediction Summary")

                    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

                    kpi1.metric(
                        "Total Deliveries",
                        f"{total:,}"
                    )

                    kpi2.metric(
                        "Predicted Delays",
                        f"{delayed:,}"
                    )

                    kpi3.metric(
                        "Predicted On-Time",
                        f"{on_time:,}"
                    )

                    kpi4.metric(
                        "Predicted Delay Rate",
                        f"{delay_rate:.2f}%"
                    )

                    st.markdown(
                        '<div class="section-heading">'
                        'Delivery Risk Distribution'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    chart_col1, chart_col2 = st.columns(2)

                    with chart_col1:

                        st.subheader("Predicted Delivery Status")

                        status_counts = (
                            results["Delay_Status"]
                            .value_counts()
                            .reindex(
                                ["On Time", "Delayed"],
                                fill_value=0
                            )
                        )

                        st.bar_chart(
                            status_counts,
                            color=TEAL
                        )

                    with chart_col2:

                        st.subheader("Risk Category Distribution")

                        risk_counts = (
                            results["Risk_Category"]
                            .value_counts()
                            .reindex(
                                [
                                    "Low Risk",
                                    "Medium Risk",
                                    "High Risk"
                                ],
                                fill_value=0
                            )
                        )

                        st.bar_chart(
                            risk_counts,
                            color=ORANGE
                        )

                    st.divider()

                    st.subheader("Detailed Prediction Results")

                    st.dataframe(
                        results,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.download_button(
                        label="⬇️ Download Prediction Results",
                        data=results.to_csv(index=False),
                        file_name="delivery_delay_predictions.csv",
                        mime="text/csv"
                    )

                    st.caption(
                        "Predicted delay rate represents the "
                        "percentage of uploaded records classified "
                        "as delayed. It is not an observed delay rate."
                    )

        except Exception as e:

            st.error(
                "Unable to process the uploaded CSV file."
            )

            st.exception(e)


# ============================================================
# 10. MODEL INFORMATION
# ============================================================

elif page == "Model Information":

    st.title("🤖 Machine Learning Model Intelligence")

    st.caption(
        "Understand the model architecture, input features, "
        "prediction methodology, and risk classification."
    )

    st.markdown(
        '<div class="section-heading">Model Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Machine Learning Model",
        "Random Forest"
    )

    col2.metric(
        "Input Features",
        "8"
    )

    col3.metric(
        "Target Classes",
        "2"
    )

    st.info(
        "The application uses a trained machine learning "
        "pipeline to estimate whether a shipment may "
        "experience a delivery delay."
    )

    st.markdown(
        '<div class="section-heading">Model Architecture</div>',
        unsafe_allow_html=True
    )

    architecture = pd.DataFrame({
        "Component": [
            "Input Data",
            "Categorical Preprocessing",
            "Numerical Preprocessing",
            "Classification Model",
            "Prediction Output"
        ],
        "Description": [
            "Eight shipment and logistics features",
            "One-Hot Encoding",
            "Standard Scaling",
            "Random Forest Classifier",
            "Predicted class and estimated delay probability"
        ]
    })

    st.dataframe(
        architecture,
        hide_index=True,
        use_container_width=True
    )

    st.markdown(
        '<div class="section-heading">Input Features</div>',
        unsafe_allow_html=True
    )

    feature_details = pd.DataFrame({
        "Feature": FEATURES,
        "Type": [
            "Categorical",
            "Categorical",
            "Categorical",
            "Categorical",
            "Categorical",
            "Categorical",
            "Numerical",
            "Numerical"
        ],
        "Business Meaning": [
            "Logistics service provider",
            "Type of shipment",
            "Transportation vehicle",
            "Delivery service category",
            "Geographical delivery region",
            "Weather during delivery",
            "Shipment travel distance",
            "Weight of the package"
        ]
    })

    st.dataframe(
        feature_details,
        hide_index=True,
        use_container_width=True
    )

    st.markdown(
        '<div class="section-heading">Prediction Classes</div>',
        unsafe_allow_html=True
    )

    class_col1, class_col2 = st.columns(2)

    with class_col1:
        st.success(
            "Class 0 — On Time"
        )

    with class_col2:
        st.error(
            "Class 1 — Delayed"
        )

    st.markdown(
        '<div class="section-heading">Risk Classification</div>',
        unsafe_allow_html=True
    )

    risk_table = pd.DataFrame({
        "Risk Category": [
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ],
        "Estimated Delay Probability": [
            "Below 40%",
            "40% to below 70%",
            "70% or above"
        ],
        "Interpretation": [
            "Lower estimated delay risk",
            "Moderate estimated delay risk",
            "Elevated estimated delay risk"
        ]
    })

    st.dataframe(
        risk_table,
        hide_index=True,
        use_container_width=True
    )

    st.warning(
        "Risk categories use application-defined probability "
        "thresholds. They are not separate model classes."
    )

    st.markdown(
        '<div class="section-heading">Model Limitations</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        - Predictions depend on the quality and
          representativeness of the training data.

        - Estimated probabilities may not be perfectly calibrated.

        - The model does not guarantee actual delivery outcomes.

        - Input values outside the supported data ranges
          are restricted by the application.

        - Operational recommendations are general guidance,
          not independently optimized logistics decisions.
        """
    )


# ============================================================
# 11. FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        AI-Powered Supply Chain Analytics & Logistics Optimization Platform
        <br>
        Delivery Risk Intelligence | Machine Learning | Streamlit
    </div>
    """,
    unsafe_allow_html=True
)