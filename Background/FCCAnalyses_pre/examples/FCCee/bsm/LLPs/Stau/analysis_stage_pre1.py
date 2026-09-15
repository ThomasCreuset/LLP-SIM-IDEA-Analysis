from argparse import ArgumentParser

processList = {

    #######################################################
    #               Background 365GeV                     #
    #######################################################
    #                                                     #
    # Test :                                              #
    #  - p8_ee_WW_ecm365                : 0.005           #
    #  - wzp6_ee_tautau_ecm365          : 0.01            #
    #  - p8_ee_tt_ecm365                : 0.01            #
    #  - p8_ee_ZZ_ecm365                : 0.001           #
    #  - wzp6_ee_nuenueH_Htautau_ecm365 : 0.05            #
    #  - wzp6_ee_bbH_Htautau_ecm365     : 0.1             #
    #                                                     #
    # Final :                                             #
    #  - p8_ee_WW_ecm365                : 0.25            #
    #  - wzp6_ee_tautau_ecm365          : 0.5             #
    #  - p8_ee_tt_ecm365                : 1.0             #
    #  - p8_ee_ZZ_ecm365                : 0.03            #
    #  - wzp6_ee_nuenueH_Htautau_ecm365 : 1.0             #
    #  - wzp6_ee_bbH_Htautau_ecm365     : 1.0             #
    #                                                     #
    #######################################################

    #'p8_ee_WW_ecm365': {'fraction': 0.25, 'chunks': 500}, # Cross section: 10.7 / N-files: 1018

    #'wzp6_ee_tautau_ecm365' : {'fraction': 0.5, 'chunks': 50}, # Cross section: 2.017 / N-files: 128

    #'p8_ee_tt_ecm365' : {'fraction': 1.0, 'chunks': 27}, # Cross section: 0.8 / N-files: 27

    #'p8_ee_ZZ_ecm365': {'fraction': 0.03, 'chunks': 300}, # Cross section: 0.6 / N-files: 615

    #'wzp6_ee_nuenueH_Htautau_ecm365': {'fraction': 1.0, 'chunks': 5}, # Cross section: 0.002 / N-files: 12

    #'wzp6_ee_bbH_Htautau_ecm365': {'fraction': 1.0, 'chunks': 10}, # Cross section: 0.001 / N-files: 10

    'p8_ee_WW_ecm240': {'fraction': 0.01, 'chunks': 50},

    'p8_ee_ZZ_ecm240': {'fraction': 0.01, 'chunks': 50},

    'mgp8_ee_zh_ecm240_hbb': {'fraction': 1, 'chunks': 50},

    'wzp6_ee_nuenueH_Htautau_ecm240': {'fraction': 1, 'chunks': 50},

    'wzp6_ee_bbH_Htautau_ecm240': {'fraction': 1, 'chunks': 50},

    } 

prodTag     = "FCCee/winter2023/IDEA/"
    # prodTag     = "FCCee/spring2021/IDEA/"

    # Input/output directories
    # uncomment the input directory you want to use

    # backgrounds are stored here:
# input_dir = '/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA'
    # input_dir = '/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023_training/IDEA/'
    # input_dir = '/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/'

    # input_dir = '/eos/user/s/svashish/FCCAnalyses/examples/FCCee/bsm/LLPs/Stau/edm4hep_output'
outputDir = '/data/dust/user/creusett/SummerSchool/Data/FCCAna/Stage1'

runBatch = True
memory = 3000
nCPUS = 4

# outputDirEos = '/eos/user/s/svashish/FCCAnalyses/examples/FCCee/bsm/LLPs/Stau/output/without_batch/'
# outputDir = '/data/dust/user/creusett/SummerSchool/Data/FCCAna/Stage2'
# n_threads = 4
# for batch
# nCPUS = 2
# eosType = "eosuser"
# batchQueue = 'tomorrow'
# compGroup = 'group_u_FCC.local_gen'


    # Optional: output directory on eos, if specified files will be copied
    # there once the batch job is done, default is empty

    
# Mandatory: Analysis class where the user defines the operations on the dataframe
class RDFanalysis():
    def analysers(df):
        '''
        Generator-level particle properties.
            '''
        cols = set(df.GetColumnNames())
        hasRecoMCLink = False
        
        cols = df.GetColumnNames()
        # For private samples with legacy or EDM4hep MC–Reco associations
        if "_RecoMCLink_from.index" in cols:
            print("INFO: Using legacy RecoMCLink")
            df = df.Alias("MCRecoAssociations0", "_RecoMCLink_from.index")
            df = df.Alias("MCRecoAssociations1", "_RecoMCLink_to.index")

        # For centrally-produced samples with EDM4hep MC–Reco associations
        elif "MCRecoAssociations#0.index" in cols:
            print("INFO: Using EDM4hep MCRecoAssociations")
            df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

        else:
            raise RuntimeError("No MC–Reco association collection found")
        
        hasEFlowTrackStates = (
        "_EFlowTrack_trackStates" in cols or
        "EFlowTrack.trackStates_begin" in cols
        )
        
        if "EFlowTrack_1" in cols:
            df = df.Alias("TrackStates", "EFlowTrack_1")
        elif "_EFlowTrack_trackStates" in cols:
            df = df.Alias("TrackStates", "_EFlowTrack_trackStates")
        elif "EFlowTrack.trackStates_begin" in cols:
            df = df.Alias("TrackStates", "EFlowTrack.trackStates_begin")
        else:
            raise RuntimeError("No Electron index collection found")
        
        if "EFlowTrack" in cols:
            df = df.Alias("TrackData", "EFlowTrack")
        elif "_EFlowTrack" in cols:
            df = df.Alias("TrackData", "_EFlowTrack")
        else:
            raise RuntimeError("No EFlowTrack TrackData collection found")

        if "Electron#0.index" in cols:
            df = df.Alias("ElectronIdx", "Electron#0.index")
        elif "Electron_objIdx.index" in cols:
            df = df.Alias("ElectronIdx", "Electron_objIdx.index")
        else:
            raise RuntimeError("No Electron index collection found")
        
        if "Muon#0.index" in cols:
            df = df.Alias("MuonIdx", "Muon#0.index")
        elif "Muon_objIdx.index" in cols:
            df = df.Alias("MuonIdx", "Muon_objIdx.index")
        else:
            raise RuntimeError("No Muon index collection found")
        
        if "Photon#0.index" in cols:
            df = df.Alias("PhotonIdx", "Photon#0.index")
        elif "Photon_objIdx.index" in cols:
            df = df.Alias("PhotonIdx", "Photon_objIdx.index")   
        else:
            raise RuntimeError("No Photon index collection found")

        df2 = (
            df
            # --------------------------
            # Generator-level particles
            # --------------------------
            # .Alias("Particle1", "_Particle_daughters.index")
            .Define("GenStau", "MCParticle::sel_pdgID(1000015,true)(Particle)")
            .Define("n_GenStau", "MCParticle::get_n(GenStau)")
            .Define("GenStau_vx", "MCParticle::get_vertex_x(GenStau)") 
            .Define("GenStau_vy", "MCParticle::get_vertex_y(GenStau)")
            .Define("GenStau_vz", "MCParticle::get_vertex_z(GenStau)")
            .Define("GenStau_Lxy", "sqrt(GenStau_vx*GenStau_vx + GenStau_vy*GenStau_vy)")
            .Define("GenStau_Lxyz", "sqrt(GenStau_vx*GenStau_vx + GenStau_vy*GenStau_vy + GenStau_vz*GenStau_vz)")
            .Define("GenStau_time", "MCParticle::get_time(GenStau)")
            # Stau daughters
            .Define("GenTau", "MCParticle::sel_pdgID(15,true)(Particle)")
            .Define("GenTau_status", "MCParticle::get_genStatus(GenTau)")
            .Define("GenGravitino", "MCParticle::sel_pdgID(1000049,false)(Particle)")
            .Define("n_GenGravitino", "MCParticle::get_n(GenGravitino)")
            .Define("GenGravitino_status", "MCParticle::get_genStatus(GenGravitino)")
            .Define("GenGravitino_e", "MCParticle::get_e(GenGravitino)")

            # Tau kinematics and vertex
            .Define("GenTau_px", "MCParticle::get_px(GenTau)")
            .Define("GenTau_py", "MCParticle::get_py(GenTau)")
            .Define("GenTau_pz", "MCParticle::get_pz(GenTau)")
            .Define("GenTau_pt", "MCParticle::get_pt(GenTau)")
            .Define("GenTau_eta", "MCParticle::get_eta(GenTau)")
            .Define("GenTau_phi", "MCParticle::get_phi(GenTau)")
            .Define("GenTau_e", "MCParticle::get_e(GenTau)")
            .Define("GenTau_charge", "MCParticle::get_charge(GenTau)")
            .Define("GenTau_vx", "MCParticle::get_vertex_x(GenTau)")
            .Define("GenTau_vy", "MCParticle::get_vertex_y(GenTau)")
            .Define("GenTau_vz", "MCParticle::get_vertex_z(GenTau)")
            .Define("GenTau_time", "MCParticle::get_time(GenTau)")
            .Define("GenTau_cTau",
            "ROOT::VecOps::RVec<float> v; "
            "for (auto t : GenTau_time) v.push_back(t * 2.99792458e10); "
            "return v;")

            .Define("Tau_prod", "MCParticle::get_vertex(GenTau)") 
            .Define("GenTau_mass", "MCParticle::get_mass(GenTau)")  
            .Define("decayLengthTau", "GenTau_vx.size() > 0 ? sqrt(GenTau_vx[0]*GenTau_vx[0] + GenTau_vy[0]*GenTau_vy[0] + GenTau_vz[0]*GenTau_vz[0]) : -1.f")

            # Final-state generator particles (status 1)
            .Define("GenElectron_PID", "MCParticle::sel_pdgID(11, true)(Particle)")
            .Define("FSGenElectron", "MCParticle::sel_genStatus(1)(GenElectron_PID)") 
            .Define("GenMuon_PID", "MCParticle::sel_pdgID(13, true)(Particle)")
            .Define("FSGenMuon", "MCParticle::sel_genStatus(1)(GenMuon_PID)")  
            .Define("GenPhoton_PID", "MCParticle::sel_pdgID(22, false)(Particle)")
            .Define("FSGenPhoton", "MCParticle::sel_genStatus(1)(GenPhoton_PID)") 

            # Kinematics helper for FSGen electrons and positrons
            .Define("n_FSGenElectron", "MCParticle::get_n(FSGenElectron)")
            .Define("FSGenElectron_e", "MCParticle::get_e(FSGenElectron)")
            .Define("FSGenElectron_p", "MCParticle::get_p(FSGenElectron)")
            .Define("FSGenElectron_pt", "MCParticle::get_pt(FSGenElectron)")
            .Define("FSGenElectron_px", "MCParticle::get_px(FSGenElectron)")
            .Define("FSGenElectron_py", "MCParticle::get_py(FSGenElectron)")
            .Define("FSGenElectron_pz", "MCParticle::get_pz(FSGenElectron)")
            .Define("FSGenElectron_eta", "MCParticle::get_eta(FSGenElectron)")
            .Define("FSGenElectron_theta", "MCParticle::get_theta(FSGenElectron)")
            .Define("FSGenElectron_phi", "MCParticle::get_phi(FSGenElectron)")
            .Define("FSGenElectron_charge", "MCParticle::get_charge(FSGenElectron)")
            .Define("FSGenElectron_vx", "MCParticle::get_vertex_x(FSGenElectron)")
            .Define("FSGenElectron_vy", "MCParticle::get_vertex_y(FSGenElectron)")
            .Define("FSGenElectron_vz", "MCParticle::get_vertex_z(FSGenElectron)")
            .Define("FSGenElectron_time", "MCParticle::get_time(FSGenElectron)")

            # Kinematics for FSGen muons and anti-muons
            .Define("n_FSGenMuon", "MCParticle::get_n(FSGenMuon)")
            .Define("FSGenMuon_e", "MCParticle::get_e(FSGenMuon)")
            .Define("FSGenMuon_p", "MCParticle::get_p(FSGenMuon)")
            .Define("FSGenMuon_pt", "MCParticle::get_pt(FSGenMuon)")
            .Define("FSGenMuon_px", "MCParticle::get_px(FSGenMuon)")
            .Define("FSGenMuon_py", "MCParticle::get_py(FSGenMuon)")
            .Define("FSGenMuon_pz", "MCParticle::get_pz(FSGenMuon)")
            .Define("FSGenMuon_eta", "MCParticle::get_eta(FSGenMuon)")
            .Define("FSGenMuon_theta", "MCParticle::get_theta(FSGenMuon)")
            .Define("FSGenMuon_phi", "MCParticle::get_phi(FSGenMuon)")
            .Define("FSGenMuon_charge", "MCParticle::get_charge(FSGenMuon)")
            .Define("FSGenMuon_vx", "MCParticle::get_vertex_x(FSGenMuon)")
            .Define("FSGenMuon_vy", "MCParticle::get_vertex_y(FSGenMuon)")
            .Define("FSGenMuon_vz", "MCParticle::get_vertex_z(FSGenMuon)")
            .Define("FSGenMuon_time", "MCParticle::get_time(FSGenMuon)")
        
            #Kinematics for FSGen photons
            .Define("n_FSGenPhoton", "MCParticle::get_n(FSGenPhoton)")
            .Define("FSGenPhoton_e", "MCParticle::get_e(FSGenPhoton)")
            .Define("FSGenPhoton_p", "MCParticle::get_p(FSGenPhoton)")
            .Define("FSGenPhoton_pt", "MCParticle::get_pt(FSGenPhoton)")
            .Define("FSGenPhoton_px", "MCParticle::get_px(FSGenPhoton)")
            .Define("FSGenPhoton_py", "MCParticle::get_py(FSGenPhoton)")
            .Define("FSGenPhoton_pz", "MCParticle::get_pz(FSGenPhoton)")
            .Define("FSGenPhoton_eta", "MCParticle::get_eta(FSGenPhoton)")
            .Define("FSGenPhoton_theta", "MCParticle::get_theta(FSGenPhoton)")
            .Define("FSGenPhoton_phi", "MCParticle::get_phi(FSGenPhoton)")

            # custon neutrino PID to include nu_e, nu_mu, nu_tau
            .Define("GenNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(16, true)(Particle)")
            .Define("FSGenNeutrino", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenNeutrino_PID)") # gen status==1 means final state particle (FS)
            .Define("n_FSGenNeutrino", "FCCAnalyses::MCParticle::get_n(FSGenNeutrino)")
            .Define("FSGenNeutrino_e", "FCCAnalyses::MCParticle::get_e(FSGenNeutrino)")
            .Define("FSGenNeutrino_p", "FCCAnalyses::MCParticle::get_p(FSGenNeutrino)")
            .Define("FSGenNeutrino_pt", "FCCAnalyses::MCParticle::get_pt(FSGenNeutrino)")
            .Define("FSGenNeutrino_px", "FCCAnalyses::MCParticle::get_px(FSGenNeutrino)")
            .Define("FSGenNeutrino_py", "FCCAnalyses::MCParticle::get_py(FSGenNeutrino)")
            .Define("FSGenNeutrino_pz", "FCCAnalyses::MCParticle::get_pz(FSGenNeutrino)")
            .Define("FSGenNeutrino_eta", "FCCAnalyses::MCParticle::get_eta(FSGenNeutrino)")
            .Define("FSGenNeutrino_theta", "FCCAnalyses::MCParticle::get_theta(FSGenNeutrino)")
            .Define("FSGenNeutrino_phi", "FCCAnalyses::MCParticle::get_phi(FSGenNeutrino)")
            .Define("FSGenNeutrino_charge", "FCCAnalyses::MCParticle::get_charge(FSGenNeutrino)")

            # Hit information for the tracks 
            .Define("RecoForTracks", "ReconstructedParticle2Track::recoParticleIndices_forTracks(TrackStates,ReconstructedParticles)")

            .Define("RecoParticles_phi", "ReconstructedParticle2Track::getRP2TRK_phi(ReconstructedParticles, TrackStates)")
            .Define("RecoParticles_d0", "ReconstructedParticle2Track::getRP2TRK_D0(ReconstructedParticles, TrackStates)")
            .Define("RecoParticles_theta", "ReconstructedParticle2Track::getRP2TRK_theta(ReconstructedParticles, TrackStates)")
            .Define("RecoParticles_p", "ReconstructedParticle2Track::getRP2TRK_mom(ReconstructedParticles, TrackStates)")
            .Define("RecoParticles_pt", "ReconstructedParticle2Track::getRP2TRK_pt(ReconstructedParticles, TrackStates)")
            
            .Define("RecoIndices", "Utils::index_range(ReconstructedParticles)")
            .Define("RecoParticles_hitsOnTrack","VertexingUtils::getHitsOnTrack(" \
            "RecoIndices, ReconstructedParticles, Particle, MCRecoAssociations0, MCRecoAssociations1)")
            .Define("RecoParticles_hitPatterns","VertexingUtils::toHitPatterns(RecoParticles_hitsOnTrack)")
            .Define("RecoParticles_firstHitLoc","VertexingUtils::getFirstHits(RecoParticles_hitPatterns)")
            .Define("RecoParticles_lastHitLoc","VertexingUtils::getLastHits(RecoParticles_hitPatterns)")
            .Define("RecoParticles_nHits","VertexingUtils::getNHits(RecoParticles_hitPatterns)")
            .Define("RecoParticles_nDriftChamberHits","VertexingUtils::getNDCHits(RecoParticles_hitPatterns)")
            # for the kink vertices, let's ask for at least 10 hits on track, of which at least 8 in the drift chamber. 
            .Define("RecoParticles_passNhits_forKV","VertexingUtils::passHitCount(RecoParticles_hitPatterns, 10,8)")


            # --------------------------
            # Reconstructed particles
            # --------------------------
            # MC Primary Vertex
            # .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )

            # Tracks
            .Define("n_RecoTracks",  "ReconstructedParticle2Track::getTK_n(TrackStates)")
            .Define("AcceptedTracks", "VertexFitterSimple::getSelectedTracks(TrackStates, 2.0)")
            .Define("n_AcceptedTracks",  "ReconstructedParticle2Track::getTK_n(AcceptedTracks)")
            .Define("TOF_AcceptedTracks", "ReconstructedTrack::tracks_TOF(AcceptedTracks, TrackStates, TrackData, TrackerHits)")
            
            # Select the tracks that are reconstructed  as primaries, so it removes all long lived decay tracks
            # this would be our stau tracks
            .Define("RecoedPrimaryTracks", "VertexFitterSimple::get_PrimaryTracks( AcceptedTracks, true, 4.5, 20e-3, 300, 0., 0., 0.)")

            # location of the primary tracks in the TrackStates collection
            .Define("TrackStateIndexOfPrimaryTracks", "ReconstructedTrack::get_indices(RecoedPrimaryTracks, TrackStates)")
            # location of the track states in the reco particles collection
            .Define("RecoParticleIndexOfAllTracks", "ReconstructedParticle2Track::recoParticleIndices_forTracks(TrackStates,ReconstructedParticles)")
            # location of the primary tracks in the reco particles collection
            .Define("RecoParticleIndexOfPrimaryTracks", "Utils::sel_byIndex(TrackStateIndexOfPrimaryTracks, RecoParticleIndexOfAllTracks)")
            
            .Define("RecoedPrimaryTracks_phi", "Utils::sel_byIndex(RecoParticleIndexOfPrimaryTracks, RecoParticles_phi)")
            .Define("RecoedPrimaryTracks_d0", "Utils::sel_byIndex(RecoParticleIndexOfPrimaryTracks, RecoParticles_d0)")
            .Define("RecoedPrimaryTracks_theta", "Utils::sel_byIndex(RecoParticleIndexOfPrimaryTracks, RecoParticles_theta)")
            .Define("RecoedPrimaryTracks_p", "Utils::sel_byIndex(RecoParticleIndexOfPrimaryTracks, RecoParticles_p)")
            .Define("RecoedPrimaryTracks_pt", "Utils::sel_byIndex(RecoParticleIndexOfPrimaryTracks, RecoParticles_pt)")
            .Define("n_RecoedPrimaryTracks", "ReconstructedParticle2Track::getTK_n(RecoedPrimaryTracks)")
            .Define("TOF_RecoedPrimaryTracks", "ReconstructedTrack::tracks_TOF(RecoedPrimaryTracks, TrackStates, TrackData, TrackerHits)")


            .Define("RecoedPrimaryTracksIndices", "Utils::index_range(RecoedPrimaryTracks)")
            .Define("PrimaryIndices", "Utils::index_range(ReconstructedParticles)")
            .Define("RecoedPrimaryTracks_hitsOnTrack","VertexingUtils::getHitsOnTrack(" \
            "RecoParticleIndexOfPrimaryTracks, ReconstructedParticles, Particle, MCRecoAssociations0, MCRecoAssociations1)")
            .Define("RecoedPrimaryTracks_hitPatterns","VertexingUtils::toHitPatterns(RecoedPrimaryTracks_hitsOnTrack)")
            .Define("RecoedPrimaryTracks_firstHitLoc","VertexingUtils::getFirstHits(RecoedPrimaryTracks_hitPatterns)")
            .Define("RecoedPrimaryTracks_lastHitLoc","VertexingUtils::getLastHits(RecoedPrimaryTracks_hitPatterns)")
            .Define("RecoedPrimaryTrack_mass", "ReconstructedTrack::getEscapingTrackMass(RecoedPrimaryTracks_pt, TOF_RecoedPrimaryTracks, RecoedPrimaryTracks_theta, 2.25, 2.5)")
            .Define("Beta_RecoedPrimaryTracks", "ReconstructedTrack::getPrimaryTrackBeta(TOF_RecoedPrimaryTracks, RecoedPrimaryTracks_theta, 2.25, 2.5)")
            # .Define("Recoed_Primary_D0sig", "ReconstructedParticle2Track::getRP2TRK_D0_sig(ReconstructedParticles, RecoedPrimaryTracks)")

            .Define("EscapingTrackIndices","Utils::selByPredicate<TVector3>(ReconstructedParticle::inTimingAcceptance)(RecoedPrimaryTracksIndices, RecoedPrimaryTracks_lastHitLoc)")
            .Define("n_EscapingTracks", "EscapingTrackIndices.size()")
            .Define("TOF_EscapingTracks","Utils::sel_byIndex(EscapingTrackIndices, TOF_RecoedPrimaryTracks)")

            .Define("EscapingTracks_pt","Utils::sel_byIndex(EscapingTrackIndices, RecoedPrimaryTracks_pt)")
            .Define("EscapingTracks_p","Utils::sel_byIndex(EscapingTrackIndices, RecoedPrimaryTracks_p)")  
            .Define("EscapingTracks_theta","Utils::sel_byIndex(EscapingTrackIndices, RecoedPrimaryTracks_theta)")
            .Define("EscapingTracks_phi","Utils::sel_byIndex(EscapingTrackIndices, RecoedPrimaryTracks_phi)")
            .Define("EscapingTracks_mass","Utils::sel_byIndex(EscapingTrackIndices, RecoedPrimaryTrack_mass)")  


            # the final primary vertex : final/refined fit
            .Define("PrimaryVertexObject",   "VertexFitterSimple::VertexFitter_Tk ( 1, RecoedPrimaryTracks, true, 4.5, 20e-3, 300 ) ") 
            .Define("PrimaryVertex",   "VertexingUtils::get_VertexData( PrimaryVertexObject )")
            .Define("PrimaryVertex_ntracks", "FCCAnalyses::VertexingUtils::get_VertexNtrk( PrimaryVertexObject )")
            # .Filter("PrimaryVertex_ntracks > 2")

            .Define("sel_tracks", "VertexFitterSimple::get_NonPrimaryTracks(AcceptedTracks, RecoedPrimaryTracks)") # 100 events/sec
            # .Define("sel_tracks_D0_DV", "ReconstructedParticle2Track::getRP2TRK_D0(ReconstructedParticles, sel_tracks)")
            # .Define("sel_tracks_Z0_DV", "ReconstructedParticle2Track::getRP2TRK_Z0(ReconstructedParticles, sel_tracks)")
            .Define("n_nonprimary_tracks", "ReconstructedParticle2Track::getTK_n(sel_tracks)")
            # .Define('sel_tracks_pt_DV', 'ReconstructedParticle2Track::getRP2TRK_mom(ReconstructedParticles ,sel_tracks)') 

            # KINK FINDER FROM SELECTED TRACKS - TARGETTING 1 PRONG TAU DECAYS 
            .Define("RecoedPrimaryTracks_charge", "ReconstructedParticle2Track::getRP2TRK_charge(ReconstructedParticles, RecoedPrimaryTracks)")
            .Define("sel_tracks_charge", "ReconstructedParticle2Track::getRP2TRK_charge(ReconstructedParticles, sel_tracks)")
            # old way:
            .Define("KinkCandidates","ReconstructedParticle2Track::findKink_candidate(ReconstructedParticles, RecoedPrimaryTracks, sel_tracks, TrackStates, RecoParticles_passNhits_forKV)")
            .Define("nKinkVertices_old", "KinkCandidates.size()")
            # this gives us the vertex object:
            .Define("KinkCandidates_VertexObject","ReconstructedParticle2Track::KinkCandidate_VertexObject(ReconstructedParticles, RecoedPrimaryTracks, sel_tracks, TrackStates, RecoParticles_passNhits_forKV )")
            .Define("nKinkVertices", "KinkCandidates_VertexObject.size()")

            .Define("KinkCandidates_passInnerHitVeto","VertexingUtils::passInnerHitVeto(KinkCandidates_VertexObject, RecoParticles_hitPatterns, RecoForTracks, true,true,false,false)")            
            .Define("nKinkCandidates_passVeto", "ROOT::VecOps::Sum(KinkCandidates_passInnerHitVeto)")
            .Define("KinkCandidates_VertexObject_passVeto", "KinkCandidates_VertexObject[KinkCandidates_passInnerHitVeto]")
            # number of tracks at the kink vertex (should be 2 for 1 prong tau decays)
            .Define("KinkVertex_ntracks", "VertexingUtils::get_VertexNtrk(KinkCandidates_VertexObject_passVeto)") 
            # invariant mass of a two track vertex   # CAUTION: m1 -> first track; m2 -> second track
            .Define("KinkVertex_invMass", "VertexingUtils::get_kink_mass(KinkCandidates_VertexObject_passVeto)")
            .Define("KinkVertex_SV" , "VertexingUtils::get_position_SV(KinkCandidates_VertexObject_passVeto)")  
            # vector of distances of all reconstructed SV from PV (in mm in xy plane)
            .Define("KinkVertex_dxy", "VertexingUtils::get_dxy_SV(KinkCandidates_VertexObject_passVeto, PrimaryVertexObject)")
            # vector of distances of all reconstructed SV from PV (in mm in 3D)
            .Define("KinkVertex_d3d", "VertexingUtils::get_d3d_SV(KinkCandidates_VertexObject_passVeto, PrimaryVertexObject)")
            .Define("KinkCosAngle", "VertexingUtils::get_PV2V0angles(KinkCandidates_VertexObject_passVeto, PrimaryVertexObject)") 
            .Define("KinkAngle",
                    "ROOT::VecOps::RVec<float> v; "
                    "for (auto cosAngle : KinkCosAngle) { "
                    "    if (cosAngle >= -1.0 && cosAngle <= 1.0) "
                    "        v.push_back(TMath::ACos(cosAngle)*180.0/TMath::Pi()); "
                    "} "
                    "return v;")
            # DISPLACED VERTICES FROM SELECTED TRACKS- TARGETTING 3 PRONG TAU DECAY
            .Filter("sel_tracks.size()>0")
            .Define("TOF_sel_tracks", "ReconstructedTrack::tracks_TOF(sel_tracks, TrackStates, TrackData, TrackerHits)")
            # find the DVs from the non-primary tracks
            .Define("Displaced_Vertex", "VertexFinderLCFIPlus::get_SV_event(sel_tracks, TrackStates, PrimaryVertexObject, true, 9., 40., 5.)")
            # number of displaced vertices found
            .Define('nDisplaced_Vertices', 'VertexingUtils::get_n_SV(Displaced_Vertex)')
            # number of tracks from the DVs
            .Define('nTracks_DV', 'VertexingUtils::get_VertexNtrk(Displaced_Vertex)') 
            # momentum of the selected tracks`  `
            # Hit pattern check- only take displaced vertices which fail this criteria (if DV passes hit criteria it is actually a KV)
            # require only outgoing tracks, no incoming tracks - veto them
            .Define("DisplacedVertices_failInnerHitVeto","VertexingUtils::passInnerHitVeto(Displaced_Vertex, RecoParticles_hitPatterns, RecoForTracks, false, true, true, false)")
            # .Define("Displaced_VertexObject_failVeto", "Displaced_Vertex[!DisplacedVertices_passInnerHitVeto]")
            # fail mask = logical NOT of pass mask
            # .Define("DisplacedVertices_failInnerHitVeto", "!DisplacedVertices_passInnerHitVeto")
            # get only the vertices that failed the veto
            .Define("Displaced_VertexObject_failVeto", "Displaced_Vertex[DisplacedVertices_failInnerHitVeto]")
            # count how many failed- sum of bool
            .Define("nDisplacedVertices_failInnerHitVeto", "ROOT::VecOps::Sum(DisplacedVertices_failInnerHitVeto)")   
            .Define('nTracks_DV_failInnerHitVeto', 'VertexingUtils::get_VertexNtrk(Displaced_VertexObject_failVeto)')
           # invariant mass at the DVs (assuming the tracks to be pions)
            .Define('invMass_seltracks_DVs', 'VertexingUtils::get_invM(Displaced_VertexObject_failVeto)')
            # get the chi2 distributions of the DVs from selected tracks - to check if tracks originate from the same physical point
            .Define("DV_evt_seltracks_chi2",    "VertexingUtils::get_chi2_SV(Displaced_VertexObject_failVeto)")
            .Define("DV_evt_seltracks_normchi2","VertexingUtils::get_norm_chi2_SV(Displaced_VertexObject_failVeto)") # DV chi2 (normalised)

            # # get the decay radius and full 3D distance of all the DVs from selected tracks
            .Define("Reco_seltracks_DVs_Lxy","VertexingUtils::get_dxy_SV(Displaced_VertexObject_failVeto, PrimaryVertexObject)")
            .Define("Reco_seltracks_DVs_Lxyz","VertexingUtils::get_d3d_SV(Displaced_VertexObject_failVeto, PrimaryVertexObject)")

            # .Define("RecoTauTracks", "VertexingUtils::get_tracksInJets(Jet, _EFlowTrack_trackStates, Jet_to_Track_indices, 0)")
            # .Define("RecoTauDecayVertexObject", "VertexFitterSimple::VertexFitter_Tk(2, RecoTauTracks)")
            # .Define("RecoTauDecayVertex", "VertexingUtils::get_VertexData(RecoTauDecayVertexObject)")
            # .Define("RecoTau_Lxy", "sqrt(RecoTauDecayVertex.position.x*RecoTauDecayVertex.position.x + RecoTauDecayVertex.position.y*RecoTauDecayVertex.position.y)")
            # .Define("RecoTau_Lxyz", "sqrt(RecoTauDecayVertex.position.x*RecoTauDecayVertex.position.x + RecoTauDecayVertex.position.y*RecoTauDecayVertex.position.y + RecoTauDecayVertex.position.z*RecoTauDecayVertex.position.z)")

            # # JETS
            .Define("n_RecoJets", "ReconstructedParticle::get_n(Jet)")
            .Define("RecoJet_e",      "ReconstructedParticle::get_e(Jet)")
            .Define("RecoJet_p",      "ReconstructedParticle::get_p(Jet)") 
            .Define("RecoJet_pt",      "ReconstructedParticle::get_pt(Jet)")
            .Define("RecoJet_px",      "ReconstructedParticle::get_px(Jet)")
            .Define("RecoJet_py",      "ReconstructedParticle::get_py(Jet)")
            .Define("RecoJet_pz",      "ReconstructedParticle::get_pz(Jet)")
		    .Define("RecoJet_eta",     "ReconstructedParticle::get_eta(Jet)") 
            .Define("RecoJet_theta",   "ReconstructedParticle::get_theta(Jet)")
		    .Define("RecoJet_phi",     "ReconstructedParticle::get_phi(Jet)") 
            .Define("RecoJet_charge",  "ReconstructedParticle::get_charge(Jet)")
            .Define("RecoJet_mvis",     "ReconstructedParticle::get_P4vis(Jet).M()")
            .Define("RecoJetTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(Jet,TrackStates))")
            .Define("RecoJetTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(Jet,TrackStates))")
            .Define("RecoJetTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(Jet,TrackStates))") 
            .Define("RecoJetTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(Jet,TrackStates))")
            .Define("RecoJetTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(Jet,TrackStates)") 
            .Define("RecoJetTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(Jet,TrackStates)")

            # Electrons
            .Alias("Electron0", "ElectronIdx")
            .Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)") 
            .Define("n_RecoElectrons", "ReconstructedParticle::get_n(RecoElectrons)")
            .Define("RecoElectrons_p", "ReconstructedParticle::get_p(RecoElectrons)")
            .Define("RecoElectrons_px", "ReconstructedParticle::get_px(RecoElectrons)")
            .Define("RecoElectrons_py", "ReconstructedParticle::get_py(RecoElectrons)")
            .Define("RecoElectrons_pz", "ReconstructedParticle::get_pz(RecoElectrons)")
            .Define("RecoElectrons_pt", "ReconstructedParticle::get_pt(RecoElectrons)")
            .Define("RecoElectrons_eta", "ReconstructedParticle::get_eta(RecoElectrons)")
            .Define("RecoElectrons_phi", "ReconstructedParticle::get_phi(RecoElectrons)")
            .Define("RecoElectrons_e", "ReconstructedParticle::get_e(RecoElectrons)")
            .Define("RecoElectrons_charge", "ReconstructedParticle::get_charge(RecoElectrons)")
            .Define("RecoElectrons_theta", "ReconstructedParticle::get_theta(RecoElectrons)")
            # invariant mass information
            # .Define("Reco_ee_energy", "if ((n_RecoElectrons>1) && (RecoElectrons_charge.at(0) != RecoElectrons_charge.at(1))) return (RecoElectrons_e.at(0) + RecoElectrons_e.at(1)); else return float(-1.);")
            # .Define("Reco_ee_px", "if ((n_RecoElectrons>1) && (RecoElectrons_charge.at(0) != RecoElectrons_charge.at(1))) return (RecoElectrons_px.at(0) + RecoElectrons_px.at(1)); else return float(-1.);")
            # .Define("Reco_ee_py", "if ((n_RecoElectrons>1) && (RecoElectrons_charge.at(0) != RecoElectrons_charge.at(1))) return (RecoElectrons_py.at(0) + RecoElectrons_py.at(1)); else return float(-1.);")
            # .Define("Reco_ee_pz", "if ((n_RecoElectrons>1) && (RecoElectrons_charge.at(0) != RecoElectrons_charge.at(1))) return (RecoElectrons_pz.at(0) + RecoElectrons_pz.at(1)); else return float(-1.);")
            # .Define("Reco_ee_invMass", 
            #     "float invMass = -1.;"
            #     "if (n_RecoElectrons > 1 && RecoElectrons_charge[0] != RecoElectrons_charge[1]) {"
            #     "   float E  = RecoElectrons_e[0]  + RecoElectrons_e[1];"
            #     "   float px = RecoElectrons_px[0] + RecoElectrons_px[1];"
            #     "   float py = RecoElectrons_py[0] + RecoElectrons_py[1];"
            #     "   float pz = RecoElectrons_pz[0] + RecoElectrons_pz[1];"
            #     "   invMass = sqrt(E*E - px*px - py*py - pz*pz);"
            #     "}"
            #     "return invMass;"
            # )

            # Muons
            .Alias("Muon0", "MuonIdx")
            .Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)") 
            .Define("n_RecoMuons", "ReconstructedParticle::get_n(RecoMuons)")
            .Define("RecoMuons_p", "ReconstructedParticle::get_p(RecoMuons)")
            .Define("RecoMuons_px", "ReconstructedParticle::get_px(RecoMuons)")
            .Define("RecoMuons_py", "ReconstructedParticle::get_py(RecoMuons)")
            .Define("RecoMuons_pz", "ReconstructedParticle::get_pz(RecoMuons)")
            .Define("RecoMuons_pt", "ReconstructedParticle::get_pt(RecoMuons)")
            .Define("RecoMuons_eta", "ReconstructedParticle::get_eta(RecoMuons)")
            .Define("RecoMuons_phi", "ReconstructedParticle::get_phi(RecoMuons)")
            .Define("RecoMuons_e", "ReconstructedParticle::get_e(RecoMuons)")
            .Define("RecoMuons_charge", "ReconstructedParticle::get_charge(RecoMuons)")
            .Define("RecoMuons_theta", "ReconstructedParticle::get_theta(RecoMuons)")
            # invariant mass information
            # .Define("Reco_mumu_energy", "if ((n_RecoMuons>1) && (RecoMuons_charge.at(0) != RecoMuons_charge.at(1))) return (RecoMuons_e.at(0) + RecoMuons_e.at(1)); else return float(-1.);")
            # .Define("Reco_mumu_px", "if ((n_RecoMuons>1) && (RecoMuons_charge.at(0) != RecoMuons_charge.at(1))) return (RecoMuons_px.at(0) + RecoMuons_px.at(1)); else return float(-1.);")
            # .Define("Reco_mumu_py", "if ((n_RecoMuons>1) && (RecoMuons_charge.at(0) != RecoMuons_charge.at(1))) return (RecoMuons_py.at(0) + RecoMuons_py.at(1)); else return float(-1.);")
            # .Define("Reco_mumu_pz", "if ((n_RecoMuons>1) && (RecoMuons_charge.at(0) != RecoMuons_charge.at(1))) return (RecoMuons_pz.at(0) + RecoMuons_pz.at(1)); else return float(-1.);")
            # .Define("Reco_mumu_invMass", 
            #     "float invMass = -1.;"
            #     "if (n_RecoMuons > 1 && RecoMuons_charge[0] != RecoMuons_charge[1]) {"
            #     "   float E  = RecoMuons_e[0]  + RecoMuons_e[1];"
            #     "   float px = RecoMuons_px[0] + RecoMuons_px[1];"
            #     "   float py = RecoMuons_py[0] + RecoMuons_py[1];"
            #     "   float pz = RecoMuons_pz[0] + RecoMuons_pz[1];"
            #     "   invMass = sqrt(E*E - px*px - py*py - pz*pz);"
            #     "}"
            #     "return invMass;"
            # )

            # # only ZZ -> llll events would have this overlap
            # .Define("muon_electron_overlap", "return (Reco_mumu_invMass>0 && Reco_ee_invMass>0);")
            # .Define("ZZ_veto", "return !(Reco_mumu_invMass>80 && Reco_mumu_invMass<100) && !(Reco_ee_invMass>80 && Reco_ee_invMass<100);")

            # PHOTONS
            .Alias("Photon0", "PhotonIdx") 
            .Define("RecoPhotons",  "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
            .Define("n_RecoPhotons",  "ReconstructedParticle::get_n(RecoPhotons)") 
            .Define("RecoPhoton_e",      "ReconstructedParticle::get_e(RecoPhotons)")
            .Define("RecoPhoton_p",      "ReconstructedParticle::get_p(RecoPhotons)")
            .Define("RecoPhoton_pt",      "ReconstructedParticle::get_pt(RecoPhotons)")
            .Define("RecoPhoton_px",      "ReconstructedParticle::get_px(RecoPhotons)")
            .Define("RecoPhoton_py",      "ReconstructedParticle::get_py(RecoPhotons)")
            .Define("RecoPhoton_pz",      "ReconstructedParticle::get_pz(RecoPhotons)")
		    .Define("RecoPhoton_eta",     "ReconstructedParticle::get_eta(RecoPhotons)")
            .Define("RecoPhoton_theta",   "ReconstructedParticle::get_theta(RecoPhotons)")
		    .Define("RecoPhoton_phi",     "ReconstructedParticle::get_phi(RecoPhotons)") 
            .Define("RecoPhoton_charge",  "ReconstructedParticle::get_charge(RecoPhotons)")

            # MET
            .Define("hasMissingET", "MissingET.size() > 0")
            .Define("RecoMissingEnergy_e", "hasMissingET ? ReconstructedParticle::get_e(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_p",  "hasMissingET ? ReconstructedParticle::get_p(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_pt",  "hasMissingET ? ReconstructedParticle::get_pt(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_px", "hasMissingET ? ReconstructedParticle::get_px(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_py", "hasMissingET ? ReconstructedParticle::get_py(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_pz", "hasMissingET ? ReconstructedParticle::get_pz(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_eta", "hasMissingET ? ReconstructedParticle::get_eta(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_theta",  "hasMissingET ? ReconstructedParticle::get_theta(MissingET)[0] : 0.f")
            .Define("RecoMissingEnergy_phi",  "hasMissingET ? ReconstructedParticle::get_phi(MissingET)[0] : 0.f")

            # Visible energy
            # need to look at what lepton does it pick up- is it accidentally a ISR or FSR electron
            # .Define("RecoVisibleEnergy",
            #     "float visE = 0.;"
            #     "for (size_t i = 0; i < n_RecoJets; i++) { visE += RecoJet_e[i]; }"
            #     "for (size_t i = 0; i < n_RecoElectrons; i++) { visE += RecoElectrons_e[i]; }"
            #     "for (size_t i = 0; i < n_RecoMuons; i++) { visE += RecoMuons_e[i]; }"
            #     "return visE;"
            # )
            # .Define("RecoMissingEnergy3D", "240. - RecoVisibleEnergy")

            # PV2V0 angles
            .Define("PV2V0Cos", "VertexingUtils::get_PV2V0angles(Displaced_VertexObject_failVeto, PrimaryVertexObject)")
        )
        return df2

# Mandatory: output function
    def output():
        '''
        Output branches to be saved in the final ROOT file.
        '''
        branch_list = [
            # Gen-level stau
            # "debug_xpos",
            # "debug_ypos",
            # "debug_zpos",
            # "GenStau",
            # "n_GenStau",
            # "GenStau_status",
            # "GenStau_vx",
            # "GenStau_vy",
            # "GenStau_vz",
            # "GenStau_Lxy",
            # "GenStau_e",
            # "GenStau_phi",
            # "GenStau_Lxyz",

            # # Stau daughters
            # "GenTau",
            # "GenGravitino",
            # "n_GenGravitino",
            # "GenGravitino_status",
            # "GenGravitino_e",

            # Tau kinematics
            # "GenTau_e",
            # "GenTau_pt",
            # "GenTau_eta",
            # "GenTau_phi",
            # "GenTau_px",
            # "GenTau_py",
            # "GenTau_pz",
            # "GenTau_charge",

            # Tau vertex
            # "GenTau_vx",
            # "GenTau_vy",
            # "GenTau_vz",
            # "decayLengthTau",

            # Final-state electrons
            # "FSGenElectron",
            # "n_FSGenElectron",
            # "FSGenElectron_e",
            # "FSGenElectron_p",
            # "FSGenElectron_pt",
            # "FSGenElectron_px",
            # "FSGenElectron_py",
            # "FSGenElectron_pz",
            # "FSGenElectron_eta",
            # "FSGenElectron_theta",
            # "FSGenElectron_phi",
            # "FSGenElectron_charge",
            # "FSGenElectron_vx",
            # "FSGenElectron_vy",
            # "FSGenElectron_vz",

            # Final-state muons
            # "FSGenMuon",
            # "n_FSGenMuon",
            # "FSGenMuon_e",
            # "FSGenMuon_p",
            # "FSGenMuon_pt",
            # "FSGenMuon_px",
            # "FSGenMuon_py",
            # "FSGenMuon_pz",
            # "FSGenMuon_eta",
            # "FSGenMuon_theta",
            # "FSGenMuon_phi",
            # "FSGenMuon_charge",
            # "FSGenMuon_vx",
            # "FSGenMuon_vy",
            # "FSGenMuon_vz",

            # Final-state photons
            # "FSGenPhoton",
            # "n_FSGenPhoton",
            # "FSGenPhoton_e",
            # "FSGenPhoton_p",
            # "FSGenPhoton_pt",
            # "FSGenPhoton_px",
            # "FSGenPhoton_py",
            # "FSGenPhoton_pz",
            # "FSGenPhoton_eta",
            # "FSGenPhoton_theta",
            # "FSGenPhoton_phi",

            # Neutrinos
            # "FSGenNeutrino",
            # "n_FSGenNeutrino",
            # "FSGenNeutrino_e",
            # "FSGenNeutrino_p",
            # "FSGenNeutrino_pt",
            # "FSGenNeutrino_px",
            # "FSGenNeutrino_py",
            # "FSGenNeutrino_pz",
            # "FSGenNeutrino_eta",
            # "FSGenNeutrino_theta",
            # "FSGenNeutrino_phi",
            # "FSGenNeutrino_charge",

            # Track information
            "n_RecoedPrimaryTracks", 
            "n_AcceptedTracks",
            "TOF_AcceptedTracks",
            "PrimaryVertex_ntracks",
            "n_RecoTracks",
            # "sel_tracks_pt_DV",
            # "sel_tracks_D0_DV",
            # "sel_tracks_Z0_DV",
            "n_nonprimary_tracks",
            
            ## DV information
            "nDisplaced_Vertices",
            "nTracks_DV",
            "nDisplacedVertices_failInnerHitVeto",

            "nTracks_DV_failInnerHitVeto",
            "invMass_seltracks_DVs",
            "DV_evt_seltracks_chi2",
            "DV_evt_seltracks_normchi2",
            "Reco_seltracks_DVs_Lxy",
            "Reco_seltracks_DVs_Lxyz",

            # Hit pattern information
            "RecoParticles_firstHitLoc",
            "RecoParticles_lastHitLoc",
            "RecoParticles_nHits",
            "RecoParticles_nDriftChamberHits",

            # Reco Jets
            # "n_RecoJets",
            # "RecoJet_e",
            # "RecoJet_p",
            # "RecoJet_pt",
            # "RecoJet_px",
            # "RecoJet_py",
            # "RecoJet_pz",
            # "RecoJet_eta",
            # "RecoJet_theta",
            # "RecoJet_phi",
            # "RecoJet_charge",
            # "RecoJet_mvis",
            # "RecoJetTrack_absD0",
            # "RecoJetTrack_absZ0",
            # "RecoJetTrack_absD0sig",
            # "RecoJetTrack_absZ0sig",
            # "RecoJetTrack_D0cov",
            # "RecoJetTrack_Z0cov",

            # Reco Electrons
            "RecoElectrons",
            "n_RecoElectrons",
            "RecoElectrons_e",
            "RecoElectrons_p",
            "RecoElectrons_pt",
            "RecoElectrons_px",
            "RecoElectrons_py",
            "RecoElectrons_pz",
            "RecoElectrons_eta",
            "RecoElectrons_theta",
            "RecoElectrons_phi",
            "RecoElectrons_charge",
            # "Reco_ee_energy",
            # "Reco_ee_px",
            # "Reco_ee_py",
            # "Reco_ee_pz",
            # "Reco_ee_invMass",

            # Reco Muons
            "RecoMuons",
            "n_RecoMuons",
            "RecoMuons_e",
            "RecoMuons_p",
            "RecoMuons_pt",
            "RecoMuons_px",
            "RecoMuons_py",
            "RecoMuons_pz",
            "RecoMuons_eta",
            "RecoMuons_theta",
            "RecoMuons_phi",
            "RecoMuons_charge",
            # "Reco_mumu_energy",
            # "Reco_mumu_px",
            # "Reco_mumu_py",
            # "Reco_mumu_pz",
            # "Reco_mumu_invMass",
            # "muon_electron_overlap",

            # Reco Photons
            # "RecoPhotons",
            # "n_RecoPhotons",
            # "RecoPhoton_e",
            # "RecoPhoton_p",
            # "RecoPhoton_pt",
            # "RecoPhoton_px",
            # "RecoPhoton_py",
            # "RecoPhoton_pz",
            # "RecoPhoton_eta",
            # "RecoPhoton_theta",
            # "RecoPhoton_phi",
            # "RecoPhoton_charge",

            # MET
            # "RecoMissingEnergy_e",
            # "RecoMissingEnergy_p",
            # "RecoMissingEnergy_pt",
            # "RecoMissingEnergy_px",
            # "RecoMissingEnergy_py",
            # "RecoMissingEnergy_pz",
            # "RecoMissingEnergy_eta",
            # "RecoMissingEnergy_theta",
            # "RecoMissingEnergy_phi",

            # Time variables
            "GenStau_time",
            "GenTau_time",
            "FSGenElectron_time",
            "FSGenMuon_time",
            "GenTau_status",
            "GenTau_cTau",
            # "GenStau_theta",
            # "GenTau_theta",

            # "RecoVisibleEnergy",
            # "RecoMissingEnergy3D",
            "RecoedPrimaryTracks_charge",
            "sel_tracks_charge",
            "RecoedPrimaryTracks_d0",
            "RecoedPrimaryTracks_phi",
            "RecoedPrimaryTracks_theta",
            "RecoedPrimaryTracks_p",
            "RecoedPrimaryTracks_pt",
            # "GenStau_daughters",
            # "GenTau_daughters",
            
            ## Kinked candidates :
            "KinkCandidates",
            "KinkCandidates_passInnerHitVeto",
            "nKinkCandidates_passVeto",
            "KinkVertex_invMass",
            "nKinkVertices",
            "KinkVertex_SV",
            "KinkVertex_ntracks",
            "KinkAngle",
            "KinkVertex_dxy",
            "KinkVertex_d3d",
            
            "PV2V0Cos",
            "RecoedPrimaryTracks_firstHitLoc",
            "RecoedPrimaryTracks_lastHitLoc",
            "Beta_RecoedPrimaryTracks",
            "RecoedPrimaryTrack_mass",
            "EscapingTracks_mass",
            "TOF_RecoedPrimaryTracks",
            "TOF_EscapingTracks",
            "TOF_sel_tracks",

            "n_EscapingTracks",
            "EscapingTracks_pt",
            "EscapingTracks_p",
            "EscapingTracks_theta",
            "EscapingTracks_phi",

        ]

        return branch_list
