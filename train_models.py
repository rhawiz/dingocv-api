import os

from app.core.train import AutocompleteTrainer

DATABASE_PATH = os.getenv("DATABASE_PATH", "dingocv_phrases.sqlite")
MODELS_PATH = os.getenv("MODELS_PATH", 'models')

trainer = AutocompleteTrainer(save_dir=os.path.abspath(MODELS_PATH), sqlite_path=os.path.abspath(DATABASE_PATH))
trainer.train()
