import solution

data = solution.read_data()
new_data = solution.transform_data(data)
outputdata = solution.reduce_duplication(new_data)
solution.write_to_csv(outputdata)