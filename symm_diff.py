import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt 
from mpmath import *
import math
from extrapolation import *

mp.dps = 500

folder = '/Users/hjaltithorisleifsson/Documents/extrapolation/diff_quot_plots/'

class SymmetricDifference(Scheme):

	def __init__(self):
		super(SymmetricDifference, self).__init__(2)

	def apply(self, quot, n):
		h = quot.h0 / n
		return (quot.f(quot.x + h) - quot.f(quot.x - h)) / (2 * h)

	def get_evals(self, n):
		return 2

class Quotient:
	def __init__(self, f, x, h0, dfx, tex, ref):
		self.f = f
		self.x = x
		self.h0 = h0
		self.ans = dfx
		self.tex = tex
		self.ref = ref

def plot_basic():
	quotients = []
	quotients.append(Quotient(lambda x: 0 if x < 0 else math.exp(-1/x), 0.0, 0.5, 0.0, '$d/dx|_{x=0}r(x)$', 'rho'))
	quotients.append(Quotient(lambda x: x * math.exp(-1.0/x**2), 0.0, 0.5, 0.0, '$d/dx|_{x=0}xe^{-1/x^2}$. $h=1/2$', 'xemxm2'))
	quotients.append(Quotient(lambda x: math.sin(x), 0.0, 0.5, 1.0, '$d/dx|_{x=0}\sin x$. $h=1/2$', 'sin'))
	quotients.append(Quotient(lambda x: 1 / (1.0 + x**2), 1.0 / math.sqrt(3), 0.5 / math.sqrt(3), -3.0 * math.sqrt(3) / 8.0, '$d/dx|_{x=1/\sqrt{3}}1/(1 + x^2)$', 'g_one_inflection'))
	quotients.append(Quotient(lambda x: 1 / (0.0001 + x**2), 0.01 / math.sqrt(3), 0.005 / math.sqrt(3), -1125000 / math.sqrt(3), '$d/dx|_{x=0.01/\sqrt{3}}1 / (0.0001 + x^2)$', 'g_tenthousandth_inflection'))
	quotients.append(Quotient(lambda x: 1 / (0.00000001 + x**2), 0.0001 / math.sqrt(3), 0.00005 / math.sqrt(3), -1125000000000 / math.sqrt(3), '$d/dx|_{x=0.0001/\sqrt{3}}1 / (10^{-8} + x^2)$', 'g_em8_inflection'))
	quotients.append(Quotient(lambda x: math.log(x + 0.0001), 0.0, 0.00005, 10000.0, '$d/dx|_{x = 0} \ln (x + 0.0001)$. $h=1/2\cdot 10^{-4}$', 'h_tenthousandth'))
	quotients.append(Quotient(lambda x: math.log(x + 0.01), 0.0, 0.005,100.0, '$d/dx|_{x=0} \ln (x + 0.01)$. $h=1/2\cdot 10^{-2}$', 'h_hundredth'))
	quotients.append(Quotient(lambda x: math.log(x + 1), 0.0, 0.5, 1.0, '$d/dx|_{x=0} \ln(x + 1)$. $h=1/2$', 'h_one'))
	quotients.append(Quotient(lambda x: x * x * math.sin(1 / x), 0.0, 1.0, 0.0, '$d/dx|_{x=0} x^2 \sin(1/x)$. $h=1$', 'xsin'))
	quotients.append(Quotient(lambda x: math.sqrt(x + 1), 0.0, 0.5, 0.5, '$d/dx|_{x=0} \sqrt{x + 1}$. $h=1/2$', 'sqrt_1'))
	quotients.append(Quotient(lambda x: math.sqrt(x + 10**(-2)), 0.0, 0.005, 5.0, '$d/dx|_{x=0}\sqrt{x + 10^{-2}}$. $h=1/2\cdot 10^{-2}$', 'sqrt_em2'))
	quotients.append(Quotient(lambda x: math.sqrt(x + 10**(-4)), 0.0, 0.00005, 50.0, '$d/dx|_{x=0}\sqrt{x + 10^{-4}}$ $h=1/2\cdot 10^{-4}$', 'sqrt_em4'))
	quotients.append(Quotient(lambda x: math.sqrt(x + 10**(-16)), 0.0, 0.5 * 10**(-16), 50000000.0, '$d/dx|_{x=0}\sqrt{x + 10^{-16}}$ $h=1/2\cdot 10^{-16}$', 'sqrt_em16'))
	quotients.append(Quotient(lambda x: math.exp(x), 0, 1.0, 1.0, '$d/dx|_{x=0}e^x$. $h=1$', 'exp_0'))

	#hp is for 'high precision'
	hp_quotients = []
	hp_quotients.append(Quotient(lambda x: 0 if x < 0 else mp.exp(-1/x), mpf('0'), mpf('0.5'), mpf('0'), '$d/dx|_{x=0}r(x)$', 'rho_hp'))
	hp_quotients.append(Quotient(lambda x: x * mp.exp(-1/mpf(x)**2), mpf('0'), mpf('0.5'), mpf('0'), '$d/dx|_{x=0}xe^{-1/x^2}$. $h=1/2$', 'xemxm2_hp'))
	hp_quotients.append(Quotient(lambda x: mp.sin(x), 0.0, mpf('0.5'), mpf('1'), '$d/dx|_{x=0}\sin x$. $h=1/2$', 'sin_hp'))
	hp_quotients.append(Quotient(lambda x: mpf(1) / (1.0 + mpf(x)**2), 1.0 / mp.sqrt(3), mpf('0.5') / mp.sqrt(3), mpf('-0.375') * mp.sqrt(3), '$d/dx|_{x=1/\sqrt{3}}1/(1 + x^2)$', 'g_one_inf_hp'))
	hp_quotients.append(Quotient(lambda x: 1 / (mpf('0.0001') + mpf(x)**2), mpf('0.01') / mp.sqrt(3), 0.005 / mp.sqrt(3), -1125000 / mp.sqrt(3), '$d/dx|_{x=0.01/\sqrt{3}}1 / (0.0001 + x^2)$', 'g_tenthousandth_inf_hp'))
	hp_quotients.append(Quotient(lambda x: 1 / (mpf('0.00000001') + mpf(x)**2), mpf('0.0001') / mp.sqrt(3), mpf('0.00005') / mp.sqrt(3), mpf('-1125000000000') / mp.sqrt(3), '$d/dx|_{x=0.0001/\sqrt{3}}1 / (10^{-8} + x^2)$', 'g_em8_inf_hp'))
	hp_quotients.append(Quotient(lambda x: mp.log(mpf(x) + mpf('0.0001')), mpf(0.0), mpf('0.00005'), mpf(10000), '$d/dx|_{x = 0} \ln (x + 0.0001)$. $h=1/2\cdot 10^{-4}$', 'h_tenthousandth_hp'))
	hp_quotients.append(Quotient(lambda x: mp.log(mpf(x) + mpf('0.01')), mpf(0.0), mpf('0.005'), mpf(100), '$d/dx|_{x=0} \ln (x + 0.01)$. $h=1/2\cdot 10^{-2}$', 'h_hundredth_hp'))
	hp_quotients.append(Quotient(lambda x: mp.log(mpf(x) + mpf(1)), mpf(0.0), mpf(0.5), mpf(1), '$d/dx|_{x=0} \ln(x + 1)$. $h=1/2$', 'h_one_hp'))
	hp_quotients.append(Quotient(lambda x: mpf(x) * mpf(x) * mp.sin(mpf(1) / mpf(x)), mpf(0.0), mpf(1.0), mpf(0.0), '$d/dx|_{x=0} x^2 \sin(1/x)$. $h=1$', 'xsin_hp'))
	hp_quotients.append(Quotient(lambda x: mp.sqrt(mpf(x) + 1), 0.0, mpf('0.5'), mpf('0.5'), '$d/dx|_{x=0} \sqrt{x + 1}$. $h=1/2$', 'sqrt_1_hp'))
	hp_quotients.append(Quotient(lambda x: mp.sqrt(mpf(x) + mpf(10)**(-2)), 0.0, mpf('0.005'), mpf('5.0'), '$d/dx|_{x=0}\sqrt{x + 10^{-2}}$. $h=1/2\cdot 10^{-2}$', 'sqrt_em2_hp'))
	hp_quotients.append(Quotient(lambda x: mp.sqrt(mpf(x) + mpf(10)**(-4)), 0.0, mpf('0.00005'), mpf('50.0'), '$d/dx|_{x=0}\sqrt{x + 10^{-4}}$ $h=1/2\cdot 10^{-4}$', 'sqrt_em4_hp'))
	hp_quotients.append(Quotient(lambda x: mp.sqrt(mpf(x) + mpf(10)**(-16)), 0.0, mpf('0.5') * mpf(10)**(-16), mpf('50000000.0'), '$d/dx|_{x=0}\sqrt{x + 10^{-16}}$ $h=1/2\cdot 10^{-16}$', 'sqrt_em16_hp'))
	hp_quotients.append(Quotient(lambda x: mp.exp(x), 0.0, mpf(1.0), mpf(1.0), '$d/dx|_{x=0}e^x$', 'exp_0_hp'))

	seqs = []
	seqs.append(romberg_seq(35))
	seqs.append(bulirsch_seq(35))
	seqs.append(harmonic_seq(35))

	sdq = SymmetricDifference()

	results_quot_seq = []
	hp_results_quot_seq = []

	for quotient in quotients:
		results_seq = []
		for seq in seqs:
			results_seq.append(analyze(quotient, sdq, seq, False))

		results_quot_seq.append(results_seq)

	for hp_quotient in hp_quotients:
		hp_results_seq = []
		for seq in seqs:
			hp_results_seq.append(analyze(hp_quotient, sdq, seq, True))

		hp_results_quot_seq.append(hp_results_seq)

	for (results_seq, quotient) in zip(results_quot_seq, quotients):
		plot_eval_error(results_seq, 'Quotient: ' + quotient.tex + '. Double precision', quotient.ref, True, folder)

	for (results_seq, quotient) in zip(hp_results_quot_seq, hp_quotients):
		plot_eval_error(results_seq, 'Quotient: %s' % quotient.tex, quotient.ref, True, folder)
		plot_trend(results_seq, 'Quotient: %s' % quotient.tex, quotient.ref, True, folder)

	file = open(folder + 'all_results.txt', 'w')	

	for hp_results_seq in hp_results_quot_seq:
		for hp_result in hp_results_seq: 
			ln_e = hp_result.ln_e
			p = opt.curve_fit(fit_func, hp_result.evals, ln_e, [0, 1.0, 1.0], maxfev = 10000)[0]
			file.write('%s & %s & \\(%.5g\\) & \\(%.5g\\) & \\(%.5g\\) \\\\\n' % (hp_result.prob_ref, hp_result.seq_ref, p[0], p[1], p[2]))

	file.close()

def main():
	plot_basic()
	