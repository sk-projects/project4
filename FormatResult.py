# -*- coding: utf-8 -*-
"""
"""

def write_cv_results_to_excel(json_cv_results, excel_results):
    import ast
    content = open(json_cv_results, "r").read()
    results = ast.literal_eval(content)
    names = list(results.keys())
    features = results['graph_Xaxis']

    import xlsxwriter

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(excel_results)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 1
    for name in names:
        worksheet.write(row, 0,     name)
        for i in range(0, len(features)):
            worksheet.write(row, col + i, round(results[name][i], 2))
        row += 1

    workbook.close()