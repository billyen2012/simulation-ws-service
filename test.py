import math
from spectrum_lib import SpectrumMath
import matplotlib.pyplot as plt
from get_data import get_data
import datetime
from time import sleep

def get_sin_wave_sample(sampling_rate: int, hz: int, step: int):
    return 50 * math.sin(hz * step * (2 - math.pi / sampling_rate))


def main():
    # spectrum setup
    sampling_rate = 250
    process_win_rate = 5
    fft_window = sampling_rate * 4
    bord_frequency = 50

    spectrum_math = SpectrumMath(sampling_rate, fft_window, process_win_rate)
    spectrum_math.init_params(bord_frequency, True)

    delta_coef = 0.0
    theta_coef = 1.0
    alpha_coef = 1.0
    beta_coef = 0.0
    gamma_coef = 0.0

    spectrum_math.set_waves_coeffs(delta_coef, theta_coef, alpha_coef, beta_coef, gamma_coef)
    spectrum_math.set_squared_spect(True)
    spectrum_math.set_hanning_win_spect()


    # figure setup
    fig, ax = plt.subplots()
    rects = ax.bar(x=['1'], height=[3], align="center")  # 40 is upper bound of y-axis
    # data extraction setup
    _data = get_data()
    start = 0
    data_count_per_round = 250
    channel = 'c1'
    while True:
        data_points = list()
        for i in range(start, start + data_count_per_round):
          data_points.append(_data[i][channel])
        print(data_points)
        start += data_count_per_round

        spectrum_math.push_data(data_points)
        spectrum_math.process_data()

        raw_spectrum_data = spectrum_math.read_raw_spectrum_info_arr()
        waves_spectrum_data = spectrum_math.read_waves_spectrum_info_arr()

        # spectrum_math.compute_spectrum(data)
        #
        # raw_spectrum_data = spectrum_math.read_raw_spectrum_info()
        # waves_spectrum_data = spectrum_math.read_waves_spectrum_info()

        # for i in range(len(raw_spectrum_data)):
        #     print(
        #         "{}: {}, {}".format(i, raw_spectrum_data[i].total_raw_pow, len(raw_spectrum_data[i].all_bins_values)))
        #     print("{}: {} {} {} {} {}".format(i, waves_spectrum_data[i].delta_raw, waves_spectrum_data[i].beta_raw,
        #                                       waves_spectrum_data[i].alpha_raw, waves_spectrum_data[i].gamma_raw,
        #                                       waves_spectrum_data[i].theta_raw))

        # if raw_spectrum_data is not None:
        #     print("{}, {}".format(raw_spectrum_data.total_raw_pow, len(raw_spectrum_data.all_bins_values)))

        print(len(waves_spectrum_data))
        for i in range(len(waves_spectrum_data)):
            alpha_theta_ratio = waves_spectrum_data[i].alpha_raw/ waves_spectrum_data[i].theta_raw
            rects[0].set_height(alpha_theta_ratio)
            rects[0].set_color("green" if alpha_theta_ratio <0.5 else "orange" if alpha_theta_ratio < 1.0 else "red")

            fig.canvas.draw()
            sleep(0.1)
            plt.pause(0.1)
        # print date time
        for txt in ax.texts:
          txt.remove()
        ax.text(0.5, 0.9, "alpha/theta ratio (channel: " + channel +")" , horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.5, 0.85, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") , horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.5, 0.8, "data points: " +  str(start + data_count_per_round), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                # if waves_spectrum_data is not None:
        #     print("{} {} {} {} {}".format(waves_spectrum_data.delta_raw, waves_spectrum_data.beta_raw,
        #                                   waves_spectrum_data.alpha_raw, waves_spectrum_data.gamma_raw,
        #                                   waves_spectrum_data.theta_raw))


        spectrum_math.set_new_sample_size()

    del spectrum_lib

if __name__ == '__main__':
    main()