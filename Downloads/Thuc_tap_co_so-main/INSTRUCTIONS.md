# 📝 Hướng dẫn Upload Project lên Git

## ✅ Đã cấu hình xong

Project đã được cấu hình để **CHỈ upload file `best.pt`**, KHÔNG upload dataset nặng.

## 🎯 Chiến lược Git

### ✅ Sẽ được upload (tracked):
- ✅ Source code (`.py` files)
- ✅ Templates HTML
- ✅ Requirements.txt
- ✅ Dockerfile
- ✅ README files
- ✅ **File `best.pt`** (model checkpoint ~20-30MB)
- ✅ Pretrained weights `efficientnet_b0_rwightman-3dd342df.pth` (21MB)

### ❌ KHÔNG upload (ignored):
- ❌ Dataset `animals/` (quá nặng, hàng GB)
- ❌ Dataset zip file
- ❌ Ảnh upload trong `static/`
- ❌ TensorBoard logs
- ❌ Training checkpoints trong `precheckpoint/`
- ❌ Python cache, virtual env, IDE files

## 📋 Các bước cần làm

### Bước 1: Lấy file best.pt

**Option A: Tải từ Google Drive**
```bash
cd source_code/checkpoint/animals/
# Tải file best.pt từ link Google Drive và đặt vào đây
```

**Option B: Train model để tạo best.pt**
```bash
cd source_code
# Cần có dataset trong animals/ folder
python Train.py -r animals -b 32 -e 50
# File best.pt sẽ tự động được tạo trong checkpoint/animals/
```

### Bước 2: Kiểm tra file best.pt đã có chưa

```bash
ls -lh source_code/checkpoint/animals/best.pt
```

Nếu file tồn tại, bạn sẽ thấy:
```
-rw-rw-r-- 1 user user 23M Feb 10 21:00 best.pt
```

### Bước 3: Test app hoạt động

```bash
cd source_code
pip install -r requirements.txt
python app.py
```

Truy cập http://localhost:5000 và thử upload ảnh để test.

### Bước 4: Upload lên Git

```bash
cd /home/nxhai/Downloads/Thuc_tap_co_so-main

# Add files
git add .gitignore
git add README.md
git add source_code/

# Commit
git commit -m "Add animal classification project with trained model"

# Push (thay your-remote-url bằng URL repo của bạn)
git remote add origin your-remote-url
git push -u origin master
```

## 📊 Kích thước upload dự kiến

| File/Folder | Size | Status |
|------------|------|---------|
| Source code | ~50KB | ✅ Upload |
| best.pt | ~20-30MB | ✅ Upload |
| efficientnet weights | 21MB | ✅ Upload |
| templates/ | ~20KB | ✅ Upload |
| **Dataset animals/** | **~1-5GB** | ❌ **KHÔNG upload** |
| **Total** | **~50MB** | ✅ Phù hợp cho Git |

## ⚠️ Lưu ý quan trọng

1. **Không có best.pt = App không chạy được**
   - File này bắt buộc để inference
   - Phải có trước khi push lên Git

2. **Dataset chỉ cần khi train**
   - Người clone repo KHÔNG cần dataset để chạy demo
   - Chỉ cần khi muốn train lại model

3. **Clone và chạy dễ dàng**
   ```bash
   git clone your-repo-url
   cd Thuc_tap_co_so-main/source_code
   pip install -r requirements.txt
   python app.py  # Chạy ngay không cần dataset!
   ```

## 🔍 Kiểm tra .gitignore đang hoạt động

Chạy lệnh này để xem file nào sẽ được commit:

```bash
cd /home/nxhai/Downloads/Thuc_tap_co_so-main
git status
```

**Kết quả mong muốn:**
- ✅ Thấy `source_code/checkpoint/animals/best.pt`
- ❌ KHÔNG thấy `source_code/animals/` (dataset)
- ❌ KHÔNG thấy `source_code/static/*.jpg`

## 🚀 Sẵn sàng!

Nếu file `best.pt` đã có trong `source_code/checkpoint/animals/`, bạn đã sẵn sàng để upload project lên Git!

Tổng dung lượng upload: **~50MB** thay vì hàng GB 🎉
