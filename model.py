from transformers import TrainerCallback

class EpochLossTracker(TrainerCallback):
    def __init__(self):
        super().__init__()
        self.epoch_losses = []
    
    def on_epoch_end(self, args, state, control, **kwargs):
        epoch_loss = state.log_history[-1]["loss"]
        self.epoch_losses.append(epoch_loss)
        print(f"Época {state.epoch}: Pérdida promedio: {epoch_loss}")