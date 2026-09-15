import argparse

parser = argparse.ArgumentParser(
    description="Calculate the stau decay width from its proper decay length."
)

parser.add_argument(
    "--ctau",
    type=float,
    default=10, # meters
    help="Stau proper decay length in meters"
)

args = parser.parse_args()

ctau_m = args.ctau
hbar_GeV_s = 6.582119569e-25   # ħ in GeV*s
c = 3e8                        # m/s

tau_s = ctau_m / c
width_GeV = hbar_GeV_s / tau_s
#print(f"for lifetime {ctau_m} (in m) the decay width is {width_GeV}")
print(f"{width_GeV:.10e}")


