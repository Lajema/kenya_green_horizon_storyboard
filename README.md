# 🌍 Kenya Green Horizon: Climate & Energy Dashboard

An interactive, multi-page Streamlit analytical dashboard mapping multi-decade structural environmental markers, power grid dynamics, and climate lifelines for Kenya using World Bank Open Data.

## 🎨 Visual Philosophy: "Old School Technical"
This application pivots away from modern minimalist styling in favor of an **engineering-focused, textbook-style aesthetic**:
* **High-Contrast Grid Lines:** Clean, sharp canvas intersections to maintain structural data tracking clarity.
* **Rigid Framing:** All visual assets are clearly framed with definite visual borders and zero rounded element weights.
* **Plain-English "Translator Notes":** Complex macroeconomic and environmental jargon is actively mapped into intuitive analogies, allowing users of all analytical backgrounds to grasp what the data means instantly.

---

## 📖 The Dashboard Storyline

The repository coordinates data patterns across a guided four-stage narrative:

### 1. 🌍 Environmental Vital Signs (Executive Summary)
* **The Story:** A quick macro check-up of Kenya’s natural assets. It measures baseline health parameters across three high-level cards: Forest Canopy Cover, Hydroelectric Generation Share, and Oil-Fired Energy Dependence.
* **The Translation:** Explains how drops in hydropower generation are directly linked to real-world climate pressures like drought cycles, which historically forced the energy sector to fire up expensive oil generators.

### 2. ⚡ The Power Grid Mix (Energy Deep Dive)
* **The Story:** A stacked resource review tracking the transition away from high-pollution fuels.
* **The Translation:** Breaks down the "recipe" of Kenya's electricity. It shows how green resource alternatives (such as massive geothermal projects) successfully step in to replace fossil fuels as the grey visual sectors shrink over the decades.

### 3. 🏭 Carbon Emissions & Forests (The Carbon Balance)
* **The Story:** A two-axis exploration tracking sector-specific pollution origins contrasted with natural land storage capabilities.
* **The Translation:** Explains that emissions don't just come from cars and manufacturing plants. In Kenya, a massive portion tracks directly back to livestock/farming footprint shifts and forest clearing. The adjacent tracking layout measures forest health as our primary shield against global warming.

### 4. 🔮 Future Green Horizons (5-Year Predictive Modeling)
* **The Story:** A machine learning forecasting workspace evaluating where Kenya's primary climate baselines are heading out through 2030.
* **The Translation:** Translates algorithmic vectors into real-world trends, revealing the future trajectory of forest cover and clean grid stability if policy dynamics and planting velocities maintain current momentum.

---

## 🛠️ Key Bug Fixes & Code Stability

### Preventing Axis Auto-Zoom Crashing
During development, narrow chronological filter ranges (e.g., viewing a single milestone year like 2011) caused Plotly to auto-zoom into micro-decimals. This triggered overlapping, unreadable labels on the Y-Axis and distorted single data points.

**The Fix:**
1.  **Explicit Vector Selection:** Transitioned from passing raw multidimensional array slices (`.values`) to targeted row selectors (`['Value']`) to normalize data parsing.
2.  **Forced Axis Boundaries:** Added standard hard-coded limits (`range=[0, 15]`) to freeze the data window within a logical environmental scope.
3.  **Strict Metric Formatting:** Enforced fixed decimal notation rules (`tickformat=".1f"`) to trim long decimal numbers into readable, clean single-decimal values (e.g., `6.3%`).

---

## 🚀 Technical Requirements & Execution

### 1. Data File Configuration
Ensure that the World Bank database target file `API_KEN_DS2_en_csv_v2_5938.csv` is saved directly inside your root project directory.

### 2. Running the Application
Install dependencies and launch the dashboard ecosystem:

```bash
pip install streamlit pandas numpy plotly scikit-learn
streamlit run green_app.py
