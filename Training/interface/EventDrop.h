#include "TFile.h"


enum class Selection {qcd};

struct DatasetDesc {
    size_t n_per_batch;
    TH1D threshold;
    std::vector<std::string> fileNames;
};

struct Dataset {
    Dataset(const DatasetDesc& desc)  : desc_(desc) {
        entryIndex_ = 0;
        if(desc.fileNames.empty())
            throw std::runtime_error("Dataset is empty");
        tuple_= std::make_unique<input_tuple::TauTuple>("taus", desc.fileNames); //input tuple
    }

    bool FillNext(input_tuple::TauTuple& outputTuple)
    {   
        size_t n = 0;
        for(; n < desc_.n_per_batch && entryIndex_ < tuple_->GetEntries(); ++entryIndex_) {
            tuple_->GetEntry(entryIndex_);
            double v = myrndm->Rndm(); // Generate random number between 0 and 1
            outputTuple() = tuple_->data();
            if (v <= desc_.threshold.GetBinContent(desc_.threshold.FindBin(outputTuple().tau_pt))){ 
                // Keep only if random number is less than the ratio calculated for that bin
                outputTuple.Fill();
            }
            ++n;
        }
        return n == desc_.n_per_batch; // File not finished if true. Else we have to stop.
    }

    DatasetDesc desc_;
    std::unique_ptr<input_tuple::TauTuple> tuple_;
    Long64_t entryIndex_;
    TRandom3 *myrndm = new TRandom3();

};

struct OutputDesc{
    std::string fileName_;
    size_t nBatches_;
};

class DataMixer {
public:
    DataMixer(const std::vector<DatasetDesc>& datasets_desc, const std::vector<OutputDesc>& outputDescs)
        : outputDescs_(outputDescs)
          
    {
        for(const auto& desc : datasets_desc) { // Creating input descriptor
            datasets_.emplace_back(desc);
        }
    }

    void Run()
    {
        for(const auto& outputDesc:outputDescs_){
            auto outputFile = std::make_unique<TFile>(outputDesc.fileName_.c_str(), "RECREATE", "", 404);
            if(!outputFile || outputFile->IsZombie())
                throw std::runtime_error("Can not create output file.");
            auto outputTuple = std::make_unique<input_tuple::TauTuple>(outputFile.get(), false);

            for(size_t i(0); i < outputDesc.nBatches_; ++i) {
                for(auto& dataset:datasets_) {
                    if(!dataset.FillNext(*outputTuple)) {
                        throw std::runtime_error("Run out of events!");
                    }
                }
            }
            outputTuple->Write();
        }

    }
private:
    std::vector<OutputDesc> outputDescs_;
    std::vector<Dataset> datasets_;
};