import PySimpleGUI as sg
import os
from pdf import Pdf


def process_pdf(DIR, pdf_path):
    p = Pdf(DIR, pdf_path)
    p_count = p.get_pages_count()
    pp_count = 0

    window['p_bar_2'].update(current_count=0, max=p_count)
    window['p_count_l'].update(f'{pp_count} pages processed from {p_count} pages')

    for _ in p.to_csv():
        pp_count += 10
        window['p_bar_2'].update(current_count=pp_count)
        window['p_count_l'].update(f'{pp_count} pages processed from {p_count} pages')

    

# Define the window's contents
layout = [
    [sg.Text('Input Foldder', size=(12,1)), sg.Input(key='folder'), sg.FolderBrowse()],
    [sg.Button('Process')],
    [sg.HorizontalLine()],
    [sg.Text('o files processed from 0 files', k='f_count_l')],
    [sg.ProgressBar(100, size=(55, 20), key='p_bar_1')],
    [sg.Text('o pages processed from 0 pages', k='p_count_l')],
    [sg.ProgressBar(100, size=(55, 20), key='p_bar_2')]
]

# Create the window
window = sg.Window('PDF Data Extracker', layout, element_justification= 'c')

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    
    # Output a message to the window
    if event == 'Process':
        if not os.path.exists(values['folder']):
            sg.popup_ok("Folder doesn't exists")
        elif not os.path.isdir(values['folder']):
            sg.popup_ok('Invalied folder path')
        else:
            f_path = values['folder']
            pdf_files = [f for f in os.listdir(f_path) if f.endswith('.pdf')]
            is_process = sg.popup_yes_no(f'{len(pdf_files)} pdf files found. Do you want to process ?')
            
            if is_process == 'Yes':
                fp_count=0
                window['p_bar_1'].update(current_count= 0, max=len(pdf_files))
                window['f_count_l'].update(f'{fp_count} files processed from {len(pdf_files)} files')
                
                for pdf_path in pdf_files:
                    process_pdf(f_path, pdf_path)
                    fp_count += 1
                    window['p_bar_1'].update(current_count= fp_count)
                    window['f_count_l'].update(f'{fp_count} files processed from {len(pdf_files)} files')
                                 
                
                
# Finish up by removing from the screen
window.close()
