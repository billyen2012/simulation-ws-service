
from spectrum_lib import SpectrumMath

sampling_rate = 250
process_win_rate = 5
fft_window = sampling_rate * 4
bord_frequency = 50


delta_coef = 0.0
theta_coef = 1.0
alpha_coef = 1.0
beta_coef = 0.0
gamma_coef = 0.0

def make_spectrum_math_obj():
  spectrum_math = SpectrumMath(sampling_rate, fft_window, process_win_rate)
  spectrum_math.init_params(bord_frequency, True)
  spectrum_math.set_waves_coeffs(delta_coef, theta_coef, alpha_coef, beta_coef, gamma_coef)
  spectrum_math.set_squared_spect(True)
  spectrum_math.set_hanning_win_spect()
  return spectrum_math

def get_spectrum(data:list[float], spectrum_math):
  spectrum_math.push_data(data)
  spectrum_math.process_data()
  return  spectrum_math.read_waves_spectrum_info_arr()