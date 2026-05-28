#!/usr/bin/env python3
# ============================================================
#  update_html_paths.py
#  Cập nhật tất cả đường dẫn ảnh trong HTML sau khi đã chạy
#  rename_images.py
#  Chạy: python update_html_paths.py
#  Đặt file này ngang hàng với các file .html
# ============================================================

import os
import re
import glob

# ── Bảng thay thế đường dẫn cũ -> mới ───────────────────
# Thứ tự quan trọng: thay thế cụ thể trước, chung sau
PATH_REPLACEMENTS = [

    # === THƯ MỤC GỐC CÓ DẤU ===
    ("images/Dự án tiêu biểu/",         "images/Du-an-tieu-bieu/"),
    ("images/Sản phẩm chủ lực/",        "images/San-pham-chu-luc/"),

    # === BECKER subfolders ===
    ("images/Becker/Bơm hút  nén khí kiểu trục vít - biến tần VADS/",
     "images/Becker/Bom-hut-nen-khi-truc-vit-bien-tan-VADS/"),
    ("images/Becker/Bơm hút chân không kiểu cánh gạt/",
     "images/Becker/Bom-hut-chan-khong-kieu-canh-gat/"),

    # === DVP - normalize case + subfolders ===
    ("images/dvp/Bơm chân không vòng dầu/",  "images/DVP/Bom-chan-khong-vong-dau/"),
    ("images/dvp/ơm chân không vòng khô/",   "images/DVP/Bom-chan-khong-vong-kho/"),
    ("images/dvp/",                            "images/DVP/"),
    ("images/DVP/Bơm chân không vòng dầu/",  "images/DVP/Bom-chan-khong-vong-dau/"),
    ("images/DVP/ơm chân không vòng khô/",   "images/DVP/Bom-chan-khong-vong-kho/"),

    # === FRIULAIR subfolders ===
    ("images/Friulair/Bộ lọc khí nén/",    "images/Friulair/Bo-loc-khi-nen/"),
    ("images/Friulair/Máy sấy khí/",        "images/Friulair/May-say-khi/"),

    # === QUINCY subfolders ===
    ("images/Quincy/Máy nén khí trục vít Quincy/",
     "images/Quincy/May-nen-khi-truc-vit-Quincy/"),
    ("images/Quincy/Máy nén khí trục vít không dầu/",
     "images/Quincy/May-nen-khi-truc-vit-khong-dau/"),
    ("images/Quincy/Oil-Free Water Injected Screw Compressors/",
     "images/Quincy/Oil-Free-Water-Injected/"),

    # === TAPFLO subfolders ===
    ("images/Tapflo/BƠM TIÊU CHUẨN THỰC PHẨM & Y TẾ/",
     "images/Tapflo/Bom-tieu-chuan-thuc-pham-y-te/"),
    ("images/Tapflo/Bơm ly tâm/",             "images/Tapflo/Bom-ly-tam/"),
    ("images/Tapflo/Bơm màng thân kim loại/", "images/Tapflo/Bom-mang-than-kim-loai/"),
    ("images/Tapflo/Bơm màng thân nhựa/",     "images/Tapflo/Bom-mang-than-nhua/"),
    ("images/Tapflo/Bơm thông minh/",         "images/Tapflo/Bom-thong-minh/"),
    ("images/Tapflo/Bơm ống/",                "images/Tapflo/Bom-ong/"),
    ("images/Tapflo/Phụ kiện/",               "images/Tapflo/Phu-kien/"),

    # === TÊN FILE CÓ DẤU / KHOẢNG TRẮNG ===
    # Thư mục Dự án tiêu biểu (đã handle folder trên, chỉ cần handle tên file)
    ("Nhà máy gỗ.png",               "Nha-may-go.png"),
    ("Nhà máy sơn.png",              "Nha-may-son.png"),
    ("Nhà máy sản xuất sợi.png",     "Nha-may-san-xuat-soi.png"),
    ("Nhà máy thuốc lá.png",         "Nha-may-thuoc-la.png"),
    ("Nhà máy thực phẩm.png",        "Nha-may-thuc-pham.png"),
    ("Nhà máy xử lý nước thải.png",  "Nha-may-xu-ly-nuoc-thai.png"),

    # Sản phẩm chủ lực
    ("May bom tapflo.jpg",           "May-bom-tapflo.jpg"),

    # Logo (khoảng trắng đôi)
    ("Logo  Friulair.png",           "Logo-Friulair.png"),
    ("Logo  HS.jpg",                 "Logo-HS.jpg"),

    # Logo (khoảng trắng đơn)
    ("Logo APE.png",                 "Logo-APE.png"),
    ("Logo BienHoa.png",             "Logo-BienHoa.png"),
    ("Logo DVP.jpg",                 "Logo-DVP.jpg"),
    ("Logo Domes.png",               "Logo-Domes.png"),
    ("Logo DongWha.png",             "Logo-DongWha.png"),
    ("Logo DuyTaan.png",             "Logo-DuyTaan.png"),
    ("Logo Insee.png",               "Logo-Insee.png"),
    ("Logo KD.jpg",                  "Logo-KD.jpg"),
    ("Logo Kluber.jpg",              "Logo-Kluber.jpg"),
    ("Logo Masan.jpg",               "Logo-Masan.jpg"),
    ("Logo Nestle.png",              "Logo-Nestle.png"),
    ("Logo OIBJC.png",               "Logo-OIBJC.png"),
    ("Logo Phu my.png",              "Logo-Phu-my.png"),
    ("Logo Pneumofore.jpg",          "Logo-Pneumofore.jpg"),
    ("Logo Quincy.png",              "Logo-Quincy.png"),
    ("Logo Scancom.jpg",             "Logo-Scancom.jpg"),
    ("Logo Solberg.png",             "Logo-Solberg.png"),
    ("Logo THP.png",                 "Logo-THP.png"),
    ("Logo TPC.png",                 "Logo-TPC.png"),
    ("Logo Theodore.jpg",            "Logo-Theodore.jpg"),
    ("Logo ThiPha.png",              "Logo-ThiPha.png"),
    ("Logo Trung Nguyen.jpg",        "Logo-Trung-Nguyen.jpg"),
    ("Logo Vinamilk.png",            "Logo-Vinamilk.png"),
    ("Logo Vinataba.png",            "Logo-Vinataba.png"),
    ("Logo bibica.jpg",              "Logo-bibica.jpg"),
    ("Logo liksin.png",              "Logo-liksin.png"),
    ("Logo tapflo.png",              "Logo-tapflo.png"),
    ("Logo toto.jpg",                "Logo-toto.jpg"),

    # Tapflo Phụ kiện - file có khoảng trắng
    ("Dau noi dang CAMLOCK.jpg",              "Dau-noi-dang-CAMLOCK.jpg"),
    ("Giap phap may bom di dong.jpg",         "Giai-phap-may-bom-di-dong.jpg"),
    ("He thong kiem soat muc chat long.jpg",  "He-thong-kiem-soat-muc-chat-long.jpg"),
    ("He thong xu ly khi.jpg",                "He-thong-xu-ly-khi.jpg"),
]

# ── Fix copyright năm ─────────────────────────────────────
COPYRIGHT_OLD = "© 2024"
COPYRIGHT_NEW = "© 2025"

# ── Tìm tất cả file HTML ─────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
html_files = glob.glob(os.path.join(script_dir, "*.html"))

# Thêm các file HTML trong thư mục con (dich-vu-detail, v.v.)
for subdir in ["dich-vu-detail"]:
    sub_path = os.path.join(script_dir, subdir)
    if os.path.isdir(sub_path):
        html_files.extend(glob.glob(os.path.join(sub_path, "*.html")))

print(f"\n📂 Tìm thấy {len(html_files)} file HTML\n")

total_changes = 0

for filepath in sorted(html_files):
    fname = os.path.relpath(filepath, script_dir)
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # Áp dụng tất cả path replacements
    for old, new in PATH_REPLACEMENTS:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            print(f"  ✅ [{fname}] '{old}' → '{new}' ({count}x)")
            total_changes += count

    # Fix copyright
    if COPYRIGHT_OLD in content:
        count = content.count(COPYRIGHT_OLD)
        content = content.replace(COPYRIGHT_OLD, COPYRIGHT_NEW)
        print(f"  📅 [{fname}] Copyright: {COPYRIGHT_OLD} → {COPYRIGHT_NEW} ({count}x)")
        total_changes += count

    # Ghi lại nếu có thay đổi
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"\n🎉 Hoàn thành! Tổng số thay đổi: {total_changes}")
print("👉 Bước tiếp theo: commit & push lên GitHub")