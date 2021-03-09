import sys
import os
import shutil
import platform

# determine platform
if platform.system() == "Windows":
    platform  = True
else:
    platform = False

# useful path
if platform:
    newpath_output = r'.\output'
    path_input = r'.\input\test'
    path_output = r'.\output\test'
    path_ref = r'.\ref\test'
else:
    newpath_output = r'./output'
    path_input = r'./input/test'
    path_output = r'./output/test'
    path_ref = r'./ref/test'


# make output folder if needed
if not os.path.exists(newpath_output):
    os.mkdir(newpath_output)

# run homework + check the result
def check(input_filename, ref_filename, output_filename):
    if platform:
        os.system('python main.py ' + input_filename + ' ' + output_filename)
    else:
        os.system('python3 main.py ' + input_filename + ' ' + output_filename)
    try:
        ref_file = open(ref_filename, "r")
    except:
        print("\n" + ref_filename + " file not found")
    try:
        output_file = open(output_filename, "r")
    except:
        print("\n" + output_filename + " file not found")
    ref = ref_file.readline()[:-1]
    output = output_file.readline()[:-1]
    if len(ref) != len(output):
        return False
    for i in range(len(ref)):
        if ref[i] != output[i]:
            return False
    return True

# print the result
def display(number):
    print("Test" + str(number), end='')
    print("...................................................", end='')
    input_filename = path_input + str(number) + '.in'
    output_filename = path_output + str(number) + '.out'
    ref_filename = path_ref + str(number) + ".ref"
    result = check(input_filename, ref_filename, output_filename)
    if result:
        if number < 5:
            print("[1/1]")
            return 1
        elif number > 9:
            print("[5/5]")
            return 5
        else:
            print("[3/3]")
            return 3
    else:
        if number < 5:
            print("[0/1]")
        elif number > 9:
            print("[0/5]")
        else:
            print("[0/3]")
    return 0

if __name__ == "__main__":
    # all tests
    if len(sys.argv) == 1:
        score = 0
        for i in range(15):
            score = score + display(i)
        print("Total", end='')
        print("...................................................", end='')
        print("[" + str(score) + "/45]")
    # 1 test
    elif len(sys.argv) == 2:
        if not int(sys.argv[1]) < 15:
            print("Wrong test number")
        else:
            display(int(sys.argv[1]))
    # something went wrong
    else:
        if platform:
            print("Wrong paramters, it should be:\n python .\checker.py test_no       OR\n python .\checker.py\n")
        else:
            print("Wrong paramters, it should be:\n python ./checker.py test_no       OR\n python ./checker.py\n")
    
    # clean up
    shutil.rmtree(newpath_output)
