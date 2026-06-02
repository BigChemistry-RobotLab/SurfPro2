import csv

out_list = set()
with open("rosen2012_table3-5_references.csv", "r") as file:
    reader = csv.reader(file)

    for r in reader:
        if len(r) == 2:
            name = r[0].lower().replace(" ", "")
            year = r[1].strip()
            out_list.add(f"{name}{year}")

with open("rosen2012_ref_list.csv", "w") as file:
    writer = csv.writer(file)
    for o in out_list:
        writer.writerow([o])


