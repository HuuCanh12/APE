#!/usr/bin/env python3
# ============================================================
#  rename_images.py
#  Đổi tên thư mục & file ảnh: bỏ dấu, bỏ khoảng trắng
#  Chạy: python rename_images.py
#  Đặt file này ngang hàng với thư mục images/
# ============================================================

import os
import re
import shutil

# ── 1. Hàm bỏ dấu tiếng Việt ─────────────────────────────
ACCENTS = {
    'à':'a','á':'a','ạ':'a','ả':'a','ã':'a',
    'â':'a','ầ':'a','ấ':'a','ậ':'a','ẩ':'a','ẫ':'a',
    'ă':'a','ằ':'a','ắ':'a','ặ':'a','ẳ':'a','ẵ':'a',
    'è':'e','é':'e','ẹ':'e','ẻ':'e','ẽ':'e',
    'ê':'e','ề':'e','ế':'e','ệ':'e','ể':'e','ễ':'e',
    'ì':'i','í':'i','ị':'i','ỉ':'i','ĩ':'i',
    'ò':'o','ó':'o','ọ':'o','ỏ':'o','õ':'o',
    'ô':'o','ồ':'o','ố':'o','ộ':'o','ổ':'o','ỗ':'o',
    'ơ':'o','ờ':'o','ớ':'o','ợ':'o','ở':'o','ỡ':'o',
    'ù':'u','ú':'u','ụ':'u','ủ':'u','ũ':'u',
    'ư':'u','ừ':'u','ứ':'u','ự':'u','ử':'u','ữ':'u',
    'ỳ':'y','ý':'y','ỵ':'y','ỷ':'y','ỹ':'y','đ':'d',
    'À':'A','Á':'A','Ạ':'A','Ả':'A','Ã':'A',
    'Â':'A','Ầ':'A','Ấ':'A','Ậ':'A','Ẩ':'A','Ẫ':'A',
    'Ă':'A','Ằ':'A','Ắ':'A','Ặ':'A','Ẳ':'A','Ẵ':'A',
    'È':'E','É':'E','Ẹ':'E','Ẻ':'E','Ẽ':'E',
    'Ê':'E','Ề':'E','Ế':'E','Ệ':'E','Ể':'E','Ễ':'E',
    'Ì':'I','Í':'I','Ị':'I','Ỉ':'I','Ĩ':'I',
    'Ò':'O','Ó':'O','Ọ':'O','Ỏ':'O','Õ':'O',
    'Ô':'O','Ồ':'O','Ố':'O','Ộ':'O','Ổ':'O','Ỗ':'O',
    'Ơ':'O','Ờ':'O','Ớ':'O','Ợ':'O','Ở':'O','Ỡ':'O',
    'Ù':'U','Ú':'U','Ụ':'U','Ủ':'U','Ũ':'U',
    'Ư':'U','Ừ':'U','Ứ':'U','Ự':'U','Ử':'U','Ữ':'U',
    'Ỳ':'Y','Ý':'Y','Ỵ':'Y','Ỷ':'Y','Ỹ':'Y','Đ':'D',
}

def remove_accents(text):
    return ''.join(ACCENTS.get(c, c) for c in text)

def slugify(name):
    """Bỏ dấu, thay khoảng trắng/ký tự đặc biệt bằng dấu -"""
    # Giữ nguyên phần extension
    base, _, ext = name.rpartition('.')
    if not base:          # không có extension (là folder)
        base = name
        ext = None

    base = remove_accents(base)
    base = re.sub(r'[&+]', '-and-', base)
    base = re.sub(r'\s+', '-', base)
    base = re.sub(r'[^\w\-]', '', base)
    base = re.sub(r'-{2,}', '-', base).strip('-')

    return f"{base}.{ext}" if ext else base

def needs_rename(name):
    """Trả về True nếu tên có dấu hoặc khoảng trắng"""
    return name != slugify(name)

# ── 2. Thu thập tất cả rename cần làm (từ sâu -> nông) ───
renames = []   # list of (old_abs_path, new_abs_path)

images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

if not os.path.isdir(images_dir):
    print("❌ Không tìm thấy thư mục images/ - hãy đặt script ngang hàng với thư mục images/")
    exit(1)

# Walk bottom-up để đổi file trước, folder sau
for dirpath, dirnames, filenames in os.walk(images_dir, topdown=False):
    # Đổi tên file trước
    for fname in filenames:
        if needs_rename(fname):
            old = os.path.join(dirpath, fname)
            new = os.path.join(dirpath, slugify(fname))
            renames.append((old, new))

    # Đổi tên thư mục
    dname = os.path.basename(dirpath)
    if needs_rename(dname):
        parent = os.path.dirname(dirpath)
        new_dir = os.path.join(parent, slugify(dname))
        renames.append((dirpath, new_dir))

# ── 3. Đặc biệt: normalize dvp -> DVP ─────────────────────
# (case change trên Linux cần bước trung gian)
for dirpath, dirnames, _ in os.walk(images_dir, topdown=False):
    dname = os.path.basename(dirpath)
    if dname == 'dvp':
        parent = os.path.dirname(dirpath)
        tmp = os.path.join(parent, '__dvp_tmp__')
        final = os.path.join(parent, 'DVP')
        renames.append((dirpath, tmp))
        renames.append((tmp, final))

# ── 4. Preview ────────────────────────────────────────────
print(f"\n📋 Tìm thấy {len(renames)} thay đổi cần thực hiện:\n")
for old, new in renames:
    rel_old = os.path.relpath(old, images_dir)
    rel_new = os.path.relpath(new, images_dir)
    kind = "📁" if os.path.isdir(old) else "🖼 "
    print(f"  {kind}  {rel_old}")
    print(f"       └─► {rel_new}\n")

# ── 5. Xác nhận trước khi thực hiện ──────────────────────
confirm = input("▶ Tiến hành đổi tên? (nhập 'yes' để xác nhận): ").strip().lower()
if confirm != 'yes':
    print("❌ Đã hủy.")
    exit(0)

# ── 6. Thực hiện đổi tên ──────────────────────────────────
success, failed = 0, 0
for old, new in renames:
    try:
        if os.path.exists(old):
            os.rename(old, new)
            success += 1
            print(f"  ✅ {os.path.basename(old)} → {os.path.basename(new)}")
        else:
            print(f"  ⚠️  Không tìm thấy (đã đổi trước?): {old}")
    except Exception as e:
        failed += 1
        print(f"  ❌ Lỗi: {old} → {new} | {e}")

print(f"\n🎉 Hoàn thành! Thành công: {success} | Thất bại: {failed}")
print("👉 Bước tiếp theo: chạy update_html_paths.py để cập nhật đường dẫn trong HTML")