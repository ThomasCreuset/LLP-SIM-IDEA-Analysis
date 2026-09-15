'''
Plotting stage of the Stau analysis
'''
import os
import ROOT
# use this : source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10
intLumi        = 1.92e7
###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
scaleSig       = 1
scaleBkg       = 1.

ana_tex        = ''
delphesVersion = ''
energy         = 240.
collider       = 'FCC-ee'

# Input/output directories
inputDir       = "/eos/home-s/svashish/FCCAnalyses/examples/FCCee/bsm/LLPs/Stau/output/final_0303/"
outdir         = "/eos/home-s/svashish/FCCPlotsAnalyses"
os.makedirs(outdir, exist_ok=True)

formats  = ['png']
yaxis    = ['log', 'lin']
stacksig = ['nostack']

splitLeg = True

# Variables to plots
variables = [
            # # Gen-level stau
            # # "n_GenStau",
            # # "GenStau_vx",
            # # "GenStau_vy",
            # # "GenStau_vz",
            # # "GenStau_Lxy",
            # # "GenStau_Lxyz",
            
            # # Tau kinematics
            "GenTau_e",
            "GenTau_pt",
            "GenTau_eta",
            "GenTau_phi",
            "GenTau_px",
            "GenTau_py",
            "GenTau_pz",
            # "GenTau_cTau",

            # Tau vertex
            "GenTau_vx",
            "GenTau_vy",
            "GenTau_vz",

            # Final-state muons
            "n_FSGenMuon",
            "FSGenMuon_e",
            "FSGenMuon_pt",
            "FSGenMuon_px",
            "FSGenMuon_py",
            "FSGenMuon_pz",
            "FSGenMuon_eta",
            "FSGenMuon_phi",
            "FSGenMuon_charge",
            "FSGenMuon_vx",
            "FSGenMuon_vy",
            "FSGenMuon_vz",

            # # Final-state electrons
            "n_FSGenElectron",
            "FSGenElectron_e",
            "FSGenElectron_pt",
            "FSGenElectron_px",
            "FSGenElectron_py",
            "FSGenElectron_pz",
            "FSGenElectron_eta",
            "FSGenElectron_phi",
            "FSGenElectron_charge",
            "FSGenElectron_vx",
            "FSGenElectron_vy",
            "FSGenElectron_vz",

            # Final-state neutrinos
            "n_FSGenNeutrino",
            "FSGenNeutrino_e",
            "FSGenNeutrino_pt",
            "FSGenNeutrino_px",
            "FSGenNeutrino_py",
            "FSGenNeutrino_pz",
            "FS_GenNeutrino_eta",    
            "FSGenNeutrino_phi",

            # Reco Jets
            "n_RecoJets",
            "RecoJet_e",
            "RecoJet_pt",
            "RecoJet_px",
            "RecoJet_py",
            "RecoJet_pz",
            "RecoJet_eta",
            "RecoJet_phi",
            "RecoJet_charge",

            # Reco Electrons
            "n_RecoElectrons",
            "RecoElectrons_e",
            "RecoElectrons_pt",
            "RecoElectrons_px",
            "RecoElectrons_py",
            "RecoElectrons_pz",
            "RecoElectrons_eta",
            "RecoElectrons_phi",
            "RecoElectrons_charge",

            # Reco Muons
            "n_RecoMuons",
            "RecoMuons_e",
            "RecoMuons_pt",
            "RecoMuons_px",
            "RecoMuons_py",
            "RecoMuons_pz",
            "RecoMuons_eta",
            "RecoMuons_phi",
            "RecoMuons_charge",

            # MET
            "RecoMissingEnergy_e",
            "RecoMissingEnergy_pt",
            "RecoMissingEnergy_eta",
            "RecoMissingEnergy_phi",

            "nDisplacedVertices_failInnerHitVeto",
            "nTracks_DV_failInnerHitVeto",
            "invMass_seltracks_DVs",
            "invMass_seltracks_DVs_zoom",
            "DV_evt_seltracks_chi2",
            "DV_evt_seltracks_normchi2",
            "Reco_seltracks_DVs_Lxy",
            "Reco_seltracks_DVs_Lxyz",

            "sel_tracks_pt_DV",
            "sel_tracks_D0_DV",
            "sel_tracks_Z0_DV",

            "KinkVertex_invMass",
            "RecoVisibleEnergy",
            "RecoMissingEnergy3D",
            "KinkVertex_dxy",
            "KinkVertex_d3d",
            "nKinkVertices",
            "KinkAngle",

]
# Define selections, labels, colors, plots, legends
selections = {}
selections[''] = [
    # "selNone",
    # "semiLeptonic",
    "semiLeptonic_KV",
    "semiLep_DV",
    # "hadronic_short_KV",
    # "hadronic_short_DV",
    "hadronic_KV",
    "hadronic_DV",
    # "hadronic_allchannels"
]

extralabel = {}
# extralabel['selNone'] = "Before selection"
# extralabel['semiLeptonic'] = "1 reco lepton"
extralabel['semiLeptonic_KV'] = "1 reco lepton + 1 KV"
extralabel['semiLep_DV'] = "1 reco lepton + 1 DV"
# extralabel['hadronic_short_KV'] = "0 reco leptons + 1 KV (short ctau)"
# extralabel['hadronic_short_DV'] = "0 reco leptons + ≥1 DV (short ctau)"
extralabel['hadronic_KV'] = "0 reco leptons + ≥1 KV"
extralabel['hadronic_DV'] = "0 reco leptons + DV + <4 jets"
# extralabel['hadronic_allchannels'] = "testing all channel versions"

color_wheel = [
    # colors from DESY color guide
    "#EB5E2D",  # Red
    "#8CBE23",  # Light green
    "#00B1AA",  # Turquoise
    "#D2006E",  # Magenta
    "#917DB9",  # Violet
    "#C3B700",  # Olive
    "#FAC800",  # Yellow
    "#B92D41",  # Dark red
    "#00A64B",  # Green
    "#006987",  # Petrol
    "#8C3C5B",  # Aubergine
    "#504F8F",  # Purple
    "#EAD21D",  # Gold
    "#0D85C2",  # Bright blue
    "#FF4000",  # Bright orange
]

colors = {}

signal_samples = [
    # 20 cm
    'FCCee_100_stau_20cm_ctau_ecm_240',
    'FCCee_105_stau_20cm_ctau_ecm_240',
    'FCCee_110_stau_20cm_ctau_ecm_240',
    'FCCee_115_stau_20cm_ctau_ecm_240',

    # 50 cm
    'FCCee_100_stau_50cm_ctau_ecm_240',
    'FCCee_105_stau_50cm_ctau_ecm_240',
    'FCCee_110_stau_50cm_ctau_ecm_240',
    'FCCee_115_stau_50cm_ctau_ecm_240',

    # 1 m
    'FCCee_100_stau_1m_ctau_ecm_240',
    'FCCee_105_stau_1m_ctau_ecm_240',
    'FCCee_110_stau_1m_ctau_ecm_240',
    'FCCee_115_stau_1m_ctau_ecm_240',

    # 2 m
    'FCCee_100_stau_2m_ctau_ecm_240',
    'FCCee_105_stau_2m_ctau_ecm_240',
    'FCCee_110_stau_2m_ctau_ecm_240',
    'FCCee_115_stau_2m_ctau_ecm_240',

    # 3 m
    'FCCee_100_stau_3m_ctau_ecm_240',
    'FCCee_105_stau_3m_ctau_ecm_240',
    'FCCee_110_stau_3m_ctau_ecm_240',
    'FCCee_115_stau_3m_ctau_ecm_240',

    # 4 m
    'FCCee_100_stau_4m_ctau_ecm_240',
    'FCCee_105_stau_4m_ctau_ecm_240',
    'FCCee_110_stau_4m_ctau_ecm_240',
    'FCCee_115_stau_4m_ctau_ecm_240',
]
for i, sample in enumerate(signal_samples):
    colors[sample] = ROOT.TColor.GetColor(color_wheel[i % len(color_wheel)])

# -----------------------
# Background
# -----------------------

colors['p8_ee_WW_ecm240'] = ROOT.TColor.GetColor(color_wheel[1])
colors['p8_ee_ZZ_ecm240'] = ROOT.TColor.GetColor(color_wheel[2])
colors['mgp8_ee_zh_ecm240_hbb'] = ROOT.TColor.GetColor(color_wheel[3])
colors['wzp6_ee_nuenueH_Htautau_ecm240'] = ROOT.TColor.GetColor(color_wheel[4])
colors['wzp6_ee_bbH_Htautau_ecm240'] = ROOT.TColor.GetColor(color_wheel[5])

# Plot and legend structure
plots = {}
plots[''] = {
    'signal': {s: [s] for s in signal_samples},
    'backgrounds': {
        'p8_ee_WW_ecm240': ['p8_ee_WW_ecm240'],
        'p8_ee_ZZ_ecm240': ['p8_ee_ZZ_ecm240'],
        'mgp8_ee_zh_ecm240_hbb': ['mgp8_ee_zh_ecm240_hbb'],
        'wzp6_ee_nuenueH_Htautau_ecm240': ['wzp6_ee_nuenueH_Htautau_ecm240'],
        'wzp6_ee_bbH_Htautau_ecm240': ['wzp6_ee_bbH_Htautau_ecm240'],
    }
}

legend = {}
leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
leg.SetTextSize(0.01)

for s in signal_samples:
    mass = s.split('_')[1]
    lifetime = s.split('_')[3]
    legend[s] = f'm_{{stau}} = {mass} GeV, {lifetime}'
    
legend['p8_ee_WW_ecm240'] = 'e^{+}e^{-} #rightarrow WW'
legend['p8_ee_ZZ_ecm240'] = 'e^{+}e^{-} #rightarrow ZZ'
legend['mgp8_ee_zh_ecm240_hbb'] = 'e^{+}e^{-} #rightarrow ZH, H #rightarrow b#bar{b}'
legend['wzp6_ee_nuenueH_Htautau_ecm240'] = 'e^{+}e^{-} #rightarrow #nu#nuH #rightarrow #tau^{+}#tau^{-}'
legend['wzp6_ee_bbH_Htautau_ecm240'] = 'e^{+}e^{-} #rightarrow bbH #rightarrow #tau^{+}#tau^{-}'