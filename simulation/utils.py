import numpy as np
import matplotlib.pyplot as plt
import os, shutil
import time

def generate_continous_function_from_discrete_data(x_val, y_val, device_name, y_label):
    file_name = "./check_values/" + device_name + "-" + y_label + ".png"
    
    # get x and y vectors
    x = np.array(x_val)
    y = np.array(y_val)

    # calculate polynomial
    z = np.polyfit(x, y, 5)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    if os.path.exists(file_name):
        return f

    fig, ax = plt.subplots()

    ax.plot(x,y,'o', label="discrete values")
    ax.plot(x_new,y_new, label="continous values")
    plt.xlim([x[0]-1, x[-1] + 1 ])

    ax.set_xlabel("Passmark score")
    ax.set_ylabel(y_label)
    ax.legend()

    fig.savefig(file_name)
    plt.close(fig)

    return f

def remove_content_check_value_directory():
    folder = './check_values'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            exit(-1)

def create_report_directory(report_path):
    try:
        os.mkdir(report_path)
    except OSError:
        print ("Creation of the directory %s failed" % report_path)
        exit(-1)
    else:
        print ("Successfully created the directory %s " % report_path)