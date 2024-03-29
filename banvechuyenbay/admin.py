from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.helpers import validate_form_on_submit
from wtforms import PasswordField, ValidationError
from wtforms.validators import DataRequired, AnyOf

from banvechuyenbay import ad, db
from banvechuyenbay.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from banvechuyenbay.models import *


class AccessibleView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.nhan_vien.user_role.name == 'Quản trị'


# Template mẫu để ghi đè các trang list, create của flask-admin
class ModelTemplate(ModelView, AccessibleView):
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    can_export = True
    create_modal = True
    edit_modal = True


class MayBayModelView(ModelTemplate):
    form_columns = ('name', 'ghe_hang_1', 'ghe_hang_2',)
    column_labels = dict(name='Tên máy bay', ghe_hang_1="Số lượng ghế hạng 1",
                         ghe_hang_2="Số lượng ghế hạng 2",)

    def create_model(self, form):
        maybay = MayBay()
        form.populate_obj(maybay)

        list = []
        for i in range(maybay.ghe_hang_1):
            ghe = Ghe()
            ghe.name = 'Ghế số ' + str(i + 1)
            ghe.available = True
            ghe.id_loai_ghe = 1
            ghe.id_may_bay = maybay.id

            list.append(ghe)

            maybay.ghe = list
            self.session.add(maybay)
            self.session.commit()

        for i in range(maybay.ghe_hang_1, maybay.ghe_hang_1 + maybay.ghe_hang_2):
            ghe = Ghe()
            ghe.name = 'Ghế số ' + str(i + 1)
            ghe.available = True
            ghe.id_loai_ghe = 2
            ghe.id_may_bay = maybay.id

            list.append(ghe)

            maybay.ghe = list
            self.session.add(maybay)
            self.session.commit()

        return True


class DuongBayModelView(ModelTemplate):
    form_columns = ('san_bay_di', 'san_bay_den', 'khoang_cach',)
    column_labels = dict(san_bay_di='Sân bay đi', san_bay_den='Sân bay đến',
                         khoang_cach='Khoảng cách (km)',)


class ChuyenBayModelView(ModelTemplate):
    form_columns = ('may_bay', 'duong_bay', 'ngay_khoi_hanh', 'thoi_gian_bay',)
    column_list = ('may_bay', 'duong_bay', 'ngay_khoi_hanh', 'thoi_gian_bay',)
    column_labels = dict(may_bay='Tên máy bay', duong_bay='Tên đường bay',
                         ngay_khoi_hanh='Ngày khởi hành', thoi_gian_bay='Thời gian bay',)


class SanBayModelView(ModelTemplate):
    form_columns = ('name', 'vi_tri',)
    column_labels = dict(name='Tên sân bay', vi_tri='Vị trí sân bay',)


class SanBayTrungGianModelView(ModelTemplate):
    form_columns = ('san_bay', 'duong_bay', 'thoi_gian_dung',)
    column_labels = dict(san_bay='Sân bay trung gian', duong_bay='Đường bay', thoi_gian_dung='Thời gian dừng',)
    column_list = ('san_bay', 'duong_bay', 'thoi_gian_dung',)


class UserRoleModelView(ModelTemplate):
    form_columns = ('name',)
    column_labels = dict(name='Vai trò',)


class NhanVienModelView(ModelTemplate):
    form_columns = ('id', 'name', 'gioi_tinh', 'ngay_sinh', 'dia_chi', 'que_quan', 'dien_thoai',
                    'avatar', 'user_role',)
    form_edit_rules = ('name', 'gioi_tinh', 'ngay_sinh', 'dia_chi', 'que_quan', 'dien_thoai',
                    'avatar', 'user_role',)
    column_labels = dict(id='Mã nhân viên', name='Họ tên', gioi_tinh='Giới tính', ngay_sinh='Ngày sinh',
                         dia_chi='Địa chỉ', que_quan='Quê quán', dien_thoai='Điện thoại',
                         avatar='Ảnh đại diện', user_role='Vai trò',)


class KhachHangModelView(ModelTemplate):
    form_columns = ('name', 'gioi_tinh', 'ngay_sinh', 'Cmnd', 'dia_chi', 'sdt', 'email',)
    column_labels = dict(name='Họ tên', gioi_tinh='Giới tính', ngay_sinh='Ngày sinh',
                         Cmnd='Căn cước công dân', dia_chi='Địa chỉ', sdt='Điện thoại',
                         email='Email',)


class AccountModelView(ModelTemplate):
    column_list = ('username', 'active', 'nhan_vien',)
    form_edit_rules = ('username', 'active',)
    form_create_rules = ('username', 'password', 'active', 'nhan_vien',)
    form_extra_fields = {
        'password': PasswordField('Password')
    }
    column_labels = dict(nhan_vien='Nhân viên',)


class GheModelView(ModelTemplate):
    form_columns = ('name', 'available', 'may_bay', 'loai_ghe')
    column_list = ('name', 'available', 'may_bay', 'loai_ghe')
    column_labels = dict(name='Tên ghế', available='Available', may_bay='Máy bay', loai_ghe='Loại ghế',)


class PhieuDatChoModelView(ModelTemplate):
    form_columns = ('ngay_xuat_phieu', 'ghe', 'khach_hang', 'confirm',)
    column_list = ('ngay_xuat_phieu', 'ghe', 'khach_hang', 'confirm',)
    column_labels = dict(ngay_xuat_phieu='Ngày xuất phiếu', ghe='Ghế', khach_hang='Khách hàng', confirm='Xác nhận',)


class LoaiGheModelView(ModelTemplate):
    form_columns = ('name', 'don_gia',)
    column_labels = dict(name='Tên hạng ghế', don_gia='Đơn giá',)


class VeModelView(ModelTemplate):
    form_columns = ('id', 'chuyen_bay', 'ghe', 'ngay_xuat_ve', 'hoa_don',)
    column_list = ('id', 'chuyen_bay', 'ghe', 'ngay_xuat_ve', 'hoa_don',)
    column_labels = dict(id='Mã vé', ngay_xuat_ve='Ngày xuất vé',
                         chuyen_bay='Tên chuyến bay', ghe='Ghế', hoa_don='Hóa đơn',)


class HoaDonModelView(ModelTemplate):
    form_columns = ('id', 'ngay_xuat_hoa_don', 'khach_hang', 'nhan_vien',)
    column_list = ('id', 'ngay_xuat_hoa_don', 'khach_hang', 'nhan_vien',)
    column_labels = dict(id='Mã hóa đơn', ngay_xuat_hoa_don='Ngày xuất hóa đơn', khach_hang='Khách hàng', nhan_vien='Nhân viên')


# Định nghĩa 1 view mới không liên quan đến các models để hiển thị cách sử dụng cho người dùng
class HelperView(AccessibleView):
    @expose('/')
    def index(self):
        return self.render('admin/helper.html')


class LogoutView(AccessibleView):
    @expose('/')
    def index(self):
        user = current_user
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        return redirect('/admin')


class ThongKeView(AccessibleView):
    @expose('/')
    def index(self):
        return self.render('admin/thongke.html')


# Nhóm các view model liên quan
group1 = "Airline"
group2 = "User"
group3 = "Ticket"

ad.add_view(SanBayModelView(SanBay, db.session, category=group1, name="Sân bay"))
ad.add_view(LoaiGheModelView(LoaiGhe, db.session, category=group1, name="Loại ghế́"))
ad.add_view(GheModelView(Ghe, db.session, category=group1, name="Ghế"))
ad.add_view(MayBayModelView(MayBay, db.session, category=group1, name="Máy bay"))
ad.add_view(DuongBayModelView(DuongBay, db.session, category=group1, name="Đường bay"))
ad.add_view(SanBayTrungGianModelView(SanBayTrungGian, db.session, category=group1, name="Sân bay trung gian"))
ad.add_view(ChuyenBayModelView(ChuyenBay, db.session, category=group1, name="Chuyến bay"))
ad.add_view(UserRoleModelView(UserRole, db.session, category=group2, name="Vai trò người dùng"))
ad.add_view(NhanVienModelView(NhanVien, db.session, category=group2, name="Nhân viên"))
ad.add_view(AccountModelView(Account, db.session, category=group2, name='Account'))
ad.add_view(KhachHangModelView(KhachHang, db.session, category=group2, name="Khách hàng"))
ad.add_view(PhieuDatChoModelView(PhieuDatCho, db.session, name="Phiếu đặt chỗ"))
ad.add_view(VeModelView(Ve, db.session, name="Vé"))
ad.add_view(HoaDonModelView(HoaDon, db.session, name="Hóa đơn"))
ad.add_view(ThongKeView(name="Thống kê"))
ad.add_view(HelperView(name="Hướng dẫn sử dụng"))
ad.add_view(LogoutView(name="Đăng xuất"))
