# Creates planes.csv with 90 planes: the triangle moves along the z axis
# (from z=5 to z=94), so the video "travels" through the tree trunk.
with open("planes.csv", "w") as f:
    for z in range(5, 95):
        f.write(f"50,10,{z},10,90,{z},90,90,{z}\n")
print("created planes.csv with 90 planes")