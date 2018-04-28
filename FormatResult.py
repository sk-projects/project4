# -*- coding: utf-8 -*-
"""
"""

import ast
content = open("cvgraph.json", "r").read()
results = ast.literal_eval(content)
names = list(results.keys())
features = results['graph_Xaxis']

import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Results.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 1
for name in names:
    worksheet.write(row, 0,     name)
    for i in range(1, len(features)):
        worksheet.write(row, col + i, round(results[name][i], 2))
    row += 1

workbook.close()