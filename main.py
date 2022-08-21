import mcaReader

with open("in/r.0.0.mca", "rb") as f:
    data = f.read()

mca = mcaReader.MCA(data)
# All chunks in mca file are read, but for demonstration purposes I'm only printing out the first one.
print(mca.chunks[0].nbt_data)
