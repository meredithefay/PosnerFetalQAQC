# Import relevant libraries
import subprocess
import sys
import os
import shutil
import datetime

path = sys.path

print('Loading necessary packages')

packages = ['openpyxl', 'gitpython', 'matplotlib', 'pytorch-ignite==0.4.2', 'itk==4.13', 'zenodo_get', 'cmake==3.11.0', 'simplereg']  # Libraries required

def install(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# def compile_ITK():
#
#     print('Running ITK compilation step 1')
#     #
#     # subprocess.check_call([sys.executable, "-m", "pip", "uninstall", itk])
#
#     home_directory = subprocess.check_output(['echo $HOME'], shell=True).decode('utf-8').strip()
#     os.chdir(home_directory)
#     # subprocess.run(['mkdir', 'build'])
#     # home_itk = os.path.join(home_directory, 'build')
#     # os.chdir(home_itk)
#
#     subprocess.run(['git', 'clone', 'https://github.com/gift-surg/ITK_NiftyMIC.git'])
#     subprocess.run(['mkdir ITK_NiftyMIC-build'], shell=True)
#     subprocess.run(['cd ITK_NiftyMIC-build'], shell=True)
#
#     # subprocess.run(['export CC=gcc-8'], shell=True)
#     # subprocess.run(['export CXX=g++-8'], shell=True)
#
#     subprocess.run(['cmake', '-D', 'CMAKE_BUILD_TYPE=Release', '-D', 'BUILD_TESTING=OFF',
#                    '-D', 'BUILD_EXAMPLES=OFF', '-D', 'BUILD_SHARED_LIBS=ON', '-D', 'ITK_WRAP_PYTHON=ON', '-D',
#                    'ITK_LEGACY_SILENT=ON', '-D', 'ITK_WRAP_float=ON', '-D', 'ITK_WRAP_double=ON', '-D',
#                    'ITK_WRAP_signed_char=ON', '-D', 'ITK_WRAP_signed_long=ON', '-D', 'ITK_WRAP_signed_short = ON',
#                    '-D', 'ITK_WRAP_unsigned_char=ON', '-D', 'ITK_WRAP_unsigned_long=ON', '-D',
#                    'ITK_WRAP_unsigned_short=ON', '-D', 'ITK_WRAP_vector_float=ON', '-D',
#                    'ITK_WRAP_vector_double=ON', '-D', 'ITK_WRAP_covariant_vector_double=ON', '-D',
#                    'Module_ITKReview=ON', '-D', 'Module_SmoothingRecursiveYvvGaussianFilter=ON', '-D',
#                    'Module_BridgeNumPy=ON', './ITK_NiftyMIC/'])
#
#     subprocess.run(['make', '-j8'])
#
#     python_directory = subprocess.check_output(['python -m site --user-site'], shell=True).decode('utf-8').strip()
#     print(python_directory)
#     path_1 = os.path.join('Wrapping', 'Generators', 'Python', 'WrapITK.pth')
#     print(path_1)
#     subprocess_path = f"cp {path_1} {python_directory}"
#     subprocess.run([subprocess_path], shell=True)
#
#     import itk
#     print(itk.Image.D3.New())
#     print(itk.OrientedGaussianInterpolateImageFilter.ID3ID3.new())

    # subprocess.run(['cp', '-r', home_itk, current_directory])

    os.chdir(current_directory)

install(packages)  # Install libraries required

# Import installed libraries
import matplotlib
matplotlib.use('Agg')
import git

current_directory = os.getcwd()  # Get current working directory

print(current_directory)

monaifbs_download_path = os.path.join(current_directory, 'MONAIfbs')  # Prep MONAIfbs directory
niftymic_download_path = os.path.join(current_directory, 'NiftyMIC')  # Prep niftymic directory

# If MONAIfbs is already downloaded, pass
if os.path.isdir(monaifbs_download_path):
    print('MONAIfbs has previously been added to your working directory')
    pass
else:  # Otherwise, create directory and download library
    print('MONAIfbs is being added to your working directory')  # Update user via command line
    os.mkdir(monaifbs_download_path)  # Make directory for

    git.Git(current_directory).clone('https://github.com/gift-surg/MONAIfbs')

    # Run additional requirements
    # read requirements.txt
    text_file = os.path.join(monaifbs_download_path, 'requirements.txt')
    with open(text_file, 'r+') as f:
        lines = [line.rstrip() for line in f]
        if lines[-1][-1] == ':':
            f.seek(0, os.SEEK_END)  # seek to end of file; f.seek(0, 2) is legal
            f.seek(f.tell() - 1, os.SEEK_SET)  # go backwards 1 bytes
            f.truncate()

    install(lines)

    subprocess.run(['pip', 'install', '-e', monaifbs_download_path])

    # Add model
    subprocess.run(['zenodo_get', '10.5281/zenodo.4282679'])
    subprocess.run(['tar', 'xvf', 'models.tar.gz'])
    subprocess.run(['mv', 'models', os.path.join(monaifbs_download_path, 'monaifbs')])


# # If NiftyMic is already downloaded, pass
# if os.path.isdir(niftymic_download_path):
#     print('NiftyMic has previously been added to your working directory')
#     pass
# else:
#     print('ITK_NiftyMic is being added to your working directory')
#
#     compile_ITK()
#
#     print('NiftyMic is being added to your working directory')
#
#     git.Git(current_directory).clone('https://github.com/gift-surg/NiftyMIC')
#
#     os.chdir(niftymic_download_path)
#     subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
#     itk_dir_command = 'export NIFTYMIC_ITK_DIR=' + os.path.join(home_directory, 'build')
#     subprocess.run([itk_dir_command], shell=True)
#     subprocess.run(['pip', 'install', '-e', niftymic_download_path])
#
#     old_path = os.path.join(niftymic_download_path, 'niftymic', 'application', 'multiply.py')
#     new_path = os.path.join(niftymic_download_path, 'niftymic', 'application', 'multiply_stack_with_mask.py')
#     os.rename(old_path, new_path)

print('Necessary downloads complete')

from tkinter import filedialog
import pandas as pd
import gzip
import itk

# Select a folder
print('Please select a directory containing your imaging data labeled as specified in the manual')
image_directory = filedialog.askdirectory()

# Find all appropriate .nii.gz files within it, organize
#
# Requirements:
#   All first-level subdirectories represent a single participant
#       Directory name will be treated as the patient ID
#   Either:
#       Subdirectories containing "sag" or "ax" or "coro" AND "t2" (any capitalization)
#       .nii or .nii.gz files containing "sag" or "ax" or "coro" AND "t2"

print('Searching for files')

sub_directories = os.listdir(image_directory)  # Remove any directories caused by open windows
if '.DS_Store' in sub_directories:
    sub_directories.remove('.DS_Store')

df = pd.DataFrame()  # Create dataframe with filenames


for sub_directory in sub_directories:
    print('Searching ' + sub_directory)

    out_folder = os.path.join(image_directory, sub_directory, 'segmentation')

    # Remove previous segmentations
    if os.path.exists(out_folder) and os.path.isdir(out_folder):
        shutil.rmtree(out_folder)

    ax_name = False  # Set up default "cannot be found"
    sag_name = False
    coro_name = False

    for root, dirnames, filenames in os.walk(os.path.join(image_directory, sub_directory)):
        for filename in filenames:
            full_name = os.path.join(root, filename)
            full_name = full_name.lower()  # Convert to all lowercase for easier string matching
            if 'nii' in full_name:
                if 'ax' in full_name and 't2w' in full_name:
                    if '.gz' in full_name:
                        with gzip.open(full_name, 'rb') as f_in:
                            subset = full_name.split('.')[0]
                            with open(subset, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                    ax_name = os.path.join(root, sub_directory + '_ax_t2w.nii')
                    os.rename(full_name, ax_name)

                elif 'sag' in full_name and 't2w' in full_name:
                    if '.gz' in full_name:
                        os.chdir(os.path.dirname(full_name))
                        with gzip.open(full_name, 'rb') as f_in:
                            subset = full_name.split('.')[0]
                            with open(subset, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                    sag_name = os.path.join(root, sub_directory + '_sag_t2w.nii')
                    os.rename(full_name, sag_name)

                elif 'coro' in full_name and 't2w' in full_name:
                    if '.gz' in full_name:
                        os.chdir(os.path.dirname(full_name))
                        with gzip.open(full_name, 'rb') as f_in:
                            subset = full_name.split('.')[0]
                            with open(subset, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                    coro_name = os.path.join(root, sub_directory + '_coro_t2w.nii')
                    os.rename(full_name, coro_name)

    if ax_name and sag_name and coro_name:
        passing = True
    else:
        passing = False

    passing_dict = {'Participant': sub_directory,
                    'Axial': ax_name,
                    'Sagittal': sag_name,
                    'Coronal': coro_name,
                    'Passing': passing}

    df = pd.concat([df, pd.DataFrame([passing_dict])], ignore_index=True)

os.chdir(image_directory)

# print('Writing excel data')

# # Create a new dated folder with analysis
# now = datetime.datetime.now()
# output_name = now.strftime('%Y_%m_%d-%H_%M_%S') + '-fetalQAQC-' + os.path.basename(image_directory)  # One level up
#
# Write excel
with pd.ExcelWriter(image_directory + '_info.xlsx') as writer:
    df.to_excel(writer, sheet_name='Passing_status')

# Begin brain segmentation
os.chdir(monaifbs_download_path)

monaifbs_script = os.path.join(monaifbs_download_path, 'monaifbs', 'src', 'inference', 'monai_dynunet_inference.py')
reconstruction_script = os.path.join(niftymic_download_path, 'niftymic_reconstruct_volume.py')
template_location = os.path.join(niftymic_download_path, 'data', 'templates', 'STA37.nii.gz')
template_mask = os.path.join(niftymic_download_path, 'data', 'templates', 'STA37_mask.nii.gz')



for i in range(len(df)):

    if df['Passing'].iloc[i]:

        print('Begin processing for participant ' + sub_directory)

        sub_directory = df['Participant'].iloc[i]

        out_folder = os.path.join(image_directory, sub_directory, 'segmentation')

        os.system('%s %s %s %s %s %s %s %s' % (sys.executable, monaifbs_script, '--in_files', df['Axial'].iloc[i],
                                 df['Sagittal'].iloc[i], df['Coronal'].iloc[i], '--out_folder', out_folder))

        print('Segmentation completed')
#
#         # Names we know
#         ax_seg_path = sub_directory + '_ax_t2w'
#         ax_seg_img = os.path.join(image_directory, sub_directory, 'segmentation',
#                                   ax_seg_path, sub_directory + '_ax_t2w_seg.nii.gz')
#
#         sag_seg_path = sub_directory + '_sag_t2w'
#         sag_seg_img = os.path.join(image_directory, sub_directory, 'segmentation',
#                                   sag_seg_path, sub_directory + '_sag_t2w_seg.nii.gz')
#
#         coro_seg_path = sub_directory + '_coro_t2w'
#         coro_seg_img = os.path.join(image_directory, sub_directory, 'segmentation',
#                                   sag_seg_path, sub_directory + '_coro_t2w_seg.nii.gz')
#
#         # out_folder_2 = os.path.join(image_directory, sub_directory, 'reconstruction')
#         out_folder_2 = os.path.join(image_directory, sub_directory, 'reconstruction', 'srr.nii.gz')
#
#         # os.system('%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' %
#         #           (sys.executable, reconstruction_script, '--filenames', df['Sagittal'].iloc[i], df['Coronal'].iloc[i],
#         #            df['Axial'].iloc[i], '--filenames-masks', sag_seg_img, coro_seg_img, ax_seg_img,
#         #            '--suffix-mask', '_seg', '--alpha', '0.005', '--threshold', '0.6', '--template',
#         #            template_location, '--template-mask', template_mask, '--dir-output', out_folder_2))
#
#         # os.system('%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' %
#         #           ('niftymic_reconstruct_volume', '--filenames', df['Sagittal'].iloc[i], df['Coronal'].iloc[i],
#         #            df['Axial'].iloc[i], '--filenames-masks', sag_seg_img, coro_seg_img, ax_seg_img,
#         #            '--suffix-mask', '_seg', '--alpha', '0.005', '--threshold', '0.6', '--template',
#         #            template_location, '--template-mask', template_mask, '--dir-output', out_folder_2))
#
#         os.system('%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' %
#                   (sys.executable, reconstruction_script, '--filenames', df['Sagittal'].iloc[i], df['Coronal'].iloc[i],
#                    df['Axial'].iloc[i], '--filenames-masks', sag_seg_img, coro_seg_img, ax_seg_img,
#                    '--suffix-mask', '_seg', '--alpha', '0.005', '--threshold', '0.6', '--template',
#                    template_location, '--template-mask', template_mask, '--output', out_folder_2))
#
#         print('Reconstruction completed')