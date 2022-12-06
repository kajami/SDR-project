import os

# Create folder for output .wav-files if not exist
try:
    os.listdir("wavIQoutput/")
except FileNotFoundError:
    os.mkdir("wavIQoutput/")

def run_command(file_name):
    # To get the name of the file without file format
    file_name_split = file_name.split(".")

    # To get the samplerate out for sox command
    file_name_parts = file_name_split[0].split("_")
    sample_rate = file_name_parts[-2]

    # sox command
    command = "sox -t raw -e floating-point -b 32 -c 2 -r %s %s %s" % (sample_rate, file_name, "wavIQoutput/" + file_name_split[0] + ".wav")
    print("Converting file %s to .wav file" % (file_name))
    os.system(command)

# Loop all files in the current folder and convert all the .raw files. If there is no raw files in the folder print error message
folder_files = os.listdir(".")
number_of_files = 0
for file_name in folder_files:
    file_name_split = file_name.split(".")
    if (len(file_name_split) == 2):
        if (file_name_split[1] == "raw"):
            run_command(file_name)
            number_of_files = number_of_files+1
if(number_of_files == 0):
    print('Error: no .raw files in folder to convert')
else:
    print(f'Total of {number_of_files} .raw files converted')