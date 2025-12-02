# Google Colab Setup Guide

## Quick Start - Run Notebook on Google Colab

### Step 1: Upload to Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click **File** → **Upload notebook**
3. Upload `analyse.ipynb` from this repository
4. Alternatively, you can open it directly from GitHub:
   - Click **File** → **Open notebook**
   - Select **GitHub** tab
   - Paste your repository URL

### Step 2: Enable GPU (Recommended)

1. Click **Runtime** → **Change runtime type**
2. Select **T4 GPU** or **A100 GPU** (if available)
3. Click **Save**

**Why GPU?** Training will be 10-20x faster with GPU enabled.

### Step 3: Run the Notebook

Simply run each cell sequentially from top to bottom:
- Click **Runtime** → **Run all** to execute all cells at once
- Or press **Shift + Enter** to run cells one by one

## What the Notebook Does

### 1. Setup & Installation
- Installs all required packages (kagglehub, transformers, torch, etc.)
- No manual installation needed

### 2. Dataset Download
- Automatically downloads handwriting dataset from Kaggle
- Dataset: [Handwritten2Text Training Dataset](https://www.kaggle.com/datasets/chaimaourgani/handwritten2text-training-dataset)

### 3. Exploratory Data Analysis (EDA)
- Dataset statistics and info
- Text length and word count distributions
- Character frequency analysis
- Sample image visualization
- Image property analysis (dimensions, aspect ratios)

### 4. Data Preprocessing
- Custom PyTorch Dataset class
- Data augmentation (brightness, contrast, blur)
- Train/Val/Test split (70/15/15)

### 5. Model Training
- TrOCR model (microsoft/trocr-base-handwritten)
- Fine-tuning on handwriting dataset
- Automatic evaluation during training
- Model saving for later use

### 6. Evaluation & Predictions
- CER (Character Error Rate) and WER (Word Error Rate)
- Visual comparison of predictions vs ground truth
- Error analysis and distribution
- Worst predictions analysis

### 7. Inference
- Ready-to-use prediction function
- Can be used on new images

## Expected Runtime

| Phase | CPU Time | GPU Time |
|-------|----------|----------|
| Installation | 2-3 min | 2-3 min |
| Dataset Download | 3-5 min | 3-5 min |
| EDA | 5-10 min | 5-10 min |
| Training (3 epochs) | 4-6 hours | 20-30 min |
| Evaluation | 10-15 min | 2-3 min |
| **Total** | **5-7 hours** | **30-50 min** |

**Recommendation:** Use GPU for training to complete in under 1 hour.

## Expected Results

After training, you should see:

- **CER (Character Error Rate):** 3-8% (lower is better)
- **WER (Word Error Rate):** 8-15% (lower is better)

These metrics depend on:
- Dataset quality
- Training epochs (more epochs = better results)
- Model configuration
- Data augmentation

## Visualizations Included

The notebook generates:

1. **Text Statistics:**
   - Length distributions
   - Word count distributions
   - Character frequency charts

2. **Image Analysis:**
   - Sample handwritten images
   - Dimension distributions
   - Aspect ratio analysis

3. **Model Performance:**
   - Training/validation loss curves
   - Prediction visualizations
   - Error distribution histograms

4. **Error Analysis:**
   - Best and worst predictions
   - CER/WER distributions
   - Detailed error breakdowns

## Troubleshooting

### Issue: Out of Memory (OOM)

**Solution:**
- Reduce batch size in training arguments:
  ```python
  per_device_train_batch_size=4  # Instead of 8
  ```
- Use smaller GPU or enable gradient checkpointing

### Issue: Kaggle Dataset Download Fails

**Solution:**
- Make sure you're logged into Kaggle
- Accept dataset terms on Kaggle website first
- Check internet connection

### Issue: Training Too Slow

**Solution:**
- Enable GPU (see Step 2 above)
- Reduce number of epochs
- Use smaller dataset subset

### Issue: Low Accuracy

**Solution:**
- Train for more epochs (5-10 instead of 3)
- Adjust learning rate
- Add more data augmentation
- Ensure dataset labels are correct

## Customization Options

### Change Model
Replace model name in the notebook:
```python
model_name = "microsoft/trocr-large-handwritten"  # Larger model
# or
model_name = "microsoft/trocr-small-handwritten"  # Smaller, faster
```

### Adjust Training
Modify training arguments:
```python
num_train_epochs=5  # More epochs
learning_rate=3e-5  # Lower learning rate
per_device_train_batch_size=16  # Larger batch
```

### Use Subset
To test quickly with smaller dataset:
```python
df_clean = df.head(1000)  # Only use 1000 samples
```

## Saving Results

### Save Model
Models are automatically saved to:
- `./trocr-handwriting/` (checkpoints)
- `./trocr-handwriting-final/` (final model)

### Download Trained Model
```python
from google.colab import files

# Download model
!zip -r trocr-handwriting-final.zip trocr-handwriting-final/
files.download('trocr-handwriting-final.zip')
```

### Export Predictions
```python
# Save predictions to CSV
error_df.to_csv('predictions.csv', index=False)
files.download('predictions.csv')
```

## Using the Trained Model Later

Load and use your trained model:

```python
from transformers import VisionEncoderDecoderModel, TrOCRProcessor
from PIL import Image

# Load model
model = VisionEncoderDecoderModel.from_pretrained("./trocr-handwriting-final")
processor = TrOCRProcessor.from_pretrained("./trocr-handwriting-final")

# Make prediction
image = Image.open("your_image.jpg").convert("RGB")
pixel_values = processor(image, return_tensors="pt").pixel_values

generated_ids = model.generate(pixel_values)
text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(f"Recognized text: {text}")
```

## Next Steps

After completing this notebook:

1. **Experiment with other models:**
   - Try Donut or LayoutLMv3 (see `src/models/`)
   - Implement ensemble approach

2. **Fine-tune further:**
   - Train for more epochs
   - Use domain-specific data
   - Adjust hyperparameters

3. **Deploy:**
   - Create REST API with FastAPI
   - Build web demo with Gradio
   - Containerize with Docker

4. **Improve:**
   - Add more augmentation
   - Try different architectures
   - Ensemble multiple models

## Resources

- [TrOCR Paper](https://arxiv.org/abs/2109.10282)
- [Hugging Face Docs](https://huggingface.co/docs/transformers/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [Project README](README.md)
- [Model Design Guide](docs/model_design.md)

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review error messages carefully
3. Consult project documentation in `docs/`
4. Check GPU memory usage

---

**Happy Training!**

Made for SOCAR Hackathon 2025 | AI Engineering Track
