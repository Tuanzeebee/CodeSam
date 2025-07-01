# -*- coding: utf-8 -*-
# ------------------------------------------------------------
#  Student GPA & Behaviour Simulation – v2 (2025-06-22)
#  • Bổ sung 4 mức “Hỗ Trợ Từ Gia Đình” chi tiết
#  • Tạo logic điểm theo phân bố (mean & std) của từng mức hỗ trợ
#  • Phát hiện & điều chỉnh dữ liệu xung đột (conflict)
# ------------------------------------------------------------

import pandas as pd
import numpy as np
import random

# === 1. TEMPLATE MÔN HỌC gốc (giữ nguyên) ===================
# ... (courses_template_raw giữ nguyên, cắt bớt ở đây cho ngắn) ...
# —— Bạn hãy giữ nguyên phần courses_template_raw như trong file gốc —— #
courses_template_raw = [
    # Học Kỳ I - Năm Học 2022-2023
    {'Kỳ': 'Học Kỳ I - Năm Học 2022-2023', 'Kỳ số': '1', 'Năm': '2022-2023', 'Mã Môn': 'CMU-SE 100',
     'Tên Môn': 'Introduction to Software Engineering', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2022-2023', 'Kỳ số': '1', 'Năm': '2022-2023', 'Mã Môn': 'CS 201',
     'Tên Môn': 'Tin Học Ứng Dụng', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2022-2023', 'Kỳ số': '1', 'Năm': '2022-2023', 'Mã Môn': 'CS 201',
     'Tên Môn': 'Tin Học Ứng Dụng', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2022-2023', 'Kỳ số': '1', 'Năm': '2022-2023', 'Mã Môn': 'CS 211',
     'Tên Môn': 'Lập Trình Cơ Sở', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2022-2023', 'Kỳ số': '1', 'Năm': '2022-2023', 'Mã Môn': 'CS 211',
     'Tên Môn': 'Lập Trình Cơ Sở', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2022-2023', 'Kỳ số': '1', 'Năm': '2022-2023', 'Mã Môn': 'DTE-IS 102',
     'Tên Môn': 'Hướng Nghiệp 1', 'Hình Thức': 'LEC', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2022-2023', 'Kỳ số': '1', 'Năm': '2022-2023', 'Mã Môn': 'IS-ENG 136',
     'Tên Môn': 'English for International School - Level 1', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    # Học Kỳ II - Năm Học 2022-2023
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'CHE 101',
     'Tên Môn': 'Hóa Học Đại Cương', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'CHE 101',
     'Tên Môn': 'Hóa Học Đại Cương', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'CMU-CS 252',
     'Tên Môn': 'Introduction to Network & Telecommunications Technology', 'Hình Thức': 'LEC', 'Số ĐVHT': 3,
     'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'CMU-CS 311',
     'Tên Môn': 'Object-Oriented Programming C++ (Advanced Concepts in Computing)', 'Hình Thức': 'LEC', 'Số ĐVHT': 3,
     'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'CMU-CS 311',
     'Tên Môn': 'Object-Oriented Programming C++ (Advanced Concepts in Computing)', 'Hình Thức': 'LAB', 'Số ĐVHT': 1,
     'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'DTE-IS 152',
     'Tên Môn': 'Hướng Nghiệp 2', 'Hình Thức': 'WOR', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'ES 101',
     'Tên Môn': 'Chạy Ngắn & Bài Thể Dục Tay Không', 'Hình Thức': 'DEM', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'IS-ENG 137',
     'Tên Môn': 'English for International School - Level 2', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'IS-ENG 186',
     'Tên Môn': 'English for International School - Level 3', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'MTH 103',
     'Tên Môn': 'Toán Cao Cấp A1', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2022-2023', 'Kỳ số': '2', 'Năm': '2022-2023', 'Mã Môn': 'MTH 103',
     'Tên Môn': 'Toán Cao Cấp A1', 'Hình Thức': 'REC', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    # Học Kỳ Hè - Năm Học 2022-2023
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2022-2023', 'Kỳ số': 'Hè', 'Năm': '2022-2023', 'Mã Môn': 'COM 141',
     'Tên Môn': 'Nói & Trình Bày (tiếng Việt)', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2022-2023', 'Kỳ số': 'Hè', 'Năm': '2022-2023', 'Mã Môn': 'PHY 101',
     'Tên Môn': 'Vật Lý Đại Cương 1', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2022-2023', 'Kỳ số': 'Hè', 'Năm': '2022-2023', 'Mã Môn': 'PHY 101',
     'Tên Môn': 'Vật Lý Đại Cương 1', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    # Học Kỳ I - Năm Học 2023-2024
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'CMU-CS 303',
     'Tên Môn': 'Fundamentals of Computing 1', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'CMU-CS 303',
     'Tên Môn': 'Fundamentals of Computing 1', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'CMU-SE 214',
     'Tên Môn': 'Requirements Engineering', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'ES 226',
     'Tên Môn': 'Cầu Lông Sơ Cấp', 'Hình Thức': 'DEM', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'HIS 222',
     'Tên Môn': 'Lịch Sử Văn Minh Thế Giới 2', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'IS-ENG 187',
     'Tên Môn': 'English for International School - Level 4', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'IS-ENG 236',
     'Tên Môn': 'English for International School - Level 5', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'MTH 104',
     'Tên Môn': 'Toán Cao Cấp A2', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'MTH 104',
     'Tên Môn': 'Toán Cao Cấp A2', 'Hình Thức': 'REC', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2023-2024', 'Kỳ số': '1', 'Năm': '2023-2024', 'Mã Môn': 'PHI 100',
     'Tên Môn': 'Phương Pháp Luận (gồm Nghiên Cứu Khoa Học)', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    # Học Kỳ II - Năm Học 2023-2024
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'CMU-CS 246',
     'Tên Môn': 'Application Development Practices', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'CMU-CS 297',
     'Tên Môn': 'Đồ Án CDIO', 'Hình Thức': 'DIS', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'CMU-CS 316',
     'Tên Môn': 'Fundamentals of Computing 2', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'CMU-ENG 130',
     'Tên Môn': 'Anh Văn Chuyên Ngành cho Sinh Viên CMU 1', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'COM 142',
     'Tên Môn': 'Viết (tiếng Việt)', 'Hình Thức': 'CON', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'ES 276',
     'Tên Môn': 'Cầu Lông Cao Cấp', 'Hình Thức': 'DEM', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'EVR 205',
     'Tên Môn': 'Sức Khỏe Môi Trường', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'MTH 254',
     'Tên Môn': 'Toán Rời Rạc & Ứng Dụng', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'MTH 254',
     'Tên Môn': 'Toán Rời Rạc & Ứng Dụng', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'STA 151',
     'Tên Môn': 'Lý Thuyết Xác Suất & Thống Kê Toán', 'Hình Thức': 'REC', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2023-2024', 'Kỳ số': '2', 'Năm': '2023-2024', 'Mã Môn': 'STA 151',
     'Tên Môn': 'Lý Thuyết Xác Suất & Thống Kê Toán', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    # Học Kỳ Hè - Năm Học 2023-2024
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2023-2024', 'Kỳ số': 'Hè', 'Năm': '2023-2024', 'Mã Môn': 'ES 100',
     'Tên Môn': 'Giáo Dục Quốc Phòng & An Ninh', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2023-2024', 'Kỳ số': 'Hè', 'Năm': '2023-2024', 'Mã Môn': 'ES 100',
     'Tên Môn': 'Giáo Dục Quốc Phòng & An Ninh', 'Hình Thức': 'DEM', 'Số ĐVHT': 5, 'Loại ĐVHT': 'Tín Chỉ'},
    # Tổng 8 tín chỉ cho ES 100
    # Học Kỳ I - Năm Học 2024-2025
    {'Kỳ': 'Học Kỳ I - Năm Học 2024-2025', 'Kỳ số': '1', 'Năm': '2024-2025', 'Mã Môn': 'CMU-IS 432',
     'Tên Môn': 'Software Project Management', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2024-2025', 'Kỳ số': '1', 'Năm': '2024-2025', 'Mã Môn': 'CMU-SE 252',
     'Tên Môn': 'Computer Science for Practicing Engineers (Software Construction)', 'Hình Thức': 'LEC', 'Số ĐVHT': 3,
     'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2024-2025', 'Kỳ số': '1', 'Năm': '2024-2025', 'Mã Môn': 'CMU-SE 303',
     'Tên Môn': 'Software Testing (Verification & Validation)', 'Hình Thức': 'LEC', 'Số ĐVHT': 3,
     'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2024-2025', 'Kỳ số': '1', 'Năm': '2024-2025', 'Mã Môn': 'IS 301',
     'Tên Môn': 'Cơ Sở Dữ Liệu', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2024-2025', 'Kỳ số': '1', 'Năm': '2024-2025', 'Mã Môn': 'MTH 291',
     'Tên Môn': 'Toán Ứng Dụng cho Công Nghệ Thông Tin 1', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ I - Năm Học 2024-2025', 'Kỳ số': '1', 'Năm': '2024-2025', 'Mã Môn': 'PHI 150',
     'Tên Môn': 'Triết Học Marx - Lenin', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    # Học Kỳ II - Năm Học 2024-2025
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'CMU-CS 445',
     'Tên Môn': 'System Integration Practices', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'CMU-CS 447',
     'Tên Môn': 'Đồ Án CDIO', 'Hình Thức': 'PRJ', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'CMU-CS 462',
     'Tên Môn': 'Software Measurements & Analysis', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'CMU-ENG 230',
     'Tên Môn': 'Anh Văn Chuyên Ngành cho Sinh Viên CMU 2', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'CS 464',
     'Tên Môn': 'Lập Trình Ứng Dụng .NET', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'CS 464',
     'Tên Môn': 'Lập Trình Ứng Dụng .NET', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'MTH 203',
     'Tên Môn': 'Toán Cao Cấp A3', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'MTH 204',
     'Tên Môn': 'Toán Cao Cấp A3 (LAB)', 'Hình Thức': 'LAB', 'Số ĐVHT': 1, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ II - Năm Học 2024-2025', 'Kỳ số': '2', 'Năm': '2024-2025', 'Mã Môn': 'MTH 341',
     'Tên Môn': 'Toán Ứng Dụng cho Công Nghệ Thông Tin 2', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    # Học Kỳ Hè - Năm Học 2024-2025
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2024-2025', 'Kỳ số': 'Hè', 'Năm': '2024-2025', 'Mã Môn': 'CMU-IS 401',
     'Tên Môn': 'Information System Applications', 'Hình Thức': 'LEC', 'Số ĐVHT': 3, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2024-2025', 'Kỳ số': 'Hè', 'Năm': '2024-2025', 'Mã Môn': 'CS 466',
     'Tên Môn': 'Perl & Python', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2024-2025', 'Kỳ số': 'Hè', 'Năm': '2024-2025', 'Mã Môn': 'LAW 201',
     'Tên Môn': 'Pháp Luật Đại Cương', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2024-2025', 'Kỳ số': 'Hè', 'Năm': '2024-2025', 'Mã Môn': 'POS 151',
     'Tên Môn': 'Kinh Tế Chính Trị Marx - Lenin', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
    {'Kỳ': 'Học Kỳ Hè - Năm Học 2024-2025', 'Kỳ số': 'Hè', 'Năm': '2024-2025', 'Mã Môn': 'POS 361',
     'Tên Môn': 'Tư Tưởng Hồ Chí Minh', 'Hình Thức': 'LEC', 'Số ĐVHT': 2, 'Loại ĐVHT': 'Tín Chỉ'},
]
# ------------------------------------------------------------
# 1A. CÁC MÔN Pass/Fail
pf_course_codes = ['ES 101', 'ES 226', 'ES 276', 'ES 100']

# ------------------------------------------------------------
# 1B. BỔ SUNG CỜ is_pf
courses_template = []
for course in courses_template_raw:
    new_course = course.copy()
    new_course['is_pf'] = new_course['Mã Môn'] in pf_course_codes
    courses_template.append(new_course)

# === 2. THANG ĐIỂM (không đổi) ===============================
grading_scale = [
    {"min_score": 9.5, "letter": "A+", "points": 4.0},
    {"min_score": 8.5, "letter": "A",  "points": 4.0},
    {"min_score": 8.0, "letter": "A-", "points": 3.65},
    {"min_score": 7.5, "letter": "B+", "points": 3.33},
    {"min_score": 7.0, "letter": "B",  "points": 3.0},
    {"min_score": 6.5, "letter": "B-", "points": 2.65},
    {"min_score": 6.0, "letter": "C+", "points": 2.33},
    {"min_score": 5.5, "letter": "C",  "points": 2.0},
    {"min_score": 4.5, "letter": "C-", "points": 1.65},
    {"min_score": 4.0, "letter": "D",  "points": 1.0},
    {"min_score": 0.0, "letter": "F",  "points": 0.0}
]
subject_type_map = {
    'CMU-SE 100': 'major',
    'CS 201': 'general',
    'CS 211': 'major',
    'DTE-IS 102': 'major',
    'IS-ENG 136': 'major',
    'CHE 101': 'general',
    'CMU-CS 252': 'major',
    'CMU-CS 311': 'major',
    'DTE-IS 152': 'major',
    'IS-ENG 137': 'major',
    'IS-ENG 186': 'major',
    'MTH 103': 'general',
    'COM 141': 'general',
    'PHY 101': 'major',
    'CMU-CS 303': 'major',
    'CMU-SE 214': 'major',
    'HIS 222': 'general',
    'IS-ENG 187': 'major',
    'IS-ENG 236': 'major',
    'MTH 104': 'general',
    'PHI 100': 'general',
    'CMU-CS 246': 'major',
    'CMU-CS 297': 'major',
    'CMU-CS 316': 'major',
    'CMU-ENG 130': 'major',
    'COM 142': 'general',
    'EVR 205': 'general',
    'MTH 254': 'major',
    'STA 151': 'general',
    'CMU-IS 432': 'major',
    'CMU-SE 252': 'major',
    'CMU-SE 303': 'major',
    'IS 301': 'major',
    'MTH 291': 'major',
    'PHI 150': 'general',
    'CMU-CS 445': 'major',
    'CMU-CS 447': 'major',
    'CMU-CS 462': 'major',
    'CMU-ENG 230': 'major',
    'CS 464': 'major',
    'MTH 203': 'general',
    'MTH 204': 'general',
    'MTH 341': 'major',
    'CMU-IS 401': 'major',
    'CS 466': 'major',
    'LAW 201': 'general',
    'POS 151': 'general',
    'POS 361': 'general',
}

difficulty_map = {
    'CMU-SE 100': 1,
    'CS 201': 1,
    'CS 211': 2,
    'DTE-IS 102': 1,
    'IS-ENG 136': 2,
    'CHE 101': 2,
    'CMU-CS 252': 1,
    'CMU-CS 311': 3,
    'DTE-IS 152': 1,
    'IS-ENG 137': 2,
    'IS-ENG 186': 2,
    'MTH 103': 3,
    'COM 141': 1,
    'PHY 101': 2,
    'CMU-CS 303': 3,
    'CMU-SE 214': 2,
    'HIS 222': 1,
    'IS-ENG 187': 2,
    'IS-ENG 236': 2,
    'MTH 104': 2,
    'PHI 100': 1,
    'CMU-CS 246': 2,
    'CMU-CS 297': 1,
    'CMU-CS 316': 3,
    'CMU-ENG 130': 2,
    'COM 142': 1,
    'EVR 205': 1,
    'MTH 254': 2,
    'STA 151': 1,
    'CMU-IS 432': 3,
    'CMU-SE 252': 3,
    'CMU-SE 303': 3,
    'IS 301': 3,
    'MTH 291': 2,
    'PHI 150': 1,
    'CMU-CS 445': 3,
    'CMU-CS 447': 2,
    'CMU-CS 462': 3,
    'CMU-ENG 230': 2,
    'CS 464': 3,
    'MTH 203': 2,
    'MTH 204': 2,
    'MTH 341': 2,
    'CMU-IS 401': 3,
    'CS 466': 3,
    'LAW 201': 1,
    'POS 151': 1,
    'POS 361': 1,
}

def get_grade_details(score, is_pf):
    """
    Trả về (điểm_gốc, điểm_chữ, điểm_quy_đổi)
    """
    if is_pf:
        diem_goc_pf = round(random.uniform(4.0, 10.0), 1)
        return diem_goc_pf, "P (P/F)", None

    diem_goc = round(score, 1)
    for grade_info in grading_scale:
        if diem_goc >= grade_info["min_score"]:
            return diem_goc, grade_info["letter"], grade_info["points"]
    return diem_goc, grading_scale[-1]["letter"], grading_scale[-1]["points"]


# === 3. THAM SỐ HỖ TRỢ TỪ GIA ĐÌNH ============================
# Thông tin mức hỗ trợ gia đình
FAMILY_SUPPORT_LEVELS = {
    "Thấp": (6.2, 1.4),
    "Trung Bình": (6.8, 1.2),
    "Cao": (7.5, 0.8),
    "Rất Cao": (8.2, 0.6),
}
FAMILY_SUPPORT_NAMES = list(FAMILY_SUPPORT_LEVELS.keys())
FAMILY_SUPPORT_WEIGHTS = [2, 3, 4, 2]

def assign_family_support_per_semester(semesters):
    # 50% sinh viên có mức hỗ trợ cố định toàn khóa, 50% thay đổi theo học kỳ
    use_fixed_support = random.random() < 0.5

    if use_fixed_support:
        fixed_value = random.choices(FAMILY_SUPPORT_NAMES, weights=FAMILY_SUPPORT_WEIGHTS, k=1)[0]
        return {
            (sem['Năm'], sem['Kỳ số']): fixed_value
            for sem in semesters
        }
    else:
        return {
            (sem['Năm'], sem['Kỳ số']): random.choices(FAMILY_SUPPORT_NAMES, weights=FAMILY_SUPPORT_WEIGHTS, k=1)[0]
            for sem in semesters
        }

def generate_student_behavior():
    attendance_pct = random.choices(range(0, 101, 10),
        weights=[1, 1, 2, 3, 5, 8, 10, 12, 15, 25, 35])[0]
    study_hours = random.choices(range(5, 41), weights=[1] * 5 + [3] * 5 + [5] * 10 + [2] * 10 + [1] * 6)[0]
    travel_time = random.randint(5, 60)
    return study_hours, f"{attendance_pct}%", travel_time, attendance_pct

def compute_gpa(attendance_pct, study_hours, travel_time, family_support):
    base = 5.0
    # Trọng số điều chỉnh điểm GPA (attendance > study > support > travel)
    base += ((attendance_pct - 50) / 50.0) * 2.3     # Tác động mạnh (±2.5)
    base += ((study_hours - 10) / 10.0) * 1.2  # Hạ từ 2.0 về 1.0 là ổn nhất
    base += {
        "Thấp": -0.3,
        "Trung Bình": 0.0,
        "Cao": 0.5,
        "Rất Cao": 0.8
    }[family_support]
    base -= ((travel_time - 30) / 30.0) * 0.5         # Tác động nhỏ (±0.5)
    noise = random.gauss(0, 0.2)
    return round(max(0.0, min(10.0, base + noise)), 1)
# Điều chỉnh giới hạn điểm cho môn chuyên ngành khó
def clamp_high_score(score, subject_code):
    subject_type = subject_type_map.get(subject_code)
    difficulty = difficulty_map.get(subject_code)

    # Nếu là môn chuyên ngành và khó (2 hoặc 3), hoặc là đại cương
    if (subject_type == 'major' and difficulty in [1,2,3]) or subject_type == 'general':
        if score >= 9.2:
            return round(random.uniform(9.0, 9.5), 1)
    return score

def validate_expected_score(subject_code, attendance_pct, study_hours, score):
    subject_type = subject_type_map.get(subject_code)
    difficulty = difficulty_map.get(subject_code)

    if subject_type == 'major':
        if difficulty == 3:
            return study_hours > 30 and attendance_pct >= 90 and score >= 7.5
        elif difficulty == 2:
            return study_hours > 20 and attendance_pct >= 90 and score >= 7.5
        elif difficulty == 1:
            return study_hours > 10 and attendance_pct >= 90 and score >= 7.7
    elif subject_type == 'general':
        return study_hours > 5 and attendance_pct >= 90 and score >= 8.0
    return True  # Không có rule áp dụng

def detect_conflict(score, attendance_pct, study_hours, travel_time, family_support):
    # Điều kiện mâu thuẫn khi GPA không tương xứng với hành vi
    if score < 5.5 and attendance_pct >= 80 and study_hours >= 15:
        return True
    elif score > 8.5 and attendance_pct <= 40 and study_hours <= 8:
        return True
    return False

# Sinh dữ liệu sinh viên
def generate_student_data(student_id, courses_template):
    semesters = []
    processed = set()
    for c in courses_template:
        key = (c['Năm'], c['Kỳ số'])
        if key not in processed:
            semesters.append({'Kỳ': c['Kỳ'], 'Kỳ số': c['Kỳ số'], 'Năm': c['Năm'], 'courses': []})
            processed.add(key)
    semesters.sort(key=lambda x: (int(x['Năm'].split('-')[0]), 3 if x['Kỳ số'] == 'Hè' else int(x['Kỳ số'])))
    for sem in semesters:
        sem['courses'] = [c.copy() for c in courses_template if c['Năm'] == sem['Năm'] and c['Kỳ số'] == sem['Kỳ số']]

    family_support_map = assign_family_support_per_semester(semesters)
    all_records = []
    total_qp = total_gpa_credits = total_earned = total_courses = 0

    for sem in semesters:
        support = family_support_map[(sem['Năm'], sem['Kỳ số'])]
        sem_qp = sem_credits = sem_earned = 0
        current_records = []

        for course in sem['courses']:
            record = course.copy()
            record['Mã SV'] = student_id
            record['Số môn trước đó'] = total_courses
            record['Tín chỉ tích lũy trước đó'] = total_earned

            study_hours, attendance_str, travel_time, attendance_pct = generate_student_behavior()
            score_raw = compute_gpa(attendance_pct, study_hours, travel_time, support)
            score = clamp_high_score(score_raw, course['Mã Môn'])
            diem_goc, diem_chu, diem_qd = get_grade_details(score, record['is_pf'])
            diem_tl = diem_qd * record['Số ĐVHT'] if diem_qd is not None else ''

            if diem_qd is not None:
                sem_qp += diem_qd * record['Số ĐVHT']
                sem_credits += record['Số ĐVHT']
            if (record['is_pf'] and diem_chu == "P (P/F)") or (not record['is_pf'] and diem_chu != "F"):
                sem_earned += record['Số ĐVHT']

            conflict = detect_conflict(score, attendance_pct, study_hours, travel_time, support)
            expected = validate_expected_score(record['Mã Môn'], attendance_pct, study_hours, score)
            record.update({
                'Điểm gốc': diem_goc,
                'Điểm chữ': diem_chu,
                'Điểm Quy đổi': diem_qd if diem_qd is not None else '',
                'Điểm tích lũy (môn)': diem_tl,
                'Thời Gian Học Một Tuần': study_hours,
                'Trình Trạng Chuyên Cần': attendance_str,
                'Thời Gian Từ Nhà Đến Trường': travel_time,
                'Hỗ Trợ Từ Gia Đình': support,
                'Xung Đột Dữ Liệu': 'Có' if conflict else 'Không',
                'Hợp Lý Theo Rule': '✅' if expected else '❌'
            })
            current_records.append(record)
        if not expected:
            print(
                f"❌ Rule fail – Môn: {record['Mã Môn']} | Điểm: {score} | Học: {study_hours}h | CC: {attendance_pct}%")

        gpa_ky = round(sem_qp / sem_credits, 2) if sem_credits else ''
        total_qp += sem_qp
        total_gpa_credits += sem_credits
        total_earned += sem_earned
        total_courses += len(sem['courses'])
        gpa_cum = round(total_qp / total_gpa_credits, 2) if total_gpa_credits else ''

        for rec in current_records:
            rec['GPA Kỳ Hiện Tại'] = gpa_ky
            rec['GPA Tích Lũy (sau kỳ này)'] = gpa_cum
            all_records.append(rec)

    return all_records

# === 6. TẠO DỮ LIỆU CHO N SINH VIÊN ==========================
all_student_data = []
for i in range(1, 5001):
    sid = f"SV{i:04d}"
    all_student_data.extend(generate_student_data(sid, courses_template))

# === 7. KẾT XUẤT DATAFRAME & CSV =============================
df = pd.DataFrame(all_student_data)

column_order = [
    'Mã SV', 'Kỳ', 'Kỳ số', 'Năm', 'Mã Môn', 'Tên Môn', 'Hình Thức',
    'Số ĐVHT', 'Loại ĐVHT',
    'Điểm gốc', 'Điểm chữ', 'Điểm Quy đổi', 'Điểm tích lũy (môn)',
    'GPA Kỳ Hiện Tại', 'GPA Tích Lũy (sau kỳ này)',
    'Số môn trước đó', 'Tín chỉ tích lũy trước đó',
    'Thời Gian Học Một Tuần', 'Trình Trạng Chuyên Cần',
    'Thời Gian Từ Nhà Đến Trường', 'Hỗ Trợ Từ Gia Đình',
    'Xung Đột Dữ Liệu', 'Hợp Lý Theo Rule'
]
df = df[column_order]
df.to_csv("generated_student_data_v5.csv", index=False, encoding='utf-8-sig')

print("✅ Đã lưu dữ liệu vào generated_student_data_v5.csv")
