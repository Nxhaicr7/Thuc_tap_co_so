# Model Checkpoint

## 📦 File cần thiết

Đặt file `best.pt` (trained model checkpoint) vào thư mục này để chạy inference.

### Cách lấy file best.pt:

1. **Từ Google Drive**: Tải từ link trong README chính
2. **Từ training**: Sau khi train xong, file sẽ tự động được lưu tại đây

### Kích thước file:

File `best.pt` thường có kích thước khoảng 20-30MB, phù hợp để upload lên Git.

### Cấu trúc file:

```python
checkpoint = {
    "epoch": int,           # Epoch number
    "best_acc": float,      # Best accuracy achieved
    "model": state_dict,    # Model weights
    "optimize": state_dict  # Optimizer state
}
```

## ⚠️ Lưu ý

- **Dataset không cần thiết** để chạy inference
- Chỉ cần file `best.pt` là có thể chạy web app
- Dataset chỉ cần khi bạn muốn train lại model
