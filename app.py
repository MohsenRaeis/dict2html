from flask import Flask, render_template, session, request
import json
import copy

# Every page has a dictionary and loading that determines the layout
app = Flask(__name__,
            template_folder='templates')
lib = {'a': 2, '3': 4}

lib_config = {'name': 'Library Dictionary', 'key_edit': False, 'val_edit': True,
              'max_value_len': 250, 'max_key_len': 50, 'columns': 2}
stress_config = {'SRX':{'53p1_PAM4': {'FIR': [0, 0.02, -0.06, 0], 'RJ': 10, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]},
                        '41p25_PAM4': {'FIR': [0, 0.0, 0.02, 0], 'RJ': 10, 'BUJ': 50, 'amp': [250e-3]},
                        '26p6_PAM4': {'FIR': [0, -0.05, -0.1, 0], 'RJ': 15, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]},
                        '25p8_NRZ': {'FIR': [0, 0.0, 0, 0], 'RJ': 16, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]}},
                 'ORX': {
                     '53p1_PAM4': {'FIR': [0, 0.02, -0.06, 0], 'RJ': 10, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]},
                     '41p25_PAM4': {'FIR': [0, 0.0, 0.02, 0], 'RJ': 10, 'BUJ': 50, 'amp': [250e-3]},
                     '26p6_PAM4': {'FIR': [0, -0.05, -0.1, 0], 'RJ': 15, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]},
                     '25p8_NRZ': {'FIR': [0, 0.0, 0, 0], 'RJ': 16, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]}},
                 'MRX': {
                     '53p1_PAM4': {'FIR': [0, 0.02, -0.06, 0], 'RJ': 10, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]},
                     '41p25_PAM4': {'FIR': [0, 0.0, 0.02, 0], 'RJ': 10, 'BUJ': 50, 'amp': [250e-3]},
                     '26p6_PAM4': {'FIR': [0, -0.05, -0.1, 0], 'RJ': 15, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]},
                     '25p8_NRZ': {'FIR': [0, 0.0, 0, 0], 'RJ': 16, 'BUJ': 50, 'amp': [180e-3, 250e-3, 325e-3]}}
                 }

JTOL_cfg = {'53p1_PAM4': {'PASS Line': [(0.04, 5), (4, 0.05), (100, 0.05)],
                          'MAX Line': [(0.04, 40), (4, 0.5), (100, 0.5)],
                          'PJ Frequencies': sorted([0.04, 0.5, 1, 2, 4, 7.5, 10, 50, 100])},
            '41p25_PAM4': {'PASS Line': [(0.04, 5), (4, 0.05), (100, 0.05)],
                          'MAX Line': [(0.04, 40), (4, 0.5), (100, 0.5)],
                          'PJ Frequencies': sorted([0.04, 0.5, 1, 2, 4, 7.5, 10, 50, 100])},
            '26p6_PAM4': {'PASS Line': [(0.04, 5), (4, 0.05), (100, 0.05)],
                          'MAX Line': [(0.04, 40), (4, 0.5), (100, 0.5)],
                          'PJ Frequencies': sorted([0.04, 0.5, 1, 2, 4, 7.5, 10, 50, 100])},
            '25p8_NRZ': {'PASS Line': [(0.04, 5), (4, 0.05), (100, 0.05)],
                          'MAX Line': [(0.04, 40), (4, 0.5), (100, 0.5)],
                          'PJ Frequencies': sorted([0.04, 0.5, 1, 2, 4, 7.5, 10, 50, 100])}}

JTOL_cfg_cfg = {'name': 'JTOL Configuration', 'key_edit': False, 'val_edit': True,
              'max_value_len': 350, 'max_key_len': 100, 'columns': 2}
JTOL_cfg_default = {'PASS Line': [(0.04, 5), (4, 0.05), (100, 0.05)],
                          'MAX Line': [(0.04, 40), (4, 0.5), (100, 0.5)],
                          'PJ Frequencies': sorted([0.04, 0.5, 1, 2, 4, 7.5, 10, 50, 100])}

file_name = 'lib.json'
with open(file_name, 'w') as writer:
    json.dump(lib, writer)

@ app.route('/', methods=['GET', 'POST'])
def home(lib=lib):
    if request.method == 'GET':
        return render_template('home.html', lib=lib, lib_config=lib_config)
    elif request.method == 'POST':
        if 'pop' in request.form.keys():
            lib.pop(request.form['pop'], None)
        elif 'add' in request.form.keys():
            temp_dict = request.form.to_dict(flat=True)
            lib[temp_dict['__Key__']] = temp_dict['__Value__']
            with open(file_name, 'w') as writer:
                json.dump(lib, writer)
        elif 'submit' in request.form.keys():
            # Building the whole library from the keys and values
            new_lib = request.form.to_dict(flat=True)
            new_lib.pop('__Key__', None)
            new_lib.pop('__Value__', None)
            new_lib.pop('__Submit__', None)
            lib = copy.copy(new_lib)
            with open(file_name, 'w') as writer:
                json.dump(lib, writer)
        return render_template('home.html', lib=lib, lib_config=lib_config)

@app.route('/JTOL_config', methods=["GET", "POST"])
def JTOL_config(lib=JTOL_cfg, lib_config=JTOL_cfg_cfg, default_dict=JTOL_cfg_default):
    if request.method == 'GET':
        return render_template('JTOL_config.html', lib=lib, lib_config=lib_config)
    elif request.method == 'POST':
        if 'pop' in request.form.keys():
            print(request.form.to_dict(flat=True))
            lib.pop(request.form['pop'], None)
        elif 'add' in request.form.keys():
            temp_dict = request.form.to_dict(flat=True)
            lib[temp_dict['__Key__']] = default_dict
            with open(file_name, 'w') as writer:
                json.dump(lib, writer)
        elif 'submit' in request.form.keys():
            # Building the whole library from the keys and values
            new_lib = request.form.to_dict(flat=True)
            print(new_lib)
        return render_template('JTOL_config.html', lib=JTOL_cfg, lib_config=JTOL_cfg_cfg)

if __name__ == '__main__':
    app.run(debug=True)