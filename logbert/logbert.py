# logbert.py
class LogBERT:
    @staticmethod
    def load_from_checkpoint(checkpoint_path):
        return LogBERT()

    def eval(self):
        pass

    def compute_anomaly_scores(self, templates):
        import torch
        return torch.tensor([0.1] * len(templates))
