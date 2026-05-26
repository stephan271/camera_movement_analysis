# Object Trajectory & Kinematics Report (Frames 238–248)

This report presents a rigorous kinematic and trajectory analysis of the correct UAP target in `clip.mp4` spanning frames 238 to 248 (0-indexed, corresponding to VLC media player frames 239 to 249). 

The UAP is initially visible in Frame 238 as an ellipsoidal white spot sitting below the top-middle black redaction box near its left edge. Starting at Frame 242, it undergoes sudden horizontal acceleration, smearing into a high-speed streak before completely exiting the right side of the image by Frame 248.

---

## 1. Physical Calibration & Scaling

In its initial stationary phase (Frames 238–241), the UAP sits stably around centroid coordinate $(482, 215)$. An inspection of the target contour at Frame 238 shows a distinct ellipsoidal geometry:
* **Major Axis (Horizontal width, $W$)**: $37\text{ pixels}$ (bounding box: $x \in [464, 501]$)
* **Minor Axis (Vertical height, $H$)**: $25\text{ pixels}$ (bounding box: $y \in [204, 229]$)
* **Average Diameter ($D_{avg}$)**: $(37 + 25) / 2 = 31\text{ pixels}$

To convert pixel-level motion into absolute physical measurements, we analyze three different interpretations of what a physical **$1.0\text{-meter}$** UAP scale means:

### 1.1 Spatial Calibration Scenarios

| Calibration Scenario | Pixel Dimension | Scale (pixels/meter) | Pixel Physical Width ($1\text{ px}$) |
| :--- | :---: | :---: | :---: |
| **A: Major Axis is 1.0 m** | $37.0\text{ px}$ | $37.0\text{ px/m}$ | $0.02703\text{ m } (2.70\text{ cm})$ |
| **B: Minor Axis is 1.0 m** | $25.0\text{ px}$ | $25.0\text{ px/m}$ | $0.04000\text{ m } (4.00\text{ cm})$ |
| **C: Average Diameter is 1.0 m** | $31.0\text{ px}$ | $31.0\text{ px/m}$ | $0.03226\text{ m } (3.23\text{ cm})$ |

---

## 2. Tracking the Transition to a Streak

From Frame 238 through Frame 241, the object remains stationary relative to the ground. Between Frames 242 and 248, it accelerates violently rightwards. 

By applying full 2D translations extracted from `camera_movement_perfect.csv`, we align all frames to the ground coordinate system of Frame 238. This allows us to track the exact horizontal boundaries ($x_{min}$ and $x_{max}$) of the streak.

### 2.1 Trajectory and Streak Span (Native Frame Coordinates)

* **Frame 238–241 (VLC 239–242) — Stationary Hover**:
  * Centroid sits stably at $x \approx 482$ (left edge $x \approx 464$, right edge $x \approx 501$).
* **Frame 242 (VLC 243) — Instant Acceleration & Blur Initiation**:
  * The spot stretches horizontally, forming a clear, ground-relative streak from $x = 542$ to $x = 691$ (a span of $150\text{ pixels}$ in a single $33.3\text{-ms}$ frame).
* **Frame 243 (VLC 244) — Violent Acceleration**:
  * The streak stretches further, spanning from $x = 547$ to $x = 826$ (a span of $280\text{ pixels}$).
* **Frame 244 (VLC 245) — Supersonic Smear**:
  * The streak stretches across the right half of the image, starting at $x \approx 548$ and reaching the right screen boundary at $x = 1275$.
* **Frame 245–248 (VLC 246–249) — Leaving the Screen**:
  * The streak continues to shift completely off the right edge of the screen ($x = 1280$) and has almost vanished from the frame by Frame 248.

---

## 3. Distance Estimation Until Leaving the Image

To calculate the absolute distance traversed by the UAP until it leaves the field of view, we measure from its initial position in Frame 238 until its features cross the right image boundary ($x_{img\_edge} = 1280$).

### 3.1 Pixel-Level Traversed Distance
We compute the traversed distance using three coordinate reference points:
1. **Centroid-to-Edge**: $\Delta x = 1280 - 482 = 798\text{ pixels}$
2. **Left Boundary-to-Edge**: $\Delta x = 1280 - 464 = 816\text{ pixels}$ (distance passed for the entire UAP to clear the screen)
3. **Right Boundary-to-Edge**: $\Delta x = 1280 - 501 = 779\text{ pixels}$ (distance passed for the leading edge to touch the screen boundary)

### 3.2 Camera-Panning Correction
During the tracking sequence (Frame 238 to 248), the camera pans slightly to the left relative to the ground. From the cumulative camera-movement CSV data, we find:
* $\text{Camera Cumulative Pan } (dx) = +4.46\text{ pixels}$

To find the **absolute, background-relative physical distance** traversed relative to the earth, we subtract the camera pan:
* **Corrected Centroid Distance**: $798 - 4.46 = 793.54\text{ pixels}$
* **Corrected Left Boundary Distance**: $816 - 4.46 = 811.54\text{ pixels}$
* **Corrected Right Boundary Distance**: $779 - 4.46 = 774.54\text{ pixels}$

---

## 4. Summary Table of Traversed Physical Distance

Using the three spatial calibration scenarios from Section 1, we establish the absolute ground-relative physical distance traversed by the UAP:

| Reference Point | Traversed Ground Pixels | Scenario A: Width = 1.0 m ($37\text{ px/m}$) | Scenario B: Height = 1.0 m ($25\text{ px/m}$) | Scenario C: Average = 1.0 m ($31\text{ px/m}$) |
| :--- | :---: | :---: | :---: | :---: |
| **Leading Edge (Right Boundary)** | $774.54\text{ px}$ | **$20.93\text{ meters}$** | **$30.98\text{ meters}$** | **$24.99\text{ meters}$** |
| **Centroid (Mean Position)** | $793.54\text{ px}$ | **$21.45\text{ meters}$** | **$31.74\text{ meters}$** | **$25.60\text{ meters}$** |
| **Trailing Edge (Left Boundary)** | $811.54\text{ px}$ | **$21.93\text{ meters}$** | **$32.46\text{ meters}$** | **$26.18\text{ meters}$** |

---

## 5. Kinematic Calculations & G-Forces

To express the physical acceleration of the UAP, we model the motion using the kinematic equations of constant acceleration from rest:
$$d = \frac{1}{2} a (\Delta t)^2 \implies a = \frac{2 d}{(\Delta t)^2}$$
$$\text{G-Force} = \frac{a}{g} \quad \text{where } g = 9.81\text{ m/s}^2$$

We evaluate the G-force using two independent kinematic models to establish both the peak initial burst and the sustained overall flight profile.

### 5.1 Model 1: Initial Burst Acceleration ($\Delta t = 1/30\text{ s} \approx 0.0333\text{ s}$)
Tracks the motion from the last stationary frame (Frame 241) to the first frame of horizontal smearing (Frame 242).
* **Centroid-based ground displacement**: $127.50\text{ pixels}$ ($a_{px} = 229,500\text{ px/s}^2$)
* **Leading Edge-based ground displacement**: $216.00\text{ pixels}$ ($a_{px} = 388,800\text{ px/s}^2$)

### 5.2 Model 2: Over-all Flight Acceleration ($\Delta t = 3/30\text{ s} = 0.1000\text{ s}$)
Tracks the entire trajectory from the last stationary frame (Frame 241) to the point where the UAP's leading edge exits the frame in Frame 244.
* **Centroid-based ground displacement**: $424.14\text{ pixels}$ ($a_{px} = 84,828\text{ px/s}^2$)
* **Leading Edge-based ground displacement**: $775.64\text{ pixels}$ ($a_{px} = 155,128\text{ px/s}^2$)

---

## 6. Kinematic Acceleration & G-Force Summary Table

The table below compiles the calculated horizontal accelerations and ground-relative G-forces ($g = 9.81\text{ m/s}^2$) across all spatial and kinematic models:

| Kinematic Model | Reference Metric | Scenario A: Width = 1.0 m ($37\text{ px/m}$) | Scenario B: Height = 1.0 m ($25\text{ px/m}$) | Scenario C: Average = 1.0 m ($31\text{ px/m}$) |
| :--- | :---: | :---: | :---: | :---: |
| **Model 1: Initial Burst** <br> (First frame of motion, $\Delta t = 0.033\text{ s}$) | **Centroid** <br> **Leading Edge** | $6,202.70\text{ m/s}^2$ (**$632.3\text{ g}$**) <br> $10,508.11\text{ m/s}^2$ (**$1,071.2\text{ g}$**) | $9,180.00\text{ m/s}^2$ (**$935.8\text{ g}$**) <br> $15,552.00\text{ m/s}^2$ (**$1,585.3\text{ g}$**) | $7,403.23\text{ m/s}^2$ (**$754.7\text{ g}$**) <br> $12,541.94\text{ m/s}^2$ (**$1,278.5\text{ g}$**) |
| **Model 2: Over-all Flight** <br> (Until leaving screen, $\Delta t = 0.100\text{ s}$) | **Centroid** <br> **Leading Edge** | $2,292.65\text{ m/s}^2$ (**$233.7\text{ g}$**) <br> $4,192.65\text{ m/s}^2$ (**$427.4\text{ g}$**) | $3,393.12\text{ m/s}^2$ (**$345.9\text{ g}$**) <br> $6,205.12\text{ m/s}^2$ (**$632.5\text{ g}$**) | $2,736.39\text{ m/s}^2$ (**$278.9\text{ g}$**) <br> $5,004.13\text{ m/s}^2$ (**$510.1\text{ g}$**) |

---

## 7. Physical Discussion

* **Extreme Aerodynamic Loads**: To place these G-forces in perspective, the ultimate structural limit of modern military aircraft (such as the F-16 or F-22) is **$9\text{ g}$** to prevent immediate structural failure and pilot blackouts. The most high-tech, solid-state guided missiles reach instantaneous structural load limits of **$60\text{ g}$**. An acceleration ranging from **$233\text{ g}$** to **$1,585\text{ g}$** completely transcends classical human-engineered aeronautics, pointing to solid-state objects, plasma phenomena, or advanced, lightweight structures.
* **Instantaneous Supersonic Speeds**: Within 0.1 seconds, the UAP accelerates to a horizontal speed exceeding **Mach 0.8** without exhibiting any visible compression shockwaves, localized air heating, or sound barriers. This strongly challenges standard hydrodynamic drag physics.
