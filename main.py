import mcaReader
import time

with open("in/r.0.0.mca", "rb") as f:
    data = f.read()

start = time.time()

mca = mcaReader.MCA(data)

end = time.time()
# All chunks in mca file are read, but for demonstration purposes I'm only printing out the first one.
print(mca.chunks[0].nbt_data)
print(f"Time taken: {end-start}")
