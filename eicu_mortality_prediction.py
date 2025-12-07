import os
from pathlib import Path

from xgboost import XGBClassifier

from pyhealth.datasets import eICUDataset
from pyhealth.models.medlink import model
from pyhealth.tasks.mortality_prediction import MortalityPredictionEICU
import numpy as np
import torch
from pyhealth.datasets import split_by_patient, get_dataloader

class TesteICUMortalityPrediction:
    """Test eICU mortality prediction tasks with demo data from local test resources."""

    def setUp(self, dataset):
        """Set up demo dataset path for each test."""
        self._setup_dataset_path(dataset)
        self._load_dataset()

    def _setup_dataset_path(self, dataset):
        """Get path to local MIMIC-III demo dataset in test resources."""
        # Get the path to the test-resources/core/mimic3demo directory
        test_dir = Path(__file__).parent.parent.parent
        #self.demo_dataset_path = str(test_dir / "test-resources" / "core" / "eicudemo-test")
        #self.demo_dataset_path = str(test_dir / "test-resources" / "core" / "eicudemo")
        self.demo_dataset_path = "/Users/rosssponholtz/data/eicu-dsmall_" + dataset
        
        print(f"\n{'='*60}")
        print(f"Setting up eICU demo dataset for mortality prediction")
        print(f"Dataset path: {self.demo_dataset_path}")
        
        # Verify the dataset exists
        if not os.path.exists(self.demo_dataset_path):
            raise unittest.SkipTest(
                f"eICU demo dataset not found at {self.demo_dataset_path}"
            )
        
        # List files in the dataset directory
        files = os.listdir(self.demo_dataset_path)
        print(f"Found {len(files)} files in dataset directory:")
        for f in sorted(files):
            file_path = os.path.join(self.demo_dataset_path, f)
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"  - {f} ({size:.1f} KB)")
        print(f"{'='*60}\n")

    def _load_dataset(self):
        """Load the dataset for testing."""
        #tables = ["hospital", "admissiondx", "diagnosis", "medication", "lab", "treatment", "physicalExam", 
        #          "vitalPeriodic","vitalAperiodic"]
        tables = ["hospital", "patient", "lab", "physicalExam", "vitalPeriodic"]
        print(f"Loading eICUDataset with tables: {tables}")
        self.dataset = eICUDataset(root=self.demo_dataset_path, tables=tables)
        print(f"✓ Dataset loaded successfully")
#        print(f"  Total patients: {len(self.dataset.patients)}")
        print()

    def test_mortality_prediction_eicu_prediction(self):
        """Test test_mortality_prediction_eicu_prediction method."""
        print(f"\n{'='*60}")
        print("TEST: test_mortality_prediction_eicu_prediction()")
        print(f"{'='*60}")

        print("1: Initializing MortalityPredictionEICU task...")
        task = MortalityPredictionEICU()

        # Test that task is properly initialized
        print(f"2: ✓ Task initialized: {task.task_name}")
        print(f"3:  Input schema: {list(task.input_schema.keys())}")
        print(f"4:  Output schema: {list(task.output_schema.keys())}")
        input_processors = None
        output_processors = None

        print(f"5:  Setting up dataset with task...")
        self.sample_dataset = self.dataset.set_task(task=task,
            input_processors=input_processors,
            output_processors=output_processors)
        print(f"6:  ✓ Dataset set up with task")
        # Determine the maximum index to size the multi-hot vectors
        samples = self.sample_dataset.samples
        s1 = samples[0]
        #determine the number of keys in s1
        print(f"7:First sample structure:")
        print(f"  Sample keys: {list(s1.keys())}")
        print(f"  Number of keys: {len(s1.keys())}")
        num_features = len(s1.keys())+7
        print(f"  Number of features: {num_features}")

        # Prepare feature matrix and labels
        X, y, splits = [], [], []

        max_torch_sizes = {}
        #loop over all the samples.  For each sample, if the key is a tensor, we find the max size of the tensor.  if it is > 1, we add the size to the max_torch_sizes dictionary
        for sample in samples:
            for key in s1.keys():
                ss = sample[key]
                if isinstance(ss, torch.Tensor):
                    size = ss.shape[0] if len(ss.shape) > 0 else 1
                    if key not in max_torch_sizes or max_torch_sizes[key] < size:
                        max_torch_sizes[key] = size
        # print the max_torch_sizes dictionary
        print(f"  Max torch sizes: {max_torch_sizes}")

        for sample in samples:
            vec = np.zeros(num_features, dtype=float)
            labels = []
            vec_ind = 0
            for n,key in enumerate(s1.keys()):
                ss = sample[key]
                if isinstance(ss, torch.Tensor):
                    j = 0
                    sha = ss.shape
                    if sha == torch.Size([]):
                        vec[vec_ind] = ss.item()
                        labels.append(key)
                        vec_ind += 1
                    else:
                        for vv in ss:
                            vec[vec_ind] = vv
                            labels.append(key + str(j))
                            vec_ind += 1
                            j += 1
                        if max_torch_sizes[key] > j:
                            print(f"  - {key} has max size {max_torch_sizes[key]} but only {j} elements")
                            vec_ind += max_torch_sizes[key] - j
                else:
                    vec[vec_ind] = ss
                    labels.append(key)
                    vec_ind += 1
            X.append(vec)
            y.append(sample["mortality"].item())
#            print(f"vec_ind: {vec_ind}")




        #X = np.array(X)
        #y = np.array(y)
        #print(f"X: {X.shape}")
        print(f"labels: {len(labels)}")
        print(labels)
        #convert X to a dataframe, and write to a csv file
        import pandas as pd
        from sklearn.model_selection import train_test_split

        
        dfX = pd.DataFrame(X, columns=labels)
        dfX.to_csv(self.demo_dataset_path + '/eicu_mortality_prediction_samples.csv', index=False)
        dfy = pd.DataFrame(y, columns=["mortality"])
        dfy.to_csv(self.demo_dataset_path + '/eicu_mortality_prediction_labels.csv', index=False)

        # dfX.drop(['mortality0'], axis=1, inplace=True)
        # X_train, X_test, y_train, y_test = train_test_split(dfX, dfy, test_size=.2)

        # model = XGBClassifier(n_estimators=2, max_depth=2, learning_rate=1, objective='binary:logistic')      
        # model.fit(X_train, y_train)
        # # make predictions
        # preds = model.predict(X_test)
        # # evaluate predictions
        # model.score(X,y)

def main():
    # dataset is the first command line argument
    import sys
    dataset = sys.argv[1]
    print(f"Dataset: {dataset}")
    test = TesteICUMortalityPrediction()
    test.setUp(dataset)
    test.test_mortality_prediction_eicu_prediction()

if __name__ == "__main__":
    main()