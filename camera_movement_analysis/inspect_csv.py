with open("/home/egli/.gemini/antigravity/brain/c389e7ca-d9dd-451a-9838-cf1dec287928/scratch/camera_movement.csv", "r") as f:
    lines = f.readlines()

print("Header:", lines[0].strip())
print("\nTransition at 280:")
for i in range(275, 286):
    if i < len(lines):
        print(f"Index {i-1:03d}: {lines[i].strip()}")

print("\nTransition at 370:")
for i in range(365, 376):
    if i < len(lines):
        print(f"Index {i-1:03d}: {lines[i].strip()}")
