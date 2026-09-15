add_test( UT_flavtagging /eos/user/s/svashish/FCCAnalyses_pre/addons/ONNXRuntime/onnxruntime-unittest flavtagging  )
set_tests_properties( UT_flavtagging PROPERTIES WORKING_DIRECTORY /eos/user/s/svashish/FCCAnalyses_pre/addons/ONNXRuntime)
set( onnxruntime-unittest_TESTS UT_flavtagging)
