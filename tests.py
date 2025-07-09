#from functions.get_files_info import get_files_info

# Test current directory
# result = get_files_info("calculator", ".")
# print("Result for current directory:\n", result)

# Test pkg directory
# result = get_files_info("calculator", "pkg")
# print("Result for 'pkg' directory:\n", result)

# Test a forbidden directory
# result = get_files_info("calculator", "/bin")
# print("Result for '/bin' directory:\n", result)

# Test directory outside working directory
# result = get_files_info("calculator", "../")
# print("Result for '../' directory:\n", result)

#from functions.get_file_content import get_file_content

# Test for main.py file
# result = get_file_content("calculator", "main.py")
# print("Result for 'main.py' file:\n", result)

# Test for pkg/calculator.py file
# result = get_file_content("calculator", "pkg/calculator.py")
# print("Result for 'pkg/calculator.py' file:\n", result)

# Test a forbidden directory
# result = get_file_content("calculator", "/bin/cat")
# print("Result for 'bin/cat' directory:\n", result)

# Test truncate
# result = get_file_content("calculator", "lorem.txt")
# print("Result for 'lorem.txt' file:\n", result)

from functions.get_write_file import write_file

# Test lorem text
result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print("Results for 'lorem.txt' file:\n", result)

# Test pkg/morelorem text
result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print("Results for 'pkg/morelorem.txt' file:\n", result)

# Test forbidden text
result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print("Results for '/tmp/temp.txt' file:\n", result)