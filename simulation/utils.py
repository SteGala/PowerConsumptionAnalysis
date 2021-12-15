import numpy as np
import matplotlib.pyplot as plt
import os, shutil
import pandas

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

def summarize_reports(N_THREAD, report_path):
    consumption_report = pandas.DataFrame()
    score_report = pandas.DataFrame()
    CPU_usage_report = pandas.DataFrame()

    for i in range(N_THREAD):
        consumption = pandas.read_csv(report_path + "/infrastructure" + str(i) + "/consumption.csv")
        score = pandas.read_csv(report_path + "/infrastructure" + str(i) + "/score.csv")
        CPU_usage = pandas.read_csv(report_path + "/infrastructure" + str(i) + "/absolute_CPU_usage.csv")

        consumption_report["date"] = consumption['date']
        score_report["date"] = score["date"]
        CPU_usage_report["date"] = CPU_usage["date"]
        consumption_report["infrastructure" + str(i)] = consumption.sum(axis=1)
        score_report["infrastructure" + str(i)] = score.sum(axis=1)
        CPU_usage_report["infrastructure" + str(i)] = CPU_usage.sum(axis=1)

    consumption_report.to_csv(report_path + '/overall_infrastructure_consumption.csv', index=None)
    score_report.to_csv(report_path + '/overall_infrastructure_score.csv', index=None)
    CPU_usage_report.to_csv(report_path + '/overall_infrastructure_CPU_usage.csv', index=None)


    '/absolute_CPU_usage.csv'