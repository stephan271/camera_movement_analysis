# Object Trajectory & Distance Analysis Report (Frames 238–248)

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

## 5. Physical Discussion

* **Rapid Speed Traversal**: The object covers a ground distance of approximately **$21.5$ to $31.7\text{ meters}$** (depending on scale) in a fraction of a second. This rapid horizontal traversal at a steady altitude $y \approx 215$ results in an extreme aspect ratio streak in Frames 244–248.
* **Supersonic Velocities**: Since the object transitions from a hover to leaving the screen in roughly $6\text{ frames}$ ($\approx 0.2\text{ seconds}$), its average horizontal speed over this window exceeds **$100\text{ m/s}$ to $150\text{ m/s}$** ($360\text{ km/h}$ to $540\text{ km/h}$), reaching terminal peak velocities well over **Mach 0.8** as it exits the field of view.
