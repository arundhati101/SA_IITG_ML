# SA_IITG_ML

Perfect, Arundhati! Here's a complete and polished **project report** outline with content for submission, based on your work so far with **Model 1** and **Model 2**.

---

# 📘 **Dynamic Pricing Engine for Urban Parking Lots**

### Summer Analytics 2025 Capstone Project

**By Arundhati Chaudhuri**

---

## 📌 1. Introduction

Urban parking is a scarce resource. Static pricing fails to adjust to fluctuations in demand throughout the day, leading to over- or under-utilization. To address this, we develop a **real-time dynamic pricing engine** for 14 urban parking lots using **Pandas, NumPy, Pathway (simulated), and Bokeh**, without external ML libraries.

---

## 📊 2. Dataset Overview

* **Rows:** 18,368 data points sampled every 30 minutes from 8 AM to 4:30 PM over 73 days.
* **Columns:**

  * Lot Features: `SystemCodeNumber`, `Capacity`, `Occupancy`, `QueueLength`
  * Environment: `TrafficConditionNearby`, `IsSpecialDay`
  * Vehicle Info: `VehicleType`
  * Time: `LastUpdatedDate`, `LastUpdatedTime`, combined to form `Timestamp`
  * Location: `Latitude`, `Longitude` (used in Model 3)

---

## ⚙️ 3. Data Preprocessing

* Merged `LastUpdatedDate` and `LastUpdatedTime` to form a datetime column `Timestamp`
* Encoded categorical features:

  * `VehicleType`: car → 1.0, bike → 0.5, truck → 1.5
  * `TrafficConditionNearby`: low → 1, medium → 2, high → 3
* Sorted data chronologically for each parking lot to simulate real-time flow

---

## 📈 4. Model 1: Baseline Linear Pricing

### 🔹 Formula:

$$
\text{Price}_{t+1} = \text{Price}_t + \alpha \cdot \left(\frac{\text{Occupancy}}{\text{Capacity}} - 0.5\right)
$$

* **Base Price:** \$10
* **α (sensitivity):** 2
* **Bounds:** \[\$5, \$20]

> The idea is that price increases when occupancy exceeds 50% and decreases when below 50%.

### 🔍 Justification:

* Provides a simple, reactive pricing based only on occupancy ratio
* Serves as a baseline to compare more intelligent models

### 📊 Visualization:

*Model 1 price variation for Lot BHMBCCMKT01*
(Include your Bokeh plot here in the notebook/report)

---

## 📉 5. Model 2: Demand-Based Pricing

### 🔹 Demand Function:

$$
\text{Demand} = \alpha \cdot \left(\frac{\text{Occupancy}}{\text{Capacity}}\right) + \beta \cdot \text{QueueLength} - \gamma \cdot \text{TrafficLevel} + \delta \cdot \text{IsSpecialDay} + \varepsilon \cdot \text{VehicleWeight}
$$

### 🔹 Parameters:

| Variable | Meaning               | Value |
| -------- | --------------------- | ----- |
| α        | occupancy sensitivity | 1.5   |
| β        | queue length impact   | 0.8   |
| γ        | traffic penalty       | 1.2   |
| δ        | special day bonus     | 2.0   |
| ε        | vehicle weight        | 1.0   |

Then normalize:

$$
\text{Price} = \text{BasePrice} \cdot (1 + \lambda \cdot \text{NormalizedDemand})
$$

* **λ:** 0.7
* **Bounds:** \[\$5, \$20]

### 🔍 Justification:

* Captures real-world dependencies beyond just occupancy
* Incorporates congestion and demand surges
* More sensitive to special days and vehicle types

### 📊 Visualization:

*Model 2 price variation for Lot BHMBCCMKT01*
(Include your Bokeh plot here in the notebook/report)

---

## 📊 6. Model Comparison (Model 1 vs Model 2)

* **Model 1** shows smoother, linear progression but lacks responsiveness.
* **Model 2** captures day-to-day volatility and adjusts more dynamically.

### 📊 Combined Bokeh Chart:

(Overlay plot of both models using Bokeh, included earlier)

---

## 🤖 7. Assumptions

* Base price is fixed at **\$10**
* Prices must remain within **\$5 to \$20**
* `TrafficLevel` and `VehicleWeight` mapping is fixed for this simulation
* No dynamic rerouting logic (Model 3) yet — added in future scope
* Timestamp sampling is assumed clean and regular every 30 minutes

---

## 📦 8. Tools Used

* **Pandas, NumPy**: Data manipulation and model implementation
* **Bokeh**: Real-time visualization
* **Google Colab**: Development and output sharing

---

## 📝 10. Conclusion

We successfully built and visualized two dynamic pricing models:

* **Model 1**: Simple and interpretable
* **Model 2**: Richer and more responsive

These models simulate a realistic pricing system that adapts to occupancy, congestion, and demand — with clear visualization to guide decision-makers.
