from mdtable import MDTable

markdown = MDTable('csvFile.csv')
markdown_string = markdown.get_table()
markdown.save_table('md.txt')