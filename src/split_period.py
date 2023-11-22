import csv

period_set = {"0限", "1限", "2限", "3限", "4限", "5限", "6限"}
day_set = {"他", "月", "火", "水", "木", "金"}

data = list()

with open('../data/syllabus_base_info.tsv', 'r', encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    next(csv_reader)
    for row in csv_reader:
        if row[3] not in period_set or row[2] not in day_set:
            row_many_period = list(row[3].split(","))
            row_many_day = list(row[2].split(","))
            for i in range(len(row_many_period)):
                period = row_many_period[i]
                day = row_many_day[i]
                row_tmp = row[:]
                row_tmp[3] = period
                row_tmp[2] = day
                data.append(row_tmp)
        else:
            data.append(row)
with open("../data/syllabus_base_info_splited_by_day_and_period.tsv", "w", encoding="utf-8") as f:
    for d in data:
        f.write("\t".join(d))
        f.write("\n")

