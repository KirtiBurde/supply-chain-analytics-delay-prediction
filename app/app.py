"""Supply Chain Risk Intelligence — Streamlit portfolio application.
Run from the repository root: python -m streamlit run app/app.py
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
import io

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Supply Chain Risk Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="auto",
)

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "delay_prediction_model.pkl"
FEATURES = [
    "Delivery_Partner", "Package_Type", "Vehicle_Type", "Delivery_Mode",
    "Region", "Weather_Condition", "Distance_km", "Package_weight_kg",
]
CATEGORIES = {
    "Delivery_Partner": ["Amazon Logistics", "Blue Dart", "Delhivery", "Dhl", "Ecom Express", "Ekart", "Fedex", "Shadowfax", "Xpressbees"],
    "Package_Type": ["Automobile Parts", "Clothing", "Cosmetics", "Documents", "Electronics", "Fragile Items", "Furniture", "Groceries", "Pharmacy"],
    "Vehicle_Type": ["Bike", "Ev Bike", "Ev Van", "Scooter", "Truck", "Van"],
    "Delivery_Mode": ["Express", "Same Day", "Standard", "Two Day"],
    "Region": ["Central", "East", "North", "South", "West"],
    "Weather_Condition": ["Clear", "Cold", "Foggy", "Hot", "Rainy", "Stormy"],
}
TRAINING_RANGES = {"Distance_km": (3.60, 297.10), "Package_weight_kg": (0.67, 49.52)}

# CSS uses Streamlit theme tokens. Risk colors remain fixed across themes.
st.markdown("""
<style>
:root {
  --surface: var(--secondary-background-color, #f1f5f9);
  --page: var(--background-color, #ffffff);
  --ink: var(--text-color, #102a43);
  --accent: var(--primary-color, #0d9488);
  --edge: color-mix(in srgb, var(--ink) 15%, transparent);
}
.block-container {max-width: 1160px; padding-top: 2rem; padding-bottom: 3rem;}
[data-testid="stSidebar"] {border-right: 1px solid var(--edge);}
.app-hero {background: linear-gradient(125deg,#0b2545,#155e75); color:#fff;
  border-radius:20px; padding:30px 32px; margin-bottom:22px;}
.app-hero h1 {color:#fff !important; margin:0 0 12px; font-size:2.25rem;}
.app-hero p {color:#d7eef2; margin:0; line-height:1.65;}
.eyebrow {font-size:.8rem; font-weight:800; letter-spacing:.13em; color:#5eead4;}
.info-card, .result-card {background:var(--surface); color:var(--ink); border:1px solid var(--edge);
  border-radius:16px; padding:23px; height:100%; overflow-wrap:anywhere;}
/* Home feature cards: consistent desktop height even when descriptions wrap. */
.info-card {min-height:210px; box-sizing:border-box; display:flex; flex-direction:column;}
.info-card h3, .result-card h3 {margin:0 0 10px; font-size:1.05rem; color:var(--ink);}
.info-card p, .result-card p {margin:5px 0; color:var(--ink); opacity:.85;}
.result-card h2 {font-size:2rem; margin:10px 0; color:var(--ink);}
.result-card .muted {font-size:.82rem; opacity:.75;}
.result-card.low {border-top:4px solid #16a34a;}
.result-card.medium {border-top:4px solid #f59e0b;}
.result-card.high {border-top:4px solid #dc2626;}
.section-heading {font-size:1.18rem; font-weight:750; margin:22px 0 12px; color:var(--ink);}
.small-note {font-size:.86rem; opacity:.8;}
.stButton button, .stDownloadButton button, .stFormSubmitButton button {min-height:44px;}
/* Streamlit already stacks columns at narrow widths; this adjusts surrounding UI. */
@media (max-width: 768px) {
  .block-container {padding:1rem .8rem 2rem;}
  .app-hero {padding:20px 18px; border-radius:14px;}
  .app-hero h1 {font-size:1.65rem;}
  .info-card, .result-card {padding:16px; border-radius:12px;}
  .info-card {min-height:0;}
  .result-card h2 {font-size:1.6rem;}
  h1 {font-size:1.65rem !important;}
  h2 {font-size:1.35rem !important;}
  .stButton button, .stDownloadButton button, .stFormSubmitButton button {width:100%;}
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading prediction model...")
def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def risk_category(probability: float) -> str:
    if probability < 0.40:
        return "Low Risk"
    if probability < 0.70:
        return "Medium Risk"
    return "High Risk"


def risk_color(risk: str) -> str:
    return {"Low Risk": "#16A34A", "Medium Risk": "#F59E0B", "High Risk": "#DC2626"}[risk]


def risk_css(risk: str) -> str:
    return {"Low Risk": "low", "Medium Risk": "medium", "High Risk": "high"}[risk]


def predict_deliveries(data: pd.DataFrame) -> pd.DataFrame:
    model = load_model()
    features = data[FEATURES].copy()
    predictions = model.predict(features)
    # The trained classifier must encode class 1 as delayed.
    classes = list(model.classes_)
    if 1 not in classes:
        raise ValueError("Model does not have class 1 (delayed). Verify the saved model.")
    delay_column = classes.index(1)
    probabilities = model.predict_proba(features)[:, delay_column]
    result = data.copy()
    result["Predicted_Delay"] = predictions.astype(int)
    result["Delay_Status"] = np.where(result["Predicted_Delay"] == 1, "DELAYED", "ON TIME")
    result["Delay_Probability"] = probabilities
    result["Delay_Risk_Percentage"] = np.round(probabilities * 100, 2)
    result["Risk_Category"] = [risk_category(p) for p in probabilities]
    return result


def out_of_training_range(data: pd.DataFrame) -> pd.Series:
    distance = pd.to_numeric(data["Distance_km"], errors="coerce")
    weight = pd.to_numeric(data["Package_weight_kg"], errors="coerce")
    return (
        (distance < TRAINING_RANGES["Distance_km"][0]) |
        (distance > TRAINING_RANGES["Distance_km"][1]) |
        (weight < TRAINING_RANGES["Package_weight_kg"][0]) |
        (weight > TRAINING_RANGES["Package_weight_kg"][1])
    )


# Defaults are illustrative operational assumptions, NOT learned training statistics.
# Missing fields cannot be inferred reliably from unrelated columns.
BULK_DEFAULTS = {
    "Delivery_Partner": "Delhivery",
    "Package_Type": "Electronics",
    "Vehicle_Type": "Van",
    "Delivery_Mode": "Standard",
    "Region": "North",
    "Weather_Condition": "Clear",
    "Distance_km": 50.0,
    "Package_weight_kg": 5.0,
}

# Common header spellings. Ambiguous headers are intentionally not guessed.
COLUMN_ALIASES = {
    "Delivery_Partner": ["delivery partner", "courier", "courier partner", "shipping partner", "logistics partner", "carrier"],
    "Package_Type": ["package type", "product type", "parcel type", "item category", "package category"],
    "Vehicle_Type": ["vehicle type", "transport type", "vehicle"],
    "Delivery_Mode": ["delivery mode", "shipping mode", "shipping method", "delivery service", "service type"],
    "Region": ["region", "delivery region", "shipping region", "zone"],
    "Weather_Condition": ["weather condition", "weather", "weather type"],
    "Distance_km": ["distance km", "distance (km)", "delivery distance km", "distance kilometers"],
    "Package_weight_kg": ["package weight kg", "package weight (kg)", "weight kg", "weight (kg)", "parcel weight kg"],
}


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).lower().strip())


def normalize_category(value, options: list[str]):
    if pd.isna(value) or not str(value).strip():
        return None
    key = normalize_header(value)
    match = {normalize_header(opt): opt for opt in options}
    # Standardize known labels but preserve genuinely unseen categories.
    # The fitted OneHotEncoder(handle_unknown="ignore") can accept these.
    return match.get(key, str(value).strip())


def prepare_bulk_data(raw: pd.DataFrame, defaults: dict) -> tuple[pd.DataFrame | None, pd.DataFrame | None, dict, list[str]]:
    """Create model-ready data without deleting original columns or inventing observations.

    Each row gets an audit flag. Missing values use user-visible defaults;
    unfamiliar but nonempty categorical values are preserved and flagged.
    At least one model feature must be identifiable in the upload.
    """
    issues = []
    if raw.empty:
        return None, None, {}, ["The uploaded file has no data rows."]
    if len(raw.columns) != len(set(map(str, raw.columns))):
        return None, None, {}, ["The file contains duplicate column names. Rename them before uploading."]

    normalized_columns = {}
    for col in raw.columns:
        normalized_columns.setdefault(normalize_header(col), []).append(col)

    matched = {}
    for feature in FEATURES:
        candidates = [feature] + COLUMN_ALIASES.get(feature, [])
        found = []
        for name in candidates:
            found.extend(normalized_columns.get(normalize_header(name), []))
        found = list(dict.fromkeys(found))
        if len(found) > 1:
            issues.append(f"Multiple columns appear to represent {feature}: {', '.join(map(str, found))}. Keep only one.")
        elif found:
            matched[feature] = found[0]
    if issues:
        return None, None, {}, issues
    if not matched:
        return None, None, {}, ["No recognizable model features found. Include at least one of the eight listed features (or a supported alias)."]

    model_data = pd.DataFrame(index=raw.index)
    flags = pd.DataFrame(index=raw.index)
    stats = {}
    for feature in FEATURES:
        if feature not in matched:
            model_data[feature] = defaults[feature]
            flags[feature] = "missing column → default"
            stats[feature] = len(raw)
            continue
        values = raw[matched[feature]]
        if feature in CATEGORIES:
            converted = values.map(lambda v: normalize_category(v, CATEGORIES[feature]))
            invalid = converted.isna()
            model_data[feature] = converted.fillna(defaults[feature])
            unseen = (~invalid) & (~converted.isin(CATEGORIES[feature]))
            flags[f"Unseen_{feature}"] = unseen.astype(bool)
        else:
            # Accept ordinary numbers and numeric text such as '12.5 km' or '5 kg'.
            cleaned_text = values.astype('string').str.strip().str.replace(',', '', regex=False)
            cleaned_text = cleaned_text.str.replace(r"(?i)\s*(km|kilometers?|kgs?|kilograms?)\s*$", "", regex=True)
            converted = pd.to_numeric(cleaned_text, errors="coerce")
            invalid = converted.isna() | ~np.isfinite(converted.fillna(-1).astype(float)) | (converted <= 0)
            model_data[feature] = converted.mask(invalid, defaults[feature]).astype(float)
        flags[feature] = np.where(invalid, "missing/invalid → default", "provided")
        stats[feature] = int(invalid.sum())

    # Only the eight feature audit columns count toward defaulted features.
    fallback_counts = (flags[FEATURES] != "provided").sum(axis=1)
    audit = pd.DataFrame({
        "Input_Features_Defaulted": fallback_counts.astype(int),
        "Input_Data_Quality": np.select(
            [fallback_counts.eq(0), fallback_counts.le(2)],
            ["Complete", "Partially defaulted"],
            default="Heavily defaulted",
        ),
    }, index=raw.index)
    audit["Defaulted_Features"] = flags[FEATURES].apply(
        lambda row: ", ".join(row.index[row != "provided"]), axis=1
    )
    unseen_cols = [f"Unseen_{f}" for f in CATEGORIES]
    for col in unseen_cols:
        if col not in flags:
            flags[col] = False
    audit["Unseen_Category_Count"] = flags[unseen_cols].sum(axis=1).astype(int)
    audit["Unseen_Categories"] = flags[unseen_cols].apply(
        lambda row: ", ".join(col.removeprefix("Unseen_") for col in row.index[row]), axis=1
    )
    unseen_values = {
        f: sorted(model_data.loc[flags[f"Unseen_{f}"], f].astype(str).unique().tolist())
        for f in CATEGORIES if flags[f"Unseen_{f}"].any()
    }
    details = {"matched": matched, "missing": [f for f in FEATURES if f not in matched],
               "defaults_used": stats, "unseen_values": unseen_values}
    return model_data[FEATURES], audit, details, []


def read_delivery_file(uploaded) -> pd.DataFrame:
    if uploaded.name.lower().endswith(".csv"):
        try:
            return pd.read_csv(uploaded, encoding="utf-8-sig")
        except UnicodeDecodeError:
            uploaded.seek(0)
            return pd.read_csv(uploaded, encoding="cp1252")
    return pd.read_excel(uploaded, engine="openpyxl")


def get_recommendation(risk: str, weather: str = "Clear") -> str:
    """Rule-based guidance, not a model-generated recommendation."""
    advice = {
        "Low Risk": {
            "Clear": "Maintain the planned delivery schedule and continue routine shipment monitoring.",
            "Rainy": "Proceed with normal monitoring; check road conditions and take rain precautions.",
            "Stormy": "Check official weather alerts before dispatch and prioritize driver safety.",
            "Foggy": "Monitor visibility and allow drivers to maintain safe speeds.",
            "Hot": "Maintain the schedule while ensuring hydration and heat-safety precautions.",
            "Cold": "Continue the plan while checking for temperature-related road disruptions.",
        },
        "Medium Risk": {
            "Clear": "Review route efficiency, monitor progress, and investigate potential operational bottlenecks.",
            "Rainy": "Review alternate routes, monitor road conditions, and alert customers to possible delays.",
            "Stormy": "Check weather warnings and dispatch feasibility; reschedule if conditions are unsafe.",
            "Foggy": "Allow additional travel time, review visibility, and monitor shipment progress.",
            "Hot": "Review delivery schedules and ensure suitable rest breaks for drivers.",
            "Cold": "Monitor road access and allow additional travel time where needed.",
        },
        "High Risk": {
            "Clear": "Investigate partner capacity and route bottlenecks; prioritize this shipment for closer monitoring.",
            "Rainy": "Prioritize safer routes, monitor disruptions, and proactively communicate likely delays.",
            "Stormy": "Prioritize driver safety, check official alerts, postpone unsafe dispatches, and update customers.",
            "Foggy": "Assess visibility and route safety; avoid unsafe dispatch and revise delivery estimates.",
            "Hot": "Review dispatch timing, protect drivers from heat exposure, and investigate delay drivers.",
            "Cold": "Check road conditions, assess delivery capacity, and communicate revised expectations.",
        },
    }
    return advice.get(risk, {}).get(weather, advice["Medium Risk"]["Clear"])


def render_risk_scale(probability: float):
    """Responsive, theme-aware HTML indicator; works with Streamlit 1.65."""
    pct = max(0.0, min(float(probability) * 100, 100.0))
    risk = risk_category(probability)
    color = risk_color(risk)
    # Constrain the badge, but not the pointer, at extreme percentages.
    badge_pos = max(8, min(pct, 92))
    html = f"""<div class="risk-panel">
<style>
.risk-panel {{background:var(--secondary-background-color, #f1f5f9);color:var(--text-color,#102a43);
 border:1px solid color-mix(in srgb,var(--text-color,#102a43) 18%,transparent);
 border-radius:16px;padding:25px 24px;margin:10px 0 22px;box-sizing:border-box;}}
.risk-title {{font-size:1rem;font-weight:700;margin-bottom:18px;}}
.risk-pointer-area {{position:relative;height:62px;}}
.risk-badge {{position:absolute;left:{badge_pos:.2f}%;transform:translateX(-50%);
 top:0;background:{color};color:white;padding:6px 10px;border-radius:8px;
 font-weight:800;font-size:.88rem;white-space:nowrap;}}
.risk-pointer {{position:absolute;left:{pct:.2f}%;transform:translateX(-50%);bottom:0;
 width:0;height:0;border-left:8px solid transparent;border-right:8px solid transparent;
 border-top:12px solid {color};}}
.risk-track {{display:flex;height:23px;width:100%;border-radius:9px;overflow:hidden;}}
.risk-ticks {{position:relative;height:28px;margin-top:8px;font-size:.75rem;opacity:.85;}}
.risk-ticks span {{position:absolute;white-space:nowrap;}}
.risk-labels {{display:flex;text-align:center;font-weight:750;font-size:.72rem;margin-top:8px;}}
.risk-labels span {{display:block;white-space:normal;}}
@media(max-width:500px) {{.risk-panel {{padding:17px 13px;}} .risk-labels {{font-size:.62rem;}}
 .risk-badge {{font-size:.76rem;padding:5px 7px;}}}}
</style>
<div class="risk-title">Estimated Delivery Delay Risk</div>
<div class="risk-pointer-area"><span class="risk-badge">{pct:.2f}%</span><span class="risk-pointer"></span></div>
<div class="risk-track"><div style="width:40%;background:#16a34a"></div><div style="width:30%;background:#f59e0b"></div><div style="width:30%;background:#dc2626"></div></div>
<div class="risk-ticks"><span style="left:0">0%</span><span style="left:40%;transform:translateX(-50%)">40%</span><span style="left:70%;transform:translateX(-50%)">70%</span><span style="right:0">100%</span></div>
<div class="risk-labels"><span style="width:40%;color:#16a34a">LOW RISK</span><span style="width:30%;color:#d97706">MEDIUM RISK</span><span style="width:30%;color:#dc2626">HIGH RISK</span></div>
</div>"""
    st.html(html)


with st.sidebar:
    st.markdown("### 🚚 Supply Chain Intelligence")
    st.caption("Delivery Risk Decision Support")
    page = st.radio(
        "Navigate",
        ["Home", "Single Delivery Prediction", "Bulk Delivery Prediction", "Model Information"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("ML predictions • Weather-aware guidance • Portfolio demonstration")

if page == "Home":
    st.markdown("""<div class="app-hero"><div class="eyebrow">AI-POWERED LOGISTICS ANALYTICS</div>
    <h1>Supply Chain Risk Intelligence</h1>
    <p>Estimate delivery delays, evaluate shipment risk, and turn predictions into actionable operational guidance.</p>
    </div>""", unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="info-card"><h3>🔍 Single Prediction</h3><p>Assess one shipment with its route, package, delivery, and weather details.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="info-card"><h3>📂 Bulk Prediction</h3><p>Upload CSV or Excel to assess many deliveries and download the scored results.</p></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="info-card"><h3>🧠 Model Transparency</h3><p>Understand model inputs, risk thresholds, and important limitations.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">How it works</div>', unsafe_allow_html=True)
    st.markdown("**1.** Enter shipment details or upload CSV/Excel.  \n**2.** The trained classifier estimates delay likelihood.  \n**3.** Review risk categories and operational guidance.")
    st.info("This is a decision-support demonstration, not a live courier tracking system.")

elif page == "Single Delivery Prediction":
    st.title("🚚 Single Delivery Risk Prediction")
    st.caption("Enter shipment information to estimate delivery delay probability using the trained ML model.")
    st.markdown('<div class="section-heading">Shipment Details</div>', unsafe_allow_html=True)
    with st.form("single_prediction_form"):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            delivery_partner = st.selectbox("Delivery Partner", CATEGORIES["Delivery_Partner"])
            package_type = st.selectbox("Package Type", CATEGORIES["Package_Type"])
            vehicle_type = st.selectbox("Vehicle Type", CATEGORIES["Vehicle_Type"])
            delivery_mode = st.selectbox("Delivery Mode", CATEGORIES["Delivery_Mode"])
        with col2:
            region = st.selectbox("Region", CATEGORIES["Region"])
            weather_condition = st.selectbox("Weather Condition", CATEGORIES["Weather_Condition"])
            distance = st.number_input("Distance (km)", min_value=0.01, value=50.0, step=1.0, format="%.2f")
            package_weight = st.number_input("Package Weight (kg)", min_value=0.01, value=5.0, step=0.5, format="%.2f")
        submitted = st.form_submit_button("🔍 Analyze Delivery Risk", type="primary", use_container_width=True)

    if submitted:
        input_data = pd.DataFrame([[
            delivery_partner, package_type, vehicle_type, delivery_mode,
            region, weather_condition, distance, package_weight,
        ]], columns=FEATURES)
        if out_of_training_range(input_data).any():
            st.warning("Some inputs are outside the ranges observed during training. Predictions may be less reliable.")
        try:
            result = predict_deliveries(input_data)
            prediction = int(result["Predicted_Delay"].iloc[0])
            probability = float(result["Delay_Probability"].iloc[0])
            risk = result["Risk_Category"].iloc[0]
            status = "DELAYED" if prediction == 1 else "ON TIME"
            st.divider()
            st.markdown('<div class="section-heading">Prediction Results</div>', unsafe_allow_html=True)
            left, right = st.columns(2)
            with left:
                st.markdown(f'<div class="result-card {risk_css(risk)}"><p>Predicted Delivery Status</p><h2>{status}</h2><p class="muted">Machine Learning Classification</p></div>', unsafe_allow_html=True)
            with right:
                st.markdown(f'<div class="result-card {risk_css(risk)}"><p>Estimated Delay Probability</p><h2>{probability * 100:.2f}%</h2><p style="color:{risk_color(risk)};font-weight:750">{risk}</p></div>', unsafe_allow_html=True)
            st.subheader("Delivery Risk Indicator")
            render_risk_scale(probability)
            st.subheader("Risk Assessment")
            if risk == "Low Risk":
                st.success("🟢 Low Risk — Lower estimated likelihood of delay.")
            elif risk == "Medium Risk":
                st.warning("🟠 Medium Risk — Moderate estimated likelihood of delay.")
            else:
                st.error("🔴 High Risk — Elevated estimated likelihood of delay.")
            st.subheader("Operational Recommendation")
            st.info(get_recommendation(risk, weather_condition))
            st.caption("Recommendations are rule-based and consider the selected weather condition and model-derived risk category. Predictions are estimates, not guarantees; risk thresholds are application-defined.")
        except Exception as exc:
            st.error("Unable to generate the delivery prediction. Check the model file and dependencies.")
            st.exception(exc)

elif page == "Bulk Delivery Prediction":
    st.title("📂 Bulk Delivery Risk Prediction")
    st.caption("Upload your own CSV or Excel file. Extra columns are preserved, common column names are recognized, and missing or messy values can be handled transparently.")

    st.markdown('<div class="section-heading">Model features (recommended)</div>', unsafe_allow_html=True)
    st.write("For the most meaningful predictions, provide all **eight** features below. Missing features can be filled with clearly disclosed defaults, but those predictions may be much less reliable.")
    requirements = pd.DataFrame({
        "Model feature": FEATURES,
        "Type": ["Category"] * 6 + ["Positive number", "Positive number"],
        "Fallback if missing or invalid": [str(BULK_DEFAULTS[f]) for f in FEATURES],
    })
    st.dataframe(requirements, hide_index=True, use_container_width=True)
    with st.expander("See accepted category values and example column names"):
        for feature, options in CATEGORIES.items():
            st.write(f"**{feature}:** {', '.join(options)}")
        st.write("Column names are matched ignoring capitalization, spaces, and punctuation. Examples: `delivery partner`, `weather`, `distance (km)`, `weight kg`.")
        st.write("Unseen categorical values (e.g., DTDC or Porter) are preserved and flagged; the trained encoder ignores unseen categories. Missing categories, invalid/nonpositive numbers, and absent columns use the displayed defaults. No missing field is inferred from the file.")

    with st.expander("Optional: change fallback values before analyzing"):
        selected_defaults = {}
        a, b = st.columns(2)
        for idx, feature in enumerate(FEATURES):
            with (a if idx % 2 == 0 else b):
                if feature in CATEGORIES:
                    selected_defaults[feature] = st.selectbox(
                        f"Default {feature}", CATEGORIES[feature],
                        index=CATEGORIES[feature].index(BULK_DEFAULTS[feature]),
                        key=f"bulk_default_{feature}",
                    )
                else:
                    selected_defaults[feature] = st.number_input(
                        f"Default {feature}", min_value=0.01,
                        value=float(BULK_DEFAULTS[feature]), format="%.2f",
                        key=f"bulk_default_{feature}",
                    )

    st.caption("A template is optional — you can upload your own file directly.")
    template = pd.DataFrame([{
        "Delivery_Partner": "Delhivery", "Package_Type": "Electronics", "Vehicle_Type": "Van",
        "Delivery_Mode": "Standard", "Region": "North", "Weather_Condition": "Clear",
        "Distance_km": 50.0, "Package_weight_kg": 5.0,
    }], columns=FEATURES)
    st.download_button("⬇️ Optional sample CSV", template.to_csv(index=False).encode("utf-8"), "delivery_template.csv", "text/csv")

    uploaded = st.file_uploader("Upload delivery data (.csv or .xlsx)", type=["csv", "xlsx"])
    if uploaded is not None:
        try:
            raw = read_delivery_file(uploaded)
            st.caption(f"Uploaded {len(raw):,} rows and {len(raw.columns)} columns.")
            with st.expander("Preview original uploaded data", expanded=False):
                st.dataframe(raw.head(20), use_container_width=True, hide_index=True)
            prepared, audit, details, errors = prepare_bulk_data(raw, selected_defaults)
        except ImportError:
            st.error("Excel support requires `openpyxl`. Add `openpyxl` to app/requirements.txt and redeploy.")
            prepared, audit, details, errors = None, None, {}, ["Missing Excel dependency"]
        except Exception as exc:
            st.error(f"Could not read or prepare this file: {exc}")
            prepared, audit, details, errors = None, None, {}, ["File could not be processed"]

        if errors:
            for message in errors:
                st.warning(message)
        else:
            st.success(f"Recognized {len(details['matched'])} of 8 model features. Extra columns will be kept in the output.")
            with st.expander("See recognized columns and cleaning report", expanded=True):
                st.write("**Matched columns:** " + ", ".join(f"{feature} ← {source}" for feature, source in details["matched"].items()))
                if details["missing"]:
                    st.warning("**Absent features filled with defaults:** " + ", ".join(details["missing"]))
                st.dataframe(pd.DataFrame({
                    "Feature": FEATURES,
                    "Rows defaulted": [details["defaults_used"][f] for f in FEATURES],
                }), hide_index=True, use_container_width=True)
                st.write("**Rows requiring at least one default:**", int((audit["Input_Features_Defaulted"] > 0).sum()))
                st.write("**Rows with 3+ defaulted features:**", int((audit["Input_Features_Defaulted"] >= 3).sum()))
                if details["unseen_values"]:
                    st.warning("Unseen category values detected. They are preserved, not replaced with known partners or other categories. The model has not learned their specific effects, so predictions may be less reliable.")
                    for feature, values in details["unseen_values"].items():
                        shown = ", ".join(values[:12])
                        suffix = f" (and {len(values)-12} more)" if len(values) > 12 else ""
                        st.write(f"**{feature}:** {shown}{suffix}")
                st.write("**Rows containing unseen categories:**", int((audit["Unseen_Category_Count"] > 0).sum()))
                st.caption("Defaults are user-adjustable assumptions, not values recovered from your dataset or learned imputation statistics. Unseen labels are passed to the model as entered after trimming whitespace.")
            outside_count = int(out_of_training_range(prepared).sum())
            if outside_count:
                st.warning(f"{outside_count:,} row(s) have distance or weight outside observed training ranges.")
            if len(details["matched"]) < 4 or (audit["Input_Features_Defaulted"] >= 3).any():
                st.warning("Some predictions rely on many assumed values. Use them only as illustrative estimates, not reliable shipment decisions.")

            if st.button("🔍 Clean Inputs & Predict Deliveries", type="primary", use_container_width=True):
                try:
                    predicted = predict_deliveries(prepared)
                    # Keep original fields, cleaned model inputs, and data-quality audit together.
                    output = raw.reset_index(drop=True).copy()
                    for feature in FEATURES:
                        output[f"Model_Input_{feature}"] = prepared[feature].to_numpy()
                    for column in audit.columns:
                        output[column] = audit[column].to_numpy()
                    for column in ["Predicted_Delay", "Delay_Status", "Delay_Probability", "Delay_Risk_Percentage", "Risk_Category"]:
                        output[column] = predicted[column].to_numpy()
                    output["Operational_Recommendation"] = [
                        get_recommendation(r, w)
                        for r, w in zip(predicted["Risk_Category"], prepared["Weather_Condition"])
                    ]
                    st.session_state["bulk_results_v2"] = output
                    st.session_state["bulk_signature_v2"] = (
                        uploaded.name, uploaded.getvalue(), tuple((k, str(v)) for k, v in selected_defaults.items())
                    )
                except Exception as exc:
                    st.error("Prediction failed; please review the uploaded data and model dependencies.")
                    st.exception(exc)

            signature = (uploaded.name, uploaded.getvalue(), tuple((k, str(v)) for k, v in selected_defaults.items()))
            if st.session_state.get("bulk_signature_v2") == signature:
                results = st.session_state["bulk_results_v2"]
                st.divider()
                a, b, c = st.columns(3)
                a.metric("Total Deliveries", f"{len(results):,}")
                b.metric("Predicted Delays", f"{int((results['Predicted_Delay'] == 1).sum()):,}")
                c.metric("Average Delay Probability", f"{results['Delay_Probability'].mean() * 100:.1f}%")
                st.markdown('<div class="section-heading">Risk Category Breakdown</div>', unsafe_allow_html=True)
                counts = results["Risk_Category"].value_counts().reindex(["Low Risk", "Medium Risk", "High Risk"], fill_value=0)
                st.bar_chart(counts.rename("Shipments"))
                st.dataframe(results, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download Results with Original & Cleaned Columns", results.to_csv(index=False).encode("utf-8-sig"), "delivery_predictions_with_audit.csv", "text/csv", use_container_width=True)
                st.caption("Original columns are preserved. `Model_Input_` fields show exactly what the classifier received. Defaults and row-level quality flags are included for transparency.")

elif page == "Model Information":
    st.title("🧠 Model Information")
    st.markdown('<div class="section-heading">Prediction Approach</div>', unsafe_allow_html=True)
    st.write("The application loads a previously trained scikit-learn classification pipeline and predicts whether a delivery is delayed (class 1) or on time (class 0). The pipeline includes preprocessing and a Random Forest classifier. Bulk uploads may contain extra fields and missing model features; missing or invalid values use disclosed user-adjustable defaults. Unseen categorical values are retained and passed to the pipeline's OneHotEncoder(handle_unknown='ignore'), so the model can produce predictions but cannot learn unseen-partner-specific behavior.")
    st.markdown('<div class="section-heading">Model Inputs</div>', unsafe_allow_html=True)
    input_details = pd.DataFrame({
        "Feature": FEATURES,
        "Type": ["Categorical"] * 6 + ["Numeric", "Numeric"],
    })
    st.dataframe(input_details, hide_index=True, use_container_width=True)
    st.markdown('<div class="section-heading">Risk Thresholds</div>', unsafe_allow_html=True)
    st.write("🟢 **Low:** below 40%  \n🟠 **Medium:** 40% to below 70%  \n🔴 **High:** 70% and above")
    st.markdown('<div class="section-heading">Limitations</div>', unsafe_allow_html=True)
    st.warning("Model probabilities are estimates and may not be calibrated. Missing features use assumed values; unseen categorical values are ignored by the trained encoder rather than learned. Both can reduce reliability. Inputs outside training ranges, changing real-world conditions, and unrepresented factors can also reduce reliability. Recommendations are rule-based, not generated by the ML model. This app does not track live weather or actual shipments.")
    st.caption("Model performance metrics should be reported only from your actual notebook evaluation results.")

st.divider()
st.caption("Supply Chain Risk Intelligence • Portfolio demonstration • Predictions support, but do not replace, operational judgment")
