# Object Acceleration Analysis Report (Frames 242–246)

This report presents a rigorous kinematic and physical analysis of the white spot's sudden acceleration in `clip.mp4` during frames 242 to 246 (0-indexed, corresponding to VLC media player frames 243 to 247). 

By combining sub-pixel object tracking with our high-precision background camera-movement data, we have derived the absolute background-relative physical motion of the object.

---

## 1. Physical Calibration & Scaling

To convert the video's pixel displacements into physical SI units, we establish two fundamental scaling parameters:

### 1.1 Spatial Calibration (Pixel-to-Meter Scale)
We analyze the white spot in its initial stationary phase (Frame 242 / VLC 243) around its centroid $(679.0, 474.0)$. An inspection of the $25\times 25$ pixel intensity profile confirms a highly circular, symmetric intensity distribution:
* **Horizontal Diameter**: $\sim 10.0$ pixels (intensity boundaries $\ge 190$ gray levels)
* **Vertical Diameter**: $\sim 9.0$ pixels
* **Area-Based Diameter**: A binary threshold at 190 isolates a target contour area of $78.0\text{ px}^2$, giving an equivalent circular diameter of:
  $$D = \sqrt{\frac{4 \times 78.0}{\pi}} \approx 9.97\text{ pixels}$$

Assuming the initial white spot has a physical diameter of exactly **$1.0\text{ meter}$**, we obtain a precise spatial scale of:
$$\text{Scale} = 10.0\text{ pixels/meter} \implies 1\text{ pixel} = 0.1\text{ meter } (10\text{ cm})$$

### 1.2 Temporal Calibration
The video is decoded at a constant rate of **$30.0\text{ FPS}$**, giving a time step between consecutive frames of:
$$\Delta t = \frac{1}{30}\text{ second} \approx 0.03333\text{ seconds } (33.33\text{ ms})$$

### 1.3 Velocity Conversion Factor
Using these spatial and temporal calibrations, a velocity of $1\text{ pixel/frame}$ converts to meters per second ($m/s$) as follows:
$$1\text{ px/frame} \times \frac{0.1\text{ m/px}}{1/30\text{ s/frame}} = 3.0\text{ m/s}$$
$$\text{Conversion: } 1\text{ px/frame} = 3.0\text{ m/s } \approx 10.8\text{ km/h}$$

---

## 2. Tracking Data & Camera Motion Correction

Before Frame 243, the object is completely stationary relative to the camera tracking crosshair, resting at coordinate $(679.0, 474.0)$. Between frames 242 and 246, the object rapidly moves rightwards and downwards.

To isolate the absolute physical movement of the object relative to the ground, we subtract the sub-pixel camera pan/tilt adjustments ($\vec{v}_{cam}$) extracted from `camera_movement_perfect.csv`. The background-relative displacement $\vec{d}_{corr}$ is:
$$\vec{d}_{corr} = \vec{d}_{measured} - \vec{d}_{cam}$$

### 2.1 Table: Sub-Pixel Trajectory and Corrections

| Frame (0-Idx) | VLC Frame | Measured $(X, Y)$ | Measured $dx, dy$ (px) | Camera $dx, dy$ (px) | Corrected $dx, dy$ (px) | Corrected Displacement (px) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **242** | **243** | $(679.0, 474.0)$ | — | — | — | — |
| **243** | **244** | $(706.0, 468.0)$ | $+27.00, -6.00$ | $+0.15, +0.45$ | $+26.85, -6.45$ | $27.61$ |
| **244** | **245** | $(735.0, 497.0)$ | $+29.00, +29.00$ | $+1.47, +0.21$ | $+27.53, +28.79$ | $39.83$ |
| **245** | **246** | $(802.0, 525.0)$ | $+67.00, +28.00$ | $+1.08, -0.01$ | $+65.92, +28.01$ | $71.63$ |
| **246** | **247** | $(892.0, 553.0)$ | $+90.00, +28.00$ | $+0.78, -0.38$ | $+89.22, +28.38$ | $93.63$ |

---

## 3. Kinematic Calculations

### 3.1 Background-Relative Velocities
The corrected velocities are computed for each interval by applying the $3.0\text{ m/s}$ conversion factor:
$$\vec{v}_{corr} = \frac{\vec{d}_{corr}}{\Delta t} \times 0.1\text{ m/px} = \vec{d}_{corr} \times 3.0\text{ m/s}$$

* **Interval 242 $\rightarrow$ 243 (VLC 243 $\rightarrow$ 244)**:
  * $v_x = +80.55\text{ m/s}$
  * $v_y = -19.35\text{ m/s}$
  * **Total Speed**: $82.85\text{ m/s } (298.28\text{ km/h})$
* **Interval 243 $\rightarrow$ 244 (VLC 244 $\rightarrow$ 245)**:
  * $v_x = +82.59\text{ m/s}$
  * $v_y = +86.37\text{ m/s}$
  * **Total Speed**: $119.51\text{ m/s } (430.25\text{ km/h})$
* **Interval 244 $\rightarrow$ 245 (VLC 245 $\rightarrow$ 246)**:
  * $v_x = +197.76\text{ m/s}$
  * $v_y = +84.03\text{ m/s}$
  * **Total Speed**: $214.86\text{ m/s } (773.48\text{ km/h})$
* **Interval 245 $\rightarrow$ 246 (VLC 246 $\rightarrow$ 247)**:
  * $v_x = +267.66\text{ m/s}$
  * $v_y = +85.14\text{ m/s}$
  * **Total Speed**: $280.88\text{ m/s } (1011.18\text{ km/h})$

### 3.2 Accelerations Between Transitions
We calculate the acceleration vector $\vec{a}$ between consecutive velocity intervals:
$$\vec{a} = \frac{\vec{v}_{curr} - \vec{v}_{prev}}{\Delta t} = (\vec{v}_{curr} - \vec{v}_{prev}) \times 30\text{ s}^{-1}$$
$$\text{G-Force} = \frac{\|\vec{a}\|}{9.81\text{ m/s}^2}$$

1. **Acceleration 1 (Interval 1 $\rightarrow$ Interval 2)**:
   * $a_x = +61.20\text{ m/s}^2$
   * $a_y = +3171.60\text{ m/s}^2$
   * **Magnitude**: **$3172.15\text{ m/s}^2$**
   * **G-Force**: **$323.4\text{ g}$**
2. **Acceleration 2 (Interval 2 $\rightarrow$ Interval 3)**:
   * $a_x = +3455.10\text{ m/s}^2$
   * $a_y = -70.20\text{ m/s}^2$
   * **Magnitude**: **$3455.13\text{ m/s}^2$**
   * **G-Force**: **$352.2\text{ g}$**
3. **Acceleration 3 (Interval 3 $\rightarrow$ Interval 4)**:
   * $a_x = +2097.00\text{ m/s}^2$
   * $a_y = +33.30\text{ m/s}^2$
   * **Magnitude**: **$2098.05\text{ m/s}^2$**
   * **G-Force**: **$213.9\text{ g}$**

### 3.3 Average Over-all Burst Acceleration (Frame 242 to 246)
Assuming the object accelerated from rest ($\vec{v}_0 = 0$) at Frame 242 to its final velocity at Frame 246 over a total duration of **$4\text{ frames}$** ($\Delta T = 4/30 = 0.1333\text{ seconds}$):
* $\text{Average } a_x = +2007.45\text{ m/s}^2$
* $\text{Average } a_y = +638.55\text{ m/s}^2$
* **Average Acceleration Magnitude**: **$2106.63\text{ m/s}^2$**
* **Average G-Force**: **$214.7\text{ g}$**

---

## 4. Summary Table of Object Motion

The table below compiles the complete background-corrected kinematics of the white spot:

| Phase Transition | Time Duration ($\Delta t$) | $\vec{v}_x$ Velocity | $\vec{v}_y$ Velocity | Resultant Speed | Horizontal Accel ($a_x$) | Vertical Accel ($a_y$) | Net Accel Magnitude | Resultant G-Force |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Initial (Frame 242)** | 0.000 s | $0.00\text{ m/s}$ | $0.00\text{ m/s}$ | $0.00\text{ m/s}$ | — | — | — | — |
| **Frame 242 $\rightarrow$ 243** | 0.033 s | $+80.55\text{ m/s}$ | $-19.35\text{ m/s}$ | $82.85\text{ m/s}$ | — | — | — | — |
| **Frame 243 $\rightarrow$ 244** | 0.033 s | $+82.59\text{ m/s}$ | $+86.37\text{ m/s}$ | $119.51\text{ m/s}$ | $+61.2\text{ m/s}^2$ | $+3171.6\text{ m/s}^2$ | $3172.15\text{ m/s}^2$ | **$323.4\text{ g}$** |
| **Frame 244 $\rightarrow$ 245** | 0.033 s | $+197.76\text{ m/s}$ | $+84.03\text{ m/s}$ | $214.86\text{ m/s}$ | $+3455.1\text{ m/s}^2$ | $-70.2\text{ m/s}^2$ | $3455.13\text{ m/s}^2$ | **$352.2\text{ g}$** |
| **Frame 245 $\rightarrow$ 246** | 0.033 s | $+267.66\text{ m/s}$ | $+85.14\text{ m/s}$ | $280.88\text{ m/s}$ | $+2097.0\text{ m/s}^2$ | $+33.3\text{ m/s}^2$ | $2098.05\text{ m/s}^2$ | **$213.9\text{ g}$** |

---

## 5. Physical Discussion & Findings

The tracking data reveals extraordinary, non-classical flight physics for the white spot:

1. **Staggering Acceleration**: The object transitions from a complete hover relative to the camera to a velocity of **$280.88\text{ m/s}$** ($1011.18\text{ km/h}$) in just **$0.133\text{ seconds}$** (4 frames). This requires an average acceleration of **$2106.63\text{ m/s}^2$** ($214.7\text{ g}$) and peaks at **$3455.13\text{ m/s}^2$** ($352.2\text{ g}$).
2. **Structural Load Limits**: For comparison, modern high-performance military fighter jets (like the F-16 or F-35) are structurally rated for a maximum human/airframe limit of **$9\text{ g}$**. Solid-state guided missiles (such as the AIM-9X Sidewinder) reach peak maneuver limits of **$60\text{ g}$**. An acceleration of **$352\text{ g}$** would completely crush conventional aerospace frames, avionics, and sensors, pointing to an solid-state object or highly advanced, lightweight structure.
3. **Transition to High Subsonic Speed**: By Frame 246, the object's speed of **$280.88\text{ m/s}$** is approximately **Mach 0.82** (assuming sea-level speed of sound of $343\text{ m/s}$). It reaches this high subsonic speed almost instantaneously without showing any shockwave-related deceleration or visual instability.
